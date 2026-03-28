# Demo Evaluation Guide

## Format

- **Duration:** 2–3 minutes per team
- **When:** Week 14 of each course
- **Who evaluates:** Instructor (+ optional peer feedback)
- **What they show:** Live run of their pipeline in Colab + repo walkthrough

---

## v1 Demo (CP1 Week 14) — 20 points

### Setup
- Student opens their repo in Colab
- Runs the pipeline top to bottom: load → clean → analyze → plot → export
- Shows the outputs

### Evaluation

| # | Criteria | Points | What to look for |
|---|----------|--------|-----------------|
| 1 | Pipeline runs end-to-end | 5 | No crashes, no manual intervention, no `input()` |
| 2 | Correct outputs | 4 | Stats on toy data match expected (see answer keys) |
| 3 | Required exports exist | 3 | cleaned.csv, report.json, timeseries.png, summary.png |
| 4 | Code quality | 3 | Functions used, logic in `/src`, not copy-pasted in notebook |
| 5 | Can explain their code | 3 | Ask "what does clean_data do?" — student answers correctly |
| 6 | Demo clarity | 2 | Clear presentation, knows what their tool does |

### Quick questions to ask
- "What happens if I give you a CSV with a missing column?"
- "How many rows did you drop and why?"
- "Show me where analyze() is defined."

---

## v2 Demo (CP2 Week 14) — 20 points

| # | Criteria | Points | What to look for |
|---|----------|--------|-----------------|
| 1 | Schema validation | 3 | Catches bad input with clear error message |
| 2 | Configurable cleaning | 3 | Change a config value → behavior changes |
| 3 | Professional plots | 3 | Labels, titles, legends, grid, saved at correct path |
| 4 | Report generation | 3 | JSON with required keys + readable Markdown |
| 5 | Code in `/src` | 3 | Notebook only imports — show the import statements |
| 6 | Testing | 3 | Run self_check(), show golden output test |
| 7 | Can explain | 2 | "How does your cleaning pipeline work?" |

### Quick questions to ask
- "Change the threshold in config and re-run. What changes?"
- "Show me report.json. What does cleaning_summary tell us?"
- "If I add a new column to the CSV, does your validator catch it?"

---

## v3 Architecture Demo (OOP Week 14) — 25 points

| # | Criteria | Points | What to look for |
|---|----------|--------|-----------------|
| 1 | 5 components | 5 | DataSource, Cleaner, Analyzer, Plotter, Reporter — all in `/src/core/` |
| 2 | Design patterns | 4 | Strategy or Factory correctly applied — not just renamed functions |
| 3 | Custom exceptions | 3 | Throw a bad input at it → get a domain-specific error, not a Python crash |
| 4 | pytest passes | 4 | Run `pytest tests/ -v` — at least 5 tests, all green |
| 5 | Plugin works | 3 | Add a new analyzer class → pipeline uses it without changing core |
| 6 | Module boundaries | 3 | Clean `__init__.py`, no circular imports, no logic in notebooks |
| 7 | Can explain architecture | 3 | "Why is Cleaner a separate class? What invariant does it protect?" |

### Quick questions to ask
- "If I wanted to add a MedianAnalyzer, what files do I touch?"
- "Show me the factory. How does it decide which analyzer to create?"
- "What happens if DataSource gets a file that doesn't exist?"

---

## v3 Performance Demo (DSA Week 14) — 25 points

| # | Criteria | Points | What to look for |
|---|----------|--------|-----------------|
| 1 | Optimized module exists | 4 | In `/src/project_name/dsa/`, not just a notebook experiment |
| 2 | Correctness preserved | 4 | Optimized gives same results as baseline (run both, compare) |
| 3 | Benchmark at 3+ sizes | 4 | e.g. n=1K, 10K, 100K — timing for both baseline and optimized |
| 4 | Speedup ≥ 1.5× | 4 | At largest n. Must be real improvement, not noise |
| 5 | Benchmark plot | 3 | Two lines (baseline vs optimized), labeled, readable |
| 6 | Big-O justification | 3 | States both complexities correctly with reasoning |
| 7 | Integrated into product | 3 | Wired into the pipeline, not a standalone script |

### Quick questions to ask
- "What is the Big-O of your baseline? Why?"
- "Show me the benchmark plot. At what n does the speedup become clear?"
- "If n doubles, how much longer does each version take?"
- "Why did you choose this data structure for the optimization?"

---

## Peer feedback (optional)

If using peer feedback during demos, give students this template:

```
Team: _______________
Track: _______________

1. Does it work? (yes / mostly / no)
2. One thing that impressed me:
3. One suggestion for improvement:
```

Peer feedback is ungraded — it's for the presenting team's benefit only.

---

## Common demo fails (and how to handle)

| Problem | Action |
|---------|--------|
| "It worked on my machine" / crashes in Colab | Student gets 5 min to fix, then re-demo. If still broken, grade on repo code + oral. |
| Student can't explain the code | Ask simpler questions. If still can't explain, individual deduction applies. |
| Exports missing | Check if they're generated but at wrong path. Partial credit if code is correct. |
| Team member absent | Present member demos. Absent member must do individual oral check next week. |
| Plagiarism suspected | Note it. Follow up with individual oral check + git blame analysis. |
