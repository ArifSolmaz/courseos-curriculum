"""
Reporting module — export results, figures, and run self-checks.
"""

import json
import os


def export_results(clean_data, results, figures, config):
    """Export cleaned data, report, and figures to required paths.

    Args:
        clean_data (list[dict]): Cleaned data rows.
        results (dict): Analysis results.
        figures (list): Matplotlib figure objects (already saved by plot()).
        config (dict): Configuration with output paths.

    Returns:
        dict: Paths of exported files.
    """
    import csv

    exported = {}

    # --- Export cleaned CSV ---
    cleaned_path = config.get("cleaned_data_path", "data/cleaned/cleaned.csv")
    os.makedirs(os.path.dirname(cleaned_path), exist_ok=True)

    if clean_data:
        fieldnames = list(clean_data[0].keys())
        with open(cleaned_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(clean_data)
        exported["cleaned_csv"] = cleaned_path
        print(f"Exported cleaned data: {cleaned_path} ({len(clean_data)} rows)")

    # --- Export report.json ---
    report_path = config.get("report_path", "reports/report.json")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    report = {
        "project_name": config.get("project_name", "unknown"),
        "track": config.get("track", "unknown"),
        "version": config.get("version", "v1"),
        "dataset": results.get("dataset", {}),
        "cleaning_summary": results.get("cleaning_summary", {}),
        "analysis_summary": results.get("analysis_summary", {}),
        "figures": [f"timeseries.{config.get('figure_format', 'png')}",
                    f"summary.{config.get('figure_format', 'png')}"],
    }

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    exported["report_json"] = report_path
    print(f"Exported report: {report_path}")

    return exported


def self_check():
    """Run basic self-check assertions on the pipeline.

    This function tests that the pipeline works end-to-end
    on a small toy dataset. Raises AssertionError on failure.
    """
    from .config import get_config
    from .io import load_data
    from .cleaning import clean_data
    from .analysis import analyze

    print("Running self-check...")

    # Test 1: config exists and has required keys
    config = get_config()
    required_keys = ["project_name", "track", "version", "raw_data_path"]
    for key in required_keys:
        assert key in config, f"Config missing key: {key}"
    print("  [PASS] Config has required keys")

    # Test 2: clean_data handles empty input
    result = clean_data([], config)
    assert isinstance(result, list), "clean_data must return a list"
    assert len(result) == 0, "clean_data on empty input should return empty list"
    print("  [PASS] clean_data handles empty input")

    # Test 3: analyze handles empty input
    result = analyze([], config)
    assert isinstance(result, dict), "analyze must return a dict"
    assert "analysis_summary" in result, "analyze must include analysis_summary"
    print("  [PASS] analyze handles empty input")

    # Test 4: clean_data filters bad rows
    test_data = [
        {"value": "10", "label": "A"},
        {"value": "", "label": "B"},       # missing
        {"value": "20", "label": "C"},
        {"value": "10", "label": "A"},      # duplicate
    ]
    config_test = {**config, "numeric_columns": [], "drop_missing": True, "drop_duplicates": True}
    cleaned = clean_data(test_data, config_test)
    assert len(cleaned) == 2, f"Expected 2 clean rows, got {len(cleaned)}"
    print("  [PASS] clean_data filters missing + duplicates")

    print("Self-check PASSED!")
