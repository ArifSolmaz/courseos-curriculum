# COURSEOS.md — Two-Year Project-First, Colab-First Curriculum (CP1 → CP2 → OOP → DSA)
**Audience:** Mechatronics Engineering undergraduates  
**Teaching mode:** Studio-based, self-paced weekly materials (no PPT/board lecturing). Instructor tutors/coaches during class.  
**Time constraints:**
- **CP1 & CP2:** 14 weeks each, **single 5-hour session/week**
- **OOP & DSA:** 14 weeks each, **3 hours/week** (separate semesters in Year 2)

---

## 0) Executive Summary
This program runs one cohort through two years of Python-based computing courses by keeping:
- **Continuity** (students keep one project across courses),
- **Choice** (students select a track aligned with their interests),
- **Uniform grading** (all tracks follow the same contract and checks),
- **Engineering realism** (tests, exports, reports, benchmarks),
- **Manageability** (templates, stable repo structure, and universal checks).

Students finish with a portfolio-quality tool that evolves as:
- **v1 (end of CP1):** functional pipeline (works end-to-end)
- **v2 (end of CP2):** robust + plots + exports + modular `/src` + tests
- **v3 (end of Year 2):** engineered architecture (OOP) + optimized module (DSA) + benchmark proof

---

## 1) Non-Negotiable Program Invariants (2-year “contract”)

### 1.1 Track selection (diversity)
Students select one track in **CP1 Week 1** and keep it for 2 years:
1. Robotics/Mechatronics  
2. Data/AI  
3. Simulation/Games  
4. Space/Astro  
5. IoT/Reporting  

### 1.1.1 Track Stability Policy

Track selection is designed to remain stable because the program keeps one repository across four courses.

- Track changes are allowed **only in CP1 Weeks 1–3** (one request, instructor-approved).
- After CP1 Week 3, tracks are **locked for the rest of CP1 and CP2**.
- Before Year 2 starts, **one exceptional reset** may be approved only if the student/group can present a clean migration plan while preserving the common repo contract.
- **No track changes** are allowed during OOP or DSA.

#### Definition of good standing
For track-change requests, “good standing” means:
- the current week’s must-pass core is completed, or an approved recovery ticket is on file,
- there is no unresolved repo structure failure,
- the student is not requesting the change to avoid missed work, failed checks, or recovery obligations.

#### Definition of clean migration plan
A clean migration plan must:
- preserve the common repo structure and contract functions,
- document what dataset/story/module is being changed,
- restore the project to a passing working state before the next week begins.

### 1.2 Year 1 Project Contract (functional pipeline)
Every track must implement these functions in `/src/<project>/`:

- `load_data(config) -> data`
- `clean_data(data, config) -> clean_data`
- `analyze(clean_data, config) -> results (dict)`
- `plot(clean_data, results, config) -> figures (list)`
- `export_results(clean_data, results, figures, config) -> exported_paths (dict)`
- `self_check() -> None` (assert-based)

### 1.3 Year 2 Project Contract (engineered + performance)
**OOP:** refactor pipeline into components with composition:
- `DataSource`, `Cleaner`, `Analyzer`, `Plotter`, `Reporter`

**DSA:** implement one performance-critical feature using an appropriate DS/algorithm and prove it:
- baseline vs optimized benchmarks
- Big-O justification
- benchmark plots

### 1.4 Weekly material package (what you publish every week)
- **Core Notebook:** concepts + worked example + micro tasks (common to all tracks)
- **Track Studio Notebook:** track-specific implementation step (same acceptance criteria)
- **Universal Check:** contract tests + export checks + quality gates

---

## 2) Studio Session Protocols (No lecturing, but highly structured)

### 2.1 CP1/CP2 — Single 5-hour weekly session (repeat every week)
**Checkpoint rule:** every session includes Setup Check → Mid Checkpoint (Must-pass core) → Pre-submit Check.

- **0:00–0:20** Warm-up: micro-quiz + “today’s acceptance criteria”
- **0:20–1:30** Core notebook (self-paced; short instructor interventions)
- **1:30–1:45** Break
- **1:45–3:15** Track studio sprint (feature implementation)
- **3:15–3:25** Break
- **3:25–4:35** Check + hardening: run tests, fix failures, export artifacts
- **4:35–5:00** Demo + reflection: 2–3 demos + reflection cell + next-step ticket

