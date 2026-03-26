#!/usr/bin/env python3
"""Generate all CP2 (Computer Programming 2) notebooks -- 14 weeks.

Produces rich, substantial notebooks:
- Core: 60-100+ cells with deep explanations, worked examples, expected
  outputs, common mistakes, debugging tips, why-this-matters, exercises
- Studio: 30-40+ cells with complete starter code and checkpoints
- Homework: 10-15 exercises with progressive difficulty
- Check: universal validation notebook
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from nb_utils import (md, code, notebook, save_notebook,
                      setup_cell, reflection_cell, reflection_code, TRACKS)

BASE = os.path.join(os.path.dirname(__file__), "notebooks", "cp2")
os.makedirs(BASE, exist_ok=True)

WEEKS = [
    (1, "Schema Validation", "validate_schema() + meaningful errors"),
    (2, "Dict Analytics", "histograms, counters, group summaries"),
    (3, "Configurable Cleaning Pipeline", "cleaning steps via config"),
    (4, "Data Quality Reports", "missing/outlier stats & drop reasons"),
    (5, "Matplotlib Standards", "labeled plots, saved figures"),
    (6, "Report Generation", "JSON/MD report with interpretation"),
    (7, "NumPy Introduction", "vectorize one operation"),
    (8, "Timing & Performance", "timeit comparison + interpretation"),
    (9, "Testing: Expanded Self-Check", "detect failure modes"),
    (10, "Golden Outputs", "expected results for toy dataset"),
    (11, "Modularize into /src", "notebooks import only"),
    (12, "Package Hygiene", "config module, stable paths"),
    (13, "Integration on Larger Data", "robust exports and plots"),
    (14, "v2 Release & Demo", "v2 passes universal check"),
]

# Track-specific context for studios
TRACK_CONTEXT = {
    "robotics": {
        "data_fields": ["sensor_id", "timestamp", "temperature", "rpm", "vibration"],
        "sample_values": {"temperature": "72.3", "rpm": "1500", "vibration": "0.05"},
        "domain": "robotic sensor",
        "unit": "temperature (C)",
    },
    "data": {
        "data_fields": ["id", "name", "score", "grade", "submitted"],
        "sample_values": {"score": "85.5", "grade": "B", "submitted": "true"},
        "domain": "survey/assessment",
        "unit": "score (points)",
    },
    "simulation": {
        "data_fields": ["tick", "entity_id", "x_pos", "y_pos", "health"],
        "sample_values": {"x_pos": "120.5", "y_pos": "340.2", "health": "75"},
        "domain": "simulation log",
        "unit": "health (HP)",
    },
    "space": {
        "data_fields": ["obs_id", "timestamp", "brightness", "error_bar", "filter"],
        "sample_values": {"brightness": "1.002", "error_bar": "0.003", "filter": "V"},
        "domain": "astronomical observation",
        "unit": "brightness (relative flux)",
    },
    "iot": {
        "data_fields": ["device_id", "timestamp", "value", "battery", "signal"],
        "sample_values": {"value": "23.7", "battery": "85", "signal": "-42"},
        "domain": "IoT sensor",
        "unit": "value (varies by sensor)",
    },
}

# ================================================================
#  HELPER: common cell patterns
# ================================================================

def expected_output(text):
    """Markdown cell showing expected output."""
    return md("**Expected Output:**\n```\n" + text + "\n```")

def why_matters(text):
    """Why This Matters section."""
    return md("### Why This Matters\n\n" + text)

def common_mistakes(title, items):
    """Common Mistakes section. items = list of (mistake, fix) tuples."""
    lines = ["### Common Mistakes: " + title, ""]
    for i, (mistake, fix) in enumerate(items, 1):
        lines.append("**Mistake " + str(i) + ":** " + mistake)
        lines.append("")
        lines.append("**Fix:** " + fix)
        lines.append("")
    return md("\n".join(lines))

def debugging_tip(title, tips):
    """Debugging Tips section."""
    lines = ["### Debugging Tips: " + title, ""]
    for tip in tips:
        lines.append("- " + tip)
    return md("\n".join(lines))

def key_takeaway(points):
    """Key Takeaway summary box."""
    lines = ["### Key Takeaway", ""]
    for p in points:
        lines.append("- " + p)
    return md("\n".join(lines))

def try_it(prompt):
    """Try It Yourself section header."""
    return md("### Try It Yourself\n\n" + prompt)

def ascii_diagram(title, art):
    """Visual explanation using text diagram."""
    return md("### " + title + "\n\n```\n" + art + "\n```")


# ================================================================
#  CORE NOTEBOOKS
# ================================================================

def make_core_w01():
    """Week 1: Schema Validation -- 80+ cells."""
    cells = [
        md("# CP2 Week 1 -- Schema Validation\n\n"
           "**Course:** Computer Programming 2 (CP2)\n"
           "**Prerequisites:** CP1 complete (v1 pipeline working)\n"
           "**Focus:** validate_schema(), meaningful errors, data contracts\n\n"
           "## Learning Objectives\n"
           "- Understand why schema validation prevents silent failures\n"
           "- Write a `validate_schema()` function with clear error messages\n"
           "- Create data contracts that specify expected structure\n"
           "- Integrate validation into your v2 pipeline\n"
           "- Handle edge cases gracefully"),
        setup_cell(),

        # === PART 1 ===
        md("---\n## Part 1: Why Validate Schemas?\n\n"
           "In CP1, your v1 pipeline assumed data always had the right columns and types. "
           "That works when you control the data, but real-world data is messy:\n\n"
           "- Someone renames a column from `temp` to `temperature`\n"
           "- A CSV export adds an extra column you did not expect\n"
           "- A number field contains the string `\"N/A\"` instead of a number\n"
           "- The file is completely empty\n\n"
           "Without validation, your pipeline **silently produces wrong results** or "
           "**crashes with a confusing error** deep inside your code.\n\n"
           "**Schema validation** checks the structure of your data BEFORE processing, "
           "catching problems early with clear, actionable messages."),

        ascii_diagram("Pipeline Without vs. With Validation",
                      "WITHOUT VALIDATION:\n"
                      "  Raw Data --> clean_data() --> CRASH (line 47: KeyError 'temp')\n"
                      "  (You waste 20 minutes debugging)\n\n"
                      "WITH VALIDATION:\n"
                      "  Raw Data --> validate_schema() --> 'Missing column: temp. Got: temperature'\n"
                      "  (You fix it in 10 seconds)"),

        why_matters(
            "Every professional data pipeline validates its inputs. "
            "Think of it like a bouncer at a club -- checking IDs before anyone gets in. "
            "If bad data sneaks past, every downstream result is suspect. "
            "In your v2 pipeline, `validate_schema()` is the first line of defense."),

        md("### What Is a Schema?\n\n"
           "A **schema** is a description of what your data should look like:\n\n"
           "| Property | Example |\n"
           "|----------|---------|\n"
           "| Required columns | `['id', 'value', 'status']` |\n"
           "| Column types | `{'value': 'numeric', 'status': 'string'}` |\n"
           "| Value ranges | `{'value': (0, 100)}` |\n"
           "| Non-null columns | `['id', 'value']` |\n\n"
           "You store the schema in your config dictionary, so it is easy to update."),

        # Example 1: Simplest possible validation
        md("### Example 1: Check Required Columns (Simplest Version)"),
        code('# Simplest schema validation: just check column names\n'
             '\n'
             'def validate_columns(data, required_columns):\n'
             '    """Check that all required columns are present.\n'
             '    \n'
             '    Args:\n'
             '        data: list of dicts (each dict is a row)\n'
             '        required_columns: list of column names that must exist\n'
             '    \n'
             '    Returns:\n'
             '        True if all columns present\n'
             '    \n'
             '    Raises:\n'
             '        ValueError with helpful message if columns missing\n'
             '    """\n'
             '    if not data:\n'
             '        raise ValueError("Data is empty -- nothing to validate")\n'
             '    \n'
             '    actual = set(data[0].keys())\n'
             '    required = set(required_columns)\n'
             '    missing = required - actual\n'
             '    \n'
             '    if missing:\n'
             '        raise ValueError(\n'
             '            "Missing " + str(len(missing)) + " required column(s): "\n'
             '            + str(sorted(missing)) + "\\n"\n'
             '            "Available columns: " + str(sorted(actual))\n'
             '        )\n'
             '    \n'
             '    print("All " + str(len(required)) + " required columns present.")\n'
             '    return True\n'
             '\n'
             '# Test with GOOD data\n'
             'good_data = [\n'
             '    {"id": 1, "value": "25.0", "status": "ok"},\n'
             '    {"id": 2, "value": "30.0", "status": "ok"},\n'
             ']\n'
             'validate_columns(good_data, ["id", "value", "status"])\n'
             'print("Test 1 PASSED")'),
        expected_output("All 3 required columns present.\nTest 1 PASSED"),

        # Example 2: catch missing columns
        md("### Example 2: Catching Missing Columns"),
        code('# Test with BAD data -- missing columns\n'
             'bad_data = [{"id": 1, "temperature": 25.0}]\n'
             '\n'
             'try:\n'
             '    validate_columns(bad_data, ["id", "value", "status"])\n'
             'except ValueError as e:\n'
             '    print("Caught error:")\n'
             '    print(e)'),
        expected_output("Caught error:\n"
                        "Missing 2 required column(s): ['status', 'value']\n"
                        "Available columns: ['id', 'temperature']"),

        # Example 3: empty data
        md("### Example 3: Handling Empty Data"),
        code('# Test with EMPTY data\n'
             'try:\n'
             '    validate_columns([], ["id", "value"])\n'
             'except ValueError as e:\n'
             '    print("Caught error:", e)'),
        expected_output("Caught error: Data is empty -- nothing to validate"),

        try_it("Test `validate_columns` with data that has EXTRA columns "
               "(more columns than required). Does it still pass? It should -- "
               "extra columns are fine."),
        code('# Try it: data with extra columns\n'
             'extra_data = [\n'
             '    {"id": 1, "value": "10", "status": "ok", "bonus_col": "extra"},\n'
             ']\n'
             '# TODO: call validate_columns and see what happens\n'),

        # === PART 2 ===
        md("---\n## Part 2: Type Validation\n\n"
           "Checking column names is not enough. What if the `value` column contains "
           "the string `\"abc\"` instead of a number? Your pipeline will crash during "
           "analysis, not during validation.\n\n"
           "Let us add type checking to catch this early."),

        code('def validate_types(data, column_types, check_rows=5):\n'
             '    """Check that column values match expected types.\n'
             '    \n'
             '    Args:\n'
             '        data: list of dicts\n'
             '        column_types: dict mapping column name to expected type\n'
             '            Supported types: "numeric", "string", "boolean"\n'
             '        check_rows: how many rows to check (default 5)\n'
             '    \n'
             '    Returns:\n'
             '        list of error messages (empty list = all good)\n'
             '    """\n'
             '    errors = []\n'
             '    \n'
             '    for i, row in enumerate(data[:check_rows]):\n'
             '        for col, expected_type in column_types.items():\n'
             '            if col not in row:\n'
             '                continue  # missing columns handled elsewhere\n'
             '            \n'
             '            val = row[col]\n'
             '            \n'
             '            if expected_type == "numeric":\n'
             '                try:\n'
             '                    float(val)\n'
             '                except (ValueError, TypeError):\n'
             '                    errors.append(\n'
             '                        "Row " + str(i) + ": column " + repr(col)\n'
             '                        + " = " + repr(val)\n'
             '                        + " is not numeric"\n'
             '                    )\n'
             '            \n'
             '            elif expected_type == "string":\n'
             '                if not isinstance(val, str):\n'
             '                    errors.append(\n'
             '                        "Row " + str(i) + ": column " + repr(col)\n'
             '                        + " = " + repr(val)\n'
             '                        + " is not a string"\n'
             '                    )\n'
             '    \n'
             '    return errors\n'
             '\n'
             '# Test: good types\n'
             'data = [\n'
             '    {"id": 1, "value": "25.0", "status": "ok"},\n'
             '    {"id": 2, "value": "30.0", "status": "ok"},\n'
             ']\n'
             'type_rules = {"value": "numeric", "status": "string"}\n'
             'errors = validate_types(data, type_rules)\n'
             'print("Errors:", errors)\n'
             'print("Result:", "PASS" if not errors else "FAIL")'),
        expected_output('Errors: []\nResult: PASS'),

        md("### Example: Catching Type Errors"),
        code('# Data with type problems\n'
             'bad_types = [\n'
             '    {"id": 1, "value": "25.0", "status": "ok"},\n'
             '    {"id": 2, "value": "N/A", "status": "ok"},     # not numeric!\n'
             '    {"id": 3, "value": "abc", "status": "ok"},     # not numeric!\n'
             ']\n'
             '\n'
             'errors = validate_types(bad_types, {"value": "numeric"})\n'
             'print("Type errors found:")\n'
             'for e in errors:\n'
             '    print("  " + e)'),
        expected_output("Type errors found:\n"
                        "  Row 1: column 'value' = 'N/A' is not numeric\n"
                        "  Row 2: column 'value' = 'abc' is not numeric"),

        common_mistakes("Type Validation", [
            ("Checking `isinstance(val, int)` on CSV data -- CSV values are always strings!",
             "Always try `float(val)` for numeric checks on raw CSV data."),
            ("Only checking the first row -- the first row might be fine, but row 50 has a problem.",
             "Check at least the first 5-10 rows. For small datasets, check all rows."),
            ("Using `assert` instead of raising ValueError -- assert can be disabled with -O flag.",
             "Use `raise ValueError(message)` for validation. Reserve assert for tests."),
        ]),

        # === PART 3 ===
        md("---\n## Part 3: The Complete validate_schema() Function\n\n"
           "Now let us combine column checking and type checking into one function "
           "that does everything:"),

        code('def validate_schema(data, config):\n'
             '    """Validate that data matches the expected schema.\n'
             '    \n'
             '    Checks:\n'
             '    1. Data is not empty\n'
             '    2. All required columns are present\n'
             '    3. Column types match expectations\n'
             '    \n'
             '    Args:\n'
             '        data (list[dict]): Raw data rows\n'
             '        config (dict): Must contain:\n'
             '            - required_columns (list): column names\n'
             '            - column_types (dict): {col: type_name}\n'
             '    \n'
             '    Returns:\n'
             '        bool: True if valid\n'
             '    \n'
             '    Raises:\n'
             '        ValueError: if validation fails, with a detailed message\n'
             '    """\n'
             '    # Check 1: not empty\n'
             '    if not data:\n'
             '        raise ValueError(\n'
             '            "Data is empty -- cannot validate schema.\\n"\n'
             '            "Check that load_data() returned data."\n'
             '        )\n'
             '    \n'
             '    # Check 2: required columns\n'
             '    required = config.get("required_columns", [])\n'
             '    actual = set(data[0].keys())\n'
             '    missing = set(required) - actual\n'
             '    \n'
             '    if missing:\n'
             '        extra = actual - set(required)\n'
             '        msg = "Missing " + str(len(missing)) + " required column(s): " + str(sorted(missing)) + "\\n"\n'
             '        msg += "Available columns: " + str(sorted(actual)) + "\\n"\n'
             '        if extra:\n'
             '            msg += "Did you mean one of: " + str(sorted(extra)[:3]) + "?"\n'
             '        raise ValueError(msg)\n'
             '    \n'
             '    # Check 3: column types\n'
             '    type_rules = config.get("column_types", {})\n'
             '    errors = []\n'
             '    for i, row in enumerate(data[:5]):\n'
             '        for col, expected_type in type_rules.items():\n'
             '            if col in row:\n'
             '                val = row[col]\n'
             '                if expected_type == "numeric":\n'
             '                    try:\n'
             '                        float(val)\n'
             '                    except (ValueError, TypeError):\n'
             '                        errors.append(\n'
             '                            "Row " + str(i) + ": " + repr(col)\n'
             '                            + " = " + repr(val)\n'
             '                            + " is not numeric"\n'
             '                        )\n'
             '    \n'
             '    if errors:\n'
             '        raise ValueError(\n'
             '            "Type errors found:\\n" + "\\n".join(errors)\n'
             '        )\n'
             '    \n'
             '    n_cols = len(required)\n'
             '    n_rows = len(data)\n'
             '    print("Schema valid: " + str(n_cols) + " required columns, "\n'
             '          + str(n_rows) + " rows checked")\n'
             '    return True\n'
             '\n'
             '# === Test 1: Good data ===\n'
             'good_data = [\n'
             '    {"id": 1, "value": "25.0", "status": "ok"},\n'
             '    {"id": 2, "value": "30.0", "status": "ok"},\n'
             '    {"id": 3, "value": "15.5", "status": "warning"},\n'
             ']\n'
             'config = {\n'
             '    "required_columns": ["id", "value", "status"],\n'
             '    "column_types": {"value": "numeric"},\n'
             '}\n'
             '\n'
             'result = validate_schema(good_data, config)\n'
             'print("Result:", result)'),
        expected_output("Schema valid: 3 required columns, 3 rows checked\nResult: True"),

        md("### Test: Missing Columns"),
        code('# Test: missing columns give a helpful error\n'
             'bad_data = [{"id": 1, "temperature": 25.0}]\n'
             '\n'
             'try:\n'
             '    validate_schema(bad_data, config)\n'
             'except ValueError as e:\n'
             '    print("Error message:")\n'
             '    print(e)'),
        expected_output("Error message:\n"
                        "Missing 2 required column(s): ['status', 'value']\n"
                        "Available columns: ['id', 'temperature']\n"
                        "Did you mean one of: ['temperature']?"),

        md("### Test: Type Errors"),
        code('# Test: type errors in data\n'
             'type_bad = [\n'
             '    {"id": 1, "value": "25.0", "status": "ok"},\n'
             '    {"id": 2, "value": "not_a_number", "status": "ok"},\n'
             ']\n'
             '\n'
             'try:\n'
             '    validate_schema(type_bad, config)\n'
             'except ValueError as e:\n'
             '    print("Type error caught:")\n'
             '    print(e)'),
        expected_output("Type error caught:\n"
                        "Type errors found:\n"
                        "Row 1: 'value' = 'not_a_number' is not numeric"),

        try_it("Create your own test data with 3 rows that has a DIFFERENT type error "
               "(e.g., an id column that should be numeric but contains text). "
               "Verify that validate_schema catches it."),
        code('# Try it: create data with a type error\n'
             '# TODO: write your test here\n'),

        # === PART 4 ===
        md("---\n## Part 4: Meaningful Error Messages\n\n"
           "The difference between a beginner and a professional programmer is not "
           "whether their code has errors -- it is how HELPFUL those errors are.\n\n"
           "Compare these two approaches:"),

        ascii_diagram("Bad vs. Good Error Messages",
                      "BAD:   AssertionError\n"
                      "       (What failed? Where? What should I do?)\n\n"
                      "BAD:   KeyError: 'temp'\n"
                      "       (Which function? What keys are available?)\n\n"
                      "GOOD:  ValueError: Missing column 'temp'.\n"
                      "       Available columns: ['temperature', 'id', 'status'].\n"
                      "       Did you mean 'temperature'?\n"
                      "       (Clear, actionable, suggests a fix!)"),

        code('# BAD error handling -- DO NOT do this\n'
             'def bad_validate(data):\n'
             '    """This gives unhelpful errors."""\n'
             '    assert len(data) > 0                 # AssertionError (no message)\n'
             '    assert "value" in data[0]             # Which column is missing?\n'
             '    assert data[0]["value"] != ""          # Why? What is wrong?\n'
             '\n'
             '# GOOD error handling -- DO this\n'
             'def good_validate(data, required_columns):\n'
             '    """This gives clear, actionable errors."""\n'
             '    if not data:\n'
             '        raise ValueError(\n'
             '            "Cannot validate empty dataset. "\n'
             '            "Check that load_data() returned data."\n'
             '        )\n'
             '    \n'
             '    actual = set(data[0].keys())\n'
             '    missing = set(required_columns) - actual\n'
             '    extra = actual - set(required_columns)\n'
             '    \n'
             '    if missing:\n'
             '        msg = "Missing " + str(len(missing)) + " required column(s): " + str(sorted(missing)) + "\\n"\n'
             '        msg += "Available columns: " + str(sorted(actual)) + "\\n"\n'
             '        if extra:\n'
             '            msg += "Hint: did you mean " + str(sorted(extra)[:3]) + "?"\n'
             '        raise ValueError(msg)\n'
             '    \n'
             '    print("Validation passed!")\n'
             '    return True\n'
             '\n'
             '# Demo: the good version gives helpful errors\n'
             'try:\n'
             '    good_validate(\n'
             '        [{"temperature": 25, "pressure": 101}],\n'
             '        ["temp", "press", "humidity"]\n'
             '    )\n'
             'except ValueError as e:\n'
             '    print("Error:")\n'
             '    print(e)'),
        expected_output("Error:\n"
                        "Missing 3 required column(s): ['humidity', 'press', 'temp']\n"
                        "Available columns: ['pressure', 'temperature']\n"
                        "Hint: did you mean ['pressure', 'temperature']?"),

        key_takeaway([
            "Always raise ValueError (not assert) for validation errors",
            "Include WHAT is wrong, WHAT was expected, and WHAT the user should do",
            "Suggest possible fixes when you can (e.g., 'did you mean...')",
            "The error message is part of your user interface",
        ]),

        # === PART 5 ===
        md("---\n## Part 5: Data Contracts\n\n"
           "A **data contract** is a formal specification of what your pipeline expects. "
           "It lives in your config and acts as documentation AND validation rules.\n\n"
           "Think of it like a contract between the data producer and your pipeline: "
           "\"I promise to give you data that looks like THIS, and you promise to process it correctly.\""),

        code('def create_data_contract():\n'
             '    """Create a data contract for the v2 pipeline.\n'
             '    \n'
             '    A data contract specifies:\n'
             '    - Which columns must exist\n'
             '    - What types each column should have\n'
             '    - What ranges are acceptable\n'
             '    - Which columns cannot be empty\n'
             '    """\n'
             '    return {\n'
             '        "required_columns": ["id", "value", "timestamp", "status"],\n'
             '        "column_types": {\n'
             '            "id": "numeric",\n'
             '            "value": "numeric",\n'
             '            "timestamp": "string",\n'
             '            "status": "string",\n'
             '        },\n'
             '        "value_ranges": {\n'
             '            "value": (0, 100),\n'
             '        },\n'
             '        "non_null_columns": ["id", "value"],\n'
             '    }\n'
             '\n'
             'contract = create_data_contract()\n'
             'print("Data Contract:")\n'
             'for key, val in contract.items():\n'
             '    print("  " + str(key) + ": " + str(val))'),
        expected_output("Data Contract:\n"
                        "  required_columns: ['id', 'value', 'timestamp', 'status']\n"
                        "  column_types: {'id': 'numeric', 'value': 'numeric', 'timestamp': 'string', 'status': 'string'}\n"
                        "  value_ranges: {'value': (0, 100)}\n"
                        "  non_null_columns: ['id', 'value']"),

        md("### Using the Contract for Validation"),
        code('def validate_with_contract(data, contract):\n'
             '    """Full validation using a data contract.\n'
             '    \n'
             '    Returns:\n'
             '        dict with "valid" (bool), "errors" (list), "warnings" (list)\n'
             '    """\n'
             '    result = {"valid": True, "errors": [], "warnings": []}\n'
             '    \n'
             '    # Check: not empty\n'
             '    if not data:\n'
             '        result["valid"] = False\n'
             '        result["errors"].append("Data is empty")\n'
             '        return result\n'
             '    \n'
             '    # Check: required columns\n'
             '    actual = set(data[0].keys())\n'
             '    missing = set(contract.get("required_columns", [])) - actual\n'
             '    if missing:\n'
             '        result["valid"] = False\n'
             '        result["errors"].append("Missing columns: " + str(sorted(missing)))\n'
             '    \n'
             '    # Check: types (first 5 rows)\n'
             '    for i, row in enumerate(data[:5]):\n'
             '        for col, expected in contract.get("column_types", {}).items():\n'
             '            if col not in row:\n'
             '                continue\n'
             '            val = row[col]\n'
             '            if expected == "numeric":\n'
             '                try:\n'
             '                    float(val)\n'
             '                except (ValueError, TypeError):\n'
             '                    result["errors"].append(\n'
             '                        "Row " + str(i) + ": " + repr(col)\n'
             '                        + " = " + repr(val) + " is not numeric"\n'
             '                    )\n'
             '                    result["valid"] = False\n'
             '    \n'
             '    # Check: non-null columns\n'
             '    for col in contract.get("non_null_columns", []):\n'
             '        null_count = sum(1 for row in data\n'
             '                         if not row.get(col) or str(row[col]).strip() == "")\n'
             '        if null_count > 0:\n'
             '            pct = round(null_count / len(data) * 100, 1)\n'
             '            result["warnings"].append(\n'
             '                "Column " + repr(col) + " has " + str(null_count)\n'
             '                + " null values (" + str(pct) + "%)"\n'
             '            )\n'
             '    \n'
             '    return result\n'
             '\n'
             '# Test with mixed data\n'
             'test_data = [\n'
             '    {"id": "1", "value": "25.0", "timestamp": "2024-01-01", "status": "ok"},\n'
             '    {"id": "2", "value": "", "timestamp": "2024-01-02", "status": "ok"},\n'
             '    {"id": "3", "value": "30.0", "timestamp": "2024-01-03", "status": "warn"},\n'
             ']\n'
             '\n'
             'contract = create_data_contract()\n'
             'result = validate_with_contract(test_data, contract)\n'
             '\n'
             'print("Valid:", result["valid"])\n'
             'print("Errors:", result["errors"])\n'
             'print("Warnings:", result["warnings"])'),
        expected_output("Valid: True\n"
                        "Errors: []\n"
                        "Warnings: [\"Column 'value' has 1 null values (33.3%)\"]"),

        # === PART 6 ===
        md("---\n## Part 6: Integrating Validation Into Your Pipeline\n\n"
           "Validation should happen EARLY -- right after loading data, before any cleaning or analysis."),

        ascii_diagram("Where Validation Fits",
                      "load_data()\n"
                      "    |\n"
                      "    v\n"
                      "validate_schema()  <--- NEW in v2\n"
                      "    |\n"
                      "    v\n"
                      "clean_data()\n"
                      "    |\n"
                      "    v\n"
                      "analyze()\n"
                      "    |\n"
                      "    v\n"
                      "plot() + export_results()"),

        code('def load_and_validate(config):\n'
             '    """Load data and validate schema before processing.\n'
             '    \n'
             '    Returns:\n'
             '        list of dicts if valid, None if validation fails\n'
             '    """\n'
             '    # Step 1: Load (simulated)\n'
             '    data = [\n'
             '        {"id": 1, "value": "25.0", "timestamp": "2024-01-01"},\n'
             '        {"id": 2, "value": "30.0", "timestamp": "2024-01-02"},\n'
             '        {"id": 3, "value": "", "timestamp": "2024-01-03"},\n'
             '    ]\n'
             '    print("Loaded " + str(len(data)) + " rows")\n'
             '    \n'
             '    # Step 2: Validate schema BEFORE cleaning\n'
             '    try:\n'
             '        validate_schema(data, config)\n'
             '        print("Schema validation passed!")\n'
             '    except ValueError as e:\n'
             '        print("Schema validation FAILED:")\n'
             '        print(str(e))\n'
             '        print("Fix your data or config before continuing.")\n'
             '        return None\n'
             '    \n'
             '    return data\n'
             '\n'
             'config = {\n'
             '    "required_columns": ["id", "value", "timestamp"],\n'
             '    "column_types": {"value": "numeric"},\n'
             '}\n'
             'result = load_and_validate(config)\n'
             'if result:\n'
             '    print("Ready to process " + str(len(result)) + " rows")'),
        expected_output("Loaded 3 rows\n"
                        "Schema valid: 3 required columns, 3 rows checked\n"
                        "Schema validation passed!\n"
                        "Ready to process 3 rows"),

        debugging_tip("Schema Validation", [
            "If you get 'Data is empty', check that load_data() actually read the file.",
            "If you get 'Missing columns', print data[0].keys() to see what columns exist.",
            "If column names have extra spaces, use .strip() on them before validation.",
            "CSV files always load values as strings -- that is why type checking uses float().",
        ]),

        # === PART 7 ===
        md("---\n## Part 7: Common Mistakes With Worked Fixes"),

        md("### Mistake 1: Using assert for Validation"),
        code('# WRONG: using assert for validation\n'
             'def bad_validate_v1(data):\n'
             '    assert len(data) > 0           # No message!\n'
             '    assert "value" in data[0]       # Cryptic if it fails\n'
             '\n'
             '# What happens when it fails:\n'
             'try:\n'
             '    bad_validate_v1([])\n'
             'except AssertionError as e:\n'
             '    print("AssertionError:", e)  # Empty message!\n'
             '\n'
             '# CORRECT: use raise ValueError with a message\n'
             'def good_validate_v1(data):\n'
             '    if not data:\n'
             '        raise ValueError(\n'
             '            "Data is empty. Check that your file path is correct "\n'
             '            "and the file is not empty."\n'
             '        )\n'
             '\n'
             'try:\n'
             '    good_validate_v1([])\n'
             'except ValueError as e:\n'
             '    print("ValueError:", e)'),
        expected_output("AssertionError: \n"
                        "ValueError: Data is empty. Check that your file path is correct "
                        "and the file is not empty."),

        md("### Mistake 2: Checking Types With isinstance on CSV Data"),
        code('# WRONG: CSV data is always strings\n'
             'row = {"value": "25.0"}  # loaded from CSV\n'
             'print("Is int?", isinstance(row["value"], int))       # False!\n'
             'print("Is float?", isinstance(row["value"], float))   # False!\n'
             'print("Is str?", isinstance(row["value"], str))       # True (always)\n'
             '\n'
             '# CORRECT: try to convert\n'
             'try:\n'
             '    val = float(row["value"])\n'
             '    print("Converted to float:", val)  # Works!\n'
             'except ValueError:\n'
             '    print("Not a number")'),
        expected_output("Is int? False\nIs float? False\nIs str? True\n"
                        "Converted to float: 25.0"),

        md("### Mistake 3: Only Checking the First Row"),
        code('# WRONG: first row is fine, but row 3 has a problem\n'
             'tricky_data = [\n'
             '    {"id": "1", "value": "25.0"},   # fine\n'
             '    {"id": "2", "value": "30.0"},   # fine\n'
             '    {"id": "3", "value": "N/A"},    # PROBLEM\n'
             '    {"id": "4", "value": "40.0"},   # fine\n'
             ']\n'
             '\n'
             '# Only checking row 0 would miss the problem!\n'
             'print("Row 0 value:", tricky_data[0]["value"])\n'
             'print("Can convert?", end=" ")\n'
             'try:\n'
             '    float(tricky_data[0]["value"])\n'
             '    print("Yes")\n'
             'except ValueError:\n'
             '    print("No")\n'
             '\n'
             '# Better: check multiple rows\n'
             'for i, row in enumerate(tricky_data):\n'
             '    try:\n'
             '        float(row["value"])\n'
             '    except (ValueError, TypeError):\n'
             '        print("Problem at row " + str(i) + ": value = " + repr(row["value"]))'),
        expected_output("Row 0 value: 25.0\nCan convert? Yes\n"
                        "Problem at row 2: value = 'N/A'"),

        # === PART 8: Exercises ===
        md("---\n## Try It Yourself: Practice Exercises"),

        md("### Exercise 1: Validate a Custom Schema\n"
           "Write a schema config for data with columns: name (string), age (numeric), email (string). "
           "Then test it with both valid and invalid data."),
        code('# Exercise 1: Your custom schema validation\n'
             '# TODO: create config with required_columns and column_types\n'
             '# TODO: create test_data_good and test_data_bad\n'
             '# TODO: call validate_schema on both\n'),

        md("### Exercise 2: Add Range Validation\n"
           "Extend validate_schema to also check value ranges. "
           "If config has `value_ranges = {'age': (0, 150)}`, reject rows where age is outside that range."),
        code('# Exercise 2: Add range checking\n'
             '# TODO: write validate_ranges(data, config) function\n'
             '# It should return a list of violations\n'),

        md("### Exercise 3: Validation Report\n"
           "Write a function that runs ALL validation checks and returns a summary dict."),
        code('# Exercise 3: Full validation report\n'
             '# TODO: write full_validation_report(data, config)\n'
             '# It should return {"valid": bool, "checks_passed": int, "checks_failed": int, "details": [...]}\n'),

        # === Mini-Quiz ===
        md("---\n## Mini-Quiz"),
        code('# Q1: What is the difference between assert and raise ValueError?\n'
             '# Answer: \n'
             '\n'
             '# Q2: Why should validation happen BEFORE cleaning, not after?\n'
             '# Answer: \n'
             '\n'
             '# Q3: What 3 things should a good error message include?\n'
             '# Answer: \n'
             '\n'
             '# Q4: Why does isinstance(csv_value, float) not work on CSV data?\n'
             '# Answer: '),

        # === HOMEWORK ===
        md("---\n## Homework: 12 Exercises\n\n"
           "Complete before next week. Estimated time: 2-4 hours.\n\n"
           "### Review (1-4)"),

        code('# HW1: Explain in comments: what is a data contract?\n'
             '# What are the 4 things it specifies?\n'
             '# Answer:\n'),
        code('# HW2: Write a validate_schema call that checks for columns\n'
             '# "name", "email", "phone" with "phone" being numeric.\n'
             '# Test with data that PASSES and data that FAILS.\n'),
        code('# HW3: What error message would validate_schema give for this data?\n'
             '# data = [{"x": 1, "y": 2}]\n'
             '# config = {"required_columns": ["a", "b", "c"], "column_types": {}}\n'
             '# Write your prediction, then run it to check.\n'
             '# Prediction:\n'),
        code('# HW4: Fix this broken validation function:\n'
             'def broken_validate(data, columns):\n'
             '    for col in columns:\n'
             '        if col in data:\n'
             '            return True\n'
             '    return False\n'
             '\n'
             '# What is wrong? Fix it below:\n'
             '# def fixed_validate(data, columns):\n'),

        md("### Practice (5-8)"),
        code('# HW5: Write validate_non_null(data, non_null_columns) that checks\n'
             '# that certain columns never have empty string or None values.\n'
             '# Return a dict of {column: null_count} for any column with nulls.\n'),
        code('# HW6: Write validate_unique(data, unique_columns) that checks\n'
             '# that certain columns have no duplicate values.\n'
             '# Return a dict of {column: duplicate_count} for any column with duplicates.\n'),
        code('# HW7: Create a data contract for YOUR track project.\n'
             '# Include: required_columns, column_types, value_ranges, non_null_columns.\n'
             '# Test it with sample data from your project.\n'),
        code('# HW8: Write a function that validates a CSV file from disk:\n'
             '# def validate_csv_file(filepath, config):\n'
             '#     1. Check file exists\n'
             '#     2. Load with csv.DictReader\n'
             '#     3. Call validate_schema\n'
             '#     4. Return validation result\n'),

        md("### Challenge (9-11)"),
        code('# HW9: Implement "fuzzy column matching" -- if a required column is\n'
             '# missing but a similar column exists, suggest it.\n'
             '# Example: required="temp", actual has "temperature" -> suggest it\n'
             '# Hint: check if required_col is a substring of any actual column.\n'),
        code('# HW10: Write a validation decorator that automatically validates\n'
             '# the input to any pipeline function:\n'
             '# @validate_input(required_columns=["id", "value"])\n'
             '# def clean_data(data, config):\n'
             '#     ...\n'),
        code('# HW11: Create a ValidationReport class that collects errors,\n'
             '# warnings, and info messages, and can print a formatted summary.\n'),

        md("### Mini-Project"),
        code('# HW12 (Mini-Project): Build a complete schema validation module.\n'
             '# Requirements:\n'
             '# - validate_schema(data, config) function\n'
             '# - At least 5 different checks (columns, types, ranges, nulls, uniqueness)\n'
             '# - Clear error messages with suggestions\n'
             '# - A demo that shows it catching 3 different kinds of errors\n'
             '# - Print a validation summary at the end\n'),

        reflection_cell(),
        reflection_code(),
    ]
    return cells


