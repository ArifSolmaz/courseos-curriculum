# CourseOS — Complete 2-Year Course Content

## Overview

| Course | Semester | Weeks | Session | Focus |
|--------|----------|-------|---------|-------|
| **CP1** | Year 1, Sem 1 | 14 | 5h/week | Python fundamentals → v1 functional pipeline |
| **CP2** | Year 1, Sem 2 | 14 | 5h/week | Robust data handling → v2 professional tool |
| **OOP** | Year 2, Sem 3 | 14 | 3h/week | Refactor into architecture → v3 components |
| **DSA** | Year 2, Sem 4 | 14 | 3h/week | Optimize + benchmark → v3 performance proof |

## Content Per Week (8 notebooks)

| Notebook | Filename | Purpose |
|----------|----------|---------|
| Core | `W{nn}_core.ipynb` | Concepts, examples, micro-tasks, mini-quiz |
| Studio (×5) | `W{nn}_studio_{track}.ipynb` | Track-specific project work |
| Check | `W{nn}_check.ipynb` | Automated pass/fail validation |
| Homework | `W{nn}_homework.ipynb` | Substantial outside-class exercises |

## 5 Tracks

1. **Robotics/Mechatronics** — MechaSense Studio (sensor streams)
2. **Data/AI** — CleanReport Pipeline (messy CSV cleanup)
3. **Simulation/Games** — SimLab Engine (discrete simulation)
4. **Space/Astro** — Lightcurve Explorer (star brightness)
5. **IoT/Reporting** — AutoDashboard Reporter (IoT dashboards)

## Directory Structure

```
course-content/
├── notebooks/
│   ├── cp1/          # 112 notebooks (14 weeks × 8)
│   ├── cp2/          # 112 notebooks
│   ├── oop/          # 112 notebooks
│   └── dsa/          # 112 notebooks
├── src/
│   └── project_template/
│       ├── __init__.py
│       ├── config.py
│       ├── io.py
│       ├── cleaning.py
│       ├── analysis.py
│       ├── plotting.py
│       ├── reporting.py
│       ├── core/     # OOP components (Year 2)
│       └── dsa/      # DSA optimized modules (Year 2)
├── tests/
│   └── test_pipeline.py
├── data/
│   ├── raw/
│   └── cleaned/
├── reports/
│   ├── figures/
│   └── benchmark/
└── README.md
```

## Total: 448 notebooks + project template + tests

## Three-Level Targets (Every Week)

- **Must-pass core**: Minimum to pass — everyone must finish this
- **Standard target**: Normal weekly goal
- **Stretch**: Optional extension for strong students

## Running in Google Colab

1. Open any `.ipynb` file in GitHub
2. Copy URL → Colab → File → Open → GitHub → paste
3. Run the setup cell first
4. Work top-to-bottom