### 2.2 OOP/DSA — 3-hour weekly session (repeat every week)
- **0:00–0:15** Warm-up quiz / code reading
- **0:15–1:20** Core notebook (architecture/algorithm demo)
- **1:20–1:30** Break
- **1:30–2:40** Studio work (refactor/implement/benchmark)
- **2:40–3:00** Tests/benchmarks + engineering note

---

## 3) Two-Year Week-by-Week Calendar

### 3.1 Year 1 Semester 1 — CP1 (14 weeks, 5h weekly)
**Goal:** basic Python + problem solving + v1 working tool (end-to-end pipeline)

**Sprint plan (CP1): 6 sprints embedded in 14 weeks**
- S1 (W1–W2) Setup + variables + I/O + numeric basics  
- S2 (W3–W4) Conditionals + rule-based decisions  
- S3 (W5–W6) Loops + batch processing  
- S4 (W7–W8) Lists + strings + parsing  
- S5 (W9–W10) Functions + refactor into pipeline  
- S6 (W11–W14) Exceptions + file I/O + integration + v1 release  

**Week-by-week (CP1)**
- **W1:** Onboarding, Colab workflow, repo workflow, Track selection, “Hello Pipeline” stub  
  - Deliverable: repo runs + placeholder `self_check()` passes
- **W2:** Variables/types/formatting + numeric tasks + config cell  
  - Deliverable: `config` used by at least one function
- **W3:** Conditionals: thresholds, validation rules  
  - Deliverable: `clean_data()` implements basic rule(s)
- **W4:** Decision logic: rule-based classifier/state labeler  
  - Deliverable: `analyze()` returns labeled outputs
- **W5:** Loops: scanning datasets, min/max/mean/count  
  - Deliverable: summary stats correct on toy dataset
- **W6:** Loops: event counting (threshold crossings / simple peaks)  
  - Deliverable: event counts + edge-case handling
- **W7:** Lists: indexing, slicing, windowed operations (loop-based)  
  - Deliverable: moving-window metric via loop
- **W8:** Strings: parse lines into structured records  
  - Deliverable: parser handles multiple formats / errors
- **W9:** Functions: refactor parsing/cleaning/analysis into functions  
  - Deliverable: pipeline functions exist and are used
- **W10:** Functions: decomposition, reuse, reducing duplication  
  - Deliverable: clearer separation + basic docstrings
- **W11:** Exceptions: robust handling (skip bad rows, count skipped)  
  - Deliverable: `clean_data()` reports skipped counts
- **W12:** File I/O: read CSV, write cleaned CSV  
  - Deliverable: `export_results()` writes required files
- **W13:** Integration: pipeline end-to-end, add plot  
  - Deliverable: `plot()` creates at least 1 figure
- **W14:** **CP1 v1 release** + demo  
  - Deliverable: v1 passes universal check + exports + 2-min demo

---

### 3.2 Year 1 Semester 2 — CP2 (14 weeks, 5h weekly)
**Goal:** v1 → v2 (robust, modular, tested, reporting + plotting standards)

**Sprint plan (CP2): 6 sprints embedded in 14 weeks**
- S7 (W1–W2) Dict analytics + schema validation  
- S8 (W3–W4) Cleaning pipeline (configurable)  
- S9 (W5–W6) Plotting standards + reporting  
- S10 (W7–W8) Numpy acceleration + timing (optional but encouraged)  
- S11 (W9–W10) Testing harness (expanded checks)  
- S12 (W11–W14) Modular `/src` layout + v2 release  

**Week-by-week (CP2)**
- **W1:** Add schema validation (`validate_schema()`) + meaningful errors  
- **W2:** Dict analytics: histograms/counters/group summaries  
- **W3:** Cleaning pipeline: configurable steps via `config`  
- **W4:** Data quality report: missing/outlier stats & drop reasons  
- **W5:** Matplotlib standards: labeled plots, saved figures  
- **W6:** Report generation: JSON/MD interpretation text  
- **W7:** Numpy intro: vectorize one operation (optional)  
- **W8:** Timing: `timeit` comparison + short interpretation  
- **W9:** Testing: expand `self_check()` to detect failure modes  
- **W10:** Golden outputs: expected results for toy dataset  
- **W11:** Modularize into `/src` (notebooks import only)  
- **W12:** Package hygiene: config module, stable paths/outputs  
- **W13:** Integration on larger data; robust exports and plots  
- **W14:** **CP2 v2 release** + demo  
  - Deliverable: v2 passes universal check + report + plots

