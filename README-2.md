# README.md — CourseOS (Colab-First Studio Courses: CP1 → CP2 → OOP → DSA)

Welcome! This repository is the **single project codebase** you will use across four courses over two years:

- **CP1 (Semester 1):** Python fundamentals → **v1 functional tool**
- **CP2 (Semester 2):** Robust data handling, plotting, testing → **v2 professional tool**
- **OOP (Year 2, Semester 3):** Refactor into maintainable architecture → **v3 architecture**
- **DSA (Year 2, Semester 4):** Optimize bottlenecks + benchmarks → **v3 performance**

This course is **studio-based and lecture-light**. You learn primarily by building through weekly Colab materials, the shared project repo, and universal checks. The instructor coaches during class and may run short mini-clinics or brief concept interventions when needed. Slides/board use is minimal and optional—the notebooks and project evidence are the main medium.

---

## 1) Track Selection (Explore first, confirm early)

You will begin CP1 by exploring the available project tracks through common starter tasks and short examples.

### Track confirmation rule
- **Weeks 1–2:** exploration
- **Week 3:** confirm your track
- After Week 3, your track is normally fixed for CP1 and CP2
- Before Year 2, one exceptional reset may be approved if the common repo contract can be preserved
- No track changes are allowed during OOP or DSA

### Important note
Track stability matters because you will keep one project repository across four courses.

### If you want to request a change
A change request may be approved only if:
- you are current on the must-pass core or have an approved recovery note,
- your repo can be adapted cleanly,
- the request is not being used to escape missed work or failed checks.

## 2) The Contract (What every project must implement)

### Year 1 Contract (CP1 + CP2): Functional Pipeline
In `/src/<project_name>/`, implement:

- `load_data(config) -> data`
- `clean_data(data, config) -> clean_data`
- `analyze(clean_data, config) -> results (dict)`
- `plot(clean_data, results, config) -> figures (list)`
- `export_results(clean_data, results, figures, config) -> exported_paths (dict)`
- `self_check() -> None` *(assert-based tests)*

### Year 2 Contract (OOP + DSA): Engineered + Optimized
- **OOP:** refactor pipeline into components in `/src/<project_name>/core/`:
  - `DataSource`, `Cleaner`, `Analyzer`, `Plotter`, `Reporter`
- **DSA:** implement one optimized module in `/src/<project_name>/dsa/` and prove it with benchmarks:
  - baseline vs optimized timing
  - benchmark plot
  - Big-O justification

---

## 3) Repository Layout (Do not change these paths)

```
/notebooks
  /cp1
  /cp2
  /oop
  /dsa
/src
  /project_name
    __init__.py
    config.py
    io.py
    cleaning.py
    analysis.py
    plotting.py
    reporting.py
    core/        # OOP (Year 2)
    dsa/         # DSA (Year 2)
/tests          # pytest (Year 2 mandatory; CP2 recommended)
/data
  raw/
  cleaned/
/reports
  figures/
  benchmark/
README.md
```

**Rule:** Notebooks should **import code from `/src`**.  
Notebooks are for running, visualizing, and reporting — not for storing large chunks of logic.

---

## 4) How to Work Each Week (Studio Workflow)

Each week you will receive:
1) **Core Notebook** — concepts, worked examples, and small tasks
2) **Track Studio Notebook** — the implementation step for your project
3) **Universal Check** — validation of your code, exports, and required evidence

Each week also has three targets:
- **Must-pass core:** minimum working version you must complete
- **Standard target:** normal weekly goal
- **Stretch:** optional extension for strong/fast groups

Your job in the weekly session is to:
- complete the must-pass core first,
- work toward the standard target,
- run the universal check,
- fix failures in `/src`,
- export required files,
- submit the required evidence.

## 5) Opening Notebooks in Google Colab

### Option A — Open from GitHub (recommended)
1. Open a notebook file in GitHub (e.g., `/notebooks/cp1/W01_*.ipynb`)
2. Copy the GitHub URL
3. Go to Colab → `File → Open notebook → GitHub`
4. Paste the URL and open

### Option B — Upload notebook
1. Download `.ipynb` from GitHub
2. Upload to Colab
3. Run it top-to-bottom

---

## 6) Connecting This Repo to Colab (Importing from `/src`)

In Colab, you must ensure Python can import from `/src`.

Typical patterns:
- If you cloned/downloaded the repo into Colab, add:

```python
import sys
sys.path.append("/content/<REPO_FOLDER>/src")
```

- If the notebooks already include setup cells, **do not delete them**.

**In CP2 and later**, the instructor may require that notebooks contain minimal logic and import from `/src`.

---

## 7) Required Outputs (Exports)

After running `export_results(...)`, your project must create:

### Year 1 minimum exports
- `data/cleaned/cleaned.csv` *(or `cleaned.json`)*
- `reports/report.json`
- `reports/figures/timeseries.png`
- `reports/figures/summary.png`

