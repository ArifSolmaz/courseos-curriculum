# Semester Setup Guide

## Before the semester starts (1–2 weeks before Week 1)

### 1. GitHub Classroom

1. Go to [classroom.github.com](https://classroom.github.com)
2. Create an organization (e.g. `mechatronics-2026`)
3. Create a classroom for the course (e.g. `CP1-Fall-2026`)
4. Create a **template repository** from this repo's `course-content/` folder:
   - Include: `/src/project_template/`, `/tests/`, `/data/`, `/reports/`, `README.md`
   - Include: `/notebooks/cp1/` (only the current semester's notebooks)
   - Exclude: `/instructor/`, generator scripts, other semesters' notebooks
5. Create an assignment:
   - Name: `cp1-project` (or `cp2-project`, `oop-project`, `dsa-project`)
   - Template: your template repo
   - Visibility: **private** (students can't see each other's work)
   - Team assignment: **yes** (pairs or small groups, 2–3 students)
6. Share the invite link with students on Day 1

### 2. Google Colab access

- Verify all students have Google accounts (university or personal)
- Test that the Colab links work: `https://colab.research.google.com/github/YOUR-ORG/...`
- If repos are private, students must connect GitHub to Colab:
  - Colab → File → Open notebook → GitHub → authorize

### 3. Prepare Week 1 materials

- Test W01_core.ipynb in Colab end-to-end
- Prepare the micro-quiz (5 questions, 10 minutes)
- Have the track exploration data ready
- Print/share the invite link for GitHub Classroom

### 4. Student roster

- Collect student IDs, emails, GitHub usernames
- If using the Flask platform: create student accounts in bulk
- Assign teams (pairs recommended for Year 1)

---

## Between semesters

### CP1 → CP2 transition
- Students keep the same repo — no new assignment needed
- Add CP2 notebooks to their repos (push to template, students pull)
- Or: students copy CP2 notebooks from the course-content repo manually
- Verify all repos have a working v1 before CP2 starts

### Year 1 → Year 2 transition
- Same repo continues
- This is the window for one exceptional track reset (if requested)
- Add `/src/project_name/core/` and `/src/project_name/dsa/` directories
- Verify pytest works: `pip install pytest && pytest tests/`

### CP2 → OOP transition
- Add OOP notebooks
- Students should have modular `/src` by now — verify

### OOP → DSA transition
- Add DSA notebooks
- Students should have OOP components + passing pytest — verify
- Add `reports/benchmark/` directory

---

## GitHub Classroom tips

- **Don't use individual assignments** if students work in pairs — use team assignments
- **Set a deadline** on GitHub Classroom for each week (optional but helpful)
- **Use the Classroom assistant CLI** to clone all repos for grading: `gh classroom clone student-repos`
- **Roster sync**: link your LMS roster to GitHub Classroom to auto-match students

---

## Checklist

```
[ ] GitHub org created
[ ] Classroom created
[ ] Template repo created (with correct semester's notebooks)
[ ] Assignment created (team, private)
[ ] Invite link tested
[ ] Colab links verified
[ ] W01 materials tested end-to-end
[ ] Student roster collected
[ ] Teams assigned
[ ] Flask platform seeded (if using)
```