---

### 3.3 Year 2 Semester 3 — OOP (14 weeks, 3h/week)
**Goal:** v2 → v3 architecture (maintainable, extensible, tested)

**Week-by-week (OOP)**
- **W1:** OOP kickoff: classes, state, invariants; introduce component architecture
- **W2:** Composition refactor: `DataSource` + `Dataset` model
- **W3:** `Cleaner` component + strategy selection (basic)
- **W4:** `Analyzer` component + stable results schema
- **W5:** `Plotter` + `Reporter` components; unify exports
- **W6:** Domain exceptions + validation flow
- **W7:** SOLID refactor pass (SRP/OCP)
- **W8:** Strategy pattern: switch analyzers/filters via config
- **W9:** Factory/registry: instantiate components from config
- **W10:** Testing upgrade: introduce pytest suite + fixtures
- **W11:** Package hygiene: module boundaries, documentation
- **W12:** Plugin exercise: add a new analyzer without touching core
- **W13:** Architecture freeze: API stability checklist
- **W14:** **v3 architecture demo** + tests pass

---

### 3.4 Year 2 Semester 4 — DSA (14 weeks, 3h/week)
**Goal:** v3 performance module + benchmark proof + complexity reasoning

**Week-by-week (DSA)**
- **W1:** Big-O + Python cost model (list/dict/set)
- **W2:** Benchmark literacy: timeit + scaling plots
- **W3:** Searching: linear vs binary applied to project
- **W4:** Sorting choices; baseline vs improved plan
- **W5:** Hashing & indexing: build `Index` module for fast lookup
- **W6:** Heap/priority queue: top-k or scheduling (track-dependent)
- **W7:** Perf sprint 1: implement optimized feature + correctness tests
- **W8:** Perf sprint 2: benchmark baseline vs optimized + plots
- **W9:** Trees/BST (light) if needed; otherwise advanced indexing patterns
- **W10:** Graph BFS/DFS if needed
- **W11:** Dijkstra optional or alternative optimization pattern
- **W12:** DP/memoization pattern applied to track bottleneck
- **W13:** Final integration: optimized feature wired into product
- **W14:** **Final performance report** + demo

---

## 4) Project Catalog (Tracks + v1/v2/v3 scope + acceptance criteria)

### 4.1 Common deliverable contract (all tracks)
**Required exports (Year 1+)**
- `/data/cleaned/cleaned.csv` (or `cleaned.json`)
- `/reports/report.json`
- `/reports/figures/timeseries.png` (main plot)
- `/reports/figures/summary.png` (hist/box/scatter etc.)

**`report.json` minimum schema**
- `project_name`, `track`, `version`
- `dataset`: `n_raw`, `n_clean`, `n_dropped`
- `cleaning_summary`: counts per reason
- `analysis_summary`: at least 3 numeric metrics
- `figures`: list of filenames

**Year 2 additions**
- `pytest` tests under `/tests`
- `/src/<project>/core/` (OOP components)
- `/src/<project>/dsa/` (optimized module)
- benchmark notebook + `benchmark_results.json` + benchmark plot

---

### 4.2 Track 1 — Robotics/Mechatronics
**Flagship Product:** **MechaSense Studio**  
**Story:** Analyze sensor streams (IMU/temp/RPM) and detect events/faults.

**v1 (CP1 end)**
- load CSV → clean invalid → basic stats + threshold events → plot timeseries → export

**v2 (CP2 end)**
- schema validation; configurable cleaning rules; per-sensor dict summaries; expanded tests; `/src` modularization

**v3 (Year 2 end)**
- OOP components (`CSVDataSource`, `RuleCleaner`, `EventAnalyzer`, `Plotter`, `Reporter`)
- DSA optimization: fast event/time-range queries via indexing + benchmark

