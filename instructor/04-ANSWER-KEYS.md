# Universal Check Answer Keys

These are the expected outputs when running the universal check on the **standard toy dataset**. Use these to verify student implementations.

---

## Toy Dataset (used across all tracks)

```python
toy_data = [
    {"id": 1, "value": "25.0"},
    {"id": 2, "value": ""},        # missing → drop
    {"id": 3, "value": "abc"},     # non-numeric → drop
    {"id": 4, "value": "50.5"},
    {"id": 5, "value": "-10"},     # out of range → drop
    {"id": 6, "value": "75.0"},
    {"id": 7, "value": "200"},     # out of range → drop
    {"id": 8, "value": "42.0"},
]

config = {"min_value": 0, "max_value": 100}
```

### Expected results

| Metric | Expected Value |
|--------|---------------|
| n_raw | 8 |
| n_clean | 4 |
| n_dropped | 4 |
| Drop: missing | 1 |
| Drop: non_numeric | 1 |
| Drop: out_of_range | 2 |
| Clean values | [25.0, 50.5, 75.0, 42.0] |
| Mean | 48.125 |
| Median | 46.25 |
| Std | ~17.81 (tolerance ±0.1) |
| Min | 25.0 |
| Max | 75.0 |

### Expected exports

| File | Must exist | Min size |
|------|-----------|----------|
| data/cleaned/cleaned.csv | Yes | > 50 bytes |
| reports/report.json | Yes | > 100 bytes |
| reports/figures/timeseries.png | Yes (from W13+) | > 1 KB |
| reports/figures/summary.png | Yes (from W13+) | > 1 KB |

### report.json required keys

```json
{
    "project_name": "string",
    "track": "string",
    "version": "v1 or v2 or v3",
    "dataset": {
        "n_raw": 8,
        "n_clean": 4,
        "n_dropped": 4
    },
    "cleaning_summary": {},
    "analysis_summary": {
        "mean": 48.125,
        "median": 46.25,
        "std": 17.81
    },
    "figures": ["timeseries.png", "summary.png"]
}
```

---

## Tolerance guidelines

| Type | Tolerance |
|------|-----------|
| Deterministic stats (mean, sum) | `abs(actual - expected) ≤ 1e-6` |
| Floating-point derived (std, variance) | `abs(actual - expected) ≤ 0.1` |
| Counts (n_raw, n_clean, events) | Exact match |
| Noisy/simulation data | Relative tolerance ≤ 1e-2 |

---

## Year 2 additions

### OOP (pytest expected)

```
tests/test_cleaning.py    → Cleaner drops invalid rows
tests/test_analysis.py    → Analyzer returns required keys
tests/test_io.py          → DataSource loads and returns Dataset
```

Minimum: 5 tests, all passing.

### DSA (benchmark expected)

| File | Must exist |
|------|-----------|
| reports/benchmark/benchmark_results.json | Yes |
| reports/benchmark/benchmark_plot.png | Yes |

benchmark_results.json must contain:
- `sizes`: list of 3+ n values
- `baseline_ms`: timing per size
- `optimized_ms`: timing per size
- `speedup`: list, max value ≥ 1.5

---

## Quick validation script

Run this in the student's repo root to check everything:

```python
import os, json

def validate_repo():
    errors = []

    # Check files
    required = [
        "data/cleaned/cleaned.csv",
        "reports/report.json",
    ]
    for f in required:
        if not os.path.exists(f) or os.path.getsize(f) == 0:
            errors.append(f"MISSING: {f}")

    # Check report.json
    try:
        with open("reports/report.json") as f:
            report = json.load(f)
        for key in ["project_name", "track", "version", "dataset", "analysis_summary"]:
            if key not in report:
                errors.append(f"report.json missing key: {key}")
        ds = report.get("dataset", {})
        if ds.get("n_clean", 0) == 0:
            errors.append("report.json: n_clean is 0")
        summary = report.get("analysis_summary", {})
        if len([v for v in summary.values() if isinstance(v, (int, float))]) < 3:
            errors.append("report.json: fewer than 3 numeric metrics")
    except Exception as e:
        errors.append(f"report.json error: {e}")

    # Check plots (CP2+)
    for fig in ["reports/figures/timeseries.png", "reports/figures/summary.png"]:
        if os.path.exists(fig) and os.path.getsize(fig) > 1000:
            pass  # ok
        # Don't fail CP1 students before W13

    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(f"  ✗ {e}")
    else:
        print("VALIDATION PASSED ✓")

    return len(errors) == 0

validate_repo()
```
