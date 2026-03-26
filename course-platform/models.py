"""Database models for CourseOS Platform."""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

# ── Association tables ──────────────────────────────────────────────

team_members = db.Table(
    "team_members",
    db.Column("student_id", db.Integer, db.ForeignKey("students.id"), primary_key=True),
    db.Column("team_id", db.Integer, db.ForeignKey("teams.id"), primary_key=True),
)


# ── Core models ─────────────────────────────────────────────────────

class Student(UserMixin, db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)  # e.g. "2025-MC-001"
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    track = db.Column(db.String(30), default="undecided")  # robotics/data/simulation/space/iot
    track_confirmed = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    submissions = db.relationship("Submission", backref="student", lazy="dynamic")
    check_results = db.relationship("CheckResult", backref="student", lazy="dynamic")
    project_phases = db.relationship("ProjectPhase", backref="student", lazy="dynamic")
    recovery_tickets = db.relationship("RecoveryTicket", backref="student", lazy="dynamic")
    reflections = db.relationship("Reflection", backref="student", lazy="dynamic")
    teams = db.relationship("Team", secondary=team_members, backref=db.backref("members", lazy="dynamic"))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_progress(self, course_code):
        """Get completion percentage for a course."""
        course = Course.query.filter_by(code=course_code).first()
        if not course:
            return 0
        total_weeks = course.weeks.count()
        if total_weeks == 0:
            return 0
        completed = 0
        for week in course.weeks:
            check = self.check_results.filter_by(week_id=week.id).order_by(CheckResult.timestamp.desc()).first()
            if check and check.passed:
                completed += 1
        return round(completed / total_weeks * 100)

    def get_current_phase(self):
        """Get the latest project phase."""
        return self.project_phases.order_by(ProjectPhase.updated_at.desc()).first()


class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    track = db.Column(db.String(30))
    repo_url = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)  # cp1, cp2, oop, dsa
    name = db.Column(db.String(120), nullable=False)
    semester = db.Column(db.Integer, nullable=False)  # 1-4
    year = db.Column(db.Integer, nullable=False)  # 1 or 2
    hours_per_week = db.Column(db.Integer, default=5)
    total_weeks = db.Column(db.Integer, default=14)
    version_target = db.Column(db.String(10))  # v1, v2, v3
    description = db.Column(db.Text)

    weeks = db.relationship("Week", backref="course", lazy="dynamic", order_by="Week.week_num")


class Week(db.Model):
    __tablename__ = "weeks"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    week_num = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    sprint = db.Column(db.String(20))  # S1, S2, etc.
    must_pass = db.Column(db.Text)  # must-pass core description
    standard_target = db.Column(db.Text)
    stretch_target = db.Column(db.Text)

    deliverables = db.relationship("Deliverable", backref="week", lazy="dynamic")
    check_results = db.relationship("CheckResult", backref="week", lazy="dynamic")

    __table_args__ = (db.UniqueConstraint("course_id", "week_num"),)


class Deliverable(db.Model):
    __tablename__ = "deliverables"

    id = db.Column(db.Integer, primary_key=True)
    week_id = db.Column(db.Integer, db.ForeignKey("weeks.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    deliverable_type = db.Column(db.String(30))  # core_notebook, studio_notebook, check, homework, export, code
    required = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=0)

    submissions = db.relationship("Submission", backref="deliverable", lazy="dynamic")


class Submission(db.Model):
    __tablename__ = "submissions"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    deliverable_id = db.Column(db.Integer, db.ForeignKey("deliverables.id"), nullable=False)
    status = db.Column(db.String(20), default="pending")  # pending, submitted, passed, failed, late
    grade = db.Column(db.String(10))  # core, standard, stretch
    notes = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime)
    graded_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class CheckResult(db.Model):
    __tablename__ = "check_results"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    week_id = db.Column(db.Integer, db.ForeignKey("weeks.id"), nullable=False)
    passed = db.Column(db.Boolean, default=False)
    total_checks = db.Column(db.Integer, default=0)
    passed_checks = db.Column(db.Integer, default=0)
    details = db.Column(db.Text)  # JSON with individual check results
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class ProjectPhase(db.Model):
    __tablename__ = "project_phases"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    course_code = db.Column(db.String(10), nullable=False)
    version = db.Column(db.String(10), nullable=False)  # v1, v2, v3-arch, v3-perf
    status = db.Column(db.String(20), default="in_progress")  # in_progress, submitted, approved, needs_work
    description = db.Column(db.Text)
    features = db.Column(db.Text)  # JSON list of implemented features
    repo_commit = db.Column(db.String(40))  # git commit hash
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RecoveryTicket(db.Model):
    __tablename__ = "recovery_tickets"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    week_id = db.Column(db.Integer, db.ForeignKey("weeks.id"), nullable=False)
    what_failed = db.Column(db.Text, nullable=False)
    what_tried = db.Column(db.Text, nullable=False)
    next_steps = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="open")  # open, in_progress, resolved
    instructor_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)

    week = db.relationship("Week")


class Reflection(db.Model):
    __tablename__ = "reflections"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    week_id = db.Column(db.Integer, db.ForeignKey("weeks.id"), nullable=False)
    learned = db.Column(db.Text)
    hardest = db.Column(db.Text)
    unclear = db.Column(db.Text)
    next_review = db.Column(db.Text)
    ai_usage = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    week = db.relationship("Week")