**Dataset plan**
- Synthetic generator (sin + noise + injected spikes)
- Optional real: smartphone sensor logs

**DSA candidates**
- Sorted event index + binary search range queries
- Heap for top-k anomalies

---

### 4.3 Track 2 — Data/AI (beginner-friendly)
**Flagship Product:** **CleanReport Pipeline**  
**Story:** Clean messy CSVs, validate schemas, generate automated reports.

**v1**
- load → clean types/missing → summary stats → distribution plots → export report

**v2**
- schema validator + reasoned dropping; dict group summaries; standard dashboard; golden-output tests; modular `/src`

**v3**
- pluggable cleaners/analyzers (Strategy); caching for aggregates; benchmark baseline scans vs cached results

**Dataset plan**
- Instructor-provided “dirty” datasets + student-chosen (schema-approved)

**DSA candidates**
- Hash-based aggregation + caching
- Heap top-k categories

---

### 4.4 Track 3 — Simulation/Games
**Flagship Product:** **SimLab Engine**  
**Story:** A discrete simulation engine with logging, scoring, and reporting.

**v1**
- timestep loop simulation; validate params; compute scores; plot trajectories; export

**v2**
- batch scenarios; config-driven runs; deterministic tests with seed; polished reporting

**v3**
- OOP: `Simulator`, `Scenario`, `Logger`, `Reporter`
- DSA: optimize collision/search/state lookup; benchmark naive vs optimized

**DSA candidates**
- Spatial hashing / grid indexing
- Optional BFS/DFS variants for navigation

---

### 4.5 Track 4 — Space/Astro
**Flagship Product:** **Lightcurve Explorer**  
**Story:** Explore toy TESS-like time series; detect dips/events; report.

**v1**
- load (time,flux) → clean NaNs/outliers → threshold dip detection → plot dips → export

**v2**
- configurable detrending; segment summaries (toy “sector” column); golden tests; improved plots

**v3**
- OOP pipeline with pluggable detrenders
- DSA: accelerate dip search/window computations + benchmark

**DSA candidates**
- prefix sums / windowed statistics
- event indexing + binary search

---

### 4.6 Track 5 — IoT/Reporting
**Flagship Product:** **AutoDashboard Reporter**  
**Story:** Given any time-series CSV, generate a standard dashboard + exports.

**v1**
- load → clean → analyze → standard plots → export

**v2**
- schema mapping (column aliases); dashboard profiles; tests; report.md + report.json

**v3**
- plugin dashboards; optimize batch processing (caching/indexing); benchmark scalability

**DSA candidates**
- caching repeated computations
- efficient batch processing queues (optional)

---

### 4.7 Alternate project options

Alternate project variants are maintained outside this operating document to keep CourseOS lean.

See: **PROJECT_BANK.md** (optional project variants compatible with the same repo contract and evidence requirements).


### 4.8 Universal acceptance criteria (track-agnostic)
A submission is “pass” if:
- all required functions exist and run top-to-bottom
- `self_check()` passes
- required exports exist at required paths
- report.json meets minimum schema keys
- at least 2 plots saved and readable
- reflection cell completed (3–5 bullets)
- (Year 2) pytest passes + benchmark artifacts present + complexity note present

---

## 5) Universal Check Specification (Contract + Tests + Quality Gates)

### 5.1 Year 1: Functional pipeline checks (assert-based)
**Checker validates:**
- **Existence:** required functions exist and are callable
- **Type/shape:** correct return types, non-empty where expected
- **Correctness:** numeric checks within tolerances on toy dataset
- **Edge cases:** at least 3 (empty row, non-numeric, out-of-range)
- **Exports:** required files exist at required paths
- **Non-interactive:** no `input()` required in grading mode

**Tolerance guidelines**
- Deterministic toy stats: `abs(a-b) <= 1e-6`
- Noisy/sim: relative tolerance (e.g., ≤ 1e-2)

**Runtime guidelines**
- `self_check()` should complete < 30 seconds on toy data
- Avoid large dataset loops inside checks

---

### 5.2 Required exports (paths and filenames)
After `export_results(...)`, these must exist:

**Year 1 minimum**
- `data/cleaned/cleaned.csv` (or `.json`)
- `reports/report.json`
- `reports/figures/timeseries.png`
- `reports/figures/summary.png`

