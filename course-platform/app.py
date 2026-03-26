"""CourseOS Platform — Student Progress & Project Tracking."""

import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, Student, Team, Course, Week, Deliverable, Submission, CheckResult, ProjectPhase, RecoveryTicket, Reflection

# ── App Setup ───────────────────────────────────────────────────────

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "courseos-dev-key-change-in-production")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///courseos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

TRACKS = {
    "robotics": {"name": "Robotics / Mechatronics", "product": "MechaSense Studio", "color": "#E53935", "icon": "🤖"},
    "data": {"name": "Data / AI", "product": "CleanReport Pipeline", "color": "#1E88E5", "icon": "📊"},
    "simulation": {"name": "Simulation / Games", "product": "SimLab Engine", "color": "#43A047", "icon": "🎮"},
    "space": {"name": "Space / Astro", "product": "Lightcurve Explorer", "color": "#8E24AA", "icon": "🌌"},
    "iot": {"name": "IoT / Reporting", "product": "AutoDashboard Reporter", "color": "#FB8C00", "icon": "📡"},
}

COURSES = {
    "cp1": {"name": "Computer Programming 1", "semester": 1, "year": 1, "hours": 5, "version": "v1",
            "desc": "Python fundamentals → v1 functional pipeline"},
    "cp2": {"name": "Computer Programming 2", "semester": 2, "year": 1, "hours": 5, "version": "v2",
            "desc": "Robust data handling → v2 professional tool"},
    "oop": {"name": "Object-Oriented Programming", "semester": 3, "year": 2, "hours": 3, "version": "v3-arch",
            "desc": "Refactor into architecture → v3 components"},
    "dsa": {"name": "Data Structures & Algorithms", "semester": 4, "year": 2, "hours": 3, "version": "v3-perf",
            "desc": "Optimize + benchmark → v3 performance proof"},
}


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Student, int(user_id))