### `report.json` minimum schema
Your `report.json` must include:
- `project_name`, `track`, `version`
- `dataset`: `n_raw`, `n_clean`, `n_dropped`
- `cleaning_summary`: counts per reason
- `analysis_summary`: at least 3 numeric metrics
- `figures`: list of filenames

### Year 2 additions
- `reports/benchmark/benchmark_results.json`
- `reports/benchmark/benchmark_plot.png`
- Passing `pytest` tests under `/tests`

---

## 8) Self-Check and Universal Check

### Your responsibility
- Run `self_check()` every week before submission.
- Run the **Universal Check Notebook** (provided weekly).
- Fix failures **in `/src`**, not by patching only the notebook.

### What is tested
- required functions exist and run
- outputs have correct types/shape
- numeric results match expectations within tolerances (toy datasets)
- edge cases (invalid rows, missing values, out-of-range)
- exports exist in correct paths and are non-empty

**No interactive input** (`input()`) is allowed in graded runs.

---

## 9) Submission Rules (Recommended Standard)

**Default repo model:** one GitHub Classroom repository per team (pair/small group). Individual accountability is enforced via quizzes, oral checks, reflections, and recovery notes.

Your instructor will specify the exact method, but typically:
- Work in Colab during class
- Save outputs and notebooks
- Push to your GitHub Classroom repository (or upload notebooks + exports as instructed)

A submission is considered valid if:
- universal check passes
- exports exist and match schema
- required plots are present
- reflection cell is completed

---

## 9.1 AI Use and Academic Integrity

AI tools may be used only if the instructor allows them for the course or assignment.

If AI assistance is allowed:
- students must still understand and be able to explain submitted code
- major AI-assisted code or debugging help must be disclosed briefly in the reflection
- copied code that the student cannot explain counts as an integrity problem

If AI assistance is not allowed:
- any undisclosed AI-generated code or text is treated like unauthorized outside help

**Rule:** “It runs” is not enough. You must be able to explain what your code does, why it works, and where the key logic lives.

## 10) Assessment (High-level rubric)

Grading is track-agnostic and based on:
- **Correctness**
- **Robustness**
- **Code quality and modularity**
- **Testing**
- **Plots/Reporting quality**
- **Engineering justification**
- (Year 2) **Architecture quality** and **Performance proof**

## 10.1 Assessment Weights (Default Policy)

Unless the instructor announces a course-specific variant, the default weights are:

### CP1 / CP2
- Weekly studio submissions + universal checks: **50%**
- Quizzes / code-reading / oral explain-your-code checks: **20%**
- Release demo (v1 or v2): **20%**
- Professional habits (reflection, checkpoint compliance, recovery completion): **10%**

### OOP / DSA
- Weekly studio submissions + tests/benchmarks: **45%**
- Quizzes / code-reading / oral checks: **20%**
- Final architecture/performance release: **25%**
- Professional habits (engineering notes, checkpoint compliance, recovery completion): **10%**

**Note:** support and recovery are part of the course design, but repeated missed checkpoints or incomplete recovery may limit a week to the must-pass/core band until stable progress is re-established.

---

## 11) Common Pitfalls (Avoid these)

- Writing major logic in notebooks instead of `/src`
- Skipping self-check and discovering failures at submission time
- Hardcoding file paths that break on Colab
- Using `input()` for graded tasks
- Not saving required exports in the required folders

---

## 12) Quick Start Checklist (Week 1)

1. Open the **Week 1 Core Notebook** in Colab
2. Run the setup cells
3. Execute the provided example from top to bottom
4. Change one parameter or small code block
5. Generate one visible output (figure, metric, or export)
6. Run the starter check
7. Save your work using the required method
8. Review the available tracks during Weeks 1–2 before confirming one in Week 3

## 13) Support Protocol (Help Queue)
When requesting help, provide:
- Track + Week/Sprint
- Notebook cell number
- Error message (copy-paste)
- What you tried (1–2 lines)

This makes tutoring efficient and fair.

---

## 14) Learning Support (Must-pass core + Recovery)

This course is designed so that nobody should fail silently.

### Weekly structure
Each week has:
- **Must-pass core**
- **Standard target**
- **Stretch extension**

If you cannot finish the standard target, focus on the must-pass core first.

### If you get stuck
Use the guided rescue parts of the notebook:
- smaller toy data,
- more scaffolding,
- debugging prompts,
- expected intermediate outputs.

### If you still cannot finish
Submit a short recovery note:
- what failed,
- what you tried,
- what you will do next.

Support is built into the course, but you are still responsible for showing progress and understanding your own code.

## 15) Teamwork, Individual Accountability, and Group Policy

Studio implementation may be collaborative, but understanding and accountability are always individual.

- Weekly code-reading quizzes are **individual**
- Oral “explain your code” checks are **individual**
- Reflections and recovery tickets are **individual**
- A student who cannot explain the submitted code may receive an individual penalty even if the group submission passes

**Rule:** group success does not override individual responsibility.
