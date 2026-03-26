"""
I/O module — loading raw data.
"""

import csv
import os


def load_data(config):
    """Load raw data from the path specified in config.

    Args:
        config (dict): Must contain 'raw_data_path'.

    Returns:
        list[dict]: Each row as a dictionary with column headers as keys.

    Raises:
        FileNotFoundError: If the raw data file does not exist.
    """
    path = config["raw_data_path"]
    if not os.path.exists(path):
        raise FileNotFoundError(f"Data file not found: {path}")

    data = []
    with open(path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(dict(row))  # convert OrderedDict to plain dict

    print(f"Loaded {len(data)} rows from {path}")
    return data
