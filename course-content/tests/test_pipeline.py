"""
Basic pipeline tests — template for students.
Year 1: run via self_check(). Year 2: run via pytest.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_config_has_required_keys():
    from project_template.config import get_config
    config = get_config()
    for key in ["project_name", "track", "version", "raw_data_path"]:
        assert key in config, f"Missing config key: {key}"


def test_clean_data_returns_list():
    from project_template.cleaning import clean_data
    from project_template.config import get_config
    result = clean_data([], get_config())
    assert isinstance(result, list)


def test_analyze_returns_dict():
    from project_template.analysis import analyze
    from project_template.config import get_config
    result = analyze([], get_config())
    assert isinstance(result, dict)
    assert "analysis_summary" in result


def test_clean_data_filters_bad_rows():
    from project_template.cleaning import clean_data
    from project_template.config import get_config
    data = [
        {"val": "10", "name": "A"},
        {"val": "", "name": "B"},
        {"val": "20", "name": "C"},
    ]
    config = {**get_config(), "drop_missing": True}
    result = clean_data(data, config)
    assert len(result) == 2