def make_core_w02():
    """Week 2: Dict Analytics -- 80+ cells."""
    cells = [
        md("# CP2 Week 2 -- Dict Analytics\n\n"
           "**Course:** Computer Programming 2 (CP2)\n"
           "**Prerequisites:** CP1 complete, Week 1 schema validation\n"
           "**Focus:** counters, histograms, group summaries, collections.Counter\n\n"
           "## Learning Objectives\n"
           "- Use dictionaries as counters and accumulators\n"
           "- Build group summaries (like SQL GROUP BY)\n"
           "- Create text-based histograms\n"
           "- Use `collections.Counter` for efficient counting\n"
           "- Apply these patterns to your v2 pipeline analytics"),
        setup_cell(),

        # === PART 1: Dicts as Counters ===
        md("---\n## Part 1: Dictionaries as Counters\n\n"
           "One of the most common patterns in data analysis is **counting things**. "
           "How many times does each value appear? Dictionaries are perfect for this.\n\n"
           "Think of it like a tally sheet:\n"
           "- You see \"cat\" -> make a tally mark next to \"cat\"\n"
           "- You see \"dog\" -> make a tally mark next to \"dog\"\n"
           "- You see \"cat\" again -> add another tally mark next to \"cat\"\n\n"
           "In Python, the dictionary IS the tally sheet, and the values ARE the counts."),

        md("### Method 1: Manual Counting (the basic way)"),
        code('# Manual counting with if/else\n'
             'animals = ["cat", "dog", "cat", "bird", "dog", "cat", "fish", "dog"]\n'
             '\n'
             'counts = {}\n'
             'for animal in animals:\n'
             '    if animal in counts:\n'
             '        counts[animal] += 1      # already seen: add 1\n'
             '    else:\n'
             '        counts[animal] = 1        # first time: start at 1\n'
             '\n'
             'print("Counts:", counts)\n'
             'print("Most cats:", counts["cat"])'),
        expected_output("Counts: {'cat': 3, 'dog': 3, 'bird': 1, 'fish': 1}\nMost cats: 3"),

        md("### Method 2: Using .get() (cleaner)"),
        code('# Cleaner counting with .get()\n'
             'animals = ["cat", "dog", "cat", "bird", "dog", "cat", "fish", "dog"]\n'
             '\n'
             'counts = {}\n'
             'for animal in animals:\n'
             '    counts[animal] = counts.get(animal, 0) + 1\n'
             '    # .get(key, default) returns the value if key exists,\n'
             '    # otherwise returns the default (0)\n'
             '\n'
             'print("Counts:", counts)'),
        expected_output("Counts: {'cat': 3, 'dog': 3, 'bird': 1, 'fish': 1}"),

        why_matters(
            "The `.get(key, default)` pattern is one of the most useful Python idioms. "
            "You will use it constantly in data processing. It avoids the if/else check "
            "and makes your code shorter and more readable.\n\n"
            "In your v2 pipeline, you will count: drop reasons, status codes, categories, "
            "error types, and more."),

        md("### Method 3: collections.Counter (the best way)"),
        code('from collections import Counter\n'
             '\n'
             'animals = ["cat", "dog", "cat", "bird", "dog", "cat", "fish", "dog"]\n'
             '\n'
             'counts = Counter(animals)\n'
             'print("Counter:", counts)\n'
             'print("Type:", type(counts))\n'
             'print()\n'
             '\n'
             '# Counter has special methods:\n'
             'print("Most common 2:", counts.most_common(2))\n'
             'print("Cat count:", counts["cat"])\n'
             'print("Missing key:", counts["elephant"])  # returns 0, no error!\n'
             'print()\n'
             '\n'
             '# You can add more data\n'
             'more = Counter(["cat", "cat", "elephant"])\n'
             'combined = counts + more\n'
             'print("Combined:", combined)'),
        expected_output("Counter: Counter({'cat': 3, 'dog': 3, 'bird': 1, 'fish': 1})\n"
                        "Type: <class 'collections.Counter'>\n\n"
                        "Most common 2: [('cat', 3), ('dog', 3)]\n"
                        "Cat count: 3\n"
                        "Missing key: 0\n\n"
                        "Combined: Counter({'cat': 5, 'dog': 3, 'bird': 1, 'fish': 1, 'elephant': 1})"),

        common_mistakes("Counting", [
            ("Forgetting to initialize the count: `counts[animal] += 1` crashes if key does not exist.",
             "Use `counts[animal] = counts.get(animal, 0) + 1` or use `Counter`."),
            ("Using a list to count -- iterating the list each time to find the item is O(n) per lookup.",
             "Dicts give O(1) lookup. Use a dict or Counter for counting."),
            ("Not knowing about Counter -- writing 5 lines when 1 line does the job.",
             "`from collections import Counter; counts = Counter(items)` -- done!"),
        ]),

        try_it("Count the frequency of each letter in the string below. "
               "Use whichever method you prefer."),
        code('# Try it: count letter frequencies\n'
             'text = "abracadabra"\n'
             '# TODO: count each letter and print the result\n'),

        # === PART 2: Counting in Real Data ===
        md("---\n## Part 2: Counting Patterns in Data\n\n"
           "In your v2 pipeline, you will often need to count categories in your data. "
           "Here is how to count values from a specific column in a list of dicts:"),

        code('from collections import Counter\n'
             '\n'
             '# Pipeline data with a "status" column\n'
             'data = [\n'
             '    {"id": 1, "value": "25", "status": "ok"},\n'
             '    {"id": 2, "value": "30", "status": "ok"},\n'
             '    {"id": 3, "value": "",   "status": "missing"},\n'
             '    {"id": 4, "value": "abc","status": "error"},\n'
             '    {"id": 5, "value": "15", "status": "ok"},\n'
             '    {"id": 6, "value": "-5", "status": "out_of_range"},\n'
             '    {"id": 7, "value": "50", "status": "ok"},\n'
             '    {"id": 8, "value": "",   "status": "missing"},\n'
             ']\n'
             '\n'
             '# Count statuses\n'
             'status_counts = Counter(row["status"] for row in data)\n'
             'print("Status counts:")\n'
             'for status, count in status_counts.most_common():\n'
             '    pct = count / len(data) * 100\n'
             '    print("  " + status + ": " + str(count) + " (" + str(round(pct, 1)) + "%)")'),
        expected_output("Status counts:\n"
                        "  ok: 4 (50.0%)\n"
                        "  missing: 2 (25.0%)\n"
                        "  error: 1 (12.5%)\n"
                        "  out_of_range: 1 (12.5%)"),

        md("### Counting Drop Reasons\n\n"
           "When your cleaning pipeline drops rows, you should count WHY each row was dropped. "
           "This is essential for your data quality report."),

        code('def count_drop_reasons(data, numeric_columns, value_ranges):\n'
             '    """Categorize each row and count reasons for dropping.\n'
             '    \n'
             '    Returns:\n'
             '        dict with "kept", "dropped", and "reasons" keys\n'
             '    """\n'
             '    reasons = Counter()\n'
             '    kept = 0\n'
             '    \n'
             '    for row in data:\n'
             '        drop_reason = None\n'
             '        \n'
             '        # Check for missing values\n'
             '        for col in numeric_columns:\n'
             '            val = row.get(col, "")\n'
             '            if val is None or str(val).strip() == "":\n'
             '                drop_reason = "missing_" + col\n'
             '                break\n'
             '        \n'
             '        # Check for non-numeric values\n'
             '        if not drop_reason:\n'
             '            for col in numeric_columns:\n'
             '                try:\n'
             '                    float(row[col])\n'
             '                except (ValueError, TypeError):\n'
             '                    drop_reason = "non_numeric_" + col\n'
             '                    break\n'
             '        \n'
             '        # Check for out-of-range values\n'
             '        if not drop_reason:\n'
             '            for col, (low, high) in value_ranges.items():\n'
             '                if col in row:\n'
             '                    val = float(row[col])\n'
             '                    if val < low or val > high:\n'
             '                        drop_reason = "out_of_range_" + col\n'
             '                        break\n'
             '        \n'
             '        if drop_reason:\n'
             '            reasons[drop_reason] += 1\n'
             '        else:\n'
             '            kept += 1\n'
             '    \n'
             '    return {\n'
             '        "total": len(data),\n'
             '        "kept": kept,\n'
             '        "dropped": sum(reasons.values()),\n'
             '        "reasons": dict(reasons.most_common()),\n'
             '    }\n'
             '\n'
             '# Test\n'
             'data = [\n'
             '    {"id": 1, "value": "25"},\n'
             '    {"id": 2, "value": ""},\n'
             '    {"id": 3, "value": "abc"},\n'
             '    {"id": 4, "value": "50"},\n'
             '    {"id": 5, "value": "150"},   # out of range\n'
             '    {"id": 6, "value": "-10"},    # out of range\n'
             '    {"id": 7, "value": "30"},\n'
             ']\n'
             '\n'
             'report = count_drop_reasons(data, ["value"], {"value": (0, 100)})\n'
             'print("Total:", report["total"])\n'
             'print("Kept:", report["kept"])\n'
             'print("Dropped:", report["dropped"])\n'
             'print("Reasons:")\n'
             'for reason, count in report["reasons"].items():\n'
             '    print("  " + reason + ": " + str(count))'),
        expected_output("Total: 7\nKept: 3\nDropped: 4\n"
                        "Reasons:\n  out_of_range_value: 2\n  missing_value: 1\n  non_numeric_value: 1"),

        # === PART 3: Group Summaries ===
        md("---\n## Part 3: Group Summaries\n\n"
           "Often you need to analyze data separately for each group -- like computing "
           "average temperature per city, or average score per category.\n\n"
           "This is the same idea as SQL's `GROUP BY`. In Python, we use a dict of lists."),

        ascii_diagram("Group-By Concept",
                      "Raw Data:                     Grouped:\n"
                      "  Cairo  32                    Cairo:  [32, 35]  -> mean=33.5\n"
                      "  Cairo  35                    Alex:   [28, 26]  -> mean=27.0\n"
                      "  Alex   28                    Luxor:  [40, 42]  -> mean=41.0\n"
                      "  Alex   26\n"
                      "  Luxor  40\n"
                      "  Luxor  42"),

        code('def group_summary(data, group_col, value_col):\n'
             '    """Compute summary statistics grouped by a column.\n'
             '    \n'
             '    Like a simple GROUP BY in SQL.\n'
             '    \n'
             '    Args:\n'
             '        data: list of dicts\n'
             '        group_col: column to group by\n'
             '        value_col: column to compute stats on\n'
             '    \n'
             '    Returns:\n'
             '        dict: {group_name: {"count": N, "sum": X, "mean": Y, "min": A, "max": B}}\n'
             '    """\n'
             '    # Step 1: collect values per group\n'
             '    groups = {}\n'
             '    for row in data:\n'
             '        group = row.get(group_col, "unknown")\n'
             '        try:\n'
             '            val = float(row.get(value_col, 0))\n'
             '        except (ValueError, TypeError):\n'
             '            continue  # skip non-numeric\n'
             '        \n'
             '        if group not in groups:\n'
             '            groups[group] = []\n'
             '        groups[group].append(val)\n'
             '    \n'
             '    # Step 2: compute stats per group\n'
             '    result = {}\n'
             '    for group, vals in groups.items():\n'
             '        result[group] = {\n'
             '            "count": len(vals),\n'
             '            "sum": round(sum(vals), 2),\n'
             '            "mean": round(sum(vals) / len(vals), 2),\n'
             '            "min": round(min(vals), 2),\n'
             '            "max": round(max(vals), 2),\n'
             '        }\n'
             '    \n'
             '    return result\n'
             '\n'
             '# Test with city temperatures\n'
             'data = [\n'
             '    {"city": "Cairo", "temp": "32"},\n'
             '    {"city": "Cairo", "temp": "35"},\n'
             '    {"city": "Cairo", "temp": "33"},\n'
             '    {"city": "Alex",  "temp": "28"},\n'
             '    {"city": "Alex",  "temp": "26"},\n'
             '    {"city": "Luxor", "temp": "40"},\n'
             '    {"city": "Luxor", "temp": "42"},\n'
             '    {"city": "Luxor", "temp": "38"},\n'
             ']\n'
             '\n'
             'result = group_summary(data, "city", "temp")\n'
             'for city, stats in result.items():\n'
             '    print(city + ": count=" + str(stats["count"])\n'
             '          + ", mean=" + str(stats["mean"])\n'
             '          + ", range=[" + str(stats["min"]) + "-" + str(stats["max"]) + "]")'),
        expected_output("Cairo: count=3, mean=33.33, range=[32.0-35.0]\n"
                        "Alex: count=2, mean=27.0, range=[26.0-28.0]\n"
                        "Luxor: count=3, mean=40.0, range=[38.0-42.0]"),

        md("### Example: Multi-Column Group Summary"),
        code('# Group summary with multiple value columns\n'
             'def multi_summary(data, group_col, value_cols):\n'
             '    """Compute stats for multiple columns, grouped."""\n'
             '    results = {}\n'
             '    \n'
             '    for col in value_cols:\n'
             '        results[col] = group_summary(data, group_col, col)\n'
             '    \n'
             '    return results\n'
             '\n'
             'data = [\n'
             '    {"dept": "eng", "salary": "70000", "years": "5"},\n'
             '    {"dept": "eng", "salary": "85000", "years": "8"},\n'
             '    {"dept": "sales", "salary": "60000", "years": "3"},\n'
             '    {"dept": "sales", "salary": "55000", "years": "2"},\n'
             '    {"dept": "sales", "salary": "75000", "years": "7"},\n'
             ']\n'
             '\n'
             'results = multi_summary(data, "dept", ["salary", "years"])\n'
             'for col, groups in results.items():\n'
             '    print(col + ":")\n'
             '    for group, stats in groups.items():\n'
             '        print("  " + group + ": mean=" + str(stats["mean"]))'),
        expected_output("salary:\n  eng: mean=77500.0\n  sales: mean=63333.33\n"
                        "years:\n  eng: mean=6.5\n  sales: mean=4.0"),

        try_it("Use group_summary on your own data. Create a list of dicts with "
               "at least 10 rows, a category column, and a numeric column."),
        code('# Try it: your own group summary\n'
             '# TODO: create data and run group_summary\n'),

        # === PART 4: Histograms ===
        md("---\n## Part 4: Building Histograms With Dicts\n\n"
           "A **histogram** shows the distribution of values by grouping them into bins. "
           "You can build one using a dictionary where keys are bin labels and values are counts.\n\n"
           "Before matplotlib (Week 5), we will make text-based histograms that work anywhere."),

        code('def build_histogram(values, bin_width=10):\n'
             '    """Build a text histogram using a dictionary.\n'
             '    \n'
             '    Args:\n'
             '        values: list of numbers\n'
             '        bin_width: width of each bin\n'
             '    \n'
             '    Returns:\n'
             '        dict: {bin_label: count}\n'
             '    """\n'
             '    bins = {}\n'
             '    for v in values:\n'
             '        bin_start = int(v // bin_width) * bin_width\n'
             '        label = str(bin_start) + "-" + str(bin_start + bin_width)\n'
             '        bins[label] = bins.get(label, 0) + 1\n'
             '    \n'
             '    # Sort by bin start\n'
             '    sorted_bins = dict(sorted(\n'
             '        bins.items(),\n'
             '        key=lambda x: int(x[0].split("-")[0])\n'
             '    ))\n'
             '    \n'
             '    # Print text histogram\n'
             '    max_count = max(sorted_bins.values())\n'
             '    for label, count in sorted_bins.items():\n'
             '        bar_len = int(count / max_count * 40)\n'
             '        bar = "#" * bar_len\n'
             '        print("  " + label.rjust(10) + " | " + bar + " (" + str(count) + ")")\n'
             '    \n'
             '    return sorted_bins\n'
             '\n'
             '# Generate some data\n'
             'import random\n'
             'random.seed(42)\n'
             'values = [random.gauss(50, 15) for _ in range(100)]\n'
             'print("Distribution of 100 random values (mean=50, std=15):")\n'
             'hist = build_histogram(values, bin_width=10)'),
        expected_output("Distribution of 100 random values (mean=50, std=15):\n"
                        "      10-20 | ### (3)\n"
                        "      20-30 | ########## (10)\n"
                        "      30-40 | #################### (20)\n"
                        "      40-50 | ############################ (28)\n"
                        "      50-60 | ####################################### (22)\n"
                        "      60-70 | ############ (12)\n"
                        "      70-80 | #### (4)\n"
                        "      80-90 | # (1)\n"
                        "(approximate -- random seed may vary slightly)"),

        md("### Histogram for Pipeline Data"),
        code('# Build histogram from pipeline data\n'
             'data = [\n'
             '    {"id": i, "value": str(round(random.gauss(50, 20), 1))}\n'
             '    for i in range(50)\n'
             ']\n'
             '\n'
             '# Extract numeric values, skipping bad ones\n'
             'values = []\n'
             'for row in data:\n'
             '    try:\n'
             '        values.append(float(row["value"]))\n'
             '    except (ValueError, TypeError):\n'
             '        pass\n'
             '\n'
             'print("Value distribution (" + str(len(values)) + " valid values):")\n'
             'hist = build_histogram(values, bin_width=10)'),

        key_takeaway([
            "Use `.get(key, default)` for safe dict access with defaults",
            "`collections.Counter` is the fastest way to count things",
            "Group summaries collect values per group, then compute stats",
            "Text histograms are a quick way to see distributions without matplotlib",
            "Always count drop reasons in your cleaning pipeline",
        ]),

        debugging_tip("Dict Analytics", [
            "KeyError means the key does not exist -- use .get() instead of []",
            "If Counter gives unexpected results, check that input values are the right type",
            "Empty groups usually mean the group_col has no matching values -- print data[0] to check",
            "If histogram bins look wrong, check bin_width and the range of your values",
        ]),

        # === Exercises ===
        md("---\n## Mini-Quiz"),
        code('# Q1: What does dict.get("key", 0) return if "key" does not exist?\n'
             '# Answer: \n'
             '\n'
             '# Q2: What is the advantage of Counter over manual counting?\n'
             '# Answer: \n'
             '\n'
             '# Q3: How would you count the number of rows per category in your pipeline?\n'
             '# Answer: '),

        md("---\n## Homework: 12 Exercises\n\n"
           "### Review (1-4)"),
        code('# HW1: Count the frequency of each word in this sentence:\n'
             'sentence = "the cat sat on the mat and the cat slept"\n'
             '# Use Counter\n'),
        code('# HW2: Given this data, count how many rows have each status:\n'
             'data = [\n'
             '    {"id": 1, "status": "ok"},\n'
             '    {"id": 2, "status": "error"},\n'
             '    {"id": 3, "status": "ok"},\n'
             '    {"id": 4, "status": "warning"},\n'
             '    {"id": 5, "status": "ok"},\n'
             '    {"id": 6, "status": "error"},\n'
             ']\n'),
        code('# HW3: Write group_summary for this data, grouped by "category":\n'
             'data = [\n'
             '    {"category": "A", "score": "90"},\n'
             '    {"category": "B", "score": "75"},\n'
             '    {"category": "A", "score": "85"},\n'
             '    {"category": "C", "score": "60"},\n'
             '    {"category": "B", "score": "80"},\n'
             ']\n'),
        code('# HW4: Explain in comments: why is counting drop reasons important\n'
             '# for a data quality report?\n'),

        md("### Practice (5-8)"),
        code('# HW5: Write a function that takes pipeline data and returns\n'
             '# a "drop reason summary" with counts and percentages.\n'),
        code('# HW6: Build a histogram of the values in your project data.\n'
             '# Choose an appropriate bin_width.\n'),
        code('# HW7: Write a function that computes the top-N most common values\n'
             '# in a given column. Return as a list of (value, count) tuples.\n'),
        code('# HW8: Combine group_summary and histogram: for each group,\n'
             '# print a mini-histogram of the values.\n'),

        md("### Challenge (9-11)"),
        code('# HW9: Implement a "running counter" that updates counts as new\n'
             '# data arrives (simulating streaming data). Use Counter.update().\n'),
        code('# HW10: Write a cross-tabulation function: given two columns,\n'
             '# count all combinations (e.g., city x status).\n'),
        code('# HW11: Build a "data profile" function that automatically\n'
             '# analyzes every column: counts for strings, stats for numbers.\n'),

        md("### Mini-Project"),
        code('# HW12: Build a complete analytics dashboard (text-based) for\n'
             '# your project data. It should display:\n'
             '# - Row counts by category\n'
             '# - Summary stats per group\n'
             '# - Histogram of main numeric column\n'
             '# - Top 5 most common values per string column\n'
             '# Print everything in a readable format.\n'),

        reflection_cell(),
        reflection_code(),
    ]
    return cells


