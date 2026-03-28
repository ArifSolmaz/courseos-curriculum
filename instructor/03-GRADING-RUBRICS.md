# Grading Rubrics

## Overall weights

### CP1 / CP2
| Component | Weight | How assessed |
|-----------|--------|--------------|
| Weekly submissions + universal checks | 50% | Auto-check pass/fail + export verification |
| Quizzes / code-reading / oral checks | 20% | Weekly micro-quiz + random oral "explain your code" |
| Release demo (v1 or v2) | 20% | Week 14 demo + repo review |
| Professional habits | 10% | Reflections, checkpoint compliance, recovery completion |

### OOP / DSA
| Component | Weight | How assessed |
|-----------|--------|--------------|
| Weekly submissions + tests/benchmarks | 45% | pytest pass + benchmark artifacts |
| Quizzes / code-reading / oral checks | 20% | Code-reading quiz + oral design justification |
| Final release (v3-arch or v3-perf) | 25% | Demo + repo review + architecture/benchmark proof |
| Professional habits | 10% | Engineering notes, checkpoint compliance, recovery |

---

## Weekly submission rubric (per week)

| Level | Points | Criteria |
|-------|--------|----------|
| **Stretch** | 100 | Standard target + stretch extension completed. Clean code, well-documented. |
| **Standard** | 85 | Standard target fully met. Universal check passes. All exports present. Reflection complete. |
| **Core** | 70 | Must-pass core completed. Universal check passes on core items. Reflection complete. |
| **Core + Recovery** | 60 | Must-pass core NOT completed but recovery ticket filed with clear plan. Ticket resolved by next week. |
| **Incomplete** | 0–40 | Must-pass core not done. No recovery ticket. Or recovery ticket not resolved. |

---

## Release demo rubric

### v1 Demo (CP1 Week 14) — /20

| Criteria | Points | Description |
|----------|--------|-------------|
| Pipeline runs end-to-end | 5 | load → clean → analyze → plot → export without crashing |
| Correct outputs | 4 | Stats match expected values on toy data |
| Exports exist | 3 | cleaned.csv, report.json, timeseries.png, summary.png |
| Code quality | 3 | Functions are used, logic is in `/src` not notebooks |
| Can explain their code | 3 | Student answers 2–3 "why did you do X?" questions |
| Reflection / demo clarity | 2 | Clear 2-min demo, knows what their tool does |

### v2 Demo (CP2 Week 14) — /20

| Criteria | Points | Description |
|----------|--------|-------------|
| Schema validation works | 3 | Catches bad data with clear error messages |
| Cleaning is configurable | 3 | Rules change via config without code edits |
| Professional plots | 3 | Labeled axes, titles, legends, saved correctly |
| Report generation | 3 | JSON + readable report with interpretation |
| Code in `/src` | 3 | Notebooks only import — no logic in notebooks |
| Testing | 3 | self_check passes, golden output test passes |
| Can explain | 2 | Answers "how does your cleaning pipeline work?" |

### v3 Architecture Demo (OOP Week 14) — /25

| Criteria | Points | Description |
|----------|--------|-------------|
| 5 components implemented | 5 | DataSource, Cleaner, Analyzer, Plotter, Reporter |
| Design patterns used | 4 | Strategy or Factory pattern correctly applied |
| Custom exceptions | 3 | Domain-specific errors with useful messages |
| pytest suite passes | 4 | At least 5 meaningful tests |
| Plugin works | 3 | Can add new analyzer without modifying core |
| Module boundaries clean | 3 | `__init__.py` exports, no circular imports |
| Can explain architecture | 3 | "Why this class boundary? What invariant?" |

### v3 Performance Demo (DSA Week 14) — /25

| Criteria | Points | Description |
|----------|--------|-------------|
| Optimized module exists | 4 | In `/src/project_name/dsa/` |
| Correctness preserved | 4 | Optimized gives same results as baseline |
| Benchmark at 3+ sizes | 4 | e.g. n=1K, 10K, 100K |
| Speedup ≥ 1.5× at largest n | 4 | Measurable, not noise |
| Benchmark plot exists | 3 | baseline vs optimized, labeled |
| Big-O justification | 3 | Correct baseline and optimized complexity |
| Integrated into product | 3 | Wired into the pipeline, not standalone |

---

## Micro-quiz rubric (per quiz)

| Score | Criteria |
|-------|----------|
| 5/5 | All questions correct, shows understanding |
| 4/5 | One minor mistake |
| 3/5 | Understands concepts but struggles with details |
| 2/5 | Significant gaps |
| 0–1/5 | Didn't attempt or fundamental misunderstanding |

Quizzes are **individual** even if the project is team-based.

---

## Oral check rubric (per check)

| Score | Criteria |
|-------|----------|
| Pass | Can explain what their code does, why it's structured this way, and what would happen if input changes |
| Partial | Can describe what the code does but can't explain why or handle edge cases |
| Fail | Cannot explain the submitted code — treated as potential integrity issue |

**Rule:** A student who fails an oral check on code they submitted may receive an individual deduction even if the group submission passes.

---

## Recovery ticket grading

| Status | Impact |
|--------|--------|
| Filed on time + resolved by next week | Full credit at core level (70%) |
| Filed on time + resolved late (within 2 weeks) | 60% for that week |
| Not filed | Week counts as incomplete (0–40%) |
| 4th+ recovery ticket in a semester | Capped at core level (60%) |

---

## Professional habits (10%)

| Criteria | Points |
|----------|--------|
| Reflections completed every week | 3 |
| Checkpoint compliance (showed up for mid-session check) | 3 |
| Recovery tickets resolved when needed | 2 |
| Commit history is regular (not just Week 14 dump) | 2 |
