"""
Analysis module — compute summary statistics and detect events.
"""


def analyze(clean_data, config):
    """Analyze cleaned data and return a results dictionary.

    Args:
        clean_data (list[dict]): Cleaned data rows.
        config (dict): Analysis configuration.

    Returns:
        dict: Results with at least 3 numeric metrics in 'analysis_summary',
              plus dataset counts and cleaning summary.
    """
    results = {
        "project_name": config.get("project_name", "unknown"),
        "track": config.get("track", "unknown"),
        "version": config.get("version", "v1"),
        "dataset": {
            "n_clean": len(clean_data),
        },
        "analysis_summary": {},
    }

    if not clean_data:
        results["analysis_summary"] = {
            "mean": 0,
            "median": 0,
            "std": 0,
        }
        return results

    # Try to find numeric columns automatically
    numeric_cols = config.get("numeric_columns", [])
    if not numeric_cols:
        # Auto-detect: try the first row's values
        for key, val in clean_data[0].items():
            try:
                float(val)
                numeric_cols.append(key)
            except (ValueError, TypeError):
                pass

    # Compute stats for first numeric column found
    if numeric_cols:
        col = numeric_cols[0]
        values = []
        for row in clean_data:
            try:
                values.append(float(row[col]))
            except (ValueError, TypeError, KeyError):
                pass

        if values:
            values_sorted = sorted(values)
            n = len(values)
            mean_val = sum(values) / n
            mid = n // 2
            median_val = values_sorted[mid] if n % 2 == 1 else (values_sorted[mid - 1] + values_sorted[mid]) / 2
            variance = sum((x - mean_val) ** 2 for x in values) / n
            std_val = variance ** 0.5

            results["analysis_summary"] = {
                "column": col,
                "count": n,
                "mean": round(mean_val, 4),
                "median": round(median_val, 4),
                "std": round(std_val, 4),
                "min": round(min(values), 4),
                "max": round(max(values), 4),
            }

            # Event detection (if threshold configured)
            threshold = config.get("threshold")
            if threshold is not None:
                events = [v for v in values if v > threshold]
                results["analysis_summary"]["events_above_threshold"] = len(events)
                results["analysis_summary"]["threshold"] = threshold

    print(f"Analysis complete: {len(results['analysis_summary'])} metrics computed")
    return results