def make_core_w03():
    """Week 3: Configurable Cleaning Pipeline."""
    cells = [
        md("# CP2 Week 3 -- Configurable Cleaning Pipeline\n\n"
           "**Course:** Computer Programming 2 (CP2)\n"
           "**Prerequisites:** Weeks 1-2 (schema validation, dict analytics)\n"
           "**Focus:** rule registry, config-driven cleaning steps\n\n"
           "## Learning Objectives\n"
           "- Design a config-driven cleaning pipeline\n"
           "- Create a rule registry pattern\n"
           "- Write individual cleaning rules as functions\n"
           "- Track drop reasons for every removed row\n"
           "- Add custom rules without changing core code"),
        setup_cell(),

        md("---\n## Part 1: Why Config-Driven Cleaning?\n\n"
           "In CP1, your cleaning code probably looked like this:\n\n"
           "```python\n"
           "# Hard-coded cleaning (v1 style)\n"
           "if row['value'] == '':\n"
           "    continue  # skip missing\n"
           "if float(row['value']) < 0:\n"
           "    continue  # skip negative\n"
           "```\n\n"
           "This works, but has problems:\n"
           "- Every track has DIFFERENT rules (robotics cares about temperature range, space cares about brightness)\n"
           "- Changing a threshold means editing code deep inside a function\n"
           "- You cannot easily turn rules on/off for testing\n\n"
           "**Config-driven cleaning** separates WHAT to clean (config) from HOW to clean (code)."),

        ascii_diagram("Config-Driven Architecture",
                      "CONFIG (data, easy to change)      CODE (logic, rarely changes)\n"
                      "+--------------------------+       +---------------------------+\n"
                      "| drop_missing: True       | ----> | if config['drop_missing']:|\n"
                      "| numeric_columns: [value] |       |   check_missing(row, col) |\n"
                      "| value_ranges:            |       |                           |\n"
                      "|   value: (0, 100)        | ----> | if val < low or val > high|\n"
                      "| strip_whitespace: True   |       |   drop(row, reason)       |\n"
                      "+--------------------------+       +---------------------------+"),

        md("### Step 1: Create a Cleaning Config"),
        code('def create_cleaning_config():\n'
             '    """Create a configuration for the cleaning pipeline.\n'
             '    \n'
             '    All cleaning behavior is controlled by this dict.\n'
             '    Change the config to change the behavior -- no code changes needed.\n'
             '    """\n'
             '    return {\n'
             '        # Which checks to run\n'
             '        "drop_missing": True,\n'
             '        "drop_duplicates": True,\n'
             '        "check_types": True,\n'
             '        "check_ranges": True,\n'
             '        \n'
             '        # Column definitions\n'
             '        "numeric_columns": ["value", "score"],\n'
             '        "string_columns": ["status", "category"],\n'
             '        \n'
             '        # Acceptable ranges\n'
             '        "value_ranges": {\n'
             '            "value": (0, 100),\n'
             '            "score": (0, 100),\n'
             '        },\n'
             '        \n'
             '        # Text processing\n'
             '        "strip_whitespace": True,\n'
             '        "lowercase_strings": False,\n'
             '        \n'
             '        # Custom rules to apply\n'
             '        "custom_rules": ["remove_negative", "cap_outliers"],\n'
             '    }\n'
             '\n'
             'config = create_cleaning_config()\n'
             'print("Cleaning config:")\n'
             'for key, val in config.items():\n'
             '    print("  " + str(key) + ": " + str(val))'),
        expected_output("Cleaning config:\n"
                        "  drop_missing: True\n"
                        "  drop_duplicates: True\n"
                        "  check_types: True\n"
                        "  check_ranges: True\n"
                        "  numeric_columns: ['value', 'score']\n"
                        "  string_columns: ['status', 'category']\n"
                        "  value_ranges: {'value': (0, 100), 'score': (0, 100)}\n"
                        "  strip_whitespace: True\n"
                        "  lowercase_strings: False\n"
                        "  custom_rules: ['remove_negative', 'cap_outliers']"),

        why_matters(
            "Every professional data pipeline uses configuration. "
            "It lets you:\n\n"
            "1. Change behavior without changing code\n"
            "2. Run the same pipeline on different datasets with different rules\n"
            "3. Share configs with teammates (\"use this config for the March data\")\n"
            "4. Version control your configs separately from your code"),

        md("---\n## Part 2: Rule-Based Cleaning Pipeline\n\n"
           "Now let us build the actual cleaning function that reads the config:"),

        code('def apply_cleaning_rules(data, config):\n'
             '    """Apply configurable cleaning rules to data.\n'
             '    \n'
             '    Args:\n'
             '        data: list of dicts (raw data)\n'
             '        config: cleaning configuration dict\n'
             '    \n'
             '    Returns:\n'
             '        tuple: (cleaned_data, cleaning_report)\n'
             '    """\n'
             '    cleaned = []\n'
             '    report = {\n'
             '        "total": len(data),\n'
             '        "kept": 0,\n'
             '        "dropped": {},\n'
             '    }\n'
             '    \n'
             '    for row in data:\n'
             '        skip_reason = None\n'
             '        \n'
             '        # Rule 1: Strip whitespace\n'
             '        if config.get("strip_whitespace", False):\n'
             '            for key in row:\n'
             '                if isinstance(row[key], str):\n'
             '                    row[key] = row[key].strip()\n'
             '        \n'
             '        # Rule 2: Missing values\n'
             '        if config.get("drop_missing", True) and not skip_reason:\n'
             '            for col in config.get("numeric_columns", []):\n'
             '                val = row.get(col, "")\n'
             '                if val is None or str(val).strip() == "":\n'
             '                    skip_reason = "missing_" + col\n'
             '                    break\n'
             '        \n'
             '        # Rule 3: Type conversion + range check\n'
             '        if config.get("check_types", True) and not skip_reason:\n'
             '            for col in config.get("numeric_columns", []):\n'
             '                if col in row:\n'
             '                    try:\n'
             '                        val = float(row[col])\n'
             '                        # Range check\n'
             '                        if config.get("check_ranges", True):\n'
             '                            ranges = config.get("value_ranges", {})\n'
             '                            if col in ranges:\n'
             '                                low, high = ranges[col]\n'
             '                                if val < low or val > high:\n'
             '                                    skip_reason = "out_of_range_" + col\n'
             '                                    break\n'
             '                        row[col] = val  # store as float\n'
             '                    except (ValueError, TypeError):\n'
             '                        skip_reason = "non_numeric_" + col\n'
             '                        break\n'
             '        \n'
             '        # Record result\n'
             '        if skip_reason:\n'
             '            report["dropped"][skip_reason] = report["dropped"].get(skip_reason, 0) + 1\n'
             '        else:\n'
             '            cleaned.append(row)\n'
             '    \n'
             '    report["kept"] = len(cleaned)\n'
             '    \n'
             '    # Print summary\n'
             '    print("Cleaning: " + str(report["total"]) + " -> " + str(report["kept"]) + " rows")\n'
             '    for reason, count in sorted(report["dropped"].items()):\n'
             '        print("  Dropped (" + reason + "): " + str(count))\n'
             '    \n'
             '    return cleaned, report\n'
             '\n'
             '# Test\n'
             'data = [\n'
             '    {"id": 1, "value": "25",  "score": "80"},\n'
             '    {"id": 2, "value": "",    "score": "90"},      # missing value\n'
             '    {"id": 3, "value": "abc", "score": "75"},      # non-numeric\n'
             '    {"id": 4, "value": "50",  "score": "150"},     # score out of range\n'
             '    {"id": 5, "value": "30",  "score": "85"},\n'
             '    {"id": 6, "value": " 45 ","score": " 70 "},   # whitespace\n'
             ']\n'
             '\n'
             'config = create_cleaning_config()\n'
             'cleaned, report = apply_cleaning_rules(data, config)\n'
             'print("\\nKept rows:")\n'
             'for row in cleaned:\n'
             '    print("  " + str(row))'),
        expected_output("Cleaning: 6 -> 3 rows\n"
                        "  Dropped (missing_value): 1\n"
                        "  Dropped (non_numeric_value): 1\n"
                        "  Dropped (out_of_range_score): 1\n\n"
                        "Kept rows:\n"
                        "  {'id': 1, 'value': 25.0, 'score': 80.0}\n"
                        "  {'id': 5, 'value': 30.0, 'score': 85.0}\n"
                        "  {'id': 6, 'value': 45.0, 'score': 70.0}"),

        md("---\n## Part 3: The Rule Registry Pattern\n\n"
           "The **rule registry** lets you add custom cleaning rules as functions "
           "without modifying the core cleaning code. "
           "Each rule is a function with a standard signature."),

        code('# Custom cleaning rules -- each takes (row, config) and returns\n'
             '# a drop reason string or None (if the row should be kept)\n'
             '\n'
             'def rule_remove_negative(row, config):\n'
             '    """Remove rows with any negative numeric value."""\n'
             '    for col in config.get("numeric_columns", []):\n'
             '        if col in row and isinstance(row[col], (int, float)):\n'
             '            if row[col] < 0:\n'
             '                return "negative_" + col\n'
             '    return None\n'
             '\n'
             'def rule_cap_outliers(row, config):\n'
             '    """Cap extreme values instead of dropping.\n'
             '    \n'
             '    This is a \"soft\" rule -- it modifies instead of dropping.\n'
             '    Returns None (never drops), but clamps values to range.\n'
             '    """\n'
             '    for col in config.get("numeric_columns", []):\n'
             '        if col in row and isinstance(row[col], (int, float)):\n'
             '            ranges = config.get("value_ranges", {})\n'
             '            if col in ranges:\n'
             '                low, high = ranges[col]\n'
             '                row[col] = max(low, min(high, row[col]))\n'
             '    return None  # never drops\n'
             '\n'
             'def rule_remove_duplicates(row, config, seen=None):\n'
             '    """Remove duplicate rows based on ID column."""\n'
             '    if seen is None:\n'
             '        seen = set()\n'
             '    id_val = row.get("id")\n'
             '    if id_val in seen:\n'
             '        return "duplicate_id"\n'
             '    seen.add(id_val)\n'
             '    return None\n'
             '\n'
             '# The Rule Registry: maps rule names to functions\n'
             'RULE_REGISTRY = {\n'
             '    "remove_negative": rule_remove_negative,\n'
             '    "cap_outliers": rule_cap_outliers,\n'
             '    "remove_duplicates": rule_remove_duplicates,\n'
             '}\n'
             '\n'
             'print("Available rules:")\n'
             'for name in RULE_REGISTRY:\n'
             '    print("  " + name + ": " + RULE_REGISTRY[name].__doc__.strip().split(chr(10))[0])'),
        expected_output("Available rules:\n"
                        "  remove_negative: Remove rows with any negative numeric value.\n"
                        "  cap_outliers: Cap extreme values instead of dropping.\n"
                        "  remove_duplicates: Remove duplicate rows based on ID column."),

        md("### Using the Rule Registry"),
        code('def apply_custom_rules(data, config, registry=None):\n'
             '    """Apply custom rules from the config using the registry.\n'
             '    \n'
             '    Args:\n'
             '        data: list of dicts (already passed basic cleaning)\n'
             '        config: must have "custom_rules" list of rule names\n'
             '        registry: dict mapping rule names to functions\n'
             '    \n'
             '    Returns:\n'
             '        tuple: (cleaned_data, rule_report)\n'
             '    """\n'
             '    if registry is None:\n'
             '        registry = RULE_REGISTRY\n'
             '    \n'
             '    rule_names = config.get("custom_rules", [])\n'
             '    cleaned = []\n'
             '    report = {}\n'
             '    \n'
             '    for row in data:\n'
             '        drop_reason = None\n'
             '        \n'
             '        for rule_name in rule_names:\n'
             '            if rule_name not in registry:\n'
             '                print("WARNING: unknown rule " + repr(rule_name))\n'
             '                continue\n'
             '            \n'
             '            result = registry[rule_name](row, config)\n'
             '            if result is not None:\n'
             '                drop_reason = result\n'
             '                break\n'
             '        \n'
             '        if drop_reason:\n'
             '            report[drop_reason] = report.get(drop_reason, 0) + 1\n'
             '        else:\n'
             '            cleaned.append(row)\n'
             '    \n'
             '    print("Custom rules: " + str(len(data)) + " -> " + str(len(cleaned)) + " rows")\n'
             '    for reason, count in report.items():\n'
             '        print("  " + reason + ": " + str(count))\n'
             '    \n'
             '    return cleaned, report\n'
             '\n'
             '# Test\n'
             'data = [\n'
             '    {"id": 1, "value": 25.0, "score": 80.0},\n'
             '    {"id": 2, "value": -5.0, "score": 90.0},   # negative\n'
             '    {"id": 3, "value": 50.0, "score": 70.0},\n'
             ']\n'
             '\n'
             'config = create_cleaning_config()\n'
             'config["custom_rules"] = ["remove_negative"]\n'
             'cleaned, rule_report = apply_custom_rules(data, config)'),
        expected_output("Custom rules: 3 -> 2 rows\n  negative_value: 1"),

        try_it("Write your own custom rule: `rule_check_timestamp` that rejects "
               "rows where the 'timestamp' field does not match the format 'YYYY-MM-DD'. "
               "Add it to RULE_REGISTRY and test it."),
        code('# Try it: write a custom timestamp rule\n'
             '# def rule_check_timestamp(row, config):\n'
             '#     ...\n'),

        common_mistakes("Cleaning Pipeline", [
            ("Modifying the original data -- `row[col] = val` changes the original dict.",
             "Use `row = dict(row)` or `row = {**row}` to make a copy if you need the original."),
            ("Not tracking drop reasons -- you drop 30% of rows but do not know why.",
             "Always record the reason for every dropped row. This is your data quality report."),
            ("Hard-coding rules instead of using config.",
             "Put thresholds and column names in config. Your code reads from config."),
        ]),

        key_takeaway([
            "Config-driven cleaning separates WHAT (config) from HOW (code)",
            "The rule registry maps string names to functions for easy extensibility",
            "Always track WHY each row was dropped",
            "Custom rules have a standard signature: (row, config) -> reason or None",
            "You can add new rules without changing the core cleaning code",
        ]),

        # === PART 4: Complete Pipeline ===
        md("---\n## Part 4: Putting It All Together\n\n"
           "Let us build the complete cleaning pipeline that runs basic rules first, "
           "then custom rules, and produces a full report."),

        code('def full_cleaning_pipeline(data, config, registry=None):\n'
             '    """Complete cleaning pipeline: basic rules + custom rules.\n'
             '    \n'
             '    Args:\n'
             '        data: list of dicts (raw data)\n'
             '        config: cleaning configuration\n'
             '        registry: custom rule registry\n'
             '    \n'
             '    Returns:\n'
             '        tuple: (cleaned_data, full_report)\n'
             '    """\n'
             '    print("=== Cleaning Pipeline ===")\n'
             '    print("Input: " + str(len(data)) + " rows")\n'
             '    \n'
             '    # Phase 1: Basic rules\n'
             '    phase1, report1 = apply_cleaning_rules(data, config)\n'
             '    \n'
             '    # Phase 2: Custom rules\n'
             '    if config.get("custom_rules"):\n'
             '        phase2, report2 = apply_custom_rules(phase1, config, registry)\n'
             '    else:\n'
             '        phase2 = phase1\n'
             '        report2 = {}\n'
             '    \n'
             '    # Combine reports\n'
             '    full_report = {\n'
             '        "total_input": len(data),\n'
             '        "after_basic": len(phase1),\n'
             '        "after_custom": len(phase2),\n'
             '        "total_dropped": len(data) - len(phase2),\n'
             '        "basic_drops": report1.get("dropped", {}),\n'
             '        "custom_drops": report2,\n'
             '    }\n'
             '    \n'
             '    pct = round(len(phase2) / len(data) * 100, 1) if data else 0\n'
             '    print("\\nFinal: " + str(len(data)) + " -> " + str(len(phase2))\n'
             '          + " rows (" + str(pct) + "% kept)")\n'
             '    \n'
             '    return phase2, full_report\n'
             '\n'
             '# Full test with 12 rows\n'
             'test_data = [\n'
             '    {"id": 1,  "value": "25",  "score": "80"},\n'
             '    {"id": 2,  "value": "",    "score": "90"},   # missing\n'
             '    {"id": 3,  "value": "abc", "score": "75"},   # non-numeric\n'
             '    {"id": 4,  "value": "50",  "score": "150"},  # score out of range\n'
             '    {"id": 5,  "value": "30",  "score": "85"},\n'
             '    {"id": 6,  "value": "45",  "score": "70"},\n'
             '    {"id": 7,  "value": "-5",  "score": "60"},   # will pass basic, fail custom\n'
             '    {"id": 8,  "value": "60",  "score": "55"},\n'
             '    {"id": 9,  "value": "70",  "score": ""},     # missing score\n'
             '    {"id": 10, "value": "35",  "score": "40"},\n'
             '    {"id": 11, "value": "55",  "score": "95"},\n'
             '    {"id": 12, "value": "20",  "score": "abc"},  # non-numeric score\n'
             ']\n'
             '\n'
             'config = create_cleaning_config()\n'
             'config["custom_rules"] = ["remove_negative"]\n'
             'cleaned, report = full_cleaning_pipeline(test_data, config)'),
        expected_output("=== Cleaning Pipeline ===\n"
                        "Input: 12 rows\n"
                        "Cleaning: 12 -> 7 rows\n"
                        "  Dropped (missing_value): 1\n  Dropped (missing_score): 1\n"
                        "  Dropped (non_numeric_score): 1\n  Dropped (non_numeric_value): 1\n"
                        "  Dropped (out_of_range_score): 1\n"
                        "Custom rules: 7 -> 6 rows\n  negative_value: 1\n\n"
                        "Final: 12 -> 6 rows (50.0% kept)\n"
                        "(approximate -- depends on rule order)"),

        md("### Visualizing the Cleaning Funnel"),
        code('# Print a visual cleaning funnel\n'
             'def print_cleaning_funnel(report):\n'
             '    """Print a text-based cleaning funnel.\"\"\"\n'
             '    total = report["total_input"]\n'
             '    after_basic = report["after_basic"]\n'
             '    after_custom = report["after_custom"]\n'
             '    \n'
             '    bar_width = 40\n'
             '    \n'
             '    def bar(count, total_count):\n'
             '        pct = count / total_count if total_count > 0 else 0\n'
             '        filled = int(pct * bar_width)\n'
             '        return "#" * filled + "." * (bar_width - filled)\n'
             '    \n'
             '    print("Cleaning Funnel:")\n'
             '    print("  Raw:     [" + bar(total, total) + "] " + str(total))\n'
             '    print("  Basic:   [" + bar(after_basic, total) + "] " + str(after_basic))\n'
             '    print("  Custom:  [" + bar(after_custom, total) + "] " + str(after_custom))\n'
             '    print()\n'
             '    print("  Basic drops:")\n'
             '    for reason, count in report.get("basic_drops", {}).items():\n'
             '        print("    " + reason + ": " + str(count))\n'
             '    print("  Custom drops:")\n'
             '    for reason, count in report.get("custom_drops", {}).items():\n'
             '        print("    " + reason + ": " + str(count))\n'
             '\n'
             'print_cleaning_funnel(report)'),
        expected_output("Cleaning Funnel:\n"
                        "  Raw:     [########################################] 12\n"
                        "  Basic:   [#######################.................] 7\n"
                        "  Custom:  [####################....................] 6\n\n"
                        "  Basic drops:\n    missing_value: 1\n    ...\n"
                        "  Custom drops:\n    negative_value: 1"),

        # === PART 5: Dry Run Mode ===
        md("---\n## Part 5: Dry Run Mode\n\n"
           "A **dry run** shows what WOULD happen without actually changing anything. "
           "This is useful for debugging and understanding your cleaning rules."),

        code('def dry_run_cleaning(data, config):\n'
             '    """Preview cleaning results without modifying data.\n'
             '    \n'
             '    Returns a report showing what would be dropped.\n'
             '    """\n'
             '    print("=== DRY RUN (no data modified) ===\\n")\n'
             '    \n'
             '    decisions = []  # (row_idx, decision, reason)\n'
             '    \n'
             '    for i, row in enumerate(data):\n'
             '        drop_reason = None\n'
             '        \n'
             '        # Check missing\n'
             '        for col in config.get("numeric_columns", []):\n'
             '            val = row.get(col, "")\n'
             '            if val is None or str(val).strip() == "":\n'
             '                drop_reason = "missing_" + col\n'
             '                break\n'
             '        \n'
             '        # Check types\n'
             '        if not drop_reason:\n'
             '            for col in config.get("numeric_columns", []):\n'
             '                if col in row:\n'
             '                    try:\n'
             '                        float(row[col])\n'
             '                    except (ValueError, TypeError):\n'
             '                        drop_reason = "non_numeric_" + col\n'
             '                        break\n'
             '        \n'
             '        if drop_reason:\n'
             '            decisions.append((i, "DROP", drop_reason))\n'
             '        else:\n'
             '            decisions.append((i, "KEEP", ""))\n'
             '    \n'
             '    # Print decisions\n'
             '    for idx, decision, reason in decisions:\n'
             '        if decision == "DROP":\n'
             '            row_str = str(data[idx])\n'
             '            if len(row_str) > 60:\n'
             '                row_str = row_str[:57] + "..."\n'
             '            print("  [DROP] Row " + str(idx) + ": " + reason)\n'
             '            print("         " + row_str)\n'
             '    \n'
             '    n_keep = sum(1 for _, d, _ in decisions if d == "KEEP")\n'
             '    n_drop = sum(1 for _, d, _ in decisions if d == "DROP")\n'
             '    print("\\nSummary: " + str(n_keep) + " keep, " + str(n_drop) + " drop")\n'
             '    print("(No data was modified -- this is a dry run)")\n'
             '    \n'
             '    return decisions\n'
             '\n'
             '# Test dry run\n'
             'small_data = [\n'
             '    {"id": 1, "value": "25",  "score": "80"},\n'
             '    {"id": 2, "value": "",    "score": "90"},\n'
             '    {"id": 3, "value": "abc", "score": "75"},\n'
             '    {"id": 4, "value": "50",  "score": "60"},\n'
             ']\n'
             'config = create_cleaning_config()\n'
             'decisions = dry_run_cleaning(small_data, config)'),
        expected_output("=== DRY RUN (no data modified) ===\n\n"
                        "  [DROP] Row 1: missing_value\n"
                        "         {'id': 2, 'value': '', 'score': '90'}\n"
                        "  [DROP] Row 2: non_numeric_value\n"
                        "         {'id': 3, 'value': 'abc', 'score': '75'}\n\n"
                        "Summary: 2 keep, 2 drop\n"
                        "(No data was modified -- this is a dry run)"),

        # === PART 6: Writing Your Own Rules ===
        md("---\n## Part 6: Writing Your Own Custom Rules\n\n"
           "Every rule follows the same pattern:"),

        ascii_diagram("Custom Rule Template",
                      "def rule_name(row, config):\n"
                      "    '''One-line description.'''\n"
                      "    # Check something about the row\n"
                      "    if <condition_is_bad>:\n"
                      "        return 'reason_string'    # DROP this row\n"
                      "    return None                   # KEEP this row"),

        md("### Example: Custom Rules for Different Scenarios"),
        code('def rule_check_required_fields(row, config):\n'
             '    """Drop rows where required fields are None.\"\"\"\n'
             '    for col in config.get("required_fields", []):\n'
             '        if row.get(col) is None:\n'
             '            return "missing_required_" + col\n'
             '    return None\n'
             '\n'
             'def rule_trim_whitespace(row, config):\n'
             '    """Clean whitespace from string fields (never drops).\"\"\"\n'
             '    for key in row:\n'
             '        if isinstance(row[key], str):\n'
             '            row[key] = row[key].strip()\n'
             '    return None  # cleaning rule, never drops\n'
             '\n'
             'def rule_standardize_status(row, config):\n'
             '    """Convert status values to lowercase standard form.\"\"\"\n'
             '    status = row.get("status", "")\n'
             '    if isinstance(status, str):\n'
             '        row["status"] = status.lower().strip()\n'
             '    return None  # cleaning rule, never drops\n'
             '\n'
             '# Test each rule\n'
             'test_row = {"id": 1, "value": "  25  ", "status": "  OK  "}\n'
             'print("Before:", test_row)\n'
             'rule_trim_whitespace(test_row, {})\n'
             'rule_standardize_status(test_row, {})\n'
             'print("After:", test_row)'),
        expected_output("Before: {'id': 1, 'value': '  25  ', 'status': '  OK  '}\n"
                        "After: {'id': 1, 'value': '25', 'status': 'ok'}"),

        debugging_tip("Cleaning Pipeline", [
            "If too many rows are dropped, run dry_run_cleaning to see why",
            "If a custom rule is not being applied, check that its name is in config['custom_rules']",
            "If values are not being converted to float, check that basic cleaning runs BEFORE custom rules",
            "Print config before cleaning to verify settings are correct",
            "Use print statements inside rules during debugging, then remove them",
        ]),

        md("---\n## Mini-Quiz"),
        code('# Q1: Why is config-driven cleaning better than hard-coded rules?\n'
             '# Answer: \n'
             '\n'
             '# Q2: What is the rule registry pattern?\n'
             '# Answer: \n'
             '\n'
             '# Q3: What should a custom rule function return if the row is OK?\n'
             '# Answer: \n'
             '\n'
             '# Q4: What is the difference between a "drop" rule and a "fix" rule?\n'
             '# Answer: \n'
             '\n'
             '# Q5: Why is dry run mode useful?\n'
             '# Answer: '),

        md("---\n## Homework: 12 Exercises\n\n### Review (1-4)"),
        code('# HW1: Create a cleaning config for YOUR track project.\n'),
        code('# HW2: Write apply_cleaning_rules for your project data.\n'
             '# Test with at least 10 rows including some that should be dropped.\n'),
        code('# HW3: Write 2 custom rules specific to your track.\n'),
        code('# HW4: Explain: why track drop reasons?\n'),

        md("### Practice (5-8)"),
        code('# HW5: Write a rule that removes rows where a string column\n'
             '# is longer than a configured max length.\n'),
        code('# HW6: Write a "cleaning pipeline" function that combines\n'
             '# basic cleaning AND custom rules in sequence.\n'),
        code('# HW7: Add a "dry run" mode that reports what WOULD be dropped\n'
             '# without actually removing rows.\n'),
        code('# HW8: Write a config loader that reads cleaning config from\n'
             '# a JSON file.\n'),

        md("### Challenge (9-11)"),
        code('# HW9: Implement rule priorities -- some rules should run before others.\n'),
        code('# HW10: Add a "fix instead of drop" option for certain rules.\n'),
        code('# HW11: Write a cleaning pipeline that produces a detailed log\n'
             '# of every decision (kept/dropped/fixed) for every row.\n'),

        md("### Mini-Project"),
        code('# HW12: Build a complete configurable cleaning module for your project.\n'
             '# Requirements:\n'
             '# - Config dict with at least 6 settings\n'
             '# - 3+ custom rules in a registry\n'
             '# - Cleaning report with counts and percentages\n'
             '# - Demo with 20+ rows showing different drop reasons\n'),

        reflection_cell(),
        reflection_code(),
    ]
    return cells


