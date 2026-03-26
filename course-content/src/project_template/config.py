"""
Configuration module — all settings in one place.
Students: edit this file to change how your pipeline behaves.
"""


def get_config():
    """Return the default project configuration dictionary.

    Returns:
        dict: Configuration with keys for paths, cleaning rules,
              analysis parameters, and plotting settings.
    """
    config = {
        # --- Project info ---
        "project_name": "my_project",
        "track": "data",           # change to your track
        "version": "v1",

        # --- File paths ---
        "raw_data_path": "data/raw/sample.csv",
        "cleaned_data_path": "data/cleaned/cleaned.csv",
        "report_path": "reports/report.json",
        "figures_dir": "reports/figures",
        "benchmark_dir": "reports/benchmark",

        # --- Cleaning rules ---
        "drop_missing": True,
        "drop_duplicates": True,
        "numeric_columns": [],        # list column names that must be numeric
        "value_ranges": {},            # e.g. {"temperature": (0, 150)}
        "custom_rules": [],            # list of rule names to apply

        # --- Analysis parameters ---
        "analysis_metrics": ["mean", "median", "std"],
        "threshold": None,             # for event detection
        "window_size": 5,              # for moving-window calculations

        # --- Plotting ---
        "figure_format": "png",
        "figure_dpi": 100,
        "plot_style": "default",
    }
    return config
