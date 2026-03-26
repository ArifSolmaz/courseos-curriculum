# CourseOS — Project-Based Python Curriculum (2 Years, 4 Courses)

A complete, studio-based curriculum for teaching Python to Mechatronics Engineering undergraduates through one continuous project that evolves across four semesters.

## Overview

Students select a project track in Week 1 and keep **one repository** across all four courses. Their project evolves from a simple script to a production-quality tool:

| Course | Semester | Hours/Week | Output |
|--------|----------|-----------|--------|
| **CP1** — Computer Programming 1 | Year 1, Sem 1 | 5h | **v1** — Functional pipeline |
| **CP2** — Computer Programming 2 | Year 1, Sem 2 | 5h | **v2** — Robust, modular, tested |
| **OOP** — Object-Oriented Programming | Year 2, Sem 3 | 3h | **v3** — Engineered architecture |
| **DSA** — Data Structures & Algorithms | Year 2, Sem 4 | 3h | **v3** — Optimized + benchmarked |

## 5 Project Tracks

| Track | Product | Domain |
|-------|---------|--------|
| Robotics/Mechatronics | MechaSense Studio | Sensor streams, fault detection |
| Data/AI | CleanReport Pipeline | CSV cleanup, automated reports |
| Simulation/Games | SimLab Engine | Discrete simulation, scoring |
| Space/Astro | Lightcurve Explorer | Star brightness, dip detection |
| IoT/Reporting | AutoDashboard Reporter | IoT dashboards, time-series |

All tracks follow the **same contract** (same function signatures, same exports, same grading).

## Repository Structure

```
.
├── COURSEOS-3.md              # Instructor governance document
├── INSTRUCTIONS.md            # How the documents relate
├── PROJECT_BANK.md            # Optional alternate project ideas
├── README.md                  # This file
│
├── course-content/            # 448 Colab notebooks + project template
│   ├── notebooks/
│   │   ├── cp1/               # 112 notebooks (14 weeks × 8)
│   │   ├── cp2/               # 112 notebooks
│   │   ├── oop/               # 112 notebooks
│   │   └── dsa/               # 112 notebooks
│   ├── src/                   # Project template code
│   │   └── project_template/
│   ├── tests/                 # Starter pytest suite
│   ├── data/                  # Data directories
│   ├── reports/               # Report output directories
│   ├── generate_cp1.py        # Notebook generators (rerunnable)
│   ├── generate_cp2.py
│   ├── generate_oop.py
│   ├── generate_dsa.py
│   └── nb_utils.py            # Shared notebook utilities
│
└── course-platform/           # Student tracking web app (Flask)
    ├── app.py                 # Main application
    ├── models.py              # Database models
    ├── templates/             # HTML templates
    ├── static/                # CSS + JS
    └── requirements.txt       # Python dependencies
```

## Per-Week Content (× 56 Weeks)

Each week provides **8 notebooks**:

| Notebook | File Pattern | Purpose |
|----------|-------------|---------|
| Core | `W{nn}_core.ipynb` | Concepts, worked examples, exercises, homework |
| Studio × 5 | `W{nn}_studio_{track}.ipynb` | Track-specific project implementation |
| Check | `W{nn}_check.ipynb` | Automated pass/fail validation |
| Homework | `W{nn}_homework.ipynb` | Substantial outside-class exercises |

## Three-Level Targets (Every Week)

- **Must-pass core** — minimum working version everyone must finish
- **Standard target** — normal weekly goal
- **Stretch** — optional extension for fast students

## Course Platform

A Flask web application for students and instructors to track progress:

- **Student Dashboard** — pipeline evolution (v1→v2→v3), course progress, recent checks
- **Week View** — deliverable checklist, universal check, reflection, recovery tickets
- **Project Evolution** — visual timeline of project phases across courses
- **Admin Panel** — student roster, progress grid, at-risk student alerts (red list)

### Running the Platform

```bash
cd course-platform
pip install -r requirements.txt
python app.py
# → http://localhost:5050
```

**Default accounts:**
- Instructor: `admin@courseos.local` / `admin123`
- Demo student: `demo@courseos.local` / `demo123`

## Regenerating Notebooks

The notebooks are generated from Python scripts. To regenerate:

```bash
cd course-content
python generate_cp1.py    # 112 notebooks
python generate_cp2.py    # 112 notebooks
python generate_oop.py    # 112 notebooks
python generate_dsa.py    # 112 notebooks
```

## The Pipeline Contract

All tracks implement the same functions in `/src/<project>/`:

### Year 1 (CP1 + CP2)
```python
load_data(config) -> data
clean_data(data, config) -> clean_data
analyze(clean_data, config) -> results (dict)
plot(clean_data, results, config) -> figures (list)
export_results(clean_data, results, figures, config) -> exported_paths (dict)
self_check() -> None
```

### Year 2 — OOP
Refactor into components: `DataSource`, `Cleaner`, `Analyzer`, `Plotter`, `Reporter`

### Year 2 — DSA
Add optimized module with: baseline vs optimized benchmarks, Big-O justification, benchmark plots

## Required Exports

| File | When |
|------|------|
| `data/cleaned/cleaned.csv` | Year 1+ |
| `reports/report.json` | Year 1+ |
| `reports/figures/timeseries.png` | Year 1+ |
| `reports/figures/summary.png` | Year 1+ |
| `reports/benchmark/benchmark_results.json` | Year 2 DSA |
| `reports/benchmark/benchmark_plot.png` | Year 2 DSA |

## License

Educational use. Adapt freely for your institution.