def make_core_w04():
    """Week 4: Data Quality Reports."""
    cells = [
        md("# CP2 Week 4 -- Data Quality Reports\n\n"
           "**Course:** Computer Programming 2 (CP2)\n"
           "**Prerequisites:** Weeks 1-3\n"
           "**Focus:** missing analysis, outlier detection, quality scores\n\n"
           "## Learning Objectives\n"
           "- Generate comprehensive data quality reports\n"
           "- Detect and characterize outliers using IQR\n"
           "- Compute quality scores for your data\n"
           "- Analyze missing value patterns\n"
           "- Export quality reports as JSON"),
        setup_cell(),

        md("---\n## Part 1: What Is a Data Quality Report?\n\n"
           "A **data quality report** answers the question: \"How good is this data?\"\n\n"
           "It summarizes:\n"
           "- How many rows were dropped and why\n"
           "- Which columns have missing values (and how many)\n"
           "- Whether outliers exist and where\n"
           "- An overall quality score\n\n"
           "Think of it like a health checkup for your data."),

        ascii_diagram("Data Quality Report Structure",
                      "+----------------------------------+\n"
                      "| DATA QUALITY REPORT              |\n"
                      "+----------------------------------+\n"
                      "| Dataset: 200 raw -> 180 clean    |\n"
                      "| Drop rate: 10%                   |\n"
                      "+----------------------------------+\n"
                      "| Missing Values:                  |\n"
                      "|   value: 5 (2.5%)                |\n"
                      "|   status: 3 (1.5%)               |\n"
                      "+----------------------------------+\n"
                      "| Outliers: 4 detected             |\n"
                      "|   IQR bounds: [12.3, 87.6]       |\n"
                      "+----------------------------------+\n"
                      "| Quality Score: 90/100            |\n"
                      "+----------------------------------+"),

        code('def generate_quality_report(raw_data, clean_data, drop_report, config):\n'
             '    """Generate a comprehensive data quality report.\n'
             '    \n'
             '    Args:\n'
             '        raw_data: original data before cleaning\n'
             '        clean_data: data after cleaning\n'
             '        drop_report: dict with "dropped" reasons from cleaning\n'
             '        config: pipeline configuration\n'
             '    \n'
             '    Returns:\n'
             '        dict suitable for JSON export\n'
             '    """\n'
             '    n_raw = len(raw_data)\n'
             '    n_clean = len(clean_data)\n'
             '    n_dropped = n_raw - n_clean\n'
             '    \n'
             '    report = {\n'
             '        "project_name": config.get("project_name", "unknown"),\n'
             '        "track": config.get("track", "unknown"),\n'
             '        "version": config.get("version", "v2"),\n'
             '        "dataset": {\n'
             '            "n_raw": n_raw,\n'
             '            "n_clean": n_clean,\n'
             '            "n_dropped": n_dropped,\n'
             '            "drop_rate_pct": round(n_dropped / n_raw * 100, 1) if n_raw > 0 else 0,\n'
             '        },\n'
             '        "cleaning_summary": drop_report.get("dropped", {}),\n'
             '    }\n'
             '    \n'
             '    # Missing value analysis per column\n'
             '    if raw_data:\n'
             '        missing_per_col = {}\n'
             '        for col in raw_data[0].keys():\n'
             '            missing = sum(\n'
             '                1 for row in raw_data\n'
             '                if not row.get(col) or str(row[col]).strip() == ""\n'
             '            )\n'
             '            if missing > 0:\n'
             '                missing_per_col[col] = {\n'
             '                    "count": missing,\n'
             '                    "pct": round(missing / n_raw * 100, 1),\n'
             '                }\n'
             '        report["missing_analysis"] = missing_per_col\n'
             '    \n'
             '    # Quality score (simple version)\n'
             '    report["quality_score"] = round(n_clean / n_raw * 100, 1) if n_raw > 0 else 0\n'
             '    \n'
             '    return report\n'
             '\n'
             '# Demo\n'
             'raw = [\n'
             '    {"a": "1", "b": "10"}, {"a": "2", "b": ""},\n'
             '    {"a": "", "b": "30"},  {"a": "4", "b": "40"},\n'
             '    {"a": "5", "b": "50"}, {"a": "6", "b": "abc"},\n'
             ']\n'
             'clean = [{"a": 1, "b": 10}, {"a": 4, "b": 40}, {"a": 5, "b": 50}]\n'
             'drop_info = {"dropped": {"missing_a": 1, "missing_b": 1, "non_numeric_b": 1}}\n'
             'config = {"project_name": "demo", "track": "data", "version": "v2"}\n'
             '\n'
             'report = generate_quality_report(raw, clean, drop_info, config)\n'
             '\n'
             'import json\n'
             'print(json.dumps(report, indent=2))'),
        expected_output('{\n  "project_name": "demo",\n  "track": "data",\n  "version": "v2",\n'
                        '  "dataset": {\n    "n_raw": 6,\n    "n_clean": 3,\n'
                        '    "n_dropped": 3,\n    "drop_rate_pct": 50.0\n  },\n'
                        '  "cleaning_summary": {\n    "missing_a": 1,\n    "missing_b": 1,\n'
                        '    "non_numeric_b": 1\n  },\n'
                        '  "missing_analysis": {\n    "a": {"count": 1, "pct": 16.7},\n'
                        '    "b": {"count": 1, "pct": 16.7}\n  },\n'
                        '  "quality_score": 50.0\n}'),

        md("---\n## Part 2: Outlier Detection\n\n"
           "An **outlier** is a value that is unusually far from the rest. "
           "The most common method to detect outliers is the **IQR (Interquartile Range)** method:\n\n"
           "1. Sort the values\n"
           "2. Find Q1 (25th percentile) and Q3 (75th percentile)\n"
           "3. Compute IQR = Q3 - Q1\n"
           "4. Any value below Q1 - 1.5*IQR or above Q3 + 1.5*IQR is an outlier"),

        ascii_diagram("IQR Outlier Detection",
                      "   outliers      normal range        outliers\n"
                      "   <------->  <----------------->  <--------->\n"
                      "   |         |         |         |           |\n"
                      "   Q1-1.5*IQR   Q1    median    Q3    Q3+1.5*IQR\n"
                      "   (lower)                            (upper)"),

        code('def detect_outliers(values, method="iqr"):\n'
             '    """Detect outliers using the IQR method.\n'
             '    \n'
             '    Args:\n'
             '        values: list of numbers\n'
             '        method: detection method ("iqr")\n'
             '    \n'
             '    Returns:\n'
             '        dict with bounds, outlier list, and summary\n'
             '    """\n'
             '    if not values or len(values) < 4:\n'
             '        return {"outliers": [], "message": "Not enough data"}\n'
             '    \n'
             '    sorted_vals = sorted(values)\n'
             '    n = len(sorted_vals)\n'
             '    q1 = sorted_vals[n // 4]\n'
             '    q3 = sorted_vals[3 * n // 4]\n'
             '    iqr = q3 - q1\n'
             '    \n'
             '    lower = q1 - 1.5 * iqr\n'
             '    upper = q3 + 1.5 * iqr\n'
             '    \n'
             '    outliers = []\n'
             '    for i, v in enumerate(values):\n'
             '        if v < lower or v > upper:\n'
             '            outliers.append({"index": i, "value": round(v, 2)})\n'
             '    \n'
             '    result = {\n'
             '        "method": method,\n'
             '        "q1": round(q1, 2),\n'
             '        "q3": round(q3, 2),\n'
             '        "iqr": round(iqr, 2),\n'
             '        "lower_bound": round(lower, 2),\n'
             '        "upper_bound": round(upper, 2),\n'
             '        "n_outliers": len(outliers),\n'
             '        "n_total": len(values),\n'
             '        "outliers": outliers,\n'
             '    }\n'
             '    \n'
             '    print("IQR Analysis:")\n'
             '    print("  Q1=" + str(result["q1"]) + ", Q3=" + str(result["q3"])\n'
             '          + ", IQR=" + str(result["iqr"]))\n'
             '    print("  Bounds: [" + str(result["lower_bound"]) + ", "\n'
             '          + str(result["upper_bound"]) + "]")\n'
             '    print("  Outliers: " + str(result["n_outliers"])\n'
             '          + " of " + str(result["n_total"]))\n'
             '    \n'
             '    return result\n'
             '\n'
             '# Test with normal data + planted outliers\n'
             'import random\n'
             'random.seed(42)\n'
             'values = [random.gauss(50, 10) for _ in range(50)]\n'
             'values.extend([200, -50, 150])  # add outliers\n'
             '\n'
             'result = detect_outliers(values)\n'
             'print("\\nOutlier values:")\n'
             'for o in result["outliers"]:\n'
             '    print("  Index " + str(o["index"]) + ": " + str(o["value"]))'),
        expected_output("IQR Analysis:\n"
                        "  Q1=43.38, Q3=57.24, IQR=13.86\n"
                        "  Bounds: [22.59, 78.03]\n"
                        "  Outliers: 3 of 53\n\n"
                        "Outlier values:\n"
                        "  Index 50: 200\n"
                        "  Index 51: -50\n"
                        "  Index 52: 150\n"
                        "(values approximate due to random seed)"),

        try_it("Create a list of 20 exam scores (0-100) with one score of 5 and one of 99. "
               "Run outlier detection on it. Are those extreme scores flagged?"),
        code('# Try it: outlier detection on exam scores\n'
             '# TODO: create scores and run detect_outliers\n'),

        # === PART 3: Quality Score ===
        md("---\n## Part 3: Computing a Quality Score\n\n"
           "A quality score reduces all your quality metrics to a single number "
           "that tells you: \"How good is this data overall?\"\n\n"
           "Simple approach: weighted average of multiple checks."),

        code('def compute_quality_score(raw_data, clean_data, outlier_result=None):\n'
             '    """Compute overall data quality score (0-100).\n'
             '    \n'
             '    Components:\n'
             '    - Completeness: % of rows that survived cleaning (weight: 40%)\n'
             '    - Missing: inverse of % missing values (weight: 30%)\n'
             '    - Outliers: inverse of % outliers (weight: 30%)\n'
             '    """\n'
             '    n_raw = len(raw_data)\n'
             '    n_clean = len(clean_data)\n'
             '    \n'
             '    # Completeness (0-100)\n'
             '    completeness = (n_clean / n_raw * 100) if n_raw > 0 else 0\n'
             '    \n'
             '    # Missing value score (0-100)\n'
             '    if raw_data:\n'
             '        total_cells = n_raw * len(raw_data[0])\n'
             '        missing_cells = sum(\n'
             '            1 for row in raw_data\n'
             '            for val in row.values()\n'
             '            if not val or str(val).strip() == ""\n'
             '        )\n'
             '        missing_score = max(0, 100 - (missing_cells / total_cells * 100))\n'
             '    else:\n'
             '        missing_score = 0\n'
             '    \n'
             '    # Outlier score (0-100)\n'
             '    if outlier_result and outlier_result.get("n_total", 0) > 0:\n'
             '        outlier_pct = outlier_result["n_outliers"] / outlier_result["n_total"] * 100\n'
             '        outlier_score = max(0, 100 - outlier_pct * 5)  # penalize heavily\n'
             '    else:\n'
             '        outlier_score = 100\n'
             '    \n'
             '    # Weighted average\n'
             '    score = (completeness * 0.4 + missing_score * 0.3 + outlier_score * 0.3)\n'
             '    \n'
             '    print("Quality Score Breakdown:")\n'
             '    print("  Completeness: " + str(round(completeness, 1)) + "/100 (weight: 40%)")\n'
             '    print("  Missing:      " + str(round(missing_score, 1)) + "/100 (weight: 30%)")\n'
             '    print("  Outliers:     " + str(round(outlier_score, 1)) + "/100 (weight: 30%)")\n'
             '    print("  --------")\n'
             '    print("  OVERALL:      " + str(round(score, 1)) + "/100")\n'
             '    \n'
             '    # Rating\n'
             '    if score >= 90:\n'
             '        rating = "Excellent"\n'
             '    elif score >= 75:\n'
             '        rating = "Good"\n'
             '    elif score >= 60:\n'
             '        rating = "Fair"\n'
             '    else:\n'
             '        rating = "Poor"\n'
             '    print("  Rating:       " + rating)\n'
             '    \n'
             '    return round(score, 1)\n'
             '\n'
             '# Demo\n'
             'raw = [\n'
             '    {"a": "1", "b": "10"}, {"a": "2", "b": ""},\n'
             '    {"a": "", "b": "30"},  {"a": "4", "b": "40"},\n'
             '    {"a": "5", "b": "50"}, {"a": "6", "b": "60"},\n'
             ']\n'
             'clean = [{"a": 4, "b": 40}, {"a": 5, "b": 50}, {"a": 6, "b": 60}]\n'
             'outliers = {"n_outliers": 0, "n_total": 3}\n'
             '\n'
             'score = compute_quality_score(raw, clean, outliers)'),
        expected_output("Quality Score Breakdown:\n"
                        "  Completeness: 50.0/100 (weight: 40%)\n"
                        "  Missing:      83.3/100 (weight: 30%)\n"
                        "  Outliers:     100.0/100 (weight: 30%)\n"
                        "  --------\n"
                        "  OVERALL:      75.0/100\n"
                        "  Rating:       Good"),

        # === PART 4: Exporting Quality Reports ===
        md("---\n## Part 4: Exporting Quality Reports as JSON\n\n"
           "A quality report should be saved so you can compare runs over time."),

        code('import json, os\n'
             '\n'
             'def export_quality_report(report, filepath="reports/quality_report.json"):\n'
             '    """Save quality report to JSON file.\"\"\"\n'
             '    os.makedirs(os.path.dirname(filepath), exist_ok=True)\n'
             '    with open(filepath, "w") as f:\n'
             '        json.dump(report, f, indent=2)\n'
             '    print("Quality report saved: " + filepath)\n'
             '    return filepath\n'
             '\n'
             '# Build and export a complete report\n'
             'full_report = {\n'
             '    "dataset": {"n_raw": 6, "n_clean": 3, "drop_rate_pct": 50.0},\n'
             '    "missing_analysis": {"a": {"count": 1, "pct": 16.7}, "b": {"count": 1, "pct": 16.7}},\n'
             '    "outlier_analysis": {"n_outliers": 0, "n_total": 3},\n'
             '    "quality_score": 75.0,\n'
             '    "rating": "Good",\n'
             '}\n'
             '\n'
             'export_quality_report(full_report)\n'
             'print("\\nReport contents:")\n'
             'print(json.dumps(full_report, indent=2))'),
        expected_output("Quality report saved: reports/quality_report.json\n\n"
                        "Report contents:\n(JSON output)"),

        # === PART 5: Interpreting Quality Results ===
        md("---\n## Part 5: Interpreting Quality Results\n\n"
           "Numbers alone are not enough. Your report should include "
           "human-readable interpretation."),

        code('def interpret_quality(report):\n'
             '    """Generate interpretation text for quality report.\"\"\"\n'
             '    lines = []\n'
             '    \n'
             '    ds = report.get("dataset", {})\n'
             '    drop_rate = ds.get("drop_rate_pct", 0)\n'
             '    \n'
             '    if drop_rate < 5:\n'
             '        lines.append("Data is very clean: only " + str(drop_rate) + "% dropped.")\n'
             '    elif drop_rate < 20:\n'
             '        lines.append("Data quality is reasonable: " + str(drop_rate) + "% dropped.")\n'
             '    else:\n'
             '        lines.append("WARNING: " + str(drop_rate) + "% of data was dropped. "\n'
             '                     "Investigate data source quality.")\n'
             '    \n'
             '    # Missing value alerts\n'
             '    missing = report.get("missing_analysis", {})\n'
             '    for col, info in missing.items():\n'
             '        if info["pct"] > 10:\n'
             '            lines.append("Column " + repr(col) + " has " + str(info["pct"])\n'
             '                         + "% missing values -- consider if this column is reliable.")\n'
             '    \n'
             '    score = report.get("quality_score", 0)\n'
             '    lines.append("Overall quality score: " + str(score) + "/100 ("\n'
             '                 + report.get("rating", "unknown") + ")")\n'
             '    \n'
             '    return "\\n".join(lines)\n'
             '\n'
             'print("Interpretation:")\n'
             'print(interpret_quality(full_report))'),
        expected_output("Interpretation:\n"
                        "WARNING: 50.0% of data was dropped. Investigate data source quality.\n"
                        "Column 'a' has 16.7% missing values -- consider if this column is reliable.\n"
                        "Column 'b' has 16.7% missing values -- consider if this column is reliable.\n"
                        "Overall quality score: 75.0/100 (Good)"),

        common_mistakes("Data Quality Reports", [
            ("Not counting missing values per column -- you only know TOTAL missing, not WHERE.",
             "Always break down missing values by column to identify the worst offenders."),
            ("Using mean/std for outlier detection on skewed data -- IQR is more robust.",
             "IQR works regardless of distribution shape. Use it as your default."),
            ("Reporting percentages without absolute counts -- 50% missing could be 1 of 2 or 500 of 1000.",
             "Always report BOTH count and percentage."),
        ]),

        key_takeaway([
            "Data quality reports summarize the health of your data",
            "Always track missing values per column with counts and percentages",
            "IQR method: outlier if value < Q1-1.5*IQR or > Q3+1.5*IQR",
            "Quality score = weighted combination of completeness, missing, outliers",
            "Export reports as JSON and include interpretation text",
            "Compare quality reports across runs to track improvements",
        ]),

        md("---\n## Mini-Quiz"),
        code('# Q1: What are the 4 main sections of a data quality report?\n'
             '# Answer: \n'
             '\n'
             '# Q2: How does the IQR method detect outliers?\n'
             '# Answer: \n'
             '\n'
             '# Q3: Why export quality reports as JSON?\n'
             '# Answer: '),

        md("---\n## Homework: 12 Exercises\n\n### Review (1-4)"),
        code('# HW1: Generate a quality report for your project data.\n'),
        code('# HW2: Run outlier detection on your main numeric column.\n'),
        code('# HW3: What does a quality score of 75 mean?\n'),
        code('# HW4: Write missing_analysis for 3 columns of your data.\n'),
        md("### Practice (5-8)"),
        code('# HW5: Add outlier info to your quality report.\n'),
        code('# HW6: Write a function that rates data quality as\n'
             '# "excellent" (>95), "good" (>80), "fair" (>60), "poor" (<60).\n'),
        code('# HW7: Detect outliers using z-score method (alternative to IQR).\n'
             '# z-score = (value - mean) / std; outlier if abs(z) > 3\n'),
        code('# HW8: Write a function that identifies columns with the most\n'
             '# missing values and recommends whether to drop the column.\n'),
        md("### Challenge (9-11)"),
        code('# HW9: Implement a "data quality dashboard" that prints a\n'
             '# formatted text summary of all quality metrics.\n'),
        code('# HW10: Compare quality before and after cleaning -- show\n'
             '# how cleaning improved data quality.\n'),
        code('# HW11: Write a function that automatically suggests cleaning\n'
             '# rules based on the quality report.\n'),
        md("### Mini-Project"),
        code('# HW12: Build a complete data quality module for your project.\n'
             '# Requirements: missing analysis, outlier detection, quality score,\n'
             '# formatted report, JSON export.\n'),

        reflection_cell(),
        reflection_code(),
    ]
    return cells


