"""
Plotting module — create and save figures.
"""

import os


def plot(clean_data, results, config):
    """Create required figures and return list of figure objects.

    Creates:
        - timeseries.png: line plot of the main numeric column
        - summary.png: histogram of the main numeric column

    Args:
        clean_data (list[dict]): Cleaned data rows.
        results (dict): Analysis results.
        config (dict): Plotting configuration.

    Returns:
        list: List of matplotlib figure objects.
    """
    # Import matplotlib here so the module can be imported without it
    try:
        import matplotlib
        matplotlib.use("Agg")  # non-interactive backend for Colab/server
        import matplotlib.pyplot as plt
    except ImportError:
        print("WARNING: matplotlib not installed. Skipping plots.")
        return []

    figures = []
    figures_dir = config.get("figures_dir", "reports/figures")
    os.makedirs(figures_dir, exist_ok=True)
    fmt = config.get("figure_format", "png")
    dpi = config.get("figure_dpi", 100)

    # Find numeric values
    numeric_cols = config.get("numeric_columns", [])
    if not numeric_cols:
        for key, val in clean_data[0].items() if clean_data else []:
            try:
                float(val)
                numeric_cols.append(key)
            except (ValueError, TypeError):
                pass

    if not numeric_cols or not clean_data:
        print("No numeric data to plot.")
        return figures

    col = numeric_cols[0]
    values = []
    for row in clean_data:
        try:
            values.append(float(row[col]))
        except (ValueError, TypeError, KeyError):
            pass

    if not values:
        print("No valid values to plot.")
        return figures

    # --- Figure 1: Time Series ---
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    ax1.plot(range(len(values)), values, linewidth=0.8, color="steelblue")
    ax1.set_title(f"Time Series — {col}", fontsize=14)
    ax1.set_xlabel("Index")
    ax1.set_ylabel(col)
    ax1.grid(True, alpha=0.3)

    # Add threshold line if configured
    threshold = config.get("threshold")
    if threshold is not None:
        ax1.axhline(y=threshold, color="red", linestyle="--", label=f"Threshold={threshold}")
        ax1.legend()

    path1 = os.path.join(figures_dir, f"timeseries.{fmt}")
    fig1.savefig(path1, dpi=dpi, bbox_inches="tight")
    plt.close(fig1)
    figures.append(fig1)
    print(f"Saved: {path1}")

    # --- Figure 2: Summary (Histogram) ---
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.hist(values, bins=min(30, max(5, len(values) // 10)), color="steelblue", edgecolor="white")
    ax2.set_title(f"Distribution — {col}", fontsize=14)
    ax2.set_xlabel(col)
    ax2.set_ylabel("Count")
    ax2.grid(True, alpha=0.3)

    # Add mean/median lines
    summary = results.get("analysis_summary", {})
    if "mean" in summary:
        ax2.axvline(x=summary["mean"], color="red", linestyle="-", label=f"Mean={summary['mean']}")
    if "median" in summary:
        ax2.axvline(x=summary["median"], color="orange", linestyle="--", label=f"Median={summary['median']}")
    ax2.legend()

    path2 = os.path.join(figures_dir, f"summary.{fmt}")
    fig2.savefig(path2, dpi=dpi, bbox_inches="tight")
    plt.close(fig2)
    figures.append(fig2)
    print(f"Saved: {path2}")

    return figures