**Year 2 additions**
- `reports/benchmark/benchmark_results.json`
- `reports/benchmark/benchmark_plot.png`
- pytest tests pass

---

### 5.3 `report.json` schema validator (minimum)
Required keys:
- `project_name` (str)
- `track` (str)
- `version` (str: "v1"/"v2"/"v3")
- `dataset` (dict): `n_raw`, `n_clean`, `n_dropped`
- `cleaning_summary` (dict): counts per reason
- `analysis_summary` (dict): ≥3 numeric metrics
- `figures` (list of filenames)

---

### 5.4 Universal Check Notebook structure (what you publish weekly)
1) Setup (imports, paths, config)  
2) Contract validation (symbol existence)  
3) Toy dataset (load or deterministic generator)  
4) Pipeline run (load→clean→analyze→plot→export)  
5) Assertions (correctness + edge cases)  
6) Export verification (existence + minimal content checks)  
7) Reflection prompt (graded)

---

### 5.5 Quality gates (lightweight but powerful)
Fail if:
- functions missing
- requires interactive input
- exports missing or wrong location
- report.json missing minimum keys
- plots missing/empty/unlabeled
- (CP2 onward) logic lives in notebooks instead of `/src`

---

### 5.6 Year 2: pytest + benchmark requirements
**Pytest minimum suite (OOP semester)**
- DataSource returns Dataset with expected fields
- Cleaner reduces invalid rows and reports dropped counts
- Analyzer returns required keys
- Reporter writes outputs and returns paths

**Benchmark requirements (DSA semester)**
- baseline + optimized timings
- n scales: at least 3 (e.g., 1e3, 1e4, 1e5)
- runtime plot baseline vs optimized
- short complexity note: baseline Big-O vs optimized Big-O

Acceptance:
- optimized version shows measurable improvement at largest n (e.g., ≥1.5× faster)

---

## 6) Recommended Repository Template (Backbone for 2 years)
All groups keep the same repo from CP1 Week 1 through Year 2.

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
    core/        # Year 2 OOP components
    dsa/         # Year 2 DSA optimized modules
/tests
  test_io.py
  test_cleaning.py
  test_analysis.py
/data
  raw/
  cleaned/
/reports
  figures/
  benchmark/