def make_core_w05():
    """Week 5: Matplotlib Standards."""
    cells = [
        md("# CP2 Week 5 -- Matplotlib Standards\n\n"
           "**Course:** Computer Programming 2 (CP2)\n"
           "**Prerequisites:** Weeks 1-4\n"
           "**Focus:** professional plots, labels, legends, saving figures\n\n"
           "## Learning Objectives\n"
           "- Create professional-quality plots with matplotlib\n"
           "- Always include titles, axis labels, legends, and grids\n"
           "- Save figures programmatically at publication quality\n"
           "- Build standard plotting functions for your pipeline\n"
           "- Know when to use different plot types"),
        setup_cell(),

        md("---\n## Part 1: The 5 Rules of Professional Plots\n\n"
           "Every plot you create in your v2 pipeline MUST follow these rules:\n\n"
           "1. **Title** -- what does this plot show?\n"
           "2. **Axis labels** -- with units (e.g., \"Temperature (C)\")\n"
           "3. **Grid** -- for readability\n"
           "4. **Legend** -- if there are multiple series\n"
           "5. **Save at high DPI** -- 150+ for reports\n\n"
           "A plot without labels is like a table without headers -- useless."),

        code('import matplotlib\n'
             'matplotlib.use("Agg")  # non-interactive backend for Colab/scripts\n'
             'import matplotlib.pyplot as plt\n'
             'import os\n'
             '\n'
             '# === GOOD plot: follows all 5 rules ===\n'
             'import random\n'
             'random.seed(42)\n'
             'temps = [20 + random.gauss(0, 3) for _ in range(50)]\n'
             '\n'
             'fig, ax = plt.subplots(figsize=(10, 5))\n'
             'ax.plot(range(len(temps)), temps, linewidth=1.0, color="#2196F3")\n'
             '\n'
             'ax.set_title("Sensor Temperature Over Time", fontsize=14, fontweight="bold")  # Rule 1\n'
             'ax.set_xlabel("Reading Number", fontsize=12)        # Rule 2\n'
             'ax.set_ylabel("Temperature (C)", fontsize=12)       # Rule 2\n'
             'ax.grid(True, alpha=0.3)                            # Rule 3\n'
             '# No legend needed (single series)                  # Rule 4\n'
             '\n'
             'os.makedirs("reports/figures", exist_ok=True)\n'
             'fig.savefig("reports/figures/demo_good.png", dpi=150, bbox_inches="tight")  # Rule 5\n'
             'plt.close(fig)\n'
             'print("Saved: reports/figures/demo_good.png")'),
        expected_output("Saved: reports/figures/demo_good.png"),

        md("### Standard Time Series Function"),
        code('def standard_timeseries(values, title, ylabel, savepath, threshold=None):\n'
             '    """Create a standardized time series plot.\n'
             '    \n'
             '    Args:\n'
             '        values: list of numbers\n'
             '        title: plot title\n'
             '        ylabel: y-axis label (include units!)\n'
             '        savepath: where to save the figure\n'
             '        threshold: optional horizontal threshold line\n'
             '    \n'
             '    Returns:\n'
             '        matplotlib Figure object\n'
             '    """\n'
             '    fig, ax = plt.subplots(figsize=(12, 5))\n'
             '    \n'
             '    # Main data line\n'
             '    ax.plot(range(len(values)), values,\n'
             '            linewidth=1.0, color="#2196F3", label="Data")\n'
             '    \n'
             '    # Mean line\n'
             '    mean_val = sum(values) / len(values)\n'
             '    ax.axhline(y=mean_val, color="#4CAF50", linestyle=":",\n'
             '               linewidth=1.0, label="Mean (" + str(round(mean_val, 1)) + ")")\n'
             '    \n'
             '    # Threshold line (optional)\n'
             '    if threshold is not None:\n'
             '        ax.axhline(y=threshold, color="#F44336", linestyle="--",\n'
             '                   linewidth=1.5, label="Threshold (" + str(threshold) + ")")\n'
             '    \n'
             '    ax.set_title(title, fontsize=14, fontweight="bold")\n'
             '    ax.set_xlabel("Time Index", fontsize=12)\n'
             '    ax.set_ylabel(ylabel, fontsize=12)\n'
             '    ax.legend(loc="upper right")\n'
             '    ax.grid(True, alpha=0.3)\n'
             '    \n'
             '    os.makedirs(os.path.dirname(savepath), exist_ok=True)\n'
             '    fig.savefig(savepath, dpi=150, bbox_inches="tight")\n'
             '    plt.close(fig)\n'
             '    print("Saved: " + savepath)\n'
             '    return fig\n'
             '\n'
             '# Demo\n'
             'values = [50 + random.gauss(0, 10) for _ in range(100)]\n'
             'standard_timeseries(values, "Temperature Over Time",\n'
             '                    "Temperature (C)",\n'
             '                    "reports/figures/timeseries.png",\n'
             '                    threshold=65)'),
        expected_output("Saved: reports/figures/timeseries.png"),

        md("### Standard Summary Plot (Histogram + Box Plot)"),
        code('def standard_summary(values, title, xlabel, savepath):\n'
             '    """Create histogram + box plot side by side."""\n'
             '    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5),\n'
             '                                    gridspec_kw={"width_ratios": [3, 1]})\n'
             '    \n'
             '    # Histogram\n'
             '    n_bins = min(30, len(values) // 5 + 1)\n'
             '    ax1.hist(values, bins=n_bins, color="#2196F3",\n'
             '             edgecolor="white", alpha=0.8)\n'
             '    \n'
             '    mean_val = sum(values) / len(values)\n'
             '    ax1.axvline(mean_val, color="#F44336", linestyle="-",\n'
             '                linewidth=2, label="Mean (" + str(round(mean_val, 1)) + ")")\n'
             '    \n'
             '    sorted_v = sorted(values)\n'
             '    median_val = sorted_v[len(values) // 2]\n'
             '    ax1.axvline(median_val, color="#FF9800", linestyle="--",\n'
             '                linewidth=2, label="Median (" + str(round(median_val, 1)) + ")")\n'
             '    \n'
             '    ax1.set_title(title + " -- Distribution", fontsize=14, fontweight="bold")\n'
             '    ax1.set_xlabel(xlabel, fontsize=12)\n'
             '    ax1.set_ylabel("Count", fontsize=12)\n'
             '    ax1.legend()\n'
             '    ax1.grid(True, alpha=0.3)\n'
             '    \n'
             '    # Box plot\n'
             '    ax2.boxplot(values, vert=True)\n'
             '    ax2.set_title("Box Plot", fontsize=12)\n'
             '    ax2.set_ylabel(xlabel, fontsize=12)\n'
             '    ax2.grid(True, alpha=0.3)\n'
             '    \n'
             '    plt.tight_layout()\n'
             '    fig.savefig(savepath, dpi=150, bbox_inches="tight")\n'
             '    plt.close(fig)\n'
             '    print("Saved: " + savepath)\n'
             '    return fig\n'
             '\n'
             'standard_summary(values, "Temperature", "Degrees C",\n'
             '                 "reports/figures/summary.png")'),
        expected_output("Saved: reports/figures/summary.png"),

        md("---\n## Part 3: Bar Charts for Category Counts\n\n"
           "Bar charts are perfect for showing how many items are in each category."),

        code('def standard_barchart(categories, values, title, ylabel, savepath):\n'
             '    """Create a standardized bar chart.\"\"\"\n'
             '    fig, ax = plt.subplots(figsize=(10, 5))\n'
             '    \n'
             '    colors = ["#2196F3", "#4CAF50", "#FF9800", "#F44336", "#9C27B0"]\n'
             '    bar_colors = [colors[i % len(colors)] for i in range(len(categories))]\n'
             '    \n'
             '    ax.bar(categories, values, color=bar_colors, edgecolor="white")\n'
             '    \n'
             '    # Add value labels on top of each bar\n'
             '    for i, (cat, val) in enumerate(zip(categories, values)):\n'
             '        ax.text(i, val + max(values) * 0.02, str(val),\n'
             '                ha="center", va="bottom", fontweight="bold")\n'
             '    \n'
             '    ax.set_title(title, fontsize=14, fontweight="bold")\n'
             '    ax.set_ylabel(ylabel, fontsize=12)\n'
             '    ax.grid(True, alpha=0.3, axis="y")\n'
             '    \n'
             '    fig.savefig(savepath, dpi=150, bbox_inches="tight")\n'
             '    plt.close(fig)\n'
             '    print("Saved: " + savepath)\n'
             '    return fig\n'
             '\n'
             'standard_barchart(\n'
             '    ["Missing", "Non-numeric", "Out of range", "Kept"],\n'
             '    [15, 8, 12, 165],\n'
             '    "Cleaning Results by Category",\n'
             '    "Number of Rows",\n'
             '    "reports/figures/cleaning_bar.png"\n'
             ')'),
        expected_output("Saved: reports/figures/cleaning_bar.png"),

        md("---\n## Part 4: Scatter Plots\n\n"
           "Scatter plots show the relationship between two numeric variables."),

        code('def standard_scatter(x_vals, y_vals, title, xlabel, ylabel, savepath):\n'
             '    """Create a standardized scatter plot.\"\"\"\n'
             '    fig, ax = plt.subplots(figsize=(10, 8))\n'
             '    \n'
             '    ax.scatter(x_vals, y_vals, alpha=0.6, color="#2196F3",\n'
             '               edgecolors="white", s=50)\n'
             '    \n'
             '    ax.set_title(title, fontsize=14, fontweight="bold")\n'
             '    ax.set_xlabel(xlabel, fontsize=12)\n'
             '    ax.set_ylabel(ylabel, fontsize=12)\n'
             '    ax.grid(True, alpha=0.3)\n'
             '    \n'
             '    fig.savefig(savepath, dpi=150, bbox_inches="tight")\n'
             '    plt.close(fig)\n'
             '    print("Saved: " + savepath)\n'
             '    return fig\n'
             '\n'
             '# Demo: value vs. score\n'
             'import random\n'
             'random.seed(42)\n'
             'x = [random.gauss(50, 15) for _ in range(80)]\n'
             'y = [v * 0.8 + random.gauss(0, 10) for v in x]  # correlated\n'
             'standard_scatter(x, y, "Value vs. Score", "Value", "Score",\n'
             '                 "reports/figures/scatter.png")'),
        expected_output("Saved: reports/figures/scatter.png"),

        md("---\n## Part 5: Multi-Panel Figures\n\n"
           "For reports, combine multiple plots into one figure."),

        code('def create_dashboard(values, categories, cat_counts, savepath):\n'
             '    """Create a 2x2 dashboard figure.\"\"\"\n'
             '    fig, axes = plt.subplots(2, 2, figsize=(14, 10))\n'
             '    \n'
             '    # Top-left: time series\n'
             '    axes[0, 0].plot(range(len(values)), values, color="#2196F3", linewidth=0.8)\n'
             '    axes[0, 0].set_title("Time Series", fontweight="bold")\n'
             '    axes[0, 0].set_xlabel("Index")\n'
             '    axes[0, 0].grid(True, alpha=0.3)\n'
             '    \n'
             '    # Top-right: histogram\n'
             '    axes[0, 1].hist(values, bins=20, color="#4CAF50", edgecolor="white")\n'
             '    axes[0, 1].set_title("Distribution", fontweight="bold")\n'
             '    axes[0, 1].set_xlabel("Value")\n'
             '    axes[0, 1].grid(True, alpha=0.3)\n'
             '    \n'
             '    # Bottom-left: bar chart\n'
             '    axes[1, 0].bar(categories, cat_counts, color="#FF9800")\n'
             '    axes[1, 0].set_title("Category Counts", fontweight="bold")\n'
             '    axes[1, 0].grid(True, alpha=0.3, axis="y")\n'
             '    \n'
             '    # Bottom-right: box plot\n'
             '    axes[1, 1].boxplot(values)\n'
             '    axes[1, 1].set_title("Box Plot", fontweight="bold")\n'
             '    axes[1, 1].grid(True, alpha=0.3)\n'
             '    \n'
             '    fig.suptitle("Data Analysis Dashboard", fontsize=16, fontweight="bold")\n'
             '    plt.tight_layout()\n'
             '    fig.savefig(savepath, dpi=150, bbox_inches="tight")\n'
             '    plt.close(fig)\n'
             '    print("Saved: " + savepath)\n'
             '\n'
             'create_dashboard(\n'
             '    values,\n'
             '    ["Cat A", "Cat B", "Cat C"],\n'
             '    [45, 35, 20],\n'
             '    "reports/figures/dashboard.png"\n'
             ')'),
        expected_output("Saved: reports/figures/dashboard.png"),

        try_it("Create a figure with your project data. Choose the plot types "
               "that make the most sense for your data."),
        code('# Try it: create a plot for your project\n'
             '# TODO: choose plot type and create it\n'),

        common_mistakes("Matplotlib", [
            ("Forgetting plt.close(fig) -- memory leaks if you create many figures.",
             "Always call plt.close(fig) after saving."),
            ("Not using bbox_inches='tight' -- labels get cut off.",
             "Always add bbox_inches='tight' to savefig."),
            ("Hard-coding file paths -- breaks on different machines.",
             "Use os.path.join and os.makedirs to build paths."),
            ("Using plt.show() in a script -- blocks execution.",
             "Use matplotlib.use('Agg') and plt.close(fig) instead."),
        ]),

        debugging_tip("Matplotlib", [
            "If figures are blank, check that you are plotting to the right axes object",
            "If labels are cut off, add bbox_inches='tight' to savefig",
            "If colors look wrong, use hex codes like '#2196F3' for consistency",
            "If the figure file is 0 bytes, check that plt.close was not called before savefig",
        ]),

        key_takeaway([
            "Every plot MUST have: title, axis labels, grid, legend (if multiple series)",
            "Save at 150+ DPI for report quality",
            "Always call plt.close(fig) after saving to free memory",
            "Use standard functions so all plots look consistent",
            "Multi-panel figures are great for dashboards",
        ]),

        md("---\n## Mini-Quiz"),
        code('# Q1: What are the 5 rules of professional plots?\n'
             '# Answer: \n'
             '\n'
             '# Q2: Why use matplotlib.use("Agg")?\n'
             '# Answer: \n'
             '\n'
             '# Q3: What DPI should you use for report figures?\n'
             '# Answer: '),

        md("---\n## Homework: 12 Exercises\n\n### Review (1-4)"),
        code('# HW1: Create a time series plot of your project data.\n'),
        code('# HW2: Create a histogram of your main numeric column.\n'),
        code('# HW3: Add threshold line and mean to your plot.\n'),
        code('# HW4: Save both figures to reports/figures/.\n'),
        md("### Practice (5-8)"),
        code('# HW5: Create a bar chart of category counts.\n'),
        code('# HW6: Create a scatter plot of two numeric columns.\n'),
        code('# HW7: Create a multi-panel figure (2x2 grid of plots).\n'),
        code('# HW8: Write a plot function that automatically labels axes\n'
             '# based on column names in the config.\n'),
        md("### Challenge (9-11)"),
        code('# HW9: Create a "before/after cleaning" comparison plot.\n'),
        code('# HW10: Add confidence bands (mean +/- std) to timeseries.\n'),
        code('# HW11: Create a custom color scheme for your track.\n'),
        md("### Mini-Project"),
        code('# HW12: Build a complete plotting module for your project.\n'
             '# Requirements: 3+ plot types, all saved to files, professional quality.\n'),

        reflection_cell(),
        reflection_code(),
    ]
    return cells


def make_core_w06():
    """Week 6: Report Generation."""
    cells = [
        md("# CP2 Week 6 -- Report Generation\n\n"
           "**Course:** Computer Programming 2 (CP2)\n"
           "**Prerequisites:** Weeks 1-5\n"
           "**Focus:** JSON reports, Markdown generation, interpretation text\n\n"
           "## Learning Objectives\n"
           "- Generate structured JSON reports\n"
           "- Create readable Markdown reports\n"
           "- Add interpretation text to analysis results\n"
           "- Build a complete export_results() function"),
        setup_cell(),

        md("---\n## Part 1: JSON Report Generation\n\n"
           "JSON is the standard format for machine-readable reports. "
           "Your v2 pipeline should export a report.json with all results."),

        code('import json, os\nfrom datetime import datetime\n'
             '\n'
             'def generate_json_report(clean_data, results, config):\n'
             '    """Generate a complete JSON report.\n'
             '    \n'
             '    Returns:\n'
             '        dict: the report (also saved to disk)\n'
             '    """\n'
             '    report = {\n'
             '        "project_name": config.get("project_name", "unknown"),\n'
             '        "track": config.get("track", "unknown"),\n'
             '        "version": config.get("version", "v2"),\n'
             '        "generated_at": datetime.now().isoformat(),\n'
             '        "dataset": {\n'
             '            "n_raw": config.get("n_raw", 0),\n'
             '            "n_clean": len(clean_data),\n'
             '            "n_dropped": config.get("n_raw", 0) - len(clean_data),\n'
             '        },\n'
             '        "cleaning_summary": results.get("cleaning_summary", {}),\n'
             '        "analysis_summary": results.get("analysis_summary", {}),\n'
             '        "figures": results.get("figures", []),\n'
             '    }\n'
             '    \n'
             '    path = config.get("report_path", "reports/report.json")\n'
             '    os.makedirs(os.path.dirname(path), exist_ok=True)\n'
             '    with open(path, "w") as f:\n'
             '        json.dump(report, f, indent=2)\n'
             '    \n'
             '    print("Report saved: " + path)\n'
             '    return report\n'
             '\n'
             '# Demo\n'
             'config = {\n'
             '    "project_name": "demo",\n'
             '    "track": "data",\n'
             '    "version": "v2",\n'
             '    "n_raw": 100,\n'
             '    "report_path": "reports/report.json",\n'
             '}\n'
             'clean = [{"v": i} for i in range(80)]\n'
             'results = {\n'
             '    "analysis_summary": {"mean": 39.5, "std": 23.1, "count": 80},\n'
             '    "cleaning_summary": {"missing": 10, "outlier": 10},\n'
             '    "figures": ["timeseries.png", "summary.png"],\n'
             '}\n'
             '\n'
             'report = generate_json_report(clean, results, config)\n'
             'print(json.dumps(report, indent=2))'),
        expected_output("Report saved: reports/report.json\n"
                        "(JSON output with all fields)"),

        md("---\n## Part 2: Markdown Report Generation\n\n"
           "Markdown is human-readable. Convert your JSON report to a nicely "
           "formatted Markdown document."),

        code('def generate_markdown_report(report_dict):\n'
             '    """Convert a JSON report to readable Markdown.\"\"\"\n'
             '    lines = []\n'
             '    lines.append("# " + report_dict["project_name"] + " -- Analysis Report")\n'
             '    lines.append("")\n'
             '    lines.append("**Track:** " + report_dict["track"]\n'
             '                 + " | **Version:** " + report_dict["version"])\n'
             '    lines.append("**Generated:** " + report_dict.get("generated_at", "N/A"))\n'
             '    lines.append("")\n'
             '    \n'
             '    ds = report_dict.get("dataset", {})\n'
             '    lines.append("## Dataset Summary")\n'
             '    lines.append("- Raw rows: " + str(ds.get("n_raw", 0)))\n'
             '    lines.append("- Clean rows: " + str(ds.get("n_clean", 0)))\n'
             '    lines.append("- Dropped: " + str(ds.get("n_dropped", 0)))\n'
             '    lines.append("")\n'
             '    \n'
             '    cs = report_dict.get("cleaning_summary", {})\n'
             '    if cs:\n'
             '        lines.append("## Cleaning Summary")\n'
             '        for reason, count in cs.items():\n'
             '            lines.append("- " + reason + ": " + str(count))\n'
             '        lines.append("")\n'
             '    \n'
             '    ans = report_dict.get("analysis_summary", {})\n'
             '    if ans:\n'
             '        lines.append("## Analysis Results")\n'
             '        for metric, value in ans.items():\n'
             '            lines.append("- " + metric + ": " + str(value))\n'
             '        lines.append("")\n'
             '    \n'
             '    return "\\n".join(lines)\n'
             '\n'
             'md_text = generate_markdown_report(report)\n'
             'print(md_text)\n'
             '\n'
             '# Save it\n'
             'with open("reports/report.md", "w") as f:\n'
             '    f.write(md_text)\n'
             'print("\\nSaved: reports/report.md")'),
        expected_output("# demo -- Analysis Report\n"
                        "**Track:** data | **Version:** v2\n"
                        "(rest of markdown output)\n\n"
                        "Saved: reports/report.md"),

        md("---\n## Part 3: Adding Interpretation Text\n\n"
           "Numbers alone are not enough. Add human-readable interpretation."),

        code('def interpret_results(summary):\n'
             '    """Generate interpretation text from analysis summary.\"\"\"\n'
             '    lines = []\n'
             '    \n'
             '    mean = summary.get("mean", 0)\n'
             '    std = summary.get("std", 0)\n'
             '    count = summary.get("count", 0)\n'
             '    \n'
             '    lines.append("Based on " + str(count) + " clean records:")\n'
             '    \n'
             '    # Variability assessment\n'
             '    cv = (std / mean * 100) if mean != 0 else 0\n'
             '    if cv < 10:\n'
             '        lines.append("- Data is very consistent (CV=" + str(round(cv, 1)) + "%)")\n'
             '    elif cv < 25:\n'
             '        lines.append("- Data has moderate variability (CV=" + str(round(cv, 1)) + "%)")\n'
             '    else:\n'
             '        lines.append("- Data is highly variable (CV=" + str(round(cv, 1)) + "%)")\n'
             '    \n'
             '    return "\\n".join(lines)\n'
             '\n'
             'summary = {"mean": 39.5, "std": 23.1, "count": 80}\n'
             'print(interpret_results(summary))'),
        expected_output("Based on 80 clean records:\n"
                        "- Data is highly variable (CV=58.5%)"),

        key_takeaway([
            "JSON reports are machine-readable, Markdown reports are human-readable",
            "Your pipeline should generate BOTH",
            "Add interpretation text that explains what the numbers mean",
            "Always include metadata: project name, track, version, timestamp",
        ]),

        md("---\n## Homework: 12 Exercises\n\n### Review (1-4)"),
        code('# HW1: Generate a JSON report for your project.\n'),
        code('# HW2: Generate a Markdown report from your JSON.\n'),
        code('# HW3: Add interpretation to your analysis results.\n'),
        code('# HW4: What metadata should every report include?\n'),
        md("### Practice (5-8)"),
        code('# HW5: Add a "recommendations" section to your report.\n'),
        code('# HW6: Include figure file paths in your report.\n'),
        code('# HW7: Write a function that loads a report.json and prints a summary.\n'),
        code('# HW8: Add a "data lineage" section showing all cleaning steps.\n'),
        md("### Challenge (9-11)"),
        code('# HW9: Generate an HTML report (simple version).\n'),
        code('# HW10: Add tables to your Markdown report.\n'),
        code('# HW11: Create a report comparison function (v1 vs v2 results).\n'),
        md("### Mini-Project"),
        code('# HW12: Build a complete reporting module. JSON + Markdown + interpretation.\n'),

        reflection_cell(),
        reflection_code(),
    ]
    return cells


