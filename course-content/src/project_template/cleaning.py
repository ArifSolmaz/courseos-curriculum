"""
Cleaning module — validate and clean raw data.
"""


def clean_data(data, config):
    """Clean raw data according to rules in config.

    Steps:
        1. Drop rows with missing values (if configured)
        2. Drop duplicate rows (if configured)
        3. Validate numeric columns
        4. Apply value range filters
        5. Track drop reasons

    Args:
        data (list[dict]): Raw data rows.
        config (dict): Cleaning configuration.

    Returns:
        list[dict]: Cleaned data rows (only valid rows kept).
    """
    cleaned = []
    drop_reasons = {
        "missing_values": 0,
        "duplicates": 0,
        "non_numeric": 0,
        "out_of_range": 0,
    }

    seen = set()  # for duplicate detection

    for row in data:
        # --- Check for missing values ---
        if config.get("drop_missing", True):
            if any(v is None or str(v).strip() == "" for v in row.values()):
                drop_reasons["missing_values"] += 1
                continue

        # --- Check for duplicates ---
        if config.get("drop_duplicates", True):
            row_key = tuple(sorted(row.items()))
            if row_key in seen:
                drop_reasons["duplicates"] += 1
                continue
            seen.add(row_key)

        # --- Validate numeric columns ---
        skip = False
        numeric_cols = config.get("numeric_columns", [])
        for col in numeric_cols:
            if col in row:
                try:
                    float(row[col])
                except (ValueError, TypeError):
                    drop_reasons["non_numeric"] += 1
                    skip = True
                    break
        if skip:
            continue

        # --- Check value ranges ---
        ranges = config.get("value_ranges", {})
        out_of_range = False
        for col, (low, high) in ranges.items():
            if col in row:
                try:
                    val = float(row[col])
                    if val < low or val > high:
                        drop_reasons["out_of_range"] += 1
                        out_of_range = True
                        break
                except (ValueError, TypeError):
                    pass
        if out_of_range:
            continue

        # Row passed all checks
        cleaned.append(row)

    n_dropped = len(data) - len(cleaned)
    print(f"Cleaning: {len(data)} raw -> {len(cleaned)} clean ({n_dropped} dropped)")
    for reason, count in drop_reasons.items():
        if count > 0:
            print(f"  - {reason}: {count}")

    return cleaned
