# INSTRUCTIONS.md — How to Use README.md, COURSEOS.md, and PROJECT_BANK.md

This repository includes three documents with **different audiences and roles**. Keep them all, but use them intentionally.

---

## 1) README.md (Student-facing)
**Purpose:** the operational guide students read first.

Use README.md to explain:
- what students do each week (Core Notebook → Studio Notebook → Universal Check)
- how track exploration/confirmation works
- submission workflow and required exports
- AI use & academic integrity expectations
- teamwork vs individual accountability
- quick start checklist (Week 1)

**Rule of thumb:** if students need it to *work and submit*, it belongs in README.md.

---

## 2) COURSEOS.md (Instructor-facing)
**Purpose:** the instructor’s operating system and governance layer.

Use COURSEOS.md to define:
- program invariants across 4 courses (CP1/CP2/OOP/DSA)
- session protocols (5h studio, 3h studio)
- project contracts and evidence standards
- support architecture (must-pass core, checkpoints, recovery)
- repository governance (recovery protocol, structure checks)
- grading policy rationale and success criteria

**Rule of thumb:** if it’s *policy, enforcement, or program design*, it belongs in COURSEOS.md.

---

## 3) PROJECT_BANK.md (Optional variants)
**Purpose:** a lightweight list of alternate project ideas that still fit the same contract.

Use PROJECT_BANK.md when:
- you want optional project variants beyond the default track flagships
- you want an “approved alternatives” catalog without bloating the operating documents

**Rule of thumb:** optional ideas live here so the main system stays lean.

---

## 4) Recommended placement in a real GitHub Classroom setup

### Minimum student repo (public to students)
- `README.md` (root)
- `/notebooks/…` weekly materials
- `/src/…` project code
- `/tests/…` (especially Year 2)
- `/data/…`, `/reports/…`

### Instructor-only (recommended)
Option A (preferred):
- keep `COURSEOS.md` and `PROJECT_BANK.md` in an instructor-only repo

Option B (single repo, still OK):
- move them into an instructor folder:
  - `/instructor/COURSEOS.md`
  - `/instructor/PROJECT_BANK.md`

---

## 5) When to update which document
- **Update README.md** when student workflow changes (submission, checks, exports, weekly targets).
- **Update COURSEOS.md** when policy changes (track rules, recovery rules, grading governance).
- **Update PROJECT_BANK.md** when you add/remove optional project variants.

---

## 6) One-sentence summary
- **README.md = student operations**
- **COURSEOS.md = instructor governance**
- **PROJECT_BANK.md = optional project variants**