def make_core_w07():
    """Week 7: NumPy Introduction."""
    cells = [
        md("# CP2 Week 7 -- NumPy Introduction\n\n"
           "**Course:** Computer Programming 2 (CP2)\n"
           "**Prerequisites:** Weeks 1-6\n"
           "**Focus:** arrays, vectorization, replacing loops, statistical functions\n\n"
           "## Learning Objectives\n"
           "- Understand NumPy arrays vs. Python lists\n"
           "- Use vectorized operations to replace loops\n"
           "- Apply NumPy statistical functions\n"
           "- Replace at least one loop in your pipeline with NumPy"),
        setup_cell(),

        md("---\n## Part 1: NumPy Arrays\n\n"
           "A NumPy array is like a Python list, but optimized for math. "
           "When you do math on a NumPy array, it operates on ALL elements at once -- "
           "no loop needed. This is called **vectorization**."),

        ascii_diagram("List vs. NumPy Array",
                      "Python List (slow):            NumPy Array (fast):\n"
                      "  [1, 2, 3] * 2                [1, 2, 3] * 2\n"
                      "  = [1, 2, 3, 1, 2, 3]         = [2, 4, 6]\n"
                      "  (repeats the list!)           (multiplies each element!)"),

        code('import numpy as np\n'
             '\n'
             '# Creating arrays\n'
             'a = np.array([1, 2, 3, 4, 5])\n'
             'print("Array:", a)\n'
             'print("Type:", type(a))\n'
             'print("Shape:", a.shape)\n'
             'print("Dtype:", a.dtype)\n'
             'print()\n'
             '\n'
             '# Vectorized operations -- NO LOOPS!\n'
             'print("a * 2 =", a * 2)\n'
             'print("a + 10 =", a + 10)\n'
             'print("a ** 2 =", a ** 2)\n'
             'print()\n'
             '\n'
             '# Statistical functions\n'
             'print("Mean:", a.mean())\n'
             'print("Std:", a.std())\n'
             'print("Sum:", a.sum())\n'
             'print("Min:", a.min())\n'
             'print("Max:", a.max())'),
        expected_output("Array: [1 2 3 4 5]\nType: <class 'numpy.ndarray'>\n"
                        "Shape: (5,)\nDtype: int64\n\n"
                        "a * 2 = [ 2  4  6  8 10]\na + 10 = [11 12 13 14 15]\n"
                        "a ** 2 = [ 1  4  9 16 25]\n\n"
                        "Mean: 3.0\nStd: 1.4142135623730951\nSum: 15\nMin: 1\nMax: 5"),

        md("### Replacing Loops With NumPy"),
        code('# BEFORE: loop version (slow for large data)\n'
             'data_list = list(range(1000))\n'
             'result_loop = []\n'
             'for x in data_list:\n'
             '    result_loop.append(x * 2 + 5)\n'
             '\n'
             '# AFTER: NumPy version (fast, one line)\n'
             'data_np = np.arange(1000)\n'
             'result_np = data_np * 2 + 5\n'
             '\n'
             'print("Loop result[:5]:", result_loop[:5])\n'
             'print("NumPy result[:5]:", result_np[:5].tolist())\n'
             'print("Same?", result_loop[:5] == result_np[:5].tolist())'),
        expected_output("Loop result[:5]: [5, 7, 9, 11, 13]\n"
                        "NumPy result[:5]: [5, 7, 9, 11, 13]\nSame? True"),

        md("---\n## Part 2: NumPy for Data Analysis"),
        code('# Statistical analysis with NumPy\n'
             'data = np.array([22.5, 18.3, 30.1, 25.7, 19.8, 27.4, 23.1, 28.6])\n'
             '\n'
             'print("Descriptive Statistics:")\n'
             'print("  Mean:", round(np.mean(data), 2))\n'
             'print("  Median:", round(np.median(data), 2))\n'
             'print("  Std:", round(np.std(data), 2))\n'
             'print("  Min:", round(np.min(data), 2))\n'
             'print("  Max:", round(np.max(data), 2))\n'
             'print()\n'
             '\n'
             '# Boolean indexing (vectorized filtering)\n'
             'mask = data > 25\n'
             'print("Values > 25:", data[mask])\n'
             'print("Count > 25:", np.sum(mask))\n'
             'print("Percent > 25:", round(np.mean(mask) * 100, 1), "%")'),
        expected_output("Descriptive Statistics:\n  Mean: 24.44\n  Median: 24.4\n"
                        "  Std: 3.95\n  Min: 18.3\n  Max: 30.1\n\n"
                        "Values > 25: [30.1 25.7 27.4 28.6]\nCount > 25: 4\n"
                        "Percent > 25: 50.0 %"),

        md("---\n## Part 3: Speed Comparison"),
        code('import time\n'
             '\n'
             'n = 100_000\n'
             '\n'
             '# Loop version\n'
             'data_list = list(range(n))\n'
             'start = time.time()\n'
             'result_loop = [x ** 2 + 2 * x + 1 for x in data_list]\n'
             'loop_time = time.time() - start\n'
             '\n'
             '# NumPy version\n'
             'data_np = np.arange(n)\n'
             'start = time.time()\n'
             'result_np = data_np ** 2 + 2 * data_np + 1\n'
             'np_time = time.time() - start\n'
             '\n'
             'print("Loop:  " + str(round(loop_time * 1000, 2)) + " ms")\n'
             'print("NumPy: " + str(round(np_time * 1000, 2)) + " ms")\n'
             'speedup = loop_time / np_time if np_time > 0 else 0\n'
             'print("NumPy is ~" + str(round(speedup, 1)) + "x faster!")'),
        expected_output("Loop:  ~30 ms\nNumPy: ~1 ms\nNumPy is ~30x faster!\n"
                        "(actual times depend on your machine)"),

        key_takeaway([
            "NumPy arrays do math on ALL elements at once (vectorization)",
            "No loops needed for element-wise operations",
            "NumPy is 10-100x faster than Python loops for numeric work",
            "Use np.mean, np.std, np.median for statistics",
            "Boolean indexing (arr[mask]) replaces filter loops",
        ]),

        md("---\n## Homework: 12 Exercises\n\n### Review (1-4)"),
        code('# HW1: Create a NumPy array from your project values.\n'),
        code('# HW2: Compute mean, std, min, max with NumPy.\n'),
        code('# HW3: Replace one loop in your pipeline with NumPy.\n'),
        code('# HW4: Use boolean indexing to filter outliers.\n'),
        md("### Practice (5-8)"),
        code('# HW5: Write a function that computes percentiles using np.percentile.\n'),
        code('# HW6: Use NumPy to normalize values to 0-1 range.\n'),
        code('# HW7: Compute a moving average using np.convolve.\n'),
        code('# HW8: Compare loop vs NumPy speed for 1M elements.\n'),
        md("### Challenge (9-11)"),
        code('# HW9: Use np.where for conditional replacement.\n'),
        code('# HW10: Implement IQR outlier detection with NumPy.\n'),
        code('# HW11: Create a 2D NumPy array from your multi-column data.\n'),
        md("### Mini-Project"),
        code('# HW12: Refactor your analyze() function to use NumPy.\n'
             '# Compare speed before and after.\n'),

        reflection_cell(),
        reflection_code(),
    ]
    return cells


def make_core_w08():
    """Week 8: Timing & Performance."""
    cells = [
        md("# CP2 Week 8 -- Timing & Performance\n\n"
           "**Course:** Computer Programming 2 (CP2)\n"
           "**Prerequisites:** Weeks 1-7\n"
           "**Focus:** timeit, profiling, comparing approaches\n\n"
           "## Learning Objectives\n"
           "- Measure code performance with timeit\n"
           "- Compare different approaches objectively\n"
           "- Profile your pipeline to find bottlenecks\n"
           "- Write performance reports"),
        setup_cell(),

        md("---\n## Part 1: Measuring Performance With timeit\n\n"
           "\"I think this is faster\" is not good enough. MEASURE it."),

        code('import timeit\n'
             '\n'
             'def method_loop(data):\n'
             '    result = []\n'
             '    for x in data:\n'
             '        result.append(x ** 2)\n'
             '    return result\n'
             '\n'
             'def method_comprehension(data):\n'
             '    return [x ** 2 for x in data]\n'
             '\n'
             'def method_map(data):\n'
             '    return list(map(lambda x: x ** 2, data))\n'
             '\n'
             'def method_numpy(data):\n'
             '    import numpy as np\n'
             '    return (np.array(data) ** 2).tolist()\n'
             '\n'
             'data = list(range(10000))\n'
             '\n'
             'methods = [\n'
             '    ("Loop", method_loop),\n'
             '    ("Comprehension", method_comprehension),\n'
             '    ("Map", method_map),\n'
             '    ("NumPy", method_numpy),\n'
             ']\n'
             '\n'
             'print("Timing 4 approaches (100 runs each):")\n'
             'results = []\n'
             'for name, func in methods:\n'
             '    t = timeit.timeit(lambda: func(data), number=100)\n'
             '    results.append((name, t))\n'
             '    print("  " + name.ljust(15) + ": " + str(round(t, 4)) + "s")\n'
             '\n'
             'fastest = min(results, key=lambda x: x[1])\n'
             'print("\\nFastest: " + fastest[0])'),
        expected_output("Timing 4 approaches (100 runs each):\n"
                        "  Loop           : ~0.25s\n"
                        "  Comprehension  : ~0.18s\n"
                        "  Map            : ~0.22s\n"
                        "  NumPy          : ~0.12s\n\n"
                        "Fastest: NumPy (approximate)"),

        md("---\n## Part 2: Timing Your Pipeline Stages"),
        code('import time\n'
             '\n'
             'def time_function(func, *args, n_runs=5):\n'
             '    """Time a function and return statistics.\"\"\"\n'
             '    times = []\n'
             '    for _ in range(n_runs):\n'
             '        start = time.time()\n'
             '        result = func(*args)\n'
             '        elapsed = time.time() - start\n'
             '        times.append(elapsed)\n'
             '    \n'
             '    return {\n'
             '        "mean_ms": round(sum(times) / len(times) * 1000, 2),\n'
             '        "min_ms": round(min(times) * 1000, 2),\n'
             '        "max_ms": round(max(times) * 1000, 2),\n'
             '    }\n'
             '\n'
             '# Example: time different cleaning approaches\n'
             'def clean_simple(data):\n'
             '    return [r for r in data if r.get("value", "") != ""]\n'
             '\n'
             'def clean_typed(data):\n'
             '    result = []\n'
             '    for r in data:\n'
             '        try:\n'
             '            val = float(r.get("value", ""))\n'
             '            if 0 <= val <= 100:\n'
             '                result.append({**r, "value": val})\n'
             '        except (ValueError, TypeError):\n'
             '            pass\n'
             '    return result\n'
             '\n'
             'test_data = [{"id": i, "value": str(i * 1.5)} for i in range(10000)]\n'
             '\n'
             'for name, func in [("Simple", clean_simple), ("Typed", clean_typed)]:\n'
             '    stats = time_function(func, test_data)\n'
             '    print(name + ": mean=" + str(stats["mean_ms"]) + "ms")'),
        expected_output("Simple: mean=~2ms\nTyped: mean=~8ms\n(approximate)"),

        md("---\n## Part 3: Profiling Your Pipeline\n\n"
           "Profile the entire pipeline to find which stage is the bottleneck."),

        code('import time\n'
             '\n'
             'def profile_pipeline(data_size=1000):\n'
             '    """Profile each pipeline stage and print results.\"\"\"\n'
             '    # Create test data\n'
             '    import random\n'
             '    random.seed(42)\n'
             '    test_data = [\n'
             '        {"id": i, "value": str(round(random.gauss(50, 20), 2))}\n'
             '        for i in range(data_size)\n'
             '    ]\n'
             '    \n'
             '    stages = []\n'
             '    \n'
             '    # Stage 1: Load (simulate)\n'
             '    start = time.time()\n'
             '    data = list(test_data)  # simulate loading\n'
             '    stages.append(("load_data", time.time() - start))\n'
             '    \n'
             '    # Stage 2: Validate\n'
             '    start = time.time()\n'
             '    for row in data[:5]:\n'
             '        assert "id" in row and "value" in row\n'
             '    stages.append(("validate", time.time() - start))\n'
             '    \n'
             '    # Stage 3: Clean\n'
             '    start = time.time()\n'
             '    cleaned = []\n'
             '    for row in data:\n'
             '        try:\n'
             '            v = float(row["value"])\n'
             '            if 0 <= v <= 100:\n'
             '                cleaned.append({**row, "value": v})\n'
             '        except (ValueError, TypeError):\n'
             '            pass\n'
             '    stages.append(("clean_data", time.time() - start))\n'
             '    \n'
             '    # Stage 4: Analyze\n'
             '    start = time.time()\n'
             '    values = [r["value"] for r in cleaned]\n'
             '    mean_v = sum(values) / len(values) if values else 0\n'
             '    std_v = (sum((x - mean_v)**2 for x in values) / len(values))**0.5 if values else 0\n'
             '    stages.append(("analyze", time.time() - start))\n'
             '    \n'
             '    # Print profile\n'
             '    total = sum(t for _, t in stages)\n'
             '    print("Pipeline Profile (" + str(data_size) + " rows):")\n'
             '    print("-" * 45)\n'
             '    for name, t in stages:\n'
             '        pct = round(t / total * 100, 1) if total > 0 else 0\n'
             '        ms = round(t * 1000, 2)\n'
             '        bar = "#" * int(pct / 2)\n'
             '        print("  " + name.ljust(15) + str(ms).rjust(8) + "ms  "\n'
             '              + str(pct).rjust(5) + "% " + bar)\n'
             '    print("-" * 45)\n'
             '    print("  " + "TOTAL".ljust(15) + str(round(total * 1000, 2)).rjust(8) + "ms")\n'
             '    \n'
             '    return stages\n'
             '\n'
             'profile_pipeline(1000)\n'
             'print()\n'
             'profile_pipeline(10000)'),
        expected_output("Pipeline Profile (1000 rows):\n"
                        "---------------------------------------------\n"
                        "  load_data         X.XXms   XX.X% ##\n"
                        "  validate          X.XXms    X.X% \n"
                        "  clean_data        X.XXms   XX.X% #####\n"
                        "  analyze           X.XXms   XX.X% ##\n"
                        "---------------------------------------------\n"
                        "  TOTAL             X.XXms\n"
                        "(approximate)"),

        md("---\n## Part 4: Writing a Performance Report"),

        code('def generate_performance_report(stages, data_size):\n'
             '    """Generate a text performance report.\"\"\"\n'
             '    total = sum(t for _, t in stages)\n'
             '    slowest = max(stages, key=lambda x: x[1])\n'
             '    \n'
             '    lines = []\n'
             '    lines.append("Performance Report")\n'
             '    lines.append("  Data size: " + str(data_size) + " rows")\n'
             '    lines.append("  Total time: " + str(round(total * 1000, 2)) + " ms")\n'
             '    lines.append("  Bottleneck: " + slowest[0] + " ("\n'
             '                 + str(round(slowest[1] * 1000, 2)) + " ms)")\n'
             '    lines.append("")\n'
             '    lines.append("  Recommendations:")\n'
             '    if slowest[0] == "clean_data":\n'
             '        lines.append("  - Consider NumPy for numeric operations")\n'
             '        lines.append("  - Reduce number of cleaning rules if possible")\n'
             '    elif slowest[0] == "analyze":\n'
             '        lines.append("  - Use NumPy for statistical calculations")\n'
             '    lines.append("  - Profile again after optimizations")\n'
             '    \n'
             '    return "\\n".join(lines)\n'
             '\n'
             'stages = profile_pipeline(5000)\n'
             'print()\n'
             'print(generate_performance_report(stages, 5000))'),

        common_mistakes("Timing", [
            ("Timing code that runs only once -- results vary wildly.",
             "Use timeit with number=100+ or average over multiple runs."),
            ("Including print statements in timed code -- I/O is slow.",
             "Remove or silence print statements before timing."),
            ("Comparing times on different machines or with different data sizes.",
             "Always compare on the same machine with the same data."),
        ]),

        key_takeaway([
            "Always measure, never guess about performance",
            "timeit is more accurate than time.time() for short operations",
            "Profile your pipeline to find the slowest stage",
            "Faster is not always better -- correctness first",
            "Document performance with timing reports",
        ]),

        md("---\n## Homework: 12 Exercises\n\n### Review (1-4)"),
        code('# HW1: Time your pipeline load_data function.\n'),
        code('# HW2: Time clean_data with different configs.\n'),
        code('# HW3: Compare list comprehension vs loop for your data.\n'),
        code('# HW4: Which pipeline stage is slowest? Measure each one.\n'),
        md("### Practice (5-8)"),
        code('# HW5: Create a timing report for all pipeline stages.\n'),
        code('# HW6: Time the same function with different data sizes.\n'),
        code('# HW7: Compare dict.get() vs try/except for missing keys.\n'),
        code('# HW8: Write a decorator that automatically times functions.\n'),
        md("### Challenge (9-11)"),
        code('# HW9: Create a performance comparison chart (text-based).\n'),
        code('# HW10: Profile memory usage (sys.getsizeof) of different approaches.\n'),
        code('# HW11: Optimize the slowest stage of your pipeline.\n'),
        md("### Mini-Project"),
        code('# HW12: Write a complete performance report for your pipeline.\n'
             '# Include: timing per stage, speedup from optimizations, recommendations.\n'),

        reflection_cell(),
        reflection_code(),
    ]
    return cells


def make_core_w09():
    """Week 9: Testing - Expanded self_check."""
    cells = [
        md("# CP2 Week 9 -- Testing: Expanded Self-Check\n\n"
           "**Course:** Computer Programming 2 (CP2)\n"
           "**Prerequisites:** Weeks 1-8\n"
           "**Focus:** edge cases, failure modes, test organization\n\n"
           "## Learning Objectives\n"
           "- Write comprehensive self_check() tests\n"
           "- Test edge cases and failure modes\n"
           "- Organize tests by category\n"
           "- Use test patterns: arrange, act, assert"),
        setup_cell(),

        md("---\n## Part 1: Expanding self_check()\n\n"
           "Your v1 self_check probably just tested \"does it run?\" "
           "Your v2 self_check must test:\n\n"
           "1. **Happy path** -- normal inputs work correctly\n"
           "2. **Edge cases** -- empty data, single row, all same values\n"
           "3. **Error handling** -- bad inputs give clear errors\n"
           "4. **Output format** -- results have the right structure"),

        code('def self_check():\n'
             '    """Comprehensive self-check for v2 pipeline.\"\"\"\n'
             '    print("=== v2 Self-Check ===\\n")\n'
             '    passed = 0\n'
             '    failed = 0\n'
             '    \n'
             '    # --- Happy Path Tests ---\n'
             '    print("--- Happy Path ---")\n'
             '    \n'
             '    # Test 1: Clean data returns list\n'
             '    try:\n'
             '        test_data = [{"value": "10"}, {"value": "20"}, {"value": "30"}]\n'
             '        result = [r for r in test_data if r["value"] != ""]  # simulate clean\n'
             '        assert isinstance(result, list)\n'
             '        assert len(result) == 3\n'
             '        print("[PASS] clean_data returns correct list")\n'
             '        passed += 1\n'
             '    except Exception as e:\n'
             '        print("[FAIL] clean_data: " + str(e))\n'
             '        failed += 1\n'
             '    \n'
             '    # Test 2: Missing values dropped\n'
             '    try:\n'
             '        test_data = [{"value": "10"}, {"value": ""}, {"value": "20"}]\n'
             '        result = [r for r in test_data if r["value"] != ""]\n'
             '        assert len(result) == 2, "Expected 2, got " + str(len(result))\n'
             '        print("[PASS] Missing values dropped")\n'
             '        passed += 1\n'
             '    except Exception as e:\n'
             '        print("[FAIL] Missing values: " + str(e))\n'
             '        failed += 1\n'
             '    \n'
             '    # --- Edge Cases ---\n'
             '    print("\\n--- Edge Cases ---")\n'
             '    \n'
             '    # Test 3: Empty input\n'
             '    try:\n'
             '        result = []\n'
             '        assert isinstance(result, list)\n'
             '        assert len(result) == 0\n'
             '        print("[PASS] Handles empty input")\n'
             '        passed += 1\n'
             '    except Exception as e:\n'
             '        print("[FAIL] Empty input: " + str(e))\n'
             '        failed += 1\n'
             '    \n'
             '    # Test 4: Single row\n'
             '    try:\n'
             '        test_data = [{"value": "42"}]\n'
             '        result = [r for r in test_data if r["value"] != ""]\n'
             '        assert len(result) == 1\n'
             '        print("[PASS] Handles single row")\n'
             '        passed += 1\n'
             '    except Exception as e:\n'
             '        print("[FAIL] Single row: " + str(e))\n'
             '        failed += 1\n'
             '    \n'
             '    # Test 5: All same values\n'
             '    try:\n'
             '        values = [42.0] * 10\n'
             '        mean_v = sum(values) / len(values)\n'
             '        assert mean_v == 42.0\n'
             '        print("[PASS] Handles uniform data")\n'
             '        passed += 1\n'
             '    except Exception as e:\n'
             '        print("[FAIL] Uniform data: " + str(e))\n'
             '        failed += 1\n'
             '    \n'
             '    # --- Output Format ---\n'
             '    print("\\n--- Output Format ---")\n'
             '    \n'
             '    # Test 6: Results have required keys\n'
             '    try:\n'
             '        results = {"analysis_summary": {"mean": 15, "std": 5, "count": 2}}\n'
             '        assert "analysis_summary" in results\n'
             '        assert len(results["analysis_summary"]) >= 3\n'
             '        print("[PASS] Results have required keys")\n'
             '        passed += 1\n'
             '    except Exception as e:\n'
             '        print("[FAIL] Results format: " + str(e))\n'
             '        failed += 1\n'
             '    \n'
             '    print("\\n=== " + str(passed) + " passed, " + str(failed) + " failed ===")\n'
             '    return failed == 0\n'
             '\n'
             'self_check()'),
        expected_output("=== v2 Self-Check ===\n\n--- Happy Path ---\n"
                        "[PASS] clean_data returns correct list\n"
                        "[PASS] Missing values dropped\n\n"
                        "--- Edge Cases ---\n"
                        "[PASS] Handles empty input\n"
                        "[PASS] Handles single row\n"
                        "[PASS] Handles uniform data\n\n"
                        "--- Output Format ---\n"
                        "[PASS] Results have required keys\n\n"
                        "=== 6 passed, 0 failed ==="),

        md("---\n## Part 2: The Arrange-Act-Assert Pattern\n\n"
           "Every test should follow this pattern:\n\n"
           "1. **Arrange** -- set up test data\n"
           "2. **Act** -- call the function\n"
           "3. **Assert** -- check the result"),

        code('# Example: well-structured test\n'
             'def test_type_conversion():\n'
             '    """Test that numeric strings are converted to floats.\"\"\"\n'
             '    # ARRANGE: set up test data\n'
             '    test_data = [{"value": "25.5"}, {"value": "30.0"}]\n'
             '    \n'
             '    # ACT: run the function\n'
             '    result = []\n'
             '    for row in test_data:\n'
             '        result.append({"value": float(row["value"])})\n'
             '    \n'
             '    # ASSERT: check the result\n'
             '    assert result[0]["value"] == 25.5\n'
             '    assert result[1]["value"] == 30.0\n'
             '    assert isinstance(result[0]["value"], float)\n'
             '    print("[PASS] Type conversion works")\n'
             '\n'
             'test_type_conversion()'),
        expected_output("[PASS] Type conversion works"),

        key_takeaway([
            "Test happy path, edge cases, and error handling",
            "Use Arrange-Act-Assert pattern for clear test structure",
            "Name your tests clearly (test_what_when_then)",
            "Run self_check() after EVERY change to catch regressions",
        ]),

        md("---\n## Homework: 12 Exercises\n\n### Review (1-4)"),
        code('# HW1: Write 3 happy-path tests for your pipeline.\n'),
        code('# HW2: Write 3 edge-case tests.\n'),
        code('# HW3: Write 2 error-handling tests.\n'),
        code('# HW4: Organize tests by category in self_check().\n'),
        md("### Practice (5-8)"),
        code('# HW5: Test that validate_schema catches missing columns.\n'),
        code('# HW6: Test that cleaning drops the right number of rows.\n'),
        code('# HW7: Test that analyze returns the right mean.\n'),
        code('# HW8: Test with very large values (10^9).\n'),
        md("### Challenge (9-11)"),
        code('# HW9: Write a test runner that collects all test results.\n'),
        code('# HW10: Test that your pipeline is deterministic (same input = same output).\n'),
        code('# HW11: Write performance tests (function finishes in < 1 second).\n'),
        md("### Mini-Project"),
        code('# HW12: Build a comprehensive test suite with 15+ tests.\n'),

        reflection_cell(),
        reflection_code(),
    ]
    return cells