# ── Auth Routes ─────────────────────────────────────────────────────

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        student = Student.query.filter_by(email=email).first()
        if student and student.check_password(password):
            login_user(student)
            return redirect(url_for("dashboard"))
        flash("Invalid email or password.", "error")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        sid = request.form.get("student_id", "").strip()
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if Student.query.filter_by(email=email).first():
            flash("Email already registered.", "error")
            return render_template("register.html")
        if Student.query.filter_by(student_id=sid).first():
            flash("Student ID already exists.", "error")
            return render_template("register.html")

        student = Student(student_id=sid, name=name, email=email)
        student.set_password(password)
        db.session.add(student)
        db.session.commit()
        login_user(student)
        flash("Welcome! Please select your track.", "success")
        return redirect(url_for("select_track"))
    return render_template("register.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# ── Dashboard ───────────────────────────────────────────────────────

@app.route("/")
@login_required
def dashboard():
    courses = Course.query.order_by(Course.semester).all()
    progress = {}
    for c in courses:
        progress[c.code] = current_user.get_progress(c.code)

    current_phase = current_user.get_current_phase()
    recent_checks = current_user.check_results.order_by(CheckResult.timestamp.desc()).limit(5).all()
    open_recovery = current_user.recovery_tickets.filter_by(status="open").count()

    # Timeline data for project evolution
    phases = current_user.project_phases.order_by(ProjectPhase.created_at).all()

    return render_template("dashboard.html",
                           courses=courses, progress=progress,
                           current_phase=current_phase,
                           recent_checks=recent_checks,
                           open_recovery=open_recovery,
                           phases=phases, tracks=TRACKS)


# ── Track Selection ─────────────────────────────────────────────────

@app.route("/track", methods=["GET", "POST"])
@login_required
def select_track():
    if request.method == "POST":
        track = request.form.get("track")
        if track in TRACKS:
            current_user.track = track
            if request.form.get("confirm") == "yes":
                current_user.track_confirmed = True
            db.session.commit()
            flash(f"Track set to {TRACKS[track]['name']}!", "success")
            return redirect(url_for("dashboard"))
        flash("Invalid track selection.", "error")
    return render_template("track.html", tracks=TRACKS)


# ── Course View ─────────────────────────────────────────────────────

@app.route("/course/<code>")
@login_required
def course_view(code):
    course = Course.query.filter_by(code=code).first_or_404()
    weeks = course.weeks.order_by(Week.week_num).all()

    week_status = {}
    for w in weeks:
        check = current_user.check_results.filter_by(week_id=w.id).order_by(CheckResult.timestamp.desc()).first()
        subs = Submission.query.filter_by(student_id=current_user.id).join(Deliverable).filter(Deliverable.week_id == w.id).all()
        submitted_count = sum(1 for s in subs if s.status in ("submitted", "passed"))
        total_deliverables = w.deliverables.count()

        week_status[w.id] = {
            "check_passed": check.passed if check else None,
            "submissions": submitted_count,
            "total": total_deliverables,
            "recovery": current_user.recovery_tickets.filter_by(week_id=w.id).first(),
        }

    return render_template("course.html", course=course, weeks=weeks,
                           week_status=week_status, tracks=TRACKS)


# ── Week Detail ─────────────────────────────────────────────────────

@app.route("/course/<code>/week/<int:week_num>")
@login_required
def week_view(code, week_num):
    course = Course.query.filter_by(code=code).first_or_404()
    week = Week.query.filter_by(course_id=course.id, week_num=week_num).first_or_404()
    deliverables = week.deliverables.order_by(Deliverable.order).all()

    sub_status = {}
    for d in deliverables:
        sub = Submission.query.filter_by(student_id=current_user.id, deliverable_id=d.id).order_by(Submission.created_at.desc()).first()
        sub_status[d.id] = sub

    check = current_user.check_results.filter_by(week_id=week.id).order_by(CheckResult.timestamp.desc()).first()
    reflection = Reflection.query.filter_by(student_id=current_user.id, week_id=week.id).first()
    recovery = RecoveryTicket.query.filter_by(student_id=current_user.id, week_id=week.id).first()

    prev_week = Week.query.filter_by(course_id=course.id, week_num=week_num - 1).first()
    next_week = Week.query.filter_by(course_id=course.id, week_num=week_num + 1).first()

    return render_template("week.html", course=course, week=week,
                           deliverables=deliverables, sub_status=sub_status,
                           check=check, reflection=reflection, recovery=recovery,
                           prev_week=prev_week, next_week=next_week, tracks=TRACKS)


# ── Submit Deliverable ──────────────────────────────────────────────

@app.route("/submit/<int:deliverable_id>", methods=["POST"])
@login_required
def submit_deliverable(deliverable_id):
    deliverable = Deliverable.query.get_or_404(deliverable_id)
    status = request.form.get("status", "submitted")
    grade = request.form.get("grade", "")
    notes = request.form.get("notes", "")

    sub = Submission.query.filter_by(student_id=current_user.id, deliverable_id=deliverable_id).first()
    if sub:
        sub.status = status
        sub.grade = grade
        sub.notes = notes
        sub.submitted_at = datetime.utcnow()
    else:
        sub = Submission(student_id=current_user.id, deliverable_id=deliverable_id,
                         status=status, grade=grade, notes=notes, submitted_at=datetime.utcnow())
        db.session.add(sub)
    db.session.commit()
    flash("Submission recorded!", "success")

    week = deliverable.week
    return redirect(url_for("week_view", code=week.course.code, week_num=week.week_num))


# ── Check Result ────────────────────────────────────────────────────

@app.route("/check/<int:week_id>", methods=["POST"])
@login_required
def submit_check(week_id):
    week = Week.query.get_or_404(week_id)
    passed = request.form.get("passed") == "true"
    total = int(request.form.get("total_checks", 0))
    passed_checks = int(request.form.get("passed_checks", 0))
    details = request.form.get("details", "")

    result = CheckResult(student_id=current_user.id, week_id=week_id,
                         passed=passed, total_checks=total,
                         passed_checks=passed_checks, details=details)
    db.session.add(result)
    db.session.commit()
    flash("Check result recorded!" if passed else "Check result recorded. Fix failures and re-run.", "success" if passed else "warning")
    return redirect(url_for("week_view", code=week.course.code, week_num=week.week_num))


# ── Project Evolution ───────────────────────────────────────────────

@app.route("/project")
@login_required
def project_view():
    phases = current_user.project_phases.order_by(ProjectPhase.created_at).all()
    courses = Course.query.order_by(Course.semester).all()

    # Build evolution timeline
    evolution = []
    for c in courses:
        course_phases = [p for p in phases if p.course_code == c.code]
        progress = current_user.get_progress(c.code)
        evolution.append({
            "course": c,
            "phases": course_phases,
            "progress": progress,
            "latest": course_phases[-1] if course_phases else None,
        })

    return render_template("project.html", evolution=evolution, tracks=TRACKS)


@app.route("/project/update", methods=["POST"])
@login_required
def update_project():
    course_code = request.form.get("course_code")
    version = request.form.get("version")
    status = request.form.get("status", "in_progress")
    description = request.form.get("description", "")
    features = request.form.get("features", "")
    commit = request.form.get("commit", "")

    phase = ProjectPhase(
        student_id=current_user.id, course_code=course_code,
        version=version, status=status, description=description,
        features=features, repo_commit=commit)
    db.session.add(phase)
    db.session.commit()
    flash("Project phase updated!", "success")
    return redirect(url_for("project_view"))


# ── Recovery Ticket ─────────────────────────────────────────────────

@app.route("/recovery/<int:week_id>", methods=["POST"])
@login_required
def submit_recovery(week_id):
    ticket = RecoveryTicket(
        student_id=current_user.id, week_id=week_id,
        what_failed=request.form.get("what_failed", ""),
        what_tried=request.form.get("what_tried", ""),
        next_steps=request.form.get("next_steps", ""))
    db.session.add(ticket)
    db.session.commit()
    flash("Recovery ticket submitted.", "info")
    week = Week.query.get(week_id)
    return redirect(url_for("week_view", code=week.course.code, week_num=week.week_num))


# ── Reflection ──────────────────────────────────────────────────────

@app.route("/reflection/<int:week_id>", methods=["POST"])
@login_required
def submit_reflection(week_id):
    existing = Reflection.query.filter_by(student_id=current_user.id, week_id=week_id).first()
    if existing:
        existing.learned = request.form.get("learned", "")
        existing.hardest = request.form.get("hardest", "")
        existing.unclear = request.form.get("unclear", "")
        existing.next_review = request.form.get("next_review", "")
        existing.ai_usage = request.form.get("ai_usage", "")
    else:
        ref = Reflection(
            student_id=current_user.id, week_id=week_id,
            learned=request.form.get("learned", ""),
            hardest=request.form.get("hardest", ""),
            unclear=request.form.get("unclear", ""),
            next_review=request.form.get("next_review", ""),
            ai_usage=request.form.get("ai_usage", ""))
        db.session.add(ref)
    db.session.commit()
    flash("Reflection saved!", "success")
    week = Week.query.get(week_id)
    return redirect(url_for("week_view", code=week.course.code, week_num=week.week_num))


# ── Admin ───────────────────────────────────────────────────────────

@app.route("/admin")
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash("Access denied.", "error")
        return redirect(url_for("dashboard"))

    students = Student.query.order_by(Student.name).all()
    courses = Course.query.order_by(Course.semester).all()
    teams = Team.query.all()

    # Red list: students who failed checks or missed cores
    red_list = []
    for s in students:
        failed_checks = s.check_results.filter_by(passed=False).count()
        open_recovery = s.recovery_tickets.filter_by(status="open").count()
        if failed_checks >= 2 or open_recovery >= 2:
            red_list.append({"student": s, "failed": failed_checks, "recovery": open_recovery})

    return render_template("admin.html", students=students, courses=courses,
                           teams=teams, red_list=red_list, tracks=TRACKS)


# ── API Endpoints (for AJAX) ────────────────────────────────────────

@app.route("/api/progress")
@login_required
def api_progress():
    courses = Course.query.order_by(Course.semester).all()
    data = {}
    for c in courses:
        data[c.code] = {
            "name": c.name,
            "progress": current_user.get_progress(c.code),
            "version": c.version_target,
        }
    return jsonify(data)


@app.route("/api/timeline")
@login_required
def api_timeline():
    phases = current_user.project_phases.order_by(ProjectPhase.created_at).all()
    data = [{
        "course": p.course_code,
        "version": p.version,
        "status": p.status,
        "date": p.created_at.isoformat(),
        "description": p.description,
    } for p in phases]
    return jsonify(data)


# ── Initialize ──────────────────────────────────────────────────────

def init_database():
    """Create tables and seed initial data."""
    db.create_all()

    # Create courses if they don't exist
    if Course.query.count() == 0:
        for code, info in COURSES.items():
            course = Course(code=code, name=info["name"], semester=info["semester"],
                            year=info["year"], hours_per_week=info["hours"],
                            total_weeks=14, version_target=info["version"],
                            description=info["desc"])
            db.session.add(course)
        db.session.commit()

        # Seed weeks
        week_data = {
            "cp1": [
                (1, "Welcome to Python & Your Pipeline", "S1"),
                (2, "Variables, Types & Numbers", "S1"),
                (3, "Making Decisions (Conditionals)", "S2"),
                (4, "Decision Logic & Classification", "S2"),
                (5, "Loops: Scanning Data", "S3"),
                (6, "Loops: Counting Events", "S3"),
                (7, "Lists: Indexing & Windows", "S4"),
                (8, "Strings: Parsing Data", "S4"),
                (9, "Functions: Building Blocks", "S5"),
                (10, "Functions: Decomposition & Reuse", "S5"),
                (11, "Exceptions: Handling Errors", "S6"),
                (12, "File I/O: Reading & Writing", "S6"),
                (13, "Integration: End-to-End Pipeline", "S6"),
                (14, "v1 Release & Demo", "S6"),
            ],
            "cp2": [
                (1, "Schema Validation", "S7"),
                (2, "Dict Analytics", "S7"),
                (3, "Configurable Cleaning Pipeline", "S8"),
                (4, "Data Quality Reports", "S8"),
                (5, "Matplotlib Standards", "S9"),
                (6, "Report Generation", "S9"),
                (7, "NumPy Introduction", "S10"),
                (8, "Timing & Performance", "S10"),
                (9, "Testing: Expanded Self-Check", "S11"),
                (10, "Golden Outputs", "S11"),
                (11, "Modularize into /src", "S12"),
                (12, "Package Hygiene", "S12"),
                (13, "Integration on Larger Data", "S12"),
                (14, "v2 Release & Demo", "S12"),
            ],
            "oop": [
                (1, "OOP Kickoff: Classes & Objects", ""),
                (2, "Composition: DataSource & Dataset", ""),
                (3, "Cleaner Component", ""),
                (4, "Analyzer Component", ""),
                (5, "Plotter & Reporter Components", ""),
                (6, "Domain Exceptions & Validation", ""),
                (7, "SOLID Principles (SRP/OCP)", ""),
                (8, "Strategy Pattern", ""),
                (9, "Factory & Registry Pattern", ""),
                (10, "Testing with pytest", ""),
                (11, "Package Hygiene", ""),
                (12, "Plugin Exercise", ""),
                (13, "Architecture Freeze", ""),
                (14, "v3 Architecture Demo", ""),
            ],
            "dsa": [
                (1, "Big-O & Python Cost Model", ""),
                (2, "Benchmark Literacy", ""),
                (3, "Searching: Linear vs Binary", ""),
                (4, "Sorting Algorithms", ""),
                (5, "Hashing & Indexing", ""),
                (6, "Heap & Priority Queue", ""),
                (7, "Performance Sprint 1", ""),
                (8, "Performance Sprint 2", ""),
                (9, "Trees & BST", ""),
                (10, "Graphs: BFS & DFS", ""),
                (11, "Shortest Paths", ""),
                (12, "Dynamic Programming", ""),
                (13, "Final Integration", ""),
                (14, "Final Performance Report", ""),
            ],
        }

        for code, weeks in week_data.items():
            course = Course.query.filter_by(code=code).first()
            for wnum, title, sprint in weeks:
                week = Week(course_id=course.id, week_num=wnum, title=title, sprint=sprint)
                db.session.add(week)

                # Add standard deliverables per week
                for order, (dtype, dname) in enumerate([
                    ("core_notebook", "Core Notebook"),
                    ("studio_notebook", "Studio Notebook"),
                    ("check", "Universal Check"),
                    ("homework", "Homework"),
                    ("export", "Required Exports"),
                    ("code", "Pipeline Code Update"),
                ]):
                    d = Deliverable(week_id=None, name=dname,
                                    deliverable_type=dtype, required=True, order=order)
                    week.deliverables.append(d)

        db.session.commit()

    # Create admin user if none exists
    if not Student.query.filter_by(is_admin=True).first():
        admin = Student(student_id="admin", name="Instructor", email="admin@courseos.local", is_admin=True)
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()

    # Create demo student if none exists
    if Student.query.count() <= 1:
        demo = Student(student_id="2025-MC-001", name="Demo Student",
                       email="demo@courseos.local", track="robotics", track_confirmed=True)
        demo.set_password("demo123")
        db.session.add(demo)
        db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        init_database()
    app.run(debug=True, port=5050)