README.md
```

**Rule:** notebooks import from `/src`. Notebooks are execution + reporting shells.

---

## 6.1 Repository Recovery Protocol

Because the program keeps one repository for multiple semesters, repo failure must have a clear and practical recovery rule.

**Recovery rule:**
- every week starts from the latest known working state
- recommended: keep a known-working checkpoint (commit) regularly; tagging is encouraged at sprint/release boundaries
- if the repo structure is broken (imports, paths, deleted files, invalid layout), restore from the latest working checkpoint before continuing
- the instructor may provide a clean recovery template for that week
- repeated repo breakage triggers a **targeted structure check** and a **reduced-scope recovery requirement** until the repo is stable again

## 7) Minimal end-of-program output (what every group graduates with)
By the end of DSA, each group must have:
- a stable `/src` codebase (components + dsa module)
- passing pytest tests
- benchmark notebook + benchmark artifacts + plot
- report generator producing JSON/MD + figures
- README that explains “run in Colab” and “run locally”

---

## 8) Instructor operations (to manage tutoring load)
- Use a help-queue protocol (track, sprint, cell number, error message, what tried)
- Run 5-minute mini-clinics when many groups share the same issue
- Weekly 10-minute code-reading quiz + occasional 2-minute “explain your code” checks (anti copy-paste)

---


## 8.1 Individual vs Group Assessment Rule

Studio implementation may be collaborative, but assessment is not fully group-based.

- Quizzes and oral checks are individual
- Reflection and recovery tickets are individual
- Demo participation may be group-based, but each student may be questioned individually
- A student who cannot explain their own submitted code may receive an individual deduction even if the shared artifact passes

This prevents weak students from disappearing inside strong groups.

## 9) Support Architecture for Struggling Students (Built-in Rescue Layer)
This program is intentionally **studio-based** and **self-paced**, which is powerful—but only if we prevent “silent failure”.
To make the system resilient for weaker students **without diluting standards**, every week has **two parallel lanes**:

- **Main lane:** standard studio workflow + full scope deliverables  
- **Rescue lane:** reduced scope + heavier scaffolding + mandatory checkpoints  

### 9.1 Three-level weekly goals (everyone sees this up front)
Every weekly package explicitly separates tasks into:

1) **Must-pass core (survival path)**  
   The smallest working version that *every* student must finish during class (with help).  
2) **Standard target (normal weekly goal)**  
   What most students should complete in the session.  
3) **Stretch extension (for strong students)**  
   Optional improvements (extra plots, extra features, optimizations, nicer reporting).

**Grading policy:** failing the standard target does not automatically fail the week if the **must-pass core** is completed and the student files a short “recovery ticket”.

### 9.2 Rescue notebooks (only when needed)
For each week, provide a “Rescue” variant (or a Rescue section inside the studio notebook):
- slower explanation + more intermediate prints/expected outputs  
- partial scaffolding (more stubs filled)  
- smaller toy dataset  
- guided debugging prompts (“if you see error X, check Y”)  

Rescue materials are not a different curriculum—they are a controlled on-ramp back to the main lane.

### 9.3 Mandatory early-warning checkpoints (diagnostic, not optional)
Do not wait until final exports fail. Each 5-hour CP session includes:
- **Setup check (first 15 minutes):** imports, paths, repo load  
- **Mid-session checkpoint (around 2:30):** must-pass core milestone  
- **Pre-submit checkpoint (before 4:35):** self-check + export existence  

If a student/group misses a checkpoint, they must switch to the Rescue lane *immediately*.

### 9.4 “Red list” intervention rule
Maintain a weekly list of students/groups who meet any of these:
- failed the same check **twice**  
- did not complete the must-pass core  
- cannot explain their own code (2-minute oral check)  
- keep patching notebooks without fixing `/src`  

**Rule:** red-list students automatically receive:
- next week’s Rescue lane tasks first, and  
- a mandatory instructor checkpoint before submission.

### 9.5 OOP and DSA concept reinforcement (micro-teaching inserts)
### 9.5.1 Minimum weekly must-pass examples for OOP and DSA

To make Rescue-lane expectations concrete:

**OOP must-pass core examples**
- implement one component with a clear responsibility
- write or pass at least one pytest for that component
- explain one design choice orally in 1–2 minutes

**DSA must-pass core examples**
- benchmark one baseline implementation correctly
- identify the current bottleneck
- state the baseline Big-O in words and symbols
- produce one benchmark artifact or timing note

OOP and DSA are the most vulnerable to “checklist completion without understanding”.
To prevent that (without reintroducing long lectures), add:

- **1-page concept sheet** each week (definitions + 1 tiny example)  
- **tiny pre-project exercise** (5–10 minutes) before integrating into the main codebase  
- **oral responsibility check** in OOP: “Why this class boundary? What invariant does it protect?”  
- **complexity sanity check** in DSA: “What is the baseline Big-O and why?”

### 9.6 Recovery mechanism (planned catch-up)
Because the work is cumulative, include a formal recovery pathway:
- **Catch-up notebook** every 3–4 weeks, OR  
- **Reduced-scope resubmission lane** tied to the same contract  

This prevents one bad week in CP1/CP2 from poisoning the rest of the semester.

### 9.7 Anti-silent-failure policy (end-of-class rule)
No student should leave class without one of:
- the **must-pass core** completed, OR  
- an instructor-approved **recovery ticket** (what failed, what they will do next, what support they need).

### 9.8 Recovery ticket limits and grade consequences

Recovery tickets are a support tool, not a parallel grading path.

Default rule:
- up to **3 recovery tickets per semester** may preserve full weekly credit if completed properly
- after that, a week completed only through recovery is capped at the **core/pass** level unless the instructor approves an exception
- repeated failure to complete recovery tasks may convert the week to non-passing

This keeps support humane without removing standards.

## 10) Program success criteria (what “good” looks like)
- CP1: most groups finish v1 in-class with passing checks
- CP2: v2 is modular, robust, and produces consistent reports
- OOP: adding a new analyzer/cleaner is easy and doesn’t break tests
- DSA: one feature is measurably faster with a benchmark and a complexity note