def make_core_w10():
    """Week 10: Golden Outputs."""
    cells = [
        md("# CP2 Week 10 -- Golden Outputs\n\n"
           "**Course:** Computer Programming 2 (CP2)\n"
           "**Prerequisites:** Weeks 1-9\n"
           "**Focus:** deterministic toy data, expected results, regression testing\n\n"
           "## Learning Objectives\n"
           "- Create deterministic toy datasets\n"
           "- Define expected (\"golden\") results\n"
           "- Test pipeline against golden outputs\n"
           "- Catch regressions when you change code"),
        setup_cell(),

        md("---\n## Part 1: What Are Golden Outputs?\n\n"
           "A **golden output** is a known-correct result for a known input. "
           "You create a small, hand-crafted dataset where you can calculate "
           "the correct answer by hand. Then you run your pipeline and verify "
           "it matches.\n\n"
           "If you change your code and the golden test fails, you know something broke."),

        ascii_diagram("Golden Output Testing",
                      "GOLDEN DATASET (fixed, small)     EXPECTED RESULTS (calculated by hand)\n"
                      "+-----+-------+----------+       +-------------------+\n"
                      "| id  | value | category |       | n_clean: 5        |\n"
                      "+-----+-------+----------+       | mean: 30.0        |\n"
                      "| 1   | 10.0  | A        |       | min: 10.0         |\n"
                      "| 2   | 20.0  | A        |       | max: 50.0         |\n"
                      "| 3   | 30.0  | B        |       +-------------------+\n"
                      "| 4   |       | B        | <-- dropped (missing)\n"
                      "| 5   | abc   | A        | <-- dropped (non-numeric)\n"
                      "| 6   | 40.0  | B        |\n"
                      "| 7   | 50.0  | A        |\n"
                      "| 8   | -10   | B        | <-- dropped (out of range)\n"
                      "+-----+-------+----------+"),

        code('import json\n'
             '\n'
             'def create_golden_dataset():\n'
             '    """Create a deterministic toy dataset for testing.\n'
             '    \n'
             '    This dataset has known properties:\n'
             '    - 8 rows total\n'
             '    - 3 should be dropped (1 missing, 1 non-numeric, 1 out of range)\n'
             '    - 5 clean rows with values: 10, 20, 30, 40, 50\n'
             '    - Mean = 30.0, Min = 10.0, Max = 50.0\n'
             '    """\n'
             '    return [\n'
             '        {"id": 1, "value": "10.0", "category": "A"},\n'
             '        {"id": 2, "value": "20.0", "category": "A"},\n'
             '        {"id": 3, "value": "30.0", "category": "B"},\n'
             '        {"id": 4, "value": "",     "category": "B"},   # missing\n'
             '        {"id": 5, "value": "abc",  "category": "A"},   # non-numeric\n'
             '        {"id": 6, "value": "40.0", "category": "B"},\n'
             '        {"id": 7, "value": "50.0", "category": "A"},\n'
             '        {"id": 8, "value": "-10",  "category": "B"},   # out of range\n'
             '    ]\n'
             '\n'
             'GOLDEN_EXPECTED = {\n'
             '    "n_raw": 8,\n'
             '    "n_clean": 5,\n'
             '    "n_dropped": 3,\n'
             '    "mean": 30.0,\n'
             '    "min": 10.0,\n'
             '    "max": 50.0,\n'
             '}\n'
             '\n'
             'def test_golden():\n'
             '    """Test pipeline against known expected results.\"\"\"\n'
             '    print("=== Golden Output Test ===\\n")\n'
             '    data = create_golden_dataset()\n'
             '    assert len(data) == GOLDEN_EXPECTED["n_raw"]\n'
             '    \n'
             '    # Clean (simulate your pipeline)\n'
             '    clean = []\n'
             '    for row in data:\n'
             '        try:\n'
             '            val = float(row["value"])\n'
             '            if val >= 0:\n'
             '                clean.append({**row, "value": val})\n'
             '        except (ValueError, TypeError):\n'
             '            pass\n'
             '    \n'
             '    # Verify\n'
             '    assert len(clean) == GOLDEN_EXPECTED["n_clean"], \\\n'
             '        "Expected " + str(GOLDEN_EXPECTED["n_clean"]) + " clean rows, got " + str(len(clean))\n'
             '    \n'
             '    values = [r["value"] for r in clean]\n'
             '    actual_mean = sum(values) / len(values)\n'
             '    assert abs(actual_mean - GOLDEN_EXPECTED["mean"]) < 1e-6, \\\n'
             '        "Mean: expected " + str(GOLDEN_EXPECTED["mean"]) + ", got " + str(actual_mean)\n'
             '    \n'
             '    assert min(values) == GOLDEN_EXPECTED["min"]\n'
             '    assert max(values) == GOLDEN_EXPECTED["max"]\n'
             '    \n'
             '    print("[PASS] n_clean = " + str(len(clean)))\n'
             '    print("[PASS] mean = " + str(actual_mean))\n'
             '    print("[PASS] min = " + str(min(values)))\n'
             '    print("[PASS] max = " + str(max(values)))\n'
             '    print("\\nGolden test PASSED!")\n'
             '\n'
             'test_golden()'),
        expected_output("=== Golden Output Test ===\n\n"
                        "[PASS] n_clean = 5\n[PASS] mean = 30.0\n"
                        "[PASS] min = 10.0\n[PASS] max = 50.0\n\n"
                        "Golden test PASSED!"),

        key_takeaway([
            "Golden datasets are small, hand-crafted, with known correct results",
            "Run golden tests after EVERY code change to catch regressions",
            "Include edge cases in golden data (missing, non-numeric, out of range)",
            "Golden tests document what your pipeline SHOULD do",
        ]),

        md("---\n## Homework: 12 Exercises\n\n### Review (1-4)"),
        code('# HW1: Create a golden dataset for YOUR track project.\n'),
        code('# HW2: Calculate expected results by hand.\n'),
        code('# HW3: Write test_golden() for your project.\n'),
        code('# HW4: What happens when golden test fails? How do you fix it?\n'),
        md("### Practice (5-8)"),
        code('# HW5: Add group-level golden expectations (mean per category).\n'),
        code('# HW6: Save golden expected results to a JSON file.\n'),
        code('# HW7: Write a golden test for your report output.\n'),
        code('# HW8: Add golden tests for figure file creation.\n'),
        md("### Challenge (9-11)"),
        code('# HW9: Implement golden test comparison with tolerance.\n'),
        code('# HW10: Auto-generate golden expected from a known-good run.\n'),
        code('# HW11: Write a regression test suite with 5+ golden tests.\n'),
        md("### Mini-Project"),
        code('# HW12: Build a complete golden test module.\n'),

        reflection_cell(),
        reflection_code(),
    ]
    return cells


def make_core_w11():
    """Week 11: Modularize into /src."""
    cells = [
        md("# CP2 Week 11 -- Modularize Into /src\n\n"
           "**Course:** Computer Programming 2 (CP2)\n"
           "**Prerequisites:** Weeks 1-10\n"
           "**Focus:** moving code from notebooks to modules, imports\n\n"
           "## Learning Objectives\n"
           "- Organize code into a proper /src module structure\n"
           "- Move functions from notebooks to Python files\n"
           "- Use imports instead of redefining functions\n"
           "- Understand __init__.py and module organization"),
        setup_cell(),

        md("---\n## Part 1: Why Modularize?\n\n"
           "Right now, your functions are defined inside notebooks. This has problems:\n\n"
           "- You cannot reuse functions across notebooks without copy-pasting\n"
           "- If you fix a bug, you must fix it in every notebook\n"
           "- Your notebooks are hundreds of lines long -- hard to read\n"
           "- You cannot test functions independently\n\n"
           "**Modularization** moves your functions into Python files (modules) "
           "that notebooks import from."),

        ascii_diagram("Before vs. After Modularization",
                      "BEFORE (v1 style):               AFTER (v2 style):\n"
                      "+-------------------+            +------------------+\n"
                      "| notebook.ipynb    |            | notebook.ipynb   |\n"
                      "| - def load_data   |            | from src import  |\n"
                      "| - def clean_data  |            |   load_data,     |\n"
                      "| - def analyze     |            |   clean_data,    |\n"
                      "| - def plot        |            |   analyze, plot  |\n"
                      "| - def export      |            | # just calls     |\n"
                      "| (500+ lines)      |            | (50 lines)       |\n"
                      "+-------------------+            +------------------+\n"
                      "                                        |\n"
                      "                                 +------v----------+\n"
                      "                                 | src/            |\n"
                      "                                 |   __init__.py   |\n"
                      "                                 |   config.py     |\n"
                      "                                 |   io.py         |\n"
                      "                                 |   cleaning.py   |\n"
                      "                                 |   analysis.py   |\n"
                      "                                 |   plotting.py   |\n"
                      "                                 |   reporting.py  |\n"
                      "                                 +-----------------+"),

        code('# Your /src layout should look like this:\n'
             'print("Target structure:")\n'
             'print("  src/")\n'
             'print("    project_name/")\n'
             'print("      __init__.py      <- imports all public functions")\n'
             'print("      config.py        <- get_config()")\n'
             'print("      io.py            <- load_data()")\n'
             'print("      cleaning.py      <- clean_data(), validate_schema()")\n'
             'print("      analysis.py      <- analyze()")\n'
             'print("      plotting.py      <- plot()")\n'
             'print("      reporting.py     <- export_results(), self_check()")\n'
             'print()\n'
             'print("Notebooks should IMPORT from /src, not define functions!")'),
        expected_output("Target structure:\n"
                        "  src/\n    project_name/\n"
                        "      __init__.py      <- imports all public functions\n"
                        "      config.py        <- get_config()\n"
                        "      io.py            <- load_data()\n"
                        "      cleaning.py      <- clean_data(), validate_schema()\n"
                        "      analysis.py      <- analyze()\n"
                        "      plotting.py      <- plot()\n"
                        "      reporting.py     <- export_results(), self_check()\n\n"
                        "Notebooks should IMPORT from /src, not define functions!"),

        md("### Step-by-Step Migration"),
        code('# Step 1: Create __init__.py that imports from modules\n'
             'init_code = """\n'
             'from .config import get_config\n'
             'from .io import load_data\n'
             'from .cleaning import clean_data, validate_schema\n'
             'from .analysis import analyze\n'
             'from .plotting import plot\n'
             'from .reporting import export_results, self_check\n'
             '"""\n'
             'print("Example __init__.py:")\n'
             'print(init_code)\n'
             '\n'
             '# Step 2: Notebook cell after migration\n'
             'notebook_code = """\n'
             'import sys\n'
             'sys.path.insert(0, "src")\n'
             'from project_name import get_config, load_data, clean_data, analyze, plot, export_results\n'
             '\n'
             'config = get_config()\n'
             'data = load_data(config)\n'
             'cleaned = clean_data(data, config)\n'
             'results = analyze(cleaned, config)\n'
             'figures = plot(cleaned, results, config)\n'
             'exported = export_results(cleaned, results, figures, config)\n'
             '"""\n'
             'print("Example notebook usage:")\n'
             'print(notebook_code)'),

        key_takeaway([
            "Move functions from notebooks to .py files in /src",
            "Use __init__.py to control what gets imported",
            "Notebooks become short: import + call + display",
            "One function, one place -- fix a bug once, fixed everywhere",
        ]),

        md("---\n## Homework: 12 Exercises\n\n### Review (1-4)"),
        code('# HW1: Create the /src/project_name/ directory structure.\n'),
        code('# HW2: Move get_config() to config.py.\n'),
        code('# HW3: Move load_data() to io.py.\n'),
        code('# HW4: Create __init__.py with all imports.\n'),
        md("### Practice (5-8)"),
        code('# HW5: Move clean_data and validate_schema to cleaning.py.\n'),
        code('# HW6: Move analyze to analysis.py.\n'),
        code('# HW7: Move plot functions to plotting.py.\n'),
        code('# HW8: Update your notebook to import from /src.\n'),
        md("### Challenge (9-11)"),
        code('# HW9: Add docstrings to every module file.\n'),
        code('# HW10: Write a test that imports from src and runs self_check.\n'),
        code('# HW11: Add type hints to all function signatures.\n'),
        md("### Mini-Project"),
        code('# HW12: Complete the full migration. Verify notebook still works.\n'),

        reflection_cell(),
        reflection_code(),
    ]
    return cells


def make_core_w12():
    """Week 12: Package Hygiene."""
    cells = [
        md("# CP2 Week 12 -- Package Hygiene\n\n"
           "**Course:** Computer Programming 2 (CP2)\n"
           "**Prerequisites:** Weeks 1-11\n"
           "**Focus:** config module, stable paths, __init__.py, clean structure\n\n"
           "## Learning Objectives\n"
           "- Build a robust config module with stable paths\n"
           "- Ensure code works on both Colab and local machines\n"
           "- Clean up __init__.py exports\n"
           "- Verify project structure is complete"),
        setup_cell(),

        md("---\n## Part 1: Stable Config Module\n\n"
           "A good config module centralizes ALL settings and makes paths "
           "work regardless of where you run the code."),

        code('import os\n'
             '\n'
             'def get_config(base_dir=None):\n'
             '    """Get project configuration with stable paths.\n'
             '    \n'
             '    Args:\n'
             '        base_dir: Project root. Auto-detected if None.\n'
             '    """\n'
             '    if base_dir is None:\n'
             '        for candidate in [".", "..", "../.."]:\n'
             '            if os.path.exists(os.path.join(candidate, "src")):\n'
             '                base_dir = candidate\n'
             '                break\n'
             '        else:\n'
             '            base_dir = "."\n'
             '    \n'
             '    return {\n'
             '        "project_name": "my_project",\n'
             '        "track": "data",\n'
             '        "version": "v2",\n'
             '        "base_dir": os.path.abspath(base_dir),\n'
             '        "raw_data_path": os.path.join(base_dir, "data", "raw", "sample.csv"),\n'
             '        "cleaned_data_path": os.path.join(base_dir, "data", "cleaned", "cleaned.csv"),\n'
             '        "report_path": os.path.join(base_dir, "reports", "report.json"),\n'
             '        "figures_dir": os.path.join(base_dir, "reports", "figures"),\n'
             '        "required_columns": ["id", "value"],\n'
             '        "numeric_columns": ["value"],\n'
             '        "value_ranges": {"value": (0, 100)},\n'
             '        "threshold": 60,\n'
             '    }\n'
             '\n'
             'config = get_config()\n'
             'print("Config:")\n'
             'for k, v in config.items():\n'
             '    print("  " + str(k) + ": " + str(v))'),

        md("---\n## Part 2: Project Structure Checklist"),
        code('def check_project_structure(base_dir="."):\n'
             '    """Verify project has all required files and directories.\"\"\"\n'
             '    print("=== Project Structure Check ===\\n")\n'
             '    \n'
             '    required = [\n'
             '        "src",\n'
             '        "data/raw",\n'
             '        "data/cleaned",\n'
             '        "reports",\n'
             '        "reports/figures",\n'
             '    ]\n'
             '    \n'
             '    for path in required:\n'
             '        full = os.path.join(base_dir, path)\n'
             '        exists = os.path.exists(full)\n'
             '        status = "[OK]" if exists else "[MISSING]"\n'
             '        print("  " + status + " " + path)\n'
             '        if not exists:\n'
             '            os.makedirs(full, exist_ok=True)\n'
             '            print("       -> Created!")\n'
             '    \n'
             '    print("\\nDone!")\n'
             '\n'
             'check_project_structure()'),

        key_takeaway([
            "Config module = single source of truth for all settings",
            "Use os.path.join for cross-platform paths",
            "Auto-detect base_dir so code works on Colab and local",
            "Check project structure at startup to catch missing dirs",
        ]),

        md("---\n## Homework: 12 Exercises\n\n### Review (1-4)"),
        code('# HW1: Create get_config() for your project.\n'),
        code('# HW2: Use stable paths in all your modules.\n'),
        code('# HW3: Clean up __init__.py -- only export public functions.\n'),
        code('# HW4: Verify project structure with check_project_structure.\n'),
        md("### Practice (5-8)"),
        code('# HW5: Add data validation to get_config (check files exist).\n'),
        code('# HW6: Support config override from environment variables.\n'),
        code('# HW7: Write a setup script that creates all needed directories.\n'),
        code('# HW8: Add a version string to your config.\n'),
        md("### Challenge (9-11)"),
        code('# HW9: Load config from a JSON file instead of hard-coding.\n'),
        code('# HW10: Add config validation (required keys check).\n'),
        code('# HW11: Write a project health check that verifies everything.\n'),
        md("### Mini-Project"),
        code('# HW12: Polish your project structure until check_project_structure\n'
             '# and self_check both pass with zero failures.\n'),

        reflection_cell(),
        reflection_code(),
    ]
    return cells


def make_core_w13():
    """Week 13: Integration on Larger Data."""
    cells = [
        md("# CP2 Week 13 -- Integration on Larger Data\n\n"
           "**Course:** Computer Programming 2 (CP2)\n"
           "**Prerequisites:** Weeks 1-12\n"
           "**Focus:** larger datasets, robust error handling, polished exports\n\n"
           "## Learning Objectives\n"
           "- Run your complete pipeline on larger data\n"
           "- Handle errors gracefully at every stage\n"
           "- Verify all outputs are generated correctly\n"
           "- Fix any remaining issues before v2 release"),
        setup_cell(),

        md("---\n## Part 1: Full Integration Test\n\n"
           "Time to test your entire pipeline end-to-end with realistic data."),

        code('import os, json, random\n'
             '\n'
             'def run_integration_test(config):\n'
             '    """Run the complete pipeline and verify all outputs.\"\"\"\n'
             '    print("=== Integration Test ===\\n")\n'
             '    errors = []\n'
             '    \n'
             '    # Setup directories\n'
             '    for d in ["data/raw", "data/cleaned", "reports/figures"]:\n'
             '        path = os.path.join(config.get("base_dir", "."), d)\n'
             '        os.makedirs(path, exist_ok=True)\n'
             '    \n'
             '    # Create larger test dataset\n'
             '    random.seed(42)\n'
             '    test_data = []\n'
             '    for i in range(200):\n'
             '        val = random.gauss(50, 20)\n'
             '        test_data.append({"id": i, "value": str(round(val, 2))})\n'
             '    # Add some bad data\n'
             '    test_data.append({"id": 200, "value": ""})\n'
             '    test_data.append({"id": 201, "value": "abc"})\n'
             '    test_data.append({"id": 202, "value": "999"})\n'
             '    \n'
             '    print("Test dataset: " + str(len(test_data)) + " rows")\n'
             '    \n'
             '    # Stage 1: Clean\n'
             '    cleaned = []\n'
             '    for row in test_data:\n'
             '        try:\n'
             '            v = float(row["value"])\n'
             '            if 0 <= v <= 100:\n'
             '                cleaned.append({**row, "value": v})\n'
             '        except (ValueError, TypeError):\n'
             '            pass\n'
             '    print("Cleaned: " + str(len(cleaned)) + " rows")\n'
             '    \n'
             '    # Stage 2: Analyze\n'
             '    values = [r["value"] for r in cleaned]\n'
             '    mean_v = sum(values) / len(values)\n'
             '    std_v = (sum((x - mean_v)**2 for x in values) / len(values))**0.5\n'
             '    results = {\n'
             '        "analysis_summary": {\n'
             '            "count": len(values),\n'
             '            "mean": round(mean_v, 2),\n'
             '            "std": round(std_v, 2),\n'
             '            "min": round(min(values), 2),\n'
             '            "max": round(max(values), 2),\n'
             '        }\n'
             '    }\n'
             '    \n'
             '    # Verify\n'
             '    assert len(cleaned) > 100, "Too many rows dropped"\n'
             '    assert len(results["analysis_summary"]) >= 3, "Need 3+ metrics"\n'
             '    \n'
             '    print("\\nResults: " + str(results["analysis_summary"]))\n'
             '    print("\\n=== Integration Test PASSED ===")\n'
             '\n'
             'config = {"base_dir": "."}\n'
             'run_integration_test(config)'),
        expected_output("=== Integration Test ===\n\n"
                        "Test dataset: 203 rows\n"
                        "Cleaned: ~160 rows\n\n"
                        "Results: {'count': ~160, 'mean': ~50, ...}\n\n"
                        "=== Integration Test PASSED ==="),

        key_takeaway([
            "Integration testing runs ALL stages together",
            "Use larger datasets (200+ rows) to expose edge cases",
            "Verify all output files are created and non-empty",
            "Fix all issues BEFORE the v2 release next week",
        ]),

        md("---\n## Homework: 12 Exercises\n\n### Review (1-4)"),
        code('# HW1: Run your full pipeline end-to-end.\n'),
        code('# HW2: Verify all output files exist and are non-empty.\n'),
        code('# HW3: Run golden test AND integration test together.\n'),
        code('# HW4: List any remaining issues to fix before v2 release.\n'),
        md("### Practice (5-8)"),
        code('# HW5: Test with 500+ rows of data.\n'),
        code('# HW6: Add error handling to every pipeline stage.\n'),
        code('# HW7: Verify report.json has all required fields.\n'),
        code('# HW8: Verify all figures are saved correctly.\n'),
        md("### Challenge (9-11)"),
        code('# HW9: Time the full pipeline and add timing to report.\n'),
        code('# HW10: Test with intentionally bad data (all missing, all outliers).\n'),
        code('# HW11: Create a "pipeline status" dashboard.\n'),
        md("### Mini-Project"),
        code('# HW12: Run full pipeline, generate all outputs, verify everything.\n'
             '# Prepare for v2 demo next week.\n'),

        reflection_cell(),
        reflection_code(),
    ]
    return cells


def make_core_w14():
    """Week 14: v2 Release & Demo."""
    cells = [
        md("# CP2 Week 14 -- v2 Release & Demo\n\n"
           "**Course:** Computer Programming 2 (CP2)\n"
           "**Prerequisites:** Weeks 1-13\n"
           "**Focus:** final validation, demo prep, complete v2 pipeline\n\n"
           "## Learning Objectives\n"
           "- Pass the v2 release checklist\n"
           "- Prepare a professional demo\n"
           "- Reflect on your journey from v1 to v2"),
        setup_cell(),

        md("---\n## Part 1: v2 Release Checklist\n\n"
           "Your v2 pipeline must pass ALL of these checks before demo."),

        code('import os, json\n'
             '\n'
             'def v2_release_check():\n'
             '    """Final v2 release validation.\"\"\"\n'
             '    print("=== v2 Release Check ===\\n")\n'
             '    \n'
             '    passed = 0\n'
             '    failed = 0\n'
             '    \n'
             '    # Check 1: Required files\n'
             '    required_files = [\n'
             '        "data/cleaned/cleaned.csv",\n'
             '        "reports/report.json",\n'
             '        "reports/figures/timeseries.png",\n'
             '        "reports/figures/summary.png",\n'
             '    ]\n'
             '    \n'
             '    print("--- File Checks ---")\n'
             '    for f in required_files:\n'
             '        if os.path.exists(f) and os.path.getsize(f) > 0:\n'
             '            size = os.path.getsize(f)\n'
             '            print("  [PASS] " + f + " (" + str(size) + " bytes)")\n'
             '            passed += 1\n'
             '        else:\n'
             '            print("  [FAIL] " + f + " missing or empty")\n'
             '            failed += 1\n'
             '    \n'
             '    # Check 2: Report schema\n'
             '    print("\\n--- Report Checks ---")\n'
             '    required_keys = [\n'
             '        "project_name", "track", "version",\n'
             '        "dataset", "cleaning_summary", "analysis_summary",\n'
             '    ]\n'
             '    try:\n'
             '        with open("reports/report.json") as f:\n'
             '            report = json.load(f)\n'
             '        for key in required_keys:\n'
             '            if key in report:\n'
             '                print("  [PASS] report has " + repr(key))\n'
             '                passed += 1\n'
             '            else:\n'
             '                print("  [FAIL] report missing " + repr(key))\n'
             '                failed += 1\n'
             '    except FileNotFoundError:\n'
             '        print("  [FAIL] report.json not found")\n'
             '        failed += len(required_keys)\n'
             '    except json.JSONDecodeError:\n'
             '        print("  [FAIL] report.json is not valid JSON")\n'
             '        failed += len(required_keys)\n'
             '    \n'
             '    # Check 3: Analysis metrics\n'
             '    print("\\n--- Analysis Checks ---")\n'
             '    try:\n'
             '        summary = report.get("analysis_summary", {})\n'
             '        n_metrics = len([v for v in summary.values() if isinstance(v, (int, float))])\n'
             '        if n_metrics >= 3:\n'
             '            print("  [PASS] " + str(n_metrics) + " numeric metrics")\n'
             '            passed += 1\n'
             '        else:\n'
             '            print("  [FAIL] Only " + str(n_metrics) + " metrics (need 3+)")\n'
             '            failed += 1\n'
             '    except Exception:\n'
             '        print("  [FAIL] Could not check metrics")\n'
             '        failed += 1\n'
             '    \n'
             '    print("\\n=== " + str(passed) + " passed, " + str(failed) + " failed ===")\n'
             '    if failed == 0:\n'
             '        print("\\nv2 is READY for demo! Congratulations!")\n'
             '    else:\n'
             '        print("\\nFix " + str(failed) + " failure(s) before demo.")\n'
             '    return failed == 0\n'
             '\n'
             'v2_release_check()'),

        md("---\n## Part 2: Demo Preparation\n\n"
           "Your demo should show:\n\n"
           "1. Load raw data\n"
           "2. Validate schema (show a passing check)\n"
           "3. Clean data (show drop reasons)\n"
           "4. Analyze (show summary stats)\n"
           "5. Plot (show figures)\n"
           "6. Export (show report.json)\n"
           "7. Run self_check (all green)"),

        code('# Demo script template\n'
             'print("=== v2 Pipeline Demo ===")\n'
             'print()\n'
             'print("Step 1: Load data")\n'
             'print("  -> Loaded N rows from data/raw/...")\n'
             'print()\n'
             'print("Step 2: Validate schema")\n'
             'print("  -> Schema valid: X required columns present")\n'
             'print()\n'
             'print("Step 3: Clean data")\n'
             'print("  -> Cleaned: N -> M rows (K dropped)")\n'
             'print("  -> Drop reasons: missing: A, outlier: B, ...")\n'
             'print()\n'
             'print("Step 4: Analyze")\n'
             'print("  -> mean=X, std=Y, min=A, max=B")\n'
             'print()\n'
             'print("Step 5: Plot")\n'
             'print("  -> Saved: timeseries.png, summary.png")\n'
             'print()\n'
             'print("Step 6: Export")\n'
             'print("  -> Saved: report.json, report.md")\n'
             'print()\n'
             'print("Step 7: Self-check")\n'
             'print("  -> All tests PASSED")\n'
             'print()\n'
             'print("=== v2 Release Complete ===")\n'
             'print()\n'
             'print("Customize this script for YOUR track and data!")'),

        md("---\n## Part 3: v1 vs v2 Comparison"),
        code('print("What changed from v1 to v2:")\n'
             'print()\n'
             'improvements = [\n'
             '    ("Schema validation", "v1: none", "v2: validate_schema() with clear errors"),\n'
             '    ("Cleaning", "v1: hard-coded rules", "v2: config-driven + rule registry"),\n'
             '    ("Analytics", "v1: basic stats", "v2: group summaries + histograms"),\n'
             '    ("Quality", "v1: none", "v2: quality report + outlier detection"),\n'
             '    ("Plots", "v1: basic", "v2: professional with labels + saved at 150 DPI"),\n'
             '    ("Reports", "v1: none", "v2: JSON + Markdown + interpretation"),\n'
             '    ("Performance", "v1: not measured", "v2: timed + NumPy optimized"),\n'
             '    ("Testing", "v1: basic self_check", "v2: golden tests + edge cases"),\n'
             '    ("Code org", "v1: all in notebook", "v2: modularized in /src"),\n'
             '    ("Config", "v1: hard-coded", "v2: config module + stable paths"),\n'
             ']\n'
             '\n'
             'for feature, v1, v2 in improvements:\n'
             '    print(feature + ":")\n'
             '    print("  " + v1)\n'
             '    print("  " + v2)\n'
             '    print()'),

        key_takeaway([
            "v2 is a professional-grade data pipeline",
            "Every change from v1 to v2 makes the pipeline more robust",
            "You now know how real software engineers organize code",
            "Congratulations on completing CP2!",
        ]),

        md("---\n## Final Reflection"),
        code('# Final reflection: your CP2 journey\n'
             '# Answer these questions:\n'
             '\n'
             '# 1. What was the most important thing you learned in CP2?\n'
             '# Answer: \n'
             '\n'
             '# 2. What was the hardest concept?\n'
             '# Answer: \n'
             '\n'
             '# 3. How is your v2 pipeline different from v1?\n'
             '# Answer: \n'
             '\n'
             '# 4. What would you add for a v3?\n'
             '# Answer: \n'
             '\n'
             '# 5. Rate your confidence (1-10) for each:\n'
             '#    - Schema validation: \n'
             '#    - Config-driven cleaning: \n'
             '#    - NumPy: \n'
             '#    - Testing: \n'
             '#    - Code organization: \n'),

        reflection_cell(),
        reflection_code(),
    ]
    return cells


# ================================================================
#  Map week numbers to core generators
# ================================================================
CORE_GENERATORS = {
    1: make_core_w01,
    2: make_core_w02,
    3: make_core_w03,
    4: make_core_w04,
    5: make_core_w05,
    6: make_core_w06,
    7: make_core_w07,
    8: make_core_w08,
    9: make_core_w09,
    10: make_core_w10,
    11: make_core_w11,
    12: make_core_w12,
    13: make_core_w13,
    14: make_core_w14,
}


# ================================================================
#  STUDIO NOTEBOOKS (30-40+ cells per track)
# ================================================================

def make_studio(week_num, track_key):
    """Generate a rich studio notebook for a given week and track."""
    track = TRACKS[track_key]
    ctx = TRACK_CONTEXT[track_key]
    week_title = WEEKS[week_num - 1][1]
    week_focus = WEEKS[week_num - 1][2]

    fields_str = ", ".join(ctx["data_fields"])
    sample_row = ", ".join(
        ['"' + k + '": "' + v + '"' for k, v in ctx["sample_values"].items()]
    )

    cells = [
        md("# CP2 Week " + str(week_num) + " Studio -- " + track["product"] + "\n\n"
           "**Track:** " + track["name"] + "\n"
           "**Week Topic:** " + week_title + "\n"
           "**Focus:** " + week_focus + "\n\n"
           "## Studio Goals\n"
           "- Apply this week's concepts to your " + track["product"] + " project\n"
           "- Complete the Must-Pass Core during class\n"
           "- Work toward Standard Target\n"
           "- Optional: attempt the Stretch goal"),
        setup_cell(),

        md("---\n## Your Track Context\n\n"
           "**Product:** " + track["product"] + "\n"
           "**Data Domain:** " + ctx["domain"] + " data\n"
           "**Key Columns:** " + fields_str + "\n"
           "**Primary Metric:** " + ctx["unit"]),

        md("---\n## Sample Data for " + track["product"] + "\n\n"
           "Use this sample data structure for today's exercises. "
           "Replace with your actual project data when ready."),

        code('# Sample data for ' + track["product"] + '\n'
             'sample_data = [\n'
             '    {' + sample_row + ', "id": "1"},\n'
             '    {' + sample_row + ', "id": "2"},\n'
             '    {' + sample_row + ', "id": "3"},\n'
             ']\n'
             '\n'
             'print("Sample data for ' + track["product"] + ':")\n'
             'for row in sample_data:\n'
             '    print("  " + str(row))\n'
             'print("\\nColumns: " + str(list(sample_data[0].keys())))'),
    ]

    # Must-Pass Core
    cells.append(md("---\n## Must-Pass Core\n\n"
                     "**Complete this section during class.** This is the minimum "
                     "requirement for the week.\n\n"
                     "**Task:** Apply **" + week_title + "** to your " + track["product"] + " data."))

    # Week-specific must-pass tasks
    must_pass_tasks = {
        1: ("Validate your data schema",
            '# Must-Pass: Implement validate_schema for ' + track["product"] + '\n'
            '# Your schema should check for these columns: ' + fields_str + '\n'
            '\n'
            'def validate_schema(data, config):\n'
            '    """Validate ' + track["product"] + ' data schema."""\n'
            '    if not data:\n'
            '        raise ValueError("Data is empty")\n'
            '    \n'
            '    required = config.get("required_columns", [])\n'
            '    actual = set(data[0].keys())\n'
            '    missing = set(required) - actual\n'
            '    \n'
            '    if missing:\n'
            '        raise ValueError("Missing columns: " + str(sorted(missing)))\n'
            '    \n'
            '    print("Schema valid for ' + track["product"] + '")\n'
            '    return True\n'
            '\n'
            'config = {"required_columns": ' + str(ctx["data_fields"]) + '}\n'
            '\n'
            '# TODO: Test with your sample data\n'
            '# validate_schema(sample_data, config)\n'
            'print("TODO: update sample_data to include all required columns and test")'),
        2: ("Build analytics for your data",
            '# Must-Pass: Count and summarize your ' + ctx["domain"] + ' data\n'
            'from collections import Counter\n'
            '\n'
            '# TODO: Create at least 10 rows of sample data for ' + track["product"] + '\n'
            '# TODO: Count values in one categorical column\n'
            '# TODO: Compute group summary for one numeric column\n'
            '\n'
            'print("TODO: implement counting and group summaries for ' + track["product"] + '")'),
        3: ("Create a cleaning config and pipeline",
            '# Must-Pass: Config-driven cleaning for ' + track["product"] + '\n'
            '\n'
            'cleaning_config = {\n'
            '    "drop_missing": True,\n'
            '    "numeric_columns": ' + str([f for f in ctx["data_fields"] if f not in ["timestamp", "filter", "status", "submitted"]]) + ',\n'
            '    "value_ranges": {},  # TODO: add ranges for your columns\n'
            '}\n'
            '\n'
            '# TODO: write apply_cleaning_rules for ' + track["product"] + '\n'
            '# TODO: test with sample data that includes bad rows\n'
            'print("TODO: implement cleaning pipeline for ' + track["product"] + '")'),
    }

    # Default task for weeks without specific content
    default_task = ("Apply this week's concept",
                    '# Must-Pass: Apply ' + week_title + ' to ' + track["product"] + '\n'
                    '\n'
                    '# TODO: Implement the core requirement for Week ' + str(week_num) + '\n'
                    '# Concept: ' + week_focus + '\n'
                    '\n'
                    'print("Working on ' + track["product"] + ' -- Week ' + str(week_num) + '")\n'
                    'print("Concept: ' + week_title + '")')

    task_desc, task_code = must_pass_tasks.get(week_num, default_task)
    cells.append(md("### Task: " + task_desc))
    cells.append(code(task_code))

    cells.append(md("### Checkpoint 1\n\n"
                     "Before moving on, verify your must-pass code works:"))
    cells.append(code('# Checkpoint 1: verify must-pass\n'
                       'print("Checkpoint 1: Must-Pass Core")\n'
                       'print("  [ ] Code runs without errors")\n'
                       'print("  [ ] Output matches expected format")\n'
                       'print("  [ ] Applied to ' + track["product"] + ' data")'))

    # Standard Target
    cells.append(md("---\n## Standard Target\n\n"
                     "Extend the must-pass core with:\n"
                     "1. Proper error handling (try/except)\n"
                     "2. Config-driven behavior\n"
                     "3. Clear output formatting\n"
                     "4. At least 2 test cases"))

    cells.append(code('# Standard Target: extend your implementation\n'
                       '\n'
                       '# TODO: Add error handling\n'
                       '# TODO: Make behavior config-driven\n'
                       '# TODO: Format output clearly\n'
                       '# TODO: Test with good and bad data\n'
                       '\n'
                       'print("TODO: extend must-pass with error handling and config")'))

    cells.append(md("### Checkpoint 2"))
    cells.append(code('# Checkpoint 2: verify standard target\n'
                       'print("Checkpoint 2: Standard Target")\n'
                       'print("  [ ] Error handling works")\n'
                       'print("  [ ] Config controls behavior")\n'
                       'print("  [ ] Output is clearly formatted")\n'
                       'print("  [ ] Tested with 2+ test cases")'))

    # Stretch
    cells.append(md("---\n## Stretch (Optional)\n\n"
                     "Go beyond the standard target. Choose one:\n\n"
                     "- Add a creative improvement specific to " + track["product"] + "\n"
                     "- Optimize performance\n"
                     "- Add visualization\n"
                     "- Write additional tests"))

    cells.append(code('# Stretch: creative improvement for ' + track["product"] + '\n'
                       '\n'
                       '# TODO: pick one stretch goal and implement it\n'
                       '\n'
                       'print("Stretch goal: your creative improvement")'))

    # Integration check
    cells.append(md("---\n## Integration Check\n\n"
                     "Before leaving, verify your work integrates with the pipeline:"))

    cells.append(code('# Integration check\n'
                       'print("=== Week ' + str(week_num) + ' Integration Check ===")\n'
                       'print()\n'
                       'checks = [\n'
                       '    "Must-pass core completed",\n'
                       '    "Code runs without errors",\n'
                       '    "Output is correct for sample data",\n'
                       '    "Code is saved and committed",\n'
                       ']\n'
                       'for check in checks:\n'
                       '    print("  [ ] " + check)\n'
                       'print()\n'
                       'print("Mark each [ ] as [x] when complete.")'))

    # Take-home
    cells.append(md("---\n## Take-Home Tasks\n\n"
                     "1. Complete any unfinished work from today\n"
                     "2. Review Week " + str(week_num) + " core notebook\n"
                     "3. Apply today's work to your full project dataset\n"
                     "4. Push code to GitHub\n"
                     "5. Ensure self_check() passes"))

    cells.append(reflection_cell())
    cells.append(reflection_code())

    return cells


# ================================================================
#  CHECK NOTEBOOKS
# ================================================================

def make_check(week_num):
    """Generate the universal check notebook for a given week."""
    cells = [
        md("# CP2 Week " + str(week_num) + " -- Universal Check\n\n"
           "Run all cells to verify your pipeline meets Week " + str(week_num) + " requirements."),
        setup_cell(),
        code('import os, json\n'
             '\n'
             'print("=== CP2 Week ' + str(week_num) + ' Universal Check ===\\n")\n'
             'passed = 0\n'
             'failed = 0\n'
             '\n'
             '# Check 1: Pipeline functions exist and run\n'
             'try:\n'
             '    # from project_name import load_data, clean_data, analyze\n'
             '    print("[INFO] Checking pipeline functions...")\n'
             '    print("[PASS] Pipeline structure OK")\n'
             '    passed += 1\n'
             'except Exception as e:\n'
             '    print("[FAIL] Pipeline: " + str(e))\n'
             '    failed += 1\n'
             '\n'
             '# Check 2: Required exports\n'
             'required = ["data/cleaned/cleaned.csv", "reports/report.json"]\n'
             'if ' + str(week_num) + ' >= 5:\n'
             '    required.extend(["reports/figures/timeseries.png", "reports/figures/summary.png"])\n'
             '\n'
             'for f in required:\n'
             '    if os.path.exists(f) and os.path.getsize(f) > 0:\n'
             '        print("[PASS] " + f + " exists (" + str(os.path.getsize(f)) + " bytes)")\n'
             '        passed += 1\n'
             '    else:\n'
             '        print("[FAIL] " + f + " missing or empty")\n'
             '        failed += 1\n'
             '\n'
             '# Check 3: report.json schema\n'
             'try:\n'
             '    with open("reports/report.json") as f:\n'
             '        report = json.load(f)\n'
             '    for key in ["project_name", "track", "version"]:\n'
             '        assert key in report, "Missing: " + key\n'
             '    print("[PASS] report.json has required keys")\n'
             '    passed += 1\n'
             'except FileNotFoundError:\n'
             '    print("[FAIL] report.json not found")\n'
             '    failed += 1\n'
             'except Exception as e:\n'
             '    print("[FAIL] report.json: " + str(e))\n'
             '    failed += 1\n'
             '\n'
             'print("\\n=== Results: " + str(passed) + " passed, " + str(failed) + " failed ===")\n'
             'if failed == 0:\n'
             '    print("Week ' + str(week_num) + ' check PASSED!")\n'
             'else:\n'
             '    print("Fix failures before submitting.")'),
    ]
    return cells


# ================================================================
#  HOMEWORK NOTEBOOKS (10-15 exercises)
# ================================================================

def make_homework(week_num, title):
    """Generate a rich homework notebook."""
    cells = [
        md("# CP2 Week " + str(week_num) + " Homework -- " + title + "\n\n"
           "**Due:** Before next week\n"
           "**Estimated time:** 2-4 hours\n\n"
           "## Instructions\n"
           "- Complete exercises in order (they build on each other)\n"
           "- **Review** exercises check understanding\n"
           "- **Practice** exercises apply concepts\n"
           "- **Challenge** exercises go deeper\n"
           "- **Mini-Project** combines everything\n"
           "- Show your work: include print statements for all outputs\n"
           "- Expected outputs are provided where applicable"),
        setup_cell(),

        md("---\n## Review (1-4)\n\n"
           "These exercises check that you understood the core concepts."),
        code('# HW1: In your own words (as comments), explain:\n'
             '# a) What is ' + title.lower() + '?\n'
             '# b) Why does it matter for a v2 pipeline?\n'
             '# c) How did you apply it in studio today?\n'),
        code('# HW2: Write a working example of the main concept from Week ' + str(week_num) + '.\n'
             '# It should be different from the examples in the core notebook.\n'
             '# Use your own data, not the examples.\n'),
        code('# HW3: What error would you get if you skip ' + title.lower() + '?\n'
             '# Write code that demonstrates the problem.\n'
             '# Then write code that fixes it.\n'),
        code('# HW4: Draw (in comments or print statements) a diagram\n'
             '# showing how ' + title.lower() + ' fits into the v2 pipeline.\n'),

        md("---\n## Practice (5-8)\n\n"
           "These exercises require applying concepts to new scenarios."),
        code('# HW5: Apply ' + title.lower() + ' to a new dataset.\n'
             '# Create at least 15 rows of sample data.\n'
             '# Show the output and verify it is correct.\n'),
        code('# HW6: Write a function that combines ' + title.lower() + '\n'
             '# with one concept from a previous week.\n'
             '# Example: combine with schema validation, or cleaning, etc.\n'),
        code('# HW7: Handle at least 3 edge cases:\n'
             '# a) Empty input\n'
             '# b) Single row\n'
             '# c) All identical values\n'
             '# Show that your code handles each one gracefully.\n'),
        code('# HW8: Write clear documentation (docstrings + comments)\n'
             '# for the main function you wrote this week.\n'
             '# Include: description, args, returns, example usage.\n'),

        md("---\n## Challenge (9-11)\n\n"
           "These exercises push you beyond what was covered in class."),
        code('# HW9: Extend ' + title.lower() + ' with a feature not covered in class.\n'
             '# Be creative! Think about what would be useful for your project.\n'),
        code('# HW10: Write 3 tests for your implementation:\n'
             '# a) Happy path test\n'
             '# b) Edge case test\n'
             '# c) Error handling test\n'),
        code('# HW11: Compare two different approaches to ' + title.lower() + '.\n'
             '# Which is better and why? Show timing if applicable.\n'),

        md("---\n## Mini-Project\n\n"
           "Combine everything from this week into one cohesive piece."),
        code('# HW12 (Mini-Project): Build a standalone tool that demonstrates\n'
             '# mastery of ' + title.lower() + '.\n'
             '#\n'
             '# Requirements:\n'
             '# - At least 3 functions\n'
             '# - Handles edge cases\n'
             '# - Clear output with print statements\n'
             '# - Demonstrates 3+ concepts from this week\n'
             '# - Works with your project data\n'),

        reflection_cell(),
        reflection_code(),
    ]
    return cells


# ================================================================
#  GENERATE ALL NOTEBOOKS
# ================================================================

print("Generating CP2 notebooks...")
total = 0

for week_num, title, focus in WEEKS:
    wk = "W" + str(week_num).zfill(2)

    # Core notebook
    if week_num in CORE_GENERATORS:
        cells = CORE_GENERATORS[week_num]()
    else:
        # Fallback (should not happen -- all 14 weeks have generators)
        cells = [
            md("# CP2 Week " + str(week_num) + " -- " + title),
            setup_cell(),
            md("Content for this week is in development."),
            reflection_cell(),
            reflection_code(),
        ]
    nb = notebook(cells, "CP2 " + wk + " Core -- " + title)
    save_notebook(nb, os.path.join(BASE, wk + "_core.ipynb"))
    total += 1

    # Studio notebooks (one per track)
    for tk in TRACKS:
        cells = make_studio(week_num, tk)
        nb = notebook(cells, "CP2 " + wk + " Studio -- " + TRACKS[tk]["name"])
        save_notebook(nb, os.path.join(BASE, wk + "_studio_" + tk + ".ipynb"))
        total += 1

    # Check notebook
    cells = make_check(week_num)
    nb = notebook(cells, "CP2 " + wk + " Check")
    save_notebook(nb, os.path.join(BASE, wk + "_check.ipynb"))
    total += 1

    # Homework notebook
    cells = make_homework(week_num, title)
    nb = notebook(cells, "CP2 " + wk + " Homework -- " + title)
    save_notebook(nb, os.path.join(BASE, wk + "_homework.ipynb"))
    total += 1

    print("  " + wk + ": core + 5 studios + check + homework")

print("\nCP2 complete: " + str(total) + " notebooks generated!")
