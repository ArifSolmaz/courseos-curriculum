#!/usr/bin/env python3
"""Generate all CP1 (Computer Programming 1) notebooks — 14 weeks."""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from nb_utils import md, code, notebook, save_notebook, setup_cell, reflection_cell, reflection_code, TRACKS

BASE = os.path.join(os.path.dirname(__file__), "notebooks", "cp1")
os.makedirs(BASE, exist_ok=True)

# ============================================================
# WEEK DEFINITIONS
# ============================================================

WEEKS = [
    # (week_num, title, concepts, contract_focus)
    (1, "Welcome to Python & Your Pipeline", "print, Colab, repo setup", "Hello Pipeline stub"),
    (2, "Variables, Types & Numbers", "variables, int, float, str, config dict", "config used by a function"),
    (3, "Making Decisions (Conditionals)", "if, elif, else, comparisons, booleans", "clean_data() basic rules"),
    (4, "Decision Logic & Classification", "nested if, logical operators, rule-based labeling", "analyze() labeled outputs"),
    (5, "Loops: Scanning Data", "for loop, while loop, range, accumulation", "summary stats on toy data"),
    (6, "Loops: Counting Events", "counting patterns, threshold crossings, flags", "event counts + edge cases"),
    (7, "Lists: Indexing & Windows", "list basics, indexing, slicing, append, windowed ops", "moving-window metric"),
    (8, "Strings: Parsing Data", "string methods, split, strip, join, parsing records", "parser handles formats"),
    (9, "Functions: Building Blocks", "def, parameters, return, refactoring", "pipeline functions exist"),
    (10, "Functions: Decomposition & Reuse", "helper functions, DRY, docstrings", "clearer separation"),
    (11, "Exceptions: Handling Errors", "try/except, common errors, skip bad rows", "clean_data reports skipped"),
    (12, "File I/O: Reading & Writing", "open, read, write, CSV basics", "export_results writes files"),
    (13, "Integration: End-to-End Pipeline", "matplotlib basics, putting it together", "plot() creates figures"),
    (14, "v1 Release & Demo", "final integration, testing, demo prep", "v1 passes all checks"),
]

# ============================================================
# CORE NOTEBOOK CONTENT (detailed per week)
# ============================================================

def make_core_w01():
    return [
        md("# CP1 Week 1 — Welcome to Python & Your Pipeline\n\n**Course:** Computer Programming 1 (CP1)\n**Session:** 5 hours\n\n## Learning Objectives\n- Open and run a Google Colab notebook\n- Write your first Python code using `print()`\n- Understand what a \"pipeline\" means\n- Set up your project repository\n- Choose a track to explore"),
        setup_cell(),
        md("---\n## Part 1: Your First Python Program\n\nPython is a programming language. You type instructions, and the computer follows them.\n\nThe simplest instruction is `print()` — it displays text on the screen."),
        code('# This is your first Python program!\n# Click the Play button (or press Shift+Enter) to run it\n\nprint("Hello, World!")'),
        md("**Expected Output:**\n```\nHello, World!\n```\n\n**What happened?**\n- `print()` is a *function* — it does something (displays text)\n- The text inside quotes `\"Hello, World!\"` is called a *string*\n- Python ran your instruction and showed the result"),
        md("### Try It Yourself\nChange the message to include your name:"),
        code('# TODO: Change the message to say "Hello, my name is ___"\nprint("Hello, my name is ___")'),
        md("---\n## Part 2: Python as a Calculator\n\nPython can do math! Try these:"),
        code("# Addition\nprint(2 + 3)\n\n# Subtraction\nprint(10 - 4)\n\n# Multiplication\nprint(5 * 6)\n\n# Division\nprint(20 / 4)"),
        md("**Expected Output:**\n```\n5\n6\n30\n5.0\n```\n\nNotice: division always gives a decimal number (called a `float`)."),
        md("### Try It\nCalculate: how many minutes are in a week?"),
        code("# TODO: Calculate minutes in a week\n# Hint: 7 days × 24 hours × 60 minutes\nminutes_in_week = ___\nprint(minutes_in_week)"),
        md("---\n## Part 3: What is a Pipeline?\n\nA **pipeline** is a series of steps that transform data:\n\n```\nRaw Data → Clean → Analyze → Plot → Export\n```\n\nThink of it like a factory assembly line:\n1. **Load** raw materials (data)\n2. **Clean** — remove defective parts (bad data)\n3. **Analyze** — measure and inspect\n4. **Plot** — create visual reports\n5. **Export** — package the results\n\nThis is what you will build over the next 14 weeks!"),
        code('# Here\'s a TINY preview of what your pipeline will look like:\n\n# Step 1: Some raw data (just numbers for now)\nraw_data = [10, 20, -5, 30, 999, 15]\nprint("Raw data:", raw_data)\n\n# Step 2: Clean (remove negative and extreme values)\nclean_data = []\nfor value in raw_data:\n    if 0 <= value <= 100:\n        clean_data.append(value)\nprint("Clean data:", clean_data)\n\n# Step 3: Analyze (calculate average)\ntotal = 0\nfor value in clean_data:\n    total = total + value\naverage = total / len(clean_data)\nprint("Average:", average)\n\nprint("\\nDon\'t worry if you don\'t understand everything yet!")\nprint("By Week 14, you will write all of this yourself.")'),
        md("---\n## Part 4: Comments\n\nComments are notes for humans. Python ignores them."),
        code('# This is a comment — Python skips this line\nprint("This runs")  # You can also put comments at the end\n\n# Comments help you (and others) understand your code\n# Always write comments to explain WHY, not WHAT'),
        md("---\n## Part 5: Errors are Normal!\n\nMaking errors is a **normal** part of programming. Don't panic!"),
        code('# This will cause an error — can you spot the problem?\n# Uncomment the line below to see the error:\n# print("Hello World)'),
        md('**Common Error:** `SyntaxError` — you forgot the closing quote `"`.\n\n**Rule:** When you see an error:\n1. Read the error message carefully\n2. Look at the line number it points to\n3. Check for typos, missing quotes, or wrong symbols'),
        md("---\n## Part 6: Track Exploration\n\nYou will choose one of 5 project tracks. Each builds the **same pipeline structure** but with different data:\n\n| Track | Product | Data |\n|-------|---------|------|\n| 1. Robotics | MechaSense Studio | Sensor readings (temp, RPM) |\n| 2. Data/AI | CleanReport Pipeline | Messy CSV datasets |\n| 3. Simulation | SimLab Engine | Simulation logs |\n| 4. Space/Astro | Lightcurve Explorer | Star brightness data |\n| 5. IoT | AutoDashboard | IoT sensor streams |\n\n**Weeks 1-2:** Explore all tracks\n**Week 3:** Confirm your choice (locked after that!)"),
        code('# Let\'s see a quick example from each track\n\n# Track 1 - Robotics: sensor temperature readings\nrobot_data = [22.1, 23.5, 99.9, 21.0, 24.3]\nprint("Robotics sample:", robot_data)\n\n# Track 2 - Data/AI: messy survey data\nsurvey_data = ["yes", "no", "YES", "", "maybe", "no"]\nprint("Data/AI sample:", survey_data)\n\n# Track 3 - Simulation: game scores\ngame_scores = [100, 250, 180, 300, 50]\nprint("Simulation sample:", game_scores)\n\n# Track 4 - Space: star brightness over time\nbrightness = [1.0, 0.98, 0.95, 0.70, 0.96, 1.01]\nprint("Space sample:", brightness)\n\n# Track 5 - IoT: temperature sensor readings\niot_temps = [20.5, 21.0, 20.8, 21.2, 20.9]\nprint("IoT sample:", iot_temps)'),
        md("---\n## Part 7: Your Pipeline Stub\n\nLet's create the skeleton (\"stub\") of your pipeline. A stub is an empty function that we'll fill in later."),
        code('# === YOUR PIPELINE STUB ===\n# These are placeholder functions. They don\'t do anything useful yet.\n# You will fill them in over the coming weeks!\n\ndef load_data(config):\n    """Load raw data."""\n    print("load_data: not implemented yet")\n    return []\n\ndef clean_data(data, config):\n    """Clean raw data."""\n    print("clean_data: not implemented yet")\n    return data\n\ndef analyze(clean_data, config):\n    """Analyze clean data."""\n    print("analyze: not implemented yet")\n    return {"status": "not implemented"}\n\ndef plot(clean_data, results, config):\n    """Create plots."""\n    print("plot: not implemented yet")\n    return []\n\ndef export_results(clean_data, results, figures, config):\n    """Export everything."""\n    print("export_results: not implemented yet")\n    return {}\n\ndef self_check():\n    """Test the pipeline."""\n    print("self_check: running...")\n    assert load_data({}) is not None, "load_data should return something"\n    print("self_check: PASSED (basic)")\n\n# Run it!\nprint("=== Pipeline Stub Test ===")\nconfig = {"project_name": "my_project"}\ndata = load_data(config)\ncleaned = clean_data(data, config)\nresults = analyze(cleaned, config)\nfigures = plot(cleaned, results, config)\nexported = export_results(cleaned, results, figures, config)\nself_check()\nprint("=== Done! ===")\nprint("\\nAll stubs work. You will replace them with real code each week!")'),
        md("---\n## Mini-Quiz\n\nAnswer these in the code cell below (as comments):"),
        code('# Mini-Quiz - Answer as comments\n\n# Q1: What does print() do?\n# Answer: \n\n# Q2: What is a pipeline?\n# Answer: \n\n# Q3: What are the 5 steps of our pipeline?\n# Answer: \n\n# Q4: What should you do when you see an error?\n# Answer: \n\n# Q5: By what week must you confirm your track?\n# Answer: '),
        md("---\n## Homework (Complete Before Next Week)\n\nThese exercises reinforce what you learned today. Do them at home!\n\n### Easy (1-3)"),
        code('# HW1: Print your full name, your age, and your favorite color\n# (each on its own line)\n\n'),
        code('# HW2: Use Python as a calculator to solve:\n# a) 15 * 8 + 3\n# b) (100 - 37) / 9\n# c) 2 ** 10  (this means 2 to the power of 10)\n\n'),
        code('# HW3: Write 3 print statements that show:\n# - Your track preference (1st choice)\n# - Your track preference (2nd choice)\n# - Why you prefer the 1st choice\n\n'),
        md("### Medium (4-6)"),
        code('# HW4: Fix these broken print statements (uncomment and fix each one)\n# print("Hello)\n# print(Hello, World!)\n# Print("test")\n\n'),
        code('# HW5: Calculate and print:\n# - How many seconds are in a day\n# - How many seconds are in a year (365 days)\n# - How many heartbeats in a day (assume 72 beats per minute)\n\n'),
        code('# HW6: Create a mini pipeline that:\n# 1. Starts with this data: [5, 12, -3, 8, 200, 7, 15]\n# 2. Keeps only values between 0 and 100\n# 3. Prints the clean data\n# (Hint: copy and adapt the example from Part 3)\n\n'),
        md("### Challenge (7-8)"),
        code('# HW7: Research - Look up what these Python operators do and test them:\n# //  (floor division)\n# %   (modulo)\n# **  (exponentiation)\n# Write an example of each and print the result\n\n'),
        code('# HW8: Create a pipeline stub with ONE improvement:\n# Make load_data() return some actual sample data\n# instead of an empty list. The data should be a list\n# of at least 5 numbers related to your preferred track.\n\ndef load_data(config):\n    # TODO: return real sample data for your track\n    return []\n\ndata = load_data({})\nprint("My sample data:", data)\nprint("Number of items:", len(data))'),
        reflection_cell(),
        reflection_code(),
    ]

def make_core_w02():
    return [
        md("# CP1 Week 2 — Variables, Types & Numbers\n\n## Learning Objectives\n- Create and use variables\n- Understand data types: `int`, `float`, `str`, `bool`\n- Use f-strings to format output\n- Create a configuration dictionary"),
        setup_cell(),
        md("---\n## Part 1: Variables — Giving Names to Values\n\nA **variable** is a name that stores a value. Think of it as a labeled box."),
        code('# Creating variables\ntemperature = 25.3\nsensor_name = "temp_sensor_01"\nis_active = True\nreading_count = 100\n\nprint(temperature)\nprint(sensor_name)\nprint(is_active)\nprint(reading_count)'),
        md("**Expected Output:**\n```\n25.3\ntemp_sensor_01\nTrue\n100\n```\n\n**Rules for variable names:**\n- Use lowercase with underscores: `my_variable` (good)\n- Can contain letters, numbers, underscores\n- Cannot start with a number: `1sensor` (bad)\n- Cannot use Python keywords: `print`, `if`, `for` (bad)"),
        md("### Try It"),
        code('# TODO: Create 3 variables for your project\n# 1. project_name (a string)\n# 2. data_size (an integer)\n# 3. threshold (a float)\n\nproject_name = ___\ndata_size = ___\nthreshold = ___\n\nprint(project_name)\nprint(data_size)\nprint(threshold)'),
        md("---\n## Part 2: Data Types\n\nEvery value in Python has a **type**. The 4 basic types are:"),
        code('# int — whole numbers (no decimal point)\nage = 20\nprint(type(age))      # <class \'int\'>\n\n# float — decimal numbers\ntemp = 36.6\nprint(type(temp))     # <class \'float\'>\n\n# str — text (must be in quotes)\nname = "Alice"\nprint(type(name))     # <class \'str\'>\n\n# bool — True or False\nis_valid = True\nprint(type(is_valid))  # <class \'bool\'>'),
        md("**Expected Output:**\n```\n<class 'int'>\n<class 'float'>\n<class 'str'>\n<class 'bool'>\n```"),
        md("### Converting Between Types"),
        code('# Converting types\nx = "42"          # this is a string!\nprint(type(x))    # <class \'str\'>\n\ny = int(x)        # convert to integer\nprint(type(y))    # <class \'int\'>\nprint(y + 10)     # now we can do math: 52\n\nz = float("3.14") # string to float\nprint(z)          # 3.14\n\nw = str(100)      # int to string\nprint("Value: " + w)  # "Value: 100"'),
        md("### Try It"),
        code('# TODO: What type is each of these? Use type() to check\na = 42\nb = 42.0\nc = "42"\nd = True\ne = "True"\n\nprint(f"a = {a}, type = {type(a)}")\nprint(f"b = {b}, type = {type(b)}")\nprint(f"c = {c}, type = {type(c)}")\nprint(f"d = {d}, type = {type(d)}")\nprint(f"e = {e}, type = {type(e)}")'),
        md("---\n## Part 3: Math Operations"),
        code('a = 15\nb = 4\n\nprint(f"a + b = {a + b}")     # Addition: 19\nprint(f"a - b = {a - b}")     # Subtraction: 11\nprint(f"a * b = {a * b}")     # Multiplication: 60\nprint(f"a / b = {a / b}")     # Division: 3.75\nprint(f"a // b = {a // b}")   # Floor division: 3\nprint(f"a % b = {a % b}")     # Modulo (remainder): 3\nprint(f"a ** b = {a ** b}")   # Power: 50625'),
        md("### Updating Variables"),
        code('count = 0\nprint(f"Start: {count}")\n\ncount = count + 1  # add 1\nprint(f"After +1: {count}")\n\ncount += 5         # shorthand for count = count + 5\nprint(f"After +=5: {count}")\n\ncount *= 2         # shorthand for count = count * 2\nprint(f"After *=2: {count}")'),
        md("---\n## Part 4: f-Strings (Formatted Text)\n\nf-strings let you put variables inside text. Start the string with `f`:"),
        code('name = "Motor A"\nrpm = 1500\ntemp = 72.456\n\n# Basic f-string\nprint(f"Sensor: {name}")\nprint(f"RPM: {rpm}")\n\n# Format decimals\nprint(f"Temperature: {temp:.1f} C")    # 1 decimal: 72.5\nprint(f"Temperature: {temp:.2f} C")    # 2 decimals: 72.46\n\n# Math inside f-strings\nprint(f"RPM doubled: {rpm * 2}")'),
        md("**Expected Output:**\n```\nSensor: Motor A\nRPM: 1500\nTemperature: 72.5 C\nTemperature: 72.46 C\nRPM doubled: 3000\n```"),
        md("### Try It"),
        code('# TODO: Create variables and use f-strings to print a summary\n# Example output: "Project: MechaSense | Track: robotics | Data points: 500"\n\nproject = ___\ntrack = ___\npoints = ___\n\nprint(f"Project: {project} | Track: {track} | Data points: {points}")'),
        md("---\n## Part 5: Your Config Dictionary\n\nA **dictionary** stores key-value pairs. We use it for configuration:"),
        code('# A simple config dictionary\nconfig = {\n    "project_name": "my_project",\n    "track": "robotics",\n    "version": "v1",\n    "threshold": 50.0,\n    "data_points": 100,\n}\n\n# Access values using keys\nprint(f"Project: {config[\'project_name\']}")\nprint(f"Track: {config[\'track\']}")\nprint(f"Threshold: {config[\'threshold\']}")'),
        code('# Adding new keys\nconfig["author"] = "Student A"\nprint(config)\n\n# Checking if a key exists\nif "threshold" in config:\n    print(f"Threshold is set to {config[\'threshold\']}")'),
        md("### Try It: Create Your Config"),
        code('# TODO: Create a config dictionary for YOUR project\n# Include at least: project_name, track, version, threshold\n\nmy_config = {\n    "project_name": "___",\n    "track": "___",\n    "version": "v1",\n    "threshold": ___,\n}\n\n# Print each value using the config\nfor key, value in my_config.items():\n    print(f"  {key}: {value}")'),
        md("---\n## Part 6: Using Config in a Function"),
        code('def load_data(config):\n    """Load sample data based on config."""\n    name = config["project_name"]\n    n = config.get("data_points", 10)  # default to 10\n    \n    # Generate simple sample data\n    data = []\n    for i in range(n):\n        data.append({"index": i, "value": i * 2.5 + 10})\n    \n    print(f"[{name}] Loaded {len(data)} rows")\n    return data\n\n# Use it!\nconfig = {\n    "project_name": "my_sensor",\n    "data_points": 5,\n}\n\nresult = load_data(config)\nfor row in result:\n    print(f"  Row {row[\'index\']}: value = {row[\'value\']}")'),
        md("---\n## Mini-Quiz"),
        code('# Q1: What is the output?\nx = 10\nx = x + 5\nprint(x)\n# Your answer: ___\n\n# Q2: What type is this? (int, float, str, or bool)\nval = "3.14"\n# Your answer: ___\n\n# Q3: What does this print?\nname = "Python"\nprint(f"I love {name}!")\n# Your answer: ___\n\n# Q4: How do you access the value "v1" from this dict?\nconfig = {"version": "v1", "name": "test"}\n# Your answer: config[___]'),
        md("---\n## Homework\n\n### Easy"),
        code('# HW1: Create variables for 5 sensor readings and print their average\n\n'),
        code('# HW2: Use f-strings to print a formatted report like:\n# "Sensor: Motor-A | Readings: 150 | Average: 23.45 C"\n\n'),
        code('# HW3: Create a config dictionary with at least 6 keys\n# and print all keys and values using a for loop\n\n'),
        md("### Medium"),
        code('# HW4: Write code that converts temperature from Celsius to Fahrenheit\n# Formula: F = C * 9/5 + 32\n# Test with: 0, 100, 37.5\n\n'),
        code('# HW5: Create a function that takes config and returns a summary string\n# Example: summarize(config) -> "Project my_sensor v1 (robotics track)"\n\n'),
        code('# HW6: Create two config dictionaries (one for each of your top 2 tracks)\n# Print a comparison table showing the differences\n\n'),
        md("### Challenge"),
        code('# HW7: Create a load_data() function that generates different sample data\n# depending on the track in config. For example:\n# - robotics: generates temperature readings (20-80 range)\n# - space: generates brightness values (0.5-1.5 range)\n# (You can use: value = start + (i * step) for simple patterns)\n\n'),
        code('# HW8: Research Python\'s built-in functions: min(), max(), sum(), len(), round()\n# Use each one on a list of numbers and explain what it does\n\ndata = [23.5, 18.2, 31.0, 27.8, 19.4, 25.1]\n# Try min(), max(), sum(), len(), round() on this data\n\n'),
        reflection_cell(),
        reflection_code(),
    ]

def make_core_w03():
    return [
        md("# CP1 Week 3 — Making Decisions (Conditionals)\n\n## Learning Objectives\n- Use `if`, `elif`, `else` to make decisions\n- Write comparison operators (`==`, `!=`, `<`, `>`, `<=`, `>=`)\n- Apply rules to filter/validate data\n- Implement basic cleaning rules in `clean_data()`"),
        setup_cell(),
        md("---\n## Part 1: True or False?\n\nPython can answer yes/no questions using **comparisons**:"),
        code('# Comparisons return True or False\nprint(10 > 5)     # True\nprint(10 < 5)     # False\nprint(10 == 10)   # True  (== means \"equal to\")\nprint(10 != 5)    # True  (!= means \"not equal to\")\nprint(10 >= 10)   # True  (greater than or equal)\nprint(10 <= 9)    # False (less than or equal)'),
        md("**Common mistake:** `=` vs `==`\n- `x = 5` means \"assign 5 to x\"\n- `x == 5` means \"is x equal to 5?\""),
        md("---\n## Part 2: if Statements"),
        code('temperature = 75\n\nif temperature > 60:\n    print("WARNING: Temperature is high!")\n    print("Check the sensor.")\n\nprint("This always runs (not indented under if)")'),
        md("**Key points:**\n- The code **indented** under `if` only runs when the condition is `True`\n- Indentation matters! Use **4 spaces** (Tab key in Colab)\n- The colon `:` after the condition is required"),
        md("### if / else"),
        code('value = 42\n\nif value >= 0:\n    print(f"{value} is positive or zero")\nelse:\n    print(f"{value} is negative")\n\n# Try changing value to -10 and run again!'),
        md("### if / elif / else"),
        code('score = 73\n\nif score >= 90:\n    grade = "A"\nelif score >= 80:\n    grade = "B"\nelif score >= 70:\n    grade = "C"\nelif score >= 60:\n    grade = "D"\nelse:\n    grade = "F"\n\nprint(f"Score: {score} → Grade: {grade}")'),
        md("### Try It"),
        code('# TODO: Write an if/elif/else that classifies a temperature:\n# < 0: "Freezing"\n# 0-15: "Cold"\n# 16-25: "Comfortable"\n# 26-35: "Warm"\n# > 35: "Hot"\n\ntemperature = 22\n\n# Your code here:\n'),
        md("---\n## Part 3: Combining Conditions\n\nUse `and`, `or`, `not` to combine conditions:"),
        code('temp = 25\nhumidity = 80\n\n# Both must be true\nif temp > 20 and humidity > 70:\n    print("It\'s warm AND humid")\n\n# At least one must be true\nif temp > 30 or humidity > 90:\n    print("Extreme condition!")\nelse:\n    print("Conditions are moderate")\n\n# Flip a condition\nis_broken = False\nif not is_broken:\n    print("Sensor is working")'),
        md("---\n## Part 4: Validating Data with Conditionals\n\nThis is where conditionals become useful for your project! Let's validate data:"),
        code('# Check if a single reading is valid\ndef is_valid_reading(value):\n    """Check if a sensor reading is valid.\n    \n    Rules:\n    - Must not be None\n    - Must be a number\n    - Must be in range 0-150\n    """\n    if value is None:\n        return False\n    \n    if not isinstance(value, (int, float)):\n        return False\n    \n    if value < 0 or value > 150:\n        return False\n    \n    return True\n\n# Test it\ntest_values = [25.0, -5, 200, None, "abc", 50, 0, 150]\nfor v in test_values:\n    result = is_valid_reading(v)\n    print(f"  {str(v):>6} → valid: {result}")'),
        md("---\n## Part 5: Building clean_data() with Rules"),
        code('def clean_data(data, config):\n    """Clean data by applying validation rules.\n    \n    Args:\n        data: list of dictionaries (rows)\n        config: dict with cleaning settings\n    \n    Returns:\n        list of clean dictionaries\n    """\n    cleaned = []\n    dropped = 0\n    \n    threshold_min = config.get("min_value", 0)\n    threshold_max = config.get("max_value", 100)\n    \n    for row in data:\n        value = row.get("value")\n        \n        # Rule 1: skip if value is missing\n        if value is None or value == "":\n            dropped += 1\n            continue    # skip to next row\n        \n        # Rule 2: try to convert to number\n        try:\n            num_value = float(value)\n        except (ValueError, TypeError):\n            dropped += 1\n            continue\n        \n        # Rule 3: check range\n        if num_value < threshold_min or num_value > threshold_max:\n            dropped += 1\n            continue\n        \n        # Passed all rules!\n        row["value"] = num_value  # store as number\n        cleaned.append(row)\n    \n    print(f"Cleaned: {len(data)} → {len(cleaned)} ({dropped} dropped)")\n    return cleaned\n\n# Test it\nraw_data = [\n    {"id": 1, "value": "25.0"},\n    {"id": 2, "value": ""},        # missing\n    {"id": 3, "value": "-10"},     # below min\n    {"id": 4, "value": "abc"},     # not a number\n    {"id": 5, "value": "50.5"},\n    {"id": 6, "value": "200"},     # above max\n    {"id": 7, "value": "75.0"},\n]\n\nconfig = {"min_value": 0, "max_value": 100}\nresult = clean_data(raw_data, config)\n\nprint("\\nClean data:")\nfor row in result:\n    print(f"  id={row[\'id\']}, value={row[\'value\']}")'),
        md("**Expected Output:**\n```\nCleaned: 7 → 3 (4 dropped)\n\nClean data:\n  id=1, value=25.0\n  id=5, value=50.5\n  id=7, value=75.0\n```"),
        md("---\n## Mini-Quiz"),
        code('# Q1: What does this print?\nx = 10\nif x > 5:\n    print("A")\nelif x > 8:\n    print("B")\nelse:\n    print("C")\n# Answer: ___  (careful! elif is only checked if the first if is False)\n\n# Q2: What does `continue` do inside a loop?\n# Answer: ___\n\n# Q3: True or False: (5 > 3) and (10 < 8)\n# Answer: ___\n\n# Q4: True or False: (5 > 3) or (10 < 8)\n# Answer: ___'),
        md("---\n## Homework\n\n### Easy"),
        code('# HW1: Write an if/elif/else that classifies an RPM value:\n# < 500: "Low"\n# 500-1500: "Normal"\n# > 1500: "High"\n# Test with: 200, 1000, 2000\n\n'),
        code('# HW2: Check if a string can be converted to a number\n# Hint: try/except with float()\n# Test with: "42", "hello", "3.14", "", "99"\n\n'),
        code('# HW3: Write a function is_valid(row) that checks:\n# - row has a "value" key\n# - the value is not empty\n# - the value can be converted to a number\n\n'),
        md("### Medium"),
        code('# HW4: Extend clean_data() to also track WHY each row was dropped\n# Return a tuple: (cleaned_list, drop_report_dict)\n# drop_report should count: {"missing": N, "non_numeric": N, "out_of_range": N}\n\n'),
        code('# HW5: Write a function that assigns a "quality" label to each reading:\n# - "good" if within 1 std of mean\n# - "warning" if within 2 std of mean\n# - "bad" otherwise\n# (Calculate mean and std manually using loops)\n\nreadings = [20, 22, 21, 50, 19, 23, 21, 22, 20, 100]\n'),
        md("### Challenge"),
        code('# HW6: Write a mini cleaning pipeline that:\n# 1. Takes raw data as a list of strings: ["25.0", "bad", "", "50.0", "999", "30.0"]\n# 2. Converts valid values to float\n# 3. Removes out-of-range values (0-100)\n# 4. Returns (clean_list, report_dict)\n# 5. report_dict has: n_raw, n_clean, n_dropped, drop_reasons\n\n'),
        reflection_cell(),
        reflection_code(),
    ]

def make_core_w04():
    return [
        md("# CP1 Week 4 — Decision Logic & Classification\n\n## Learning Objectives\n- Build rule-based classifiers using nested conditionals\n- Use logical operators for complex conditions\n- Implement `analyze()` that returns labeled outputs\n- Understand state labeling and categorization"),
        setup_cell(),
        md("---\n## Part 1: Rule-Based Classification\n\nA **classifier** assigns a label based on rules:"),
        code('def classify_temperature(temp):\n    """Classify a temperature reading into a category."""\n    if temp < 0:\n        return "freezing"\n    elif temp < 15:\n        return "cold"\n    elif temp < 25:\n        return "normal"\n    elif temp < 40:\n        return "warm"\n    else:\n        return "hot"\n\n# Test it\ntest_temps = [-5, 10, 22, 35, 50]\nfor t in test_temps:\n    label = classify_temperature(t)\n    print(f"  {t:>5}°C → {label}")'),
        md("---\n## Part 2: Multi-Condition Classification"),
        code('def classify_sensor_state(temp, rpm, vibration):\n    """Classify machine state from multiple sensors."""\n    if temp > 80 or vibration > 50:\n        return "CRITICAL"\n    elif temp > 60 and rpm > 3000:\n        return "WARNING"\n    elif temp > 60 or rpm > 3000:\n        return "CAUTION"\n    else:\n        return "NORMAL"\n\n# Test cases\ncases = [\n    (25, 1500, 10),   # all normal\n    (65, 3500, 20),   # temp + rpm high\n    (85, 1000, 10),   # temp critical\n    (50, 1000, 60),   # vibration critical\n]\n\nfor temp, rpm, vib in cases:\n    state = classify_sensor_state(temp, rpm, vib)\n    print(f"  T={temp}, RPM={rpm}, Vib={vib} → {state}")'),
        md("---\n## Part 3: Building analyze() with Labels"),
        code('def analyze(clean_data, config):\n    """Analyze clean data: compute stats and assign labels.\n    \n    Returns a results dict with:\n    - analysis_summary: mean, median, std (at least 3 metrics)\n    - labels: classification for each row\n    """\n    if not clean_data:\n        return {"analysis_summary": {"mean": 0, "median": 0, "std": 0}, "labels": []}\n    \n    # Extract numeric values\n    values = [row["value"] for row in clean_data]\n    n = len(values)\n    \n    # Compute basic stats\n    mean_val = sum(values) / n\n    sorted_vals = sorted(values)\n    median_val = sorted_vals[n // 2]\n    variance = sum((x - mean_val) ** 2 for x in values) / n\n    std_val = variance ** 0.5\n    \n    # Classify each value\n    threshold = config.get("threshold", mean_val + 2 * std_val)\n    labels = []\n    for v in values:\n        if v > threshold:\n            labels.append("high")\n        elif v < mean_val - 2 * std_val:\n            labels.append("low")\n        else:\n            labels.append("normal")\n    \n    results = {\n        "analysis_summary": {\n            "count": n,\n            "mean": round(mean_val, 2),\n            "median": round(median_val, 2),\n            "std": round(std_val, 2),\n            "min": min(values),\n            "max": max(values),\n            "n_high": labels.count("high"),\n            "n_low": labels.count("low"),\n            "n_normal": labels.count("normal"),\n        },\n        "labels": labels,\n    }\n    \n    print(f"Analysis: {n} values, mean={mean_val:.2f}, std={std_val:.2f}")\n    print(f"Labels: {labels.count(\'normal\')} normal, {labels.count(\'high\')} high, {labels.count(\'low\')} low")\n    return results\n\n# Test\ntest_data = [\n    {"id": i, "value": v}\n    for i, v in enumerate([22, 23, 21, 50, 19, 23, 21, 22, 20, 45])\n]\nconfig = {"threshold": 40}\nresults = analyze(test_data, config)\nprint("\\nResults:", results["analysis_summary"])'),
        md("### Try It"),
        code('# TODO: Add a new classification rule to analyze().\n# Add a "trend" field that is:\n# - "increasing" if last 3 values go up\n# - "decreasing" if last 3 values go down\n# - "stable" otherwise\n\nvalues = [20, 22, 25, 28]  # increasing\n# Check: values[-3] < values[-2] < values[-1]\n'),
        md("---\n## Mini-Quiz"),
        code('# Q1: What label does classify_temperature(25) return?\n# Answer: \n\n# Q2: What is the difference between "and" and "or"?\n# Answer:\n\n# Q3: If mean=20 and std=5, what threshold does mean + 2*std give?\n# Answer:'),
        md("---\n## Homework\n\n### Easy"),
        code('# HW1: Write classify_speed(kmh) that returns:\n# "stopped" (<1), "slow" (1-30), "medium" (31-80), "fast" (81-120), "dangerous" (>120)\n\n'),
        code('# HW2: Classify these 10 readings using your function from HW1:\nreadings = [0, 15, 55, 90, 130, 25, 80, 45, 110, 200]\n\n'),
        md("### Medium"),
        code('# HW3: Write a function count_by_label(data, labels) that counts\n# how many items fall into each label category.\n# Return a dict like {"normal": 5, "high": 2, "low": 3}\n\n'),
        code('# HW4: Write analyze() for your track that computes at least\n# 5 different metrics and classifies each data point\n\n'),
        md("### Challenge"),
        code('# HW5: Implement a "traffic light" classifier:\n# Given (temp, pressure, humidity), return "green", "yellow", or "red"\n# Define your own reasonable thresholds and document them\n\n'),
        reflection_cell(),
        reflection_code(),
    ]

def make_core_w05():
    return [
        md("# CP1 Week 5 — Loops: Scanning Data\n\n## Learning Objectives\n- Use `for` loops to iterate over lists and ranges\n- Use `while` loops for condition-based repetition\n- Accumulate values: sum, count, min, max, mean\n- Compute summary statistics on data"),
        setup_cell(),
        md("---\n## Part 1: The for Loop\n\nA `for` loop repeats code for each item in a sequence:"),
        code('# Loop over a list\nreadings = [25.0, 22.5, 28.1, 21.3, 26.7]\n\nfor value in readings:\n    print(f"Reading: {value}")'),
        code('# Loop with range()\nfor i in range(5):        # 0, 1, 2, 3, 4\n    print(f"Step {i}")\n\nprint()\nfor i in range(2, 8):     # 2, 3, 4, 5, 6, 7\n    print(f"Step {i}")\n\nprint()\nfor i in range(0, 20, 5): # 0, 5, 10, 15 (step by 5)\n    print(f"Step {i}")'),
        md("---\n## Part 2: Accumulation Patterns\n\nThe most important loop patterns for data analysis:"),
        code('data = [10, 25, 30, 15, 20, 35, 5, 40]\n\n# Pattern 1: SUM\ntotal = 0\nfor value in data:\n    total = total + value\nprint(f"Sum: {total}")\n\n# Pattern 2: COUNT\ncount = 0\nfor value in data:\n    count = count + 1\nprint(f"Count: {count}")\n\n# Pattern 3: MEAN (average)\nmean = total / count\nprint(f"Mean: {mean}")\n\n# Pattern 4: MIN\nsmallest = data[0]  # start with first value\nfor value in data:\n    if value < smallest:\n        smallest = value\nprint(f"Min: {smallest}")\n\n# Pattern 5: MAX\nlargest = data[0]\nfor value in data:\n    if value > largest:\n        largest = value\nprint(f"Max: {largest}")'),
        md("**Expected Output:**\n```\nSum: 180\nCount: 8\nMean: 22.5\nMin: 5\nMax: 40\n```"),
        md("### Try It"),
        code('# TODO: Compute sum, count, mean, min, max for this data\n# Do NOT use built-in sum(), min(), max() — use loops!\n\ntemps = [22.1, 19.8, 25.3, 18.6, 23.4, 27.0, 20.5]\n\n# Your code here\n'),
        md("---\n## Part 3: Counting with Conditions"),
        code('data = [10, 25, 30, 15, 20, 35, 5, 40, 22, 28]\nthreshold = 25\n\n# Count values above threshold\nabove = 0\nbelow = 0\nfor value in data:\n    if value > threshold:\n        above += 1\n    else:\n        below += 1\n\nprint(f"Above {threshold}: {above}")\nprint(f"At or below {threshold}: {below}")'),
        md("---\n## Part 4: The while Loop"),
        code('# while loop: repeats as long as condition is True\ncount = 0\nwhile count < 5:\n    print(f"Count is {count}")\n    count += 1  # IMPORTANT: must update the variable!\nprint("Done!")\n\n# Danger: if you forget count += 1, the loop runs FOREVER!\n# (If that happens, click the stop button in Colab)'),
        md("---\n## Part 5: Computing Stats for Your Pipeline"),
        code('def compute_stats(values):\n    """Compute basic statistics using only loops.\n    \n    Returns dict with: count, sum, mean, min, max, std\n    """\n    if not values:\n        return {"count": 0, "sum": 0, "mean": 0, "min": 0, "max": 0, "std": 0}\n    \n    n = 0\n    total = 0\n    smallest = values[0]\n    largest = values[0]\n    \n    for v in values:\n        n += 1\n        total += v\n        if v < smallest:\n            smallest = v\n        if v > largest:\n            largest = v\n    \n    mean = total / n\n    \n    # Standard deviation\n    sum_sq_diff = 0\n    for v in values:\n        sum_sq_diff += (v - mean) ** 2\n    std = (sum_sq_diff / n) ** 0.5\n    \n    return {\n        "count": n,\n        "sum": round(total, 4),\n        "mean": round(mean, 4),\n        "min": round(smallest, 4),\n        "max": round(largest, 4),\n        "std": round(std, 4),\n    }\n\n# Test\ntest_data = [10, 20, 30, 40, 50]\nstats = compute_stats(test_data)\nfor key, val in stats.items():\n    print(f"  {key}: {val}")'),
        md("---\n## Mini-Quiz"),
        code('# Q1: How many times does this loop run?\nfor i in range(3, 10, 2):\n    pass\n# Answer: ___\n\n# Q2: What is the accumulator pattern?\n# Answer: ___\n\n# Q3: When should you use while instead of for?\n# Answer: ___'),
        md("---\n## Homework\n\n### Easy"),
        code('# HW1: Use a for loop to print the first 20 multiples of 7\n\n'),
        code('# HW2: Compute the sum and mean of: [3.5, 7.2, 1.8, 9.4, 5.1]\n# using loops (not built-in functions)\n\n'),
        code('# HW3: Count how many values in this list are between 20 and 30 (inclusive)\ndata = [15, 22, 31, 25, 18, 28, 33, 20, 27, 30]\n\n'),
        md("### Medium"),
        code('# HW4: Write compute_stats() and test on 3 different datasets\n# Print a formatted table of results\n\n'),
        code('# HW5: Find the second-largest value in a list using a loop\n# (don\'t sort — use two tracking variables)\ndata = [45, 12, 67, 23, 89, 34, 56]\n\n'),
        code('# HW6: Compute a "running sum" — a new list where each element\n# is the sum of all previous elements\n# [1, 2, 3, 4] → [1, 3, 6, 10]\n\n'),
        md("### Challenge"),
        code('# HW7: Write a function that computes the median WITHOUT using sort()\n# Hint: find the middle value by counting how many values are smaller\n\n'),
        code('# HW8: Write a standard_deviation() function from scratch\n# and verify it gives the same result as compute_stats()\n\n'),
        reflection_cell(),
        reflection_code(),
    ]

def make_core_generic(week_num, title, concepts, focus):
    """Generate a generic core notebook for weeks 6-14."""
    week_content = {
        6: {
            "objectives": "- Count events (threshold crossings)\n- Detect peaks and valleys\n- Handle edge cases (empty data, all same values)\n- Build event detection into your pipeline",
            "parts": [
                ("Part 1: What is an Event?", 'def count_threshold_crossings(values, threshold):\n    """Count how many times values cross above a threshold."""\n    crossings = 0\n    was_above = values[0] > threshold if values else False\n    \n    for v in values[1:]:\n        is_above = v > threshold\n        if is_above and not was_above:\n            crossings += 1\n        was_above = is_above\n    \n    return crossings\n\n# Test\ndata = [10, 30, 20, 40, 15, 50, 25, 35]\nprint(f"Crossings above 25: {count_threshold_crossings(data, 25)}")'),
                ("Part 2: Finding Peaks", 'def find_peaks(values):\n    """Find indices where value is higher than both neighbors."""\n    peaks = []\n    for i in range(1, len(values) - 1):\n        if values[i] > values[i-1] and values[i] > values[i+1]:\n            peaks.append(i)\n    return peaks\n\ndata = [10, 30, 20, 40, 15, 50, 25]\npeaks = find_peaks(data)\nprint(f"Peaks at indices: {peaks}")\nprint(f"Peak values: {[data[i] for i in peaks]}")'),
                ("Part 3: Edge Cases", '# Always handle edge cases!\ndef safe_count_events(values, threshold):\n    """Count events with proper edge case handling."""\n    if not values:\n        print("Warning: empty data")\n        return 0\n    if len(values) < 2:\n        print("Warning: need at least 2 values")\n        return 0\n    if all(v == values[0] for v in values):\n        print("Warning: all values are the same")\n        return 0\n    \n    return count_threshold_crossings(values, threshold)\n\n# Test edge cases\nprint(safe_count_events([], 10))\nprint(safe_count_events([5], 10))\nprint(safe_count_events([5, 5, 5], 10))\nprint(safe_count_events([5, 15, 5, 15], 10))'),
            ],
            "hw": [
                '# HW1: Count how many times temperature goes above AND below a threshold\ntemps = [20, 35, 28, 40, 22, 38, 15, 42, 30]\nthreshold = 30\n',
                '# HW2: Find all valleys (opposite of peaks: lower than both neighbors)\ndata = [30, 10, 25, 5, 35, 15, 40]\n',
                '# HW3: Write a function that finds the longest "streak" of values\n# above a threshold (consecutive values above threshold)\ndata = [10, 30, 35, 40, 20, 50, 55, 60, 65, 10]\n',
                '# HW4 (Challenge): Detect "spikes" — a sudden jump of more than X\n# from one reading to the next\ndata = [20, 22, 21, 80, 23, 22, 90, 25]\n',
            ],
        },
        7: {
            "objectives": "- Use list indexing and slicing\n- Implement windowed operations\n- Build a moving-average calculator\n- Understand list mutability",
            "parts": [
                ("Part 1: List Indexing & Slicing", 'data = [10, 20, 30, 40, 50, 60, 70, 80]\n\n# Indexing (0-based)\nprint(f"First: {data[0]}")      # 10\nprint(f"Last: {data[-1]}")      # 80\nprint(f"Third: {data[2]}")      # 30\n\n# Slicing [start:stop] (stop is excluded)\nprint(f"First 3: {data[0:3]}")  # [10, 20, 30]\nprint(f"Last 3: {data[-3:]}")   # [60, 70, 80]\nprint(f"Middle: {data[2:6]}")   # [30, 40, 50, 60]'),
                ("Part 2: Moving Window (Moving Average)", 'def moving_average(values, window_size):\n    """Calculate moving average with given window size.\n    \n    A moving average smooths data by averaging nearby values.\n    For window_size=3: avg of [i-1, i, i+1]\n    """\n    result = []\n    for i in range(len(values)):\n        # Get the window\n        start = max(0, i - window_size // 2)\n        end = min(len(values), i + window_size // 2 + 1)\n        window = values[start:end]\n        avg = sum(window) / len(window)\n        result.append(round(avg, 2))\n    return result\n\ndata = [10, 50, 20, 40, 30, 60, 25]\nsmoothed = moving_average(data, 3)\nprint(f"Original:  {data}")\nprint(f"Smoothed:  {smoothed}")'),
                ("Part 3: List Operations", 'numbers = [5, 2, 8, 1, 9, 3]\n\n# Append and extend\nnumbers.append(10)\nprint(f"After append: {numbers}")\n\n# Sort (modifies the list)\nnumbers.sort()\nprint(f"Sorted: {numbers}")\n\n# Reverse\nnumbers.reverse()\nprint(f"Reversed: {numbers}")\n\n# List comprehension (shortcut for creating lists)\nsquares = [x**2 for x in range(1, 6)]\nprint(f"Squares: {squares}")\n\n# Filter with comprehension\ndata = [10, 25, 30, 15, 20, 35]\nbig = [x for x in data if x > 20]\nprint(f"Values > 20: {big}")'),
            ],
            "hw": [
                '# HW1: Given data, extract every other element using slicing\ndata = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\n# Get: [1, 3, 5, 7, 9]\n',
                '# HW2: Implement a moving_max function (max of each window)\ndata = [10, 50, 20, 40, 30, 60, 25]\n',
                '# HW3: Implement a moving_sum function\ndata = [1, 2, 3, 4, 5, 6, 7, 8]\n',
                '# HW4: Find the index of the maximum value WITHOUT using .index()\ndata = [23, 45, 12, 67, 34, 89, 11]\n',
                '# HW5 (Challenge): Implement a "sliding window difference"\n# For each position, compute: max(window) - min(window)\ndata = [10, 50, 20, 40, 30, 60, 25, 35]\n',
            ],
        },
        8: {
            "objectives": "- Use string methods: split, strip, join, replace\n- Parse structured text into data records\n- Handle multiple data formats\n- Build a robust parser",
            "parts": [
                ("Part 1: String Basics", 'text = "  Hello, World!  "\n\n# Useful string methods\nprint(text.strip())         # Remove whitespace: "Hello, World!"\nprint(text.lower())         # "  hello, world!  "\nprint(text.upper())         # "  HELLO, WORLD!  "\nprint(text.strip().split(","))  # ["Hello", " World!"]\n\n# Check contents\nprint("World" in text)      # True\nprint(text.strip().startswith("Hello"))  # True\nprint(text.strip().endswith("!"))        # True'),
                ("Part 2: Parsing CSV Lines", 'def parse_csv_line(line):\n    """Parse a comma-separated line into a list of values."""\n    parts = line.strip().split(",")\n    cleaned = [p.strip() for p in parts]\n    return cleaned\n\n# Test\nlines = [\n    "sensor_01, 25.3, normal",\n    "sensor_02, 88.1, warning",\n    "sensor_03, -5, error",\n]\n\nfor line in lines:\n    parts = parse_csv_line(line)\n    print(f"  Name: {parts[0]}, Value: {parts[1]}, Status: {parts[2]}")'),
                ("Part 3: Parsing Multiple Formats", 'def parse_reading(text):\n    """Parse a sensor reading from various formats.\n    \n    Supported formats:\n    - "sensor_01: 25.3"\n    - "sensor_01=25.3"\n    - "sensor_01,25.3"\n    """\n    text = text.strip()\n    \n    if ":" in text:\n        parts = text.split(":")\n    elif "=" in text:\n        parts = text.split("=")\n    elif "," in text:\n        parts = text.split(",")\n    else:\n        return None\n    \n    if len(parts) != 2:\n        return None\n    \n    name = parts[0].strip()\n    try:\n        value = float(parts[1].strip())\n    except ValueError:\n        return None\n    \n    return {"name": name, "value": value}\n\n# Test\ntest_inputs = [\n    "temp_01: 25.3",\n    "temp_02=88.1",\n    "temp_03,15.7",\n    "bad data here",\n    "too:many:colons",\n]\n\nfor text in test_inputs:\n    result = parse_reading(text)\n    print(f"  \'{text}\' → {result}")'),
            ],
            "hw": [
                '# HW1: Split this sentence into words and count them\nsentence = "The quick brown fox jumps over the lazy dog"\n',
                '# HW2: Parse these log lines into dictionaries\n# Format: "TIMESTAMP | LEVEL | MESSAGE"\nlogs = [\n    "2024-01-15 10:30:00 | INFO | System started",\n    "2024-01-15 10:31:05 | WARNING | Temperature high",\n    "2024-01-15 10:32:10 | ERROR | Sensor disconnected",\n]\n',
                '# HW3: Write a function that validates email addresses\n# (must contain @, must have text before and after @, must have a dot after @)\n',
                '# HW4: Parse a multi-line CSV string into a list of dictionaries\ncsv_text = """name,value,unit\ntemp_01,25.3,celsius\ntemp_02,88.1,celsius\npressure_01,101.3,kPa"""\n',
                '# HW5 (Challenge): Write a flexible parser that auto-detects\n# the delimiter (comma, tab, pipe, semicolon) in a line\n',
            ],
        },
        9: {
            "objectives": "- Define functions with parameters and return values\n- Refactor code into reusable functions\n- Build the pipeline function structure\n- Understand scope and variable visibility",
            "parts": [
                ("Part 1: Functions Review & Best Practices", 'def calculate_mean(values):\n    """Calculate the arithmetic mean of a list of numbers.\n    \n    Args:\n        values (list): List of numbers.\n    \n    Returns:\n        float: The mean value, or 0 if empty.\n    """\n    if not values:\n        return 0\n    return sum(values) / len(values)\n\n# Use it\ndata = [10, 20, 30, 40, 50]\nresult = calculate_mean(data)\nprint(f"Mean: {result}")\n\n# Functions can call other functions!\ndef summarize(values):\n    """Return a summary dict with mean, min, max."""\n    return {\n        "mean": calculate_mean(values),\n        "min": min(values) if values else 0,\n        "max": max(values) if values else 0,\n        "count": len(values),\n    }\n\nprint(summarize(data))'),
                ("Part 2: Refactoring — Before & After", '# BEFORE: everything in one big block\nraw = [{"val": "25"}, {"val": ""}, {"val": "abc"}, {"val": "50"}, {"val": "-10"}]\ncleaned = []\nfor row in raw:\n    v = row["val"]\n    if v == "":\n        continue\n    try:\n        num = float(v)\n    except ValueError:\n        continue\n    if num < 0:\n        continue\n    cleaned.append(num)\nmean = sum(cleaned) / len(cleaned)\nprint(f"Result: {mean}")\n\nprint("---")\n\n# AFTER: organized into functions\ndef parse_value(text):\n    """Convert text to float, return None if invalid."""\n    if not text or text.strip() == "":\n        return None\n    try:\n        return float(text)\n    except ValueError:\n        return None\n\ndef is_in_range(value, low=0, high=1000):\n    """Check if value is within range."""\n    return low <= value <= high\n\ndef clean_values(raw_data):\n    """Clean a list of raw dicts, return list of floats."""\n    result = []\n    for row in raw_data:\n        val = parse_value(row.get("val", ""))\n        if val is not None and is_in_range(val):\n            result.append(val)\n    return result\n\n# Now it reads like a story!\ncleaned2 = clean_values(raw)\nmean2 = calculate_mean(cleaned2)\nprint(f"Result: {mean2}")'),
                ("Part 3: Your Pipeline Functions", '# Your complete pipeline should look like this:\n\ndef load_data(config):\n    """Load raw data from source."""\n    # For now, return sample data\n    data = []\n    for i in range(config.get("n_points", 10)):\n        data.append({"index": i, "value": str(20 + i * 3.5)})\n    print(f"Loaded {len(data)} rows")\n    return data\n\ndef clean_data(data, config):\n    """Clean data: parse values, filter invalid."""\n    cleaned = []\n    for row in data:\n        val = parse_value(row.get("value", ""))\n        if val is not None and is_in_range(val, config.get("min", 0), config.get("max", 100)):\n            cleaned.append({**row, "value": val})\n    print(f"Cleaned: {len(data)} → {len(cleaned)}")\n    return cleaned\n\ndef analyze(clean_data, config):\n    """Analyze data: compute stats, classify."""\n    values = [r["value"] for r in clean_data]\n    stats = summarize(values)\n    print(f"Analysis: mean={stats[\'mean\']:.2f}")\n    return {"analysis_summary": stats}\n\n# Run the pipeline!\nconfig = {"n_points": 20, "min": 0, "max": 80}\ndata = load_data(config)\ncleaned = clean_data(data, config)\nresults = analyze(cleaned, config)\nprint("\\nResults:", results)'),
            ],
            "hw": [
                '# HW1: Write a function that takes a list and returns\n# a new list with duplicates removed (keep first occurrence)\n\n',
                '# HW2: Write three small helper functions and one main function\n# that calls all three. Example: compute_stats calls mean(), std(), median()\n\n',
                '# HW3: Refactor this messy code into clean functions:\ndata = [10, 20, 30, 40, 50]\ntotal = 0\nfor x in data:\n    total += x\nmean = total / len(data)\ndev = 0\nfor x in data:\n    dev += (x - mean) ** 2\nstd = (dev / len(data)) ** 0.5\nprint(f"Mean: {mean}, Std: {std}")\n',
                '# HW4: Write a complete mini-pipeline with:\n# load_data() -> clean_data() -> analyze() -> print_report()\n# Test it end-to-end\n\n',
                '# HW5 (Challenge): Write a function that accepts another function\n# as a parameter. Example: apply_to_all(data, transform_func)\n\n',
            ],
        },
        10: {
            "objectives": "- Write clean, reusable helper functions\n- Follow DRY principle (Don't Repeat Yourself)\n- Add docstrings to functions\n- Improve function decomposition",
            "parts": [
                ("Part 1: DRY — Don't Repeat Yourself", '# BAD: repeated logic\ndef process_temps(data):\n    total = 0\n    for v in data:\n        total += v\n    return total / len(data)\n\ndef process_pressure(data):\n    total = 0\n    for v in data:\n        total += v\n    return total / len(data)\n\n# GOOD: one reusable function\ndef mean(data):\n    """Calculate mean of any numeric list."""\n    if not data:\n        return 0\n    return sum(data) / len(data)\n\ntemps = [20, 25, 30]\npressures = [101, 102, 100]\nprint(f"Mean temp: {mean(temps)}")\nprint(f"Mean pressure: {mean(pressures)}")'),
                ("Part 2: Default Parameters & Flexibility", 'def clean_column(data, column="value", min_val=0, max_val=100, drop_missing=True):\n    """Clean a specific column from data rows.\n    \n    Args:\n        data: list of dicts\n        column: which key to clean (default: "value")\n        min_val: minimum valid value (default: 0)\n        max_val: maximum valid value (default: 100)\n        drop_missing: skip rows with missing values (default: True)\n    \n    Returns:\n        list of dicts with valid values\n    """\n    result = []\n    for row in data:\n        val = row.get(column)\n        if val is None and drop_missing:\n            continue\n        try:\n            num = float(val)\n        except (ValueError, TypeError):\n            continue\n        if min_val <= num <= max_val:\n            result.append({**row, column: num})\n    return result\n\n# Use with defaults\ndata = [{"value": "25"}, {"value": ""}, {"value": "50"}]\nprint(clean_column(data))\n\n# Use with custom settings\nprint(clean_column(data, min_val=30, max_val=100))'),
                ("Part 3: Docstrings", 'def analyze_pipeline(data, config):\n    """Run the full analysis pipeline.\n    \n    This function orchestrates the complete data analysis:\n    1. Extract numeric values\n    2. Compute summary statistics\n    3. Classify each value\n    4. Return structured results\n    \n    Args:\n        data (list[dict]): Cleaned data rows, each with a \"value\" key.\n        config (dict): Configuration with optional \"threshold\" key.\n    \n    Returns:\n        dict: Results containing:\n            - \"stats\": dict with count, mean, std, min, max\n            - \"labels\": list of labels for each value\n            - \"summary\": text summary\n    \n    Example:\n        >>> results = analyze_pipeline([{\"value\": 10}], {\"threshold\": 5})\n        >>> results[\"stats\"][\"mean\"]\n        10.0\n    """\n    values = [row["value"] for row in data]\n    if not values:\n        return {"stats": {}, "labels": [], "summary": "No data"}\n    \n    m = sum(values) / len(values)\n    threshold = config.get("threshold", m * 1.5)\n    labels = ["high" if v > threshold else "normal" for v in values]\n    \n    return {\n        "stats": {"count": len(values), "mean": round(m, 2)},\n        "labels": labels,\n        "summary": f"{len(values)} values analyzed, {labels.count(\'high\')} high"\n    }\n\n# Test\nresult = analyze_pipeline([{"value": 10}, {"value": 50}, {"value": 20}], {"threshold": 30})\nprint(result["summary"])\n\n# You can view the docstring with help()\nhelp(analyze_pipeline)'),
            ],
            "hw": [
                '# HW1: Find 3 places in your project code where you repeat logic.\n# Refactor them into shared helper functions.\n\n',
                '# HW2: Add docstrings to ALL of your pipeline functions\n# (load_data, clean_data, analyze, plot, export_results)\n\n',
                '# HW3: Write a \"utility\" module with at least 5 reusable helpers:\n# mean(), median(), std(), is_numeric(), safe_float()\n\n',
                '# HW4: Create a function with 4+ parameters, each with defaults.\n# Show 3 different ways to call it.\n\n',
                '# HW5 (Challenge): Write a function decorator that prints\n# "Calling function_name..." before each call\n# Hint: research Python decorators\n\n',
            ],
        },
        11: {
            "objectives": "- Handle errors with try/except\n- Use different exception types\n- Skip bad rows and count reasons\n- Make `clean_data()` report skipped rows",
            "parts": [
                ("Part 1: try/except Basics", 'def safe_float(text):\n    """Convert text to float safely."""\n    try:\n        return float(text)\n    except (ValueError, TypeError):\n        return None\n\n# Test\ntest_values = ["42", "3.14", "abc", "", None, "  7  "]\nfor v in test_values:\n    result = safe_float(v)\n    print(f"  {str(v):>8} → {result}")'),
                ("Part 2: Different Exception Types", '# Common exceptions you\'ll encounter:\n\n# ValueError: wrong type of value\ntry:\n    int("abc")\nexcept ValueError as e:\n    print(f"ValueError: {e}")\n\n# KeyError: missing dictionary key\ntry:\n    d = {"a": 1}\n    print(d["b"])\nexcept KeyError as e:\n    print(f"KeyError: {e}")\n\n# FileNotFoundError\ntry:\n    with open("nonexistent.txt") as f:\n        pass\nexcept FileNotFoundError as e:\n    print(f"FileNotFoundError: {e}")\n\n# TypeError: wrong operation for type\ntry:\n    "hello" + 5\nexcept TypeError as e:\n    print(f"TypeError: {e}")'),
                ("Part 3: Robust clean_data with Skip Reporting", 'def clean_data_robust(data, config):\n    """Clean data with detailed skip reporting.\n    \n    Returns:\n        tuple: (cleaned_list, report_dict)\n    """\n    cleaned = []\n    report = {"missing": 0, "non_numeric": 0, "out_of_range": 0, "other": 0}\n    \n    min_val = config.get("min_value", float("-inf"))\n    max_val = config.get("max_value", float("inf"))\n    \n    for i, row in enumerate(data):\n        try:\n            val = row.get("value")\n            \n            # Check missing\n            if val is None or str(val).strip() == "":\n                report["missing"] += 1\n                continue\n            \n            # Convert to number\n            try:\n                num = float(val)\n            except (ValueError, TypeError):\n                report["non_numeric"] += 1\n                continue\n            \n            # Check range\n            if num < min_val or num > max_val:\n                report["out_of_range"] += 1\n                continue\n            \n            cleaned.append({**row, "value": num})\n            \n        except Exception as e:\n            report["other"] += 1\n            print(f"  Unexpected error at row {i}: {e}")\n    \n    total_dropped = sum(report.values())\n    print(f"Cleaning: {len(data)} raw → {len(cleaned)} clean ({total_dropped} dropped)")\n    for reason, count in report.items():\n        if count > 0:\n            print(f"  - {reason}: {count}")\n    \n    return cleaned, report\n\n# Test\nraw = [\n    {"id": 1, "value": "25.0"},\n    {"id": 2, "value": ""},\n    {"id": 3, "value": "abc"},\n    {"id": 4, "value": "500"},\n    {"id": 5, "value": None},\n    {"id": 6, "value": "42.0"},\n]\n\nconfig = {"min_value": 0, "max_value": 100}\ncleaned, report = clean_data_robust(raw, config)\nprint(f"\\nReport: {report}")'),
            ],
            "hw": [
                '# HW1: Write a function read_numbers(text_list) that converts\n# a list of strings to numbers, skipping invalid ones.\n# Return (numbers, error_count)\ndata = ["10", "abc", "20.5", "", "30", "xyz", "40"]\n',
                '# HW2: Write a safe_divide(a, b) function that handles ZeroDivisionError\n\n',
                '# HW3: Update YOUR clean_data() to track skip reasons\n# Return (cleaned, {"missing": N, "bad_type": N, "out_of_range": N})\n\n',
                '# HW4: Write a function that reads a file safely\n# If the file doesn\'t exist, return a default value instead of crashing\n\n',
                '# HW5 (Challenge): Create a \"validation chain\" — a list of functions.\n# Each function checks one rule. If any fails, the row is dropped.\n# Log which rule caused the drop.\n\n',
            ],
        },
        12: {
            "objectives": "- Read CSV files with Python\n- Write cleaned data to CSV\n- Create and write JSON files\n- Implement `export_results()` properly",
            "parts": [
                ("Part 1: Reading CSV Files", 'import csv\nimport os\n\n# Create a sample CSV for testing\nos.makedirs("data/raw", exist_ok=True)\nwith open("data/raw/sample.csv", "w", newline="") as f:\n    writer = csv.writer(f)\n    writer.writerow(["id", "timestamp", "value", "status"])\n    writer.writerow([1, "2024-01-01", "25.3", "ok"])\n    writer.writerow([2, "2024-01-02", "88.1", "warning"])\n    writer.writerow([3, "2024-01-03", "", "error"])\n    writer.writerow([4, "2024-01-04", "42.0", "ok"])\n    writer.writerow([5, "2024-01-05", "abc", "error"])\nprint("Created sample.csv")\n\n# Read it back\nwith open("data/raw/sample.csv", "r") as f:\n    reader = csv.DictReader(f)\n    data = list(reader)\n\nfor row in data:\n    print(row)'),
                ("Part 2: Writing CSV and JSON", 'import json\n\n# Write cleaned CSV\nos.makedirs("data/cleaned", exist_ok=True)\nclean = [row for row in data if row["value"] and row["status"] == "ok"]\n\nwith open("data/cleaned/cleaned.csv", "w", newline="") as f:\n    writer = csv.DictWriter(f, fieldnames=["id", "timestamp", "value", "status"])\n    writer.writeheader()\n    writer.writerows(clean)\nprint(f"Wrote {len(clean)} rows to cleaned.csv")\n\n# Write JSON report\nos.makedirs("reports", exist_ok=True)\nreport = {\n    "project_name": "my_project",\n    "track": "data",\n    "version": "v1",\n    "dataset": {"n_raw": len(data), "n_clean": len(clean), "n_dropped": len(data) - len(clean)},\n    "analysis_summary": {"mean": 33.65, "min": 25.3, "max": 42.0},\n    "figures": ["timeseries.png", "summary.png"],\n}\n\nwith open("reports/report.json", "w") as f:\n    json.dump(report, f, indent=2)\nprint("Wrote report.json")'),
                ("Part 3: Building export_results()", 'def export_results(clean_data, results, figures, config):\n    """Export all pipeline outputs to required paths."""\n    exported = {}\n    \n    # 1. Export cleaned CSV\n    csv_path = config.get("cleaned_data_path", "data/cleaned/cleaned.csv")\n    os.makedirs(os.path.dirname(csv_path), exist_ok=True)\n    if clean_data:\n        keys = list(clean_data[0].keys())\n        with open(csv_path, "w", newline="") as f:\n            w = csv.DictWriter(f, fieldnames=keys)\n            w.writeheader()\n            w.writerows(clean_data)\n        exported["cleaned_csv"] = csv_path\n        print(f"Exported: {csv_path}")\n    \n    # 2. Export report.json\n    report_path = config.get("report_path", "reports/report.json")\n    os.makedirs(os.path.dirname(report_path), exist_ok=True)\n    with open(report_path, "w") as f:\n        json.dump(results, f, indent=2)\n    exported["report"] = report_path\n    print(f"Exported: {report_path}")\n    \n    return exported\n\n# Test it\nexported = export_results(\n    clean,\n    report,\n    [],\n    {"cleaned_data_path": "data/cleaned/cleaned.csv", "report_path": "reports/report.json"}\n)\nprint(f"\\nExported files: {exported}")'),
            ],
            "hw": [
                '# HW1: Write a function load_csv(path) that reads any CSV file\n# and returns a list of dictionaries\n\n',
                '# HW2: Write a function save_csv(data, path) that writes\n# a list of dictionaries to a CSV file\n\n',
                '# HW3: Create a complete export_results() for your track\n# that writes: cleaned.csv, report.json\n\n',
                '# HW4: Write a function that reads report.json back\n# and prints a formatted summary\n\n',
                '# HW5 (Challenge): Write a function that can export to\n# multiple formats (CSV, JSON, TXT) based on a config setting\n\n',
            ],
        },
        13: {
            "objectives": "- Create plots with matplotlib\n- Build `plot()` function for the pipeline\n- Combine all pipeline stages end-to-end\n- Generate required figures (timeseries + summary)",
            "parts": [
                ("Part 1: Matplotlib Basics", 'import matplotlib\nmatplotlib.use("Agg")\nimport matplotlib.pyplot as plt\nimport os\n\n# Simple line plot\ndata = [10, 15, 13, 18, 20, 17, 22, 25, 23, 28]\n\nplt.figure(figsize=(10, 4))\nplt.plot(data, marker="o", color="steelblue")\nplt.title("My First Plot")\nplt.xlabel("Time Step")\nplt.ylabel("Value")\nplt.grid(True, alpha=0.3)\nos.makedirs("reports/figures", exist_ok=True)\nplt.savefig("reports/figures/test_plot.png", dpi=100, bbox_inches="tight")\nplt.show()\nprint("Plot saved!")'),
                ("Part 2: Histogram & Multiple Plots", '# Histogram\nimport random\nrandom.seed(42)\nvalues = [random.gauss(50, 15) for _ in range(200)]\n\nfig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))\n\n# Left: time series\nax1.plot(values, linewidth=0.8, color="steelblue")\nax1.set_title("Time Series")\nax1.set_xlabel("Index")\nax1.set_ylabel("Value")\nax1.grid(True, alpha=0.3)\n\n# Right: histogram\nax2.hist(values, bins=20, color="steelblue", edgecolor="white")\nax2.set_title("Distribution")\nax2.set_xlabel("Value")\nax2.set_ylabel("Count")\nax2.axvline(sum(values)/len(values), color="red", label="Mean")\nax2.legend()\n\nplt.tight_layout()\nplt.savefig("reports/figures/combined.png", dpi=100)\nplt.show()'),
                ("Part 3: Pipeline plot() Function", 'def plot(clean_data, results, config):\n    """Create and save required figures.\n    \n    Creates:\n    - timeseries.png: line plot of values over time\n    - summary.png: histogram of value distribution\n    """\n    values = [row["value"] for row in clean_data if "value" in row]\n    if not values:\n        print("No data to plot")\n        return []\n    \n    fig_dir = config.get("figures_dir", "reports/figures")\n    os.makedirs(fig_dir, exist_ok=True)\n    figures = []\n    \n    # Figure 1: Time Series\n    fig1, ax = plt.subplots(figsize=(10, 4))\n    ax.plot(values, linewidth=0.8, color="steelblue")\n    ax.set_title(f"{config.get(\'project_name\', \'Project\')} — Time Series")\n    ax.set_xlabel("Index")\n    ax.set_ylabel("Value")\n    ax.grid(True, alpha=0.3)\n    \n    threshold = config.get("threshold")\n    if threshold:\n        ax.axhline(y=threshold, color="red", linestyle="--", label=f"Threshold={threshold}")\n        ax.legend()\n    \n    path1 = os.path.join(fig_dir, "timeseries.png")\n    fig1.savefig(path1, dpi=100, bbox_inches="tight")\n    figures.append(fig1)\n    plt.close(fig1)\n    print(f"Saved: {path1}")\n    \n    # Figure 2: Summary\n    fig2, ax = plt.subplots(figsize=(8, 4))\n    ax.hist(values, bins=min(20, len(values)//5+1), color="steelblue", edgecolor="white")\n    ax.set_title("Value Distribution")\n    ax.set_xlabel("Value")\n    ax.set_ylabel("Count")\n    \n    summary = results.get("analysis_summary", {})\n    if "mean" in summary:\n        ax.axvline(summary["mean"], color="red", label=f"Mean={summary[\'mean\']}")\n        ax.legend()\n    \n    path2 = os.path.join(fig_dir, "summary.png")\n    fig2.savefig(path2, dpi=100, bbox_inches="tight")\n    figures.append(fig2)\n    plt.close(fig2)\n    print(f"Saved: {path2}")\n    \n    return figures\n\n# Test with sample data\ntest_data = [{"value": random.gauss(50, 10)} for _ in range(100)]\ntest_results = {"analysis_summary": {"mean": 50}}\ntest_config = {"project_name": "Test", "figures_dir": "reports/figures", "threshold": 65}\nplot(test_data, test_results, test_config)'),
            ],
            "hw": [
                '# HW1: Create a scatter plot of two related variables\n\n',
                '# HW2: Create a bar chart showing counts by category\n\n',
                '# HW3: Run YOUR complete pipeline end-to-end:\n# load_data → clean_data → analyze → plot → export_results\n# Verify all exports exist\n\n',
                '# HW4: Add a third figure to your plot() function\n# (box plot, scatter, or bar chart)\n\n',
                '# HW5 (Challenge): Create a \"dashboard\" with 4 subplots\n# showing different views of your data\n\n',
            ],
        },
        14: {
            "objectives": "- Run the complete v1 pipeline end-to-end\n- Pass all universal checks\n- Verify all required exports\n- Prepare for the v1 demo",
            "parts": [
                ("Part 1: v1 Release Checklist", '# v1 Release Checklist\nchecklist = [\n    "load_data() loads raw data correctly",\n    "clean_data() filters invalid rows and reports drops",\n    "analyze() returns dict with 3+ numeric metrics",\n    "plot() creates timeseries.png and summary.png",\n    "export_results() writes cleaned.csv and report.json",\n    "self_check() passes all assertions",\n    "All required exports exist at correct paths",\n    "report.json has all required keys",\n    "Plots have titles, axis labels, and are readable",\n    "No input() calls anywhere",\n]\n\nprint("=== v1 Release Checklist ===")\nfor i, item in enumerate(checklist, 1):\n    print(f"  [ ] {i}. {item}")'),
                ("Part 2: Run Full Pipeline", 'import csv, json, os\n\n# === DEFINE YOUR PIPELINE FUNCTIONS HERE ===\n# (Or import from /src if you\'ve modularized)\n\ndef get_config():\n    return {\n        "project_name": "my_project",\n        "track": "data",\n        "version": "v1",\n        "raw_data_path": "data/raw/sample.csv",\n        "cleaned_data_path": "data/cleaned/cleaned.csv",\n        "report_path": "reports/report.json",\n        "figures_dir": "reports/figures",\n        "min_value": 0,\n        "max_value": 100,\n        "threshold": 60,\n    }\n\nconfig = get_config()\nprint(f"Project: {config[\'project_name\']} ({config[\'track\']}) {config[\'version\']}")\nprint(f"Running full pipeline...")\n\n# Step 1: Load\n# data = load_data(config)\n\n# Step 2: Clean\n# cleaned = clean_data(data, config)\n\n# Step 3: Analyze\n# results = analyze(cleaned, config)\n\n# Step 4: Plot\n# figures = plot(cleaned, results, config)\n\n# Step 5: Export\n# exported = export_results(cleaned, results, figures, config)\n\nprint("\\n=== Pipeline complete! ===")\nprint("Uncomment the steps above once your functions are ready.")'),
                ("Part 3: Self-Check", 'def self_check():\n    """Comprehensive self-check for v1 release."""\n    print("=== Running Self-Check ===")\n    passed = 0\n    failed = 0\n    \n    # Check 1: Required files exist\n    required_files = [\n        "data/cleaned/cleaned.csv",\n        "reports/report.json",\n        "reports/figures/timeseries.png",\n        "reports/figures/summary.png",\n    ]\n    for f in required_files:\n        if os.path.exists(f) and os.path.getsize(f) > 0:\n            print(f"  [PASS] {f} exists")\n            passed += 1\n        else:\n            print(f"  [FAIL] {f} missing or empty")\n            failed += 1\n    \n    # Check 2: report.json has required keys\n    try:\n        with open("reports/report.json") as f:\n            report = json.load(f)\n        required_keys = ["project_name", "track", "version", "dataset", "analysis_summary", "figures"]\n        for key in required_keys:\n            assert key in report, f"report.json missing key: {key}"\n        print(f"  [PASS] report.json has all required keys")\n        passed += 1\n    except Exception as e:\n        print(f"  [FAIL] report.json check: {e}")\n        failed += 1\n    \n    print(f"\\n=== Results: {passed} passed, {failed} failed ===")\n    if failed == 0:\n        print("CONGRATULATIONS! Your v1 is ready for demo!")\n    else:\n        print("Fix the failures above before demo.")\n\nself_check()'),
            ],
            "hw": [
                '# HW1: Run self_check() on your project and fix any failures\n\n',
                '# HW2: Prepare a 2-minute demo script:\n# - What does your project do?\n# - Show one interesting finding\n# - Show one plot\n\n',
                '# HW3: Review your code — add comments explaining the WHY\n# for your 3 most complex functions\n\n',
                '# HW4: Write a summary of what you learned in CP1\n# (This helps you prepare for CP2!)\n\n',
            ],
        },
    }

    cells = [
        md(f"# CP1 Week {week_num} — {title}\n\n## Learning Objectives\n{week_content[week_num]['objectives']}"),
        setup_cell(),
    ]

    for part_title, part_code in week_content[week_num]["parts"]:
        cells.append(md(f"---\n## {part_title}"))
        cells.append(code(part_code))

    cells.append(md("---\n## Mini-Quiz"))
    cells.append(code(f"# Q1: What was the most important concept from Week {week_num}?\n# Answer: \n\n# Q2: How does this week's concept connect to your pipeline?\n# Answer: "))

    cells.append(md("---\n## Homework\n\nComplete these exercises before next week:"))
    for i, hw in enumerate(week_content[week_num]["hw"], 1):
        cells.append(code(hw))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# STUDIO NOTEBOOK GENERATORS (track-specific)
# ============================================================

TRACK_DATA = {
    "robotics": {
        "name": "Robotics/Mechatronics",
        "product": "MechaSense Studio",
        "dataset_desc": "sensor readings (temperature, RPM, vibration)",
        "sample_data": '[{"timestamp": "00:01", "temp": 25.3, "rpm": 1500, "vibration": 12},\n {"timestamp": "00:02", "temp": 26.1, "rpm": 1520, "vibration": 13},\n {"timestamp": "00:03", "temp": 85.0, "rpm": 3500, "vibration": 55},\n {"timestamp": "00:04", "temp": 24.8, "rpm": 1490, "vibration": 11},\n {"timestamp": "00:05", "temp": -5.0, "rpm": 0, "vibration": 0}]',
        "value_col": "temp",
        "threshold": 60,
        "range": "(0, 150)",
    },
    "data": {
        "name": "Data/AI",
        "product": "CleanReport Pipeline",
        "dataset_desc": "messy survey/CSV data with missing values and inconsistent types",
        "sample_data": '[{"id": 1, "age": "25", "score": "88.5", "city": "Cairo"},\n {"id": 2, "age": "", "score": "92.0", "city": "Alex"},\n {"id": 3, "age": "abc", "score": "75.0", "city": ""},\n {"id": 4, "age": "30", "score": "-10", "city": "Cairo"},\n {"id": 5, "age": "22", "score": "95.5", "city": "Luxor"}]',
        "value_col": "score",
        "threshold": 80,
        "range": "(0, 100)",
    },
    "simulation": {
        "name": "Simulation/Games",
        "product": "SimLab Engine",
        "dataset_desc": "simulation timestep logs with position, velocity, and score",
        "sample_data": '[{"step": 0, "x": 0.0, "y": 0.0, "velocity": 1.0, "score": 0},\n {"step": 1, "x": 1.0, "y": 0.5, "velocity": 1.2, "score": 10},\n {"step": 2, "x": 2.1, "y": 1.2, "velocity": -0.5, "score": 20},\n {"step": 3, "x": 3.0, "y": 2.0, "velocity": 1.5, "score": 35},\n {"step": 4, "x": 4.2, "y": 2.8, "velocity": 999, "score": -1}]',
        "value_col": "score",
        "threshold": 25,
        "range": "(0, 500)",
    },
    "space": {
        "name": "Space/Astro",
        "product": "Lightcurve Explorer",
        "dataset_desc": "star brightness (flux) measurements over time",
        "sample_data": '[{"time": 0.0, "flux": 1.000, "sector": "A"},\n {"time": 0.1, "flux": 0.998, "sector": "A"},\n {"time": 0.2, "flux": 0.700, "sector": "A"},\n {"time": 0.3, "flux": 0.985, "sector": "A"},\n {"time": 0.4, "flux": -0.1, "sector": "B"},\n {"time": 0.5, "flux": 1.010, "sector": "B"}]',
        "value_col": "flux",
        "threshold": 0.9,
        "range": "(0, 2)",
    },
    "iot": {
        "name": "IoT/Reporting",
        "product": "AutoDashboard Reporter",
        "dataset_desc": "IoT sensor time series (temperature, humidity, pressure)",
        "sample_data": '[{"ts": "2024-01-01 00:00", "device": "D01", "temp": 22.5, "humidity": 45},\n {"ts": "2024-01-01 01:00", "device": "D01", "temp": 23.0, "humidity": 47},\n {"ts": "2024-01-01 02:00", "device": "D02", "temp": "", "humidity": 50},\n {"ts": "2024-01-01 03:00", "device": "D01", "temp": 99.9, "humidity": 30},\n {"ts": "2024-01-01 04:00", "device": "D02", "temp": 21.8, "humidity": 48}]',
        "value_col": "temp",
        "threshold": 35,
        "range": "(0, 60)",
    },
}

# Weekly studio descriptions per track
STUDIO_WEEKLY = {
    1: {"task": "Set up your project repo stub and explore your track's sample data", "deliverable": "repo runs + placeholder self_check() passes"},
    2: {"task": "Create config dict for your track and use it in load_data()", "deliverable": "config used by at least one function"},
    3: {"task": "Implement validation rules in clean_data() for your track's data", "deliverable": "clean_data() implements basic rules"},
    4: {"task": "Build analyze() that classifies/labels your track's data", "deliverable": "analyze() returns labeled outputs"},
    5: {"task": "Compute summary statistics using loops on your track data", "deliverable": "summary stats correct on toy dataset"},
    6: {"task": "Detect and count events in your track data (threshold crossings)", "deliverable": "event counts + edge-case handling"},
    7: {"task": "Implement moving-window operations on your track data", "deliverable": "moving-window metric via loop"},
    8: {"task": "Parse raw text/CSV data into structured records for your track", "deliverable": "parser handles multiple formats/errors"},
    9: {"task": "Refactor your code into clean pipeline functions", "deliverable": "pipeline functions exist and are used"},
    10: {"task": "Improve function decomposition, add docstrings, reduce duplication", "deliverable": "clearer separation + basic docstrings"},
    11: {"task": "Add robust error handling to clean_data() — skip and count bad rows", "deliverable": "clean_data() reports skipped counts"},
    12: {"task": "Implement full file I/O: read CSV, write cleaned.csv and report.json", "deliverable": "export_results() writes required files"},
    13: {"task": "Build plot() and run the complete pipeline end-to-end", "deliverable": "plot() creates at least 1 figure"},
    14: {"task": "Final integration, pass universal check, prepare demo", "deliverable": "v1 passes universal check + exports + demo"},
}


def make_studio(week_num, track_key):
    """Generate a studio notebook for a specific week and track."""
    track = TRACK_DATA[track_key]
    studio = STUDIO_WEEKLY[week_num]

    cells = [
        md(f"# CP1 Week {week_num} Studio — {track['product']}\n**Track:** {track['name']}\n**Task:** {studio['task']}\n**Deliverable:** {studio['deliverable']}"),
        setup_cell(),
        md(f"---\n## Your Track Data\n\n**{track['product']}** works with {track['dataset_desc']}.\n\nHere's your sample data:"),
        code(f"# Sample data for {track['name']} track\nsample_data = {track['sample_data']}\n\nprint(f\"Loaded {{len(sample_data)}} rows\")\nfor row in sample_data:\n    print(f\"  {{row}}\")"),
    ]

    # Must-pass core
    cells.append(md(f"---\n## Must-Pass Core\n\nYou MUST complete this before moving on."))

    if week_num <= 2:
        cells.append(code(f'# Must-pass: Create your config and verify data loads\nconfig = {{\n    "project_name": "{track["product"].lower().replace(" ", "_")}",\n    "track": "{track_key}",\n    "version": "v1",\n    "value_column": "{track["value_col"]}",\n    "threshold": {track["threshold"]},\n}}\n\nprint("Config:")\nfor k, v in config.items():\n    print(f"  {{k}}: {{v}}")\n\n# Verify sample data structure\nassert len(sample_data) > 0, "Need at least 1 row"\nassert "{track["value_col"]}" in sample_data[0], "Missing {track["value_col"]} column"\nprint("\\nMust-pass core: PASSED!")'))
    elif week_num <= 4:
        cells.append(code(f'# Must-pass: Implement basic validation for {track["value_col"]}\ndef clean_data(data, config):\n    """Clean {track["name"]} data."""\n    cleaned = []\n    dropped = 0\n    \n    for row in data:\n        val = row.get("{track["value_col"]}")\n        \n        # Rule: skip missing/invalid values\n        if val is None or val == "":\n            dropped += 1\n            continue\n        \n        try:\n            num = float(val)\n        except (ValueError, TypeError):\n            dropped += 1\n            continue\n        \n        # Rule: must be in range {track["range"]}\n        low, high = {track["range"]}\n        if num < low or num > high:\n            dropped += 1\n            continue\n        \n        cleaned.append({{**row, "{track["value_col"]}": num}})\n    \n    print(f"Cleaned: {{len(data)}} → {{len(cleaned)}} ({{dropped}} dropped)")\n    return cleaned\n\n# Test it\nresult = clean_data(sample_data, config)\nprint(f"\\nClean rows:")\nfor row in result:\n    print(f"  {{row}}")\n\nassert len(result) < len(sample_data), "Should have dropped at least 1 row"\nprint("\\nMust-pass core: PASSED!")'))
    elif week_num <= 8:
        cells.append(code(f'# Must-pass: Compute basic stats on {track["value_col"]}\nvalues = []\nfor row in sample_data:\n    try:\n        values.append(float(row["{track["value_col"]}"]))\n    except (ValueError, TypeError, KeyError):\n        pass\n\nif values:\n    total = sum(values)\n    count = len(values)\n    mean = total / count\n    print(f"Count: {{count}}")\n    print(f"Mean {track["value_col"]}: {{mean:.2f}}")\n    print(f"Min: {{min(values)}}")\n    print(f"Max: {{max(values)}}")\n    \n    above = sum(1 for v in values if v > {track["threshold"]})\n    print(f"Above threshold ({track["threshold"]}): {{above}}")\n\nprint("\\nMust-pass core: PASSED!")'))
    else:
        cells.append(code(f'# Must-pass: Run pipeline end-to-end for {track["product"]}\nconfig = {{\n    "project_name": "{track["product"].lower().replace(" ", "_")}",\n    "track": "{track_key}",\n    "version": "v1",\n    "value_column": "{track["value_col"]}",\n    "threshold": {track["threshold"]},\n}}\n\n# TODO: Implement or import your pipeline functions\n# data = load_data(config)\n# cleaned = clean_data(data, config)\n# results = analyze(cleaned, config)\n# figures = plot(cleaned, results, config)\n# exported = export_results(cleaned, results, figures, config)\n\nprint("TODO: Uncomment and implement the pipeline steps above")\nprint("Must-pass core: check your implementation!")'))

    # Standard target
    cells.append(md("---\n## Standard Target\n\nIf you finished the must-pass core, continue here:"))
    cells.append(code(f'# Standard target for Week {week_num}\n# {studio["task"]}\n\n# TODO: Extend your implementation to handle:\n# 1. Multiple data formats\n# 2. Better error messages\n# 3. More detailed output\n\nprint("Work on the standard target now...")'))

    # Stretch
    cells.append(md("---\n## Stretch (Optional)\n\nFor fast students who finished the standard target:"))
    cells.append(code(f'# Stretch goal for Week {week_num}\n# Add one extra feature that makes your {track["product"]} better.\n# Ideas:\n# - Extra validation rule\n# - Additional metric or classification\n# - Better formatting or reporting\n\nprint("Stretch goal: add your improvement here")'))

    # Take-home
    cells.append(md(f"---\n## Take-Home Tasks\n\n1. Make sure your must-pass core works completely\n2. If you didn't finish the standard target, complete it at home\n3. Review the core notebook concepts from Week {week_num}\n4. Push your code to GitHub"))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# CHECK NOTEBOOK GENERATOR
# ============================================================

def make_check(week_num):
    """Generate a universal check notebook for the week."""
    cells = [
        md(f"# CP1 Week {week_num} — Universal Check\n\nThis notebook validates your pipeline for Week {week_num}.\nRun all cells. Fix any FAIL results in your `/src` code."),
        setup_cell(),
        md("---\n## Setup: Define Expected Behavior"),
    ]

    if week_num <= 3:
        cells.append(code(f'import os\n\nprint("=== CP1 Week {week_num} Universal Check ===")\nprint()\n\npassed = 0\nfailed = 0\n\n# Check 1: Config exists\ntry:\n    config = {{\n        "project_name": "test",\n        "track": "test",\n        "version": "v1",\n    }}\n    assert isinstance(config, dict)\n    assert "project_name" in config\n    print("[PASS] Config is a valid dict with required keys")\n    passed += 1\nexcept Exception as e:\n    print(f"[FAIL] Config check: {{e}}")\n    failed += 1\n\n# Check 2: Pipeline stubs exist\ntry:\n    # If using /src imports:\n    # from project_template.io import load_data\n    # For now, check that functions are defined\n    print("[INFO] Checking if pipeline functions are defined...")\n    print("[PASS] Basic structure check")\n    passed += 1\nexcept Exception as e:\n    print(f"[FAIL] Function check: {{e}}")\n    failed += 1\n\nprint(f"\\n=== Results: {{passed}} passed, {{failed}} failed ===")\nif failed == 0:\n    print("Week {week_num} check PASSED!")\nelse:\n    print("Fix failures before submitting.")'))
    elif week_num <= 8:
        cells.append(code(f'import os\n\nprint("=== CP1 Week {week_num} Universal Check ===")\nprint()\n\npassed = 0\nfailed = 0\n\n# Toy dataset for testing\ntoy_data = [\n    {{"id": 1, "value": "25.0"}},\n    {{"id": 2, "value": ""}},\n    {{"id": 3, "value": "abc"}},\n    {{"id": 4, "value": "50.5"}},\n    {{"id": 5, "value": "-10"}},\n    {{"id": 6, "value": "75.0"}},\n]\n\nconfig = {{"min_value": 0, "max_value": 100, "project_name": "test", "track": "test", "version": "v1"}}\n\n# Check 1: clean_data exists and works\ntry:\n    # result = clean_data(toy_data, config)\n    # For now, simulate:\n    result = [row for row in toy_data if row["value"] not in ("", "abc", "-10")]\n    assert isinstance(result, list), "clean_data must return a list"\n    assert len(result) == 3, f"Expected 3 clean rows, got {{len(result)}}"\n    print("[PASS] clean_data returns correct count")\n    passed += 1\nexcept Exception as e:\n    print(f"[FAIL] clean_data: {{e}}")\n    failed += 1\n\n# Check 2: analyze exists and returns dict\ntry:\n    # results = analyze(result, config)\n    results = {{"analysis_summary": {{"mean": 50.17, "count": 3}}}}\n    assert isinstance(results, dict)\n    assert "analysis_summary" in results\n    summary = results["analysis_summary"]\n    assert len(summary) >= 2, "Need at least 2 metrics"\n    print("[PASS] analyze returns dict with metrics")\n    passed += 1\nexcept Exception as e:\n    print(f"[FAIL] analyze: {{e}}")\n    failed += 1\n\nprint(f"\\n=== Results: {{passed}} passed, {{failed}} failed ===")\nif failed == 0:\n    print("Week {week_num} check PASSED!")\nelse:\n    print("Fix failures before submitting.")'))
    else:
        cells.append(code(f'import os, json\n\nprint("=== CP1 Week {week_num} Universal Check ===")\nprint()\n\npassed = 0\nfailed = 0\n\n# Check 1: Required exports exist\nrequired_files = [\n    "data/cleaned/cleaned.csv",\n    "reports/report.json",\n]\nif {week_num} >= 13:\n    required_files.extend([\n        "reports/figures/timeseries.png",\n        "reports/figures/summary.png",\n    ])\n\nfor filepath in required_files:\n    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:\n        print(f"[PASS] {{filepath}} exists ({{os.path.getsize(filepath)}} bytes)")\n        passed += 1\n    else:\n        print(f"[FAIL] {{filepath}} missing or empty")\n        failed += 1\n\n# Check 2: report.json schema\ntry:\n    with open("reports/report.json") as f:\n        report = json.load(f)\n    \n    required_keys = ["project_name", "track", "version"]\n    for key in required_keys:\n        assert key in report, f"Missing key: {{key}}"\n    print("[PASS] report.json has required keys")\n    passed += 1\nexcept FileNotFoundError:\n    print("[FAIL] report.json not found")\n    failed += 1\nexcept Exception as e:\n    print(f"[FAIL] report.json: {{e}}")\n    failed += 1\n\n# Check 3: No input() calls\ntry:\n    import ast\n    # Check src files for input() calls\n    src_files = []\n    for root, dirs, files in os.walk("src"):\n        for f in files:\n            if f.endswith(".py"):\n                src_files.append(os.path.join(root, f))\n    \n    found_input = False\n    for filepath in src_files:\n        with open(filepath) as f:\n            content = f.read()\n        if "input(" in content:\n            print(f"[FAIL] Found input() in {{filepath}}")\n            found_input = True\n            failed += 1\n    \n    if not found_input:\n        print("[PASS] No input() calls found in /src")\n        passed += 1\nexcept Exception as e:\n    print(f"[WARN] Could not check for input(): {{e}}")\n\nprint(f"\\n=== Results: {{passed}} passed, {{failed}} failed ===")\nif failed == 0:\n    print("Week {week_num} check PASSED!")\nelse:\n    print("Fix failures and re-run this check.")'))

    return cells


# ============================================================
# HOMEWORK NOTEBOOK GENERATOR
# ============================================================

def make_homework(week_num, title):
    """Generate a standalone homework notebook."""
    hw_content = {
        1: {
            "review": '# Review Exercise: Python Basics\n\n# 1. What does print() do? Write an example.\n\n\n# 2. Name 3 math operators in Python.\n\n\n# 3. What is a variable?\n\n',
            "practice": [
                '# Practice 1: Print a box pattern using print()\n# Expected output:\n# +------+\n# |      |\n# |      |\n# +------+\n\n',
                '# Practice 2: Calculate the area of a circle with radius 7\n# Formula: area = pi * r^2 (use 3.14159 for pi)\n\n',
                '# Practice 3: Create 5 variables with different types (int, float, str, bool)\n# and print each with its type\n\n',
                '# Practice 4: Calculate: if you save $5 per day,\n# how much will you have after 1 year (365 days)?\n\n',
                '# Practice 5: Calculate BMI: weight(kg) / height(m)^2\n# Test with weight=70, height=1.75\n\n',
            ],
            "challenge": [
                '# Challenge 1: Write a program that converts:\n# a) Kilometers to miles (1 km = 0.621371 miles)\n# b) Celsius to Fahrenheit (F = C * 9/5 + 32)\n# c) Hours to seconds\n# Test each conversion with 3 different values\n\n',
                '# Challenge 2: Research and use Python\'s math module\n# Calculate: sqrt(144), ceil(3.2), floor(3.8), pow(2, 10)\nimport math\n\n',
            ],
            "mini_project": '# Mini-Project: Personal Dashboard\n# Create variables for:\n# - Your name, age, major\n# - Current semester, GPA\n# - Hours spent coding this week\n# Print a formatted "dashboard" showing all info nicely\n# Example:\n# ===== Personal Dashboard =====\n# Name: Ahmed | Age: 20\n# Major: Mechatronics Engineering\n# Semester: 3 | GPA: 3.5\n# Coding hours this week: 8\n# ================================\n\n',
        },
        2: {
            "review": '# Review: Variables and Types\n\n# 1. What are the 4 basic Python types?\n\n\n# 2. How do you convert "42" to an integer?\n\n\n# 3. What is an f-string? Write an example.\n\n',
            "practice": [
                '# Practice 1: Create a config dictionary with 8+ keys\n# for your chosen track\n\n',
                '# Practice 2: Use f-strings to format these values:\n# price = 19.99, quantity = 3, tax_rate = 0.14\n# Print: "Subtotal: $59.97 | Tax: $8.40 | Total: $68.37"\n\n',
                '# Practice 3: Swap two variables WITHOUT using a third variable\na = 10\nb = 20\n# After swap: a should be 20, b should be 10\n\n',
                '# Practice 4: Create a dictionary of dictionaries:\n# 3 sensors, each with name, type, unit, last_reading\n\n',
                '# Practice 5: Calculate compound interest\n# Formula: A = P * (1 + r/n)^(nt)\n# P=1000, r=0.05, n=12, t=5\n\n',
            ],
            "challenge": [
                '# Challenge 1: Write a "type checker" that takes any value\n# and prints its type and a description\n# Example: check(42) -> "42 is an int (whole number)"\n\n',
                '# Challenge 2: Create a nested config dictionary:\n# config["cleaning"]["rules"]["temperature"] = {"min": 0, "max": 100}\n# Access and print the nested values\n\n',
            ],
            "mini_project": '# Mini-Project: Unit Converter\n# Create a config dictionary with conversion factors:\n# {"km_to_miles": 0.621371, "c_to_f": [1.8, 32], "kg_to_lb": 2.20462}\n# Use it to convert 5 different measurements\n# Print each conversion formatted nicely with f-strings\n\n',
        },
    }

    # For weeks 3-14, generate a generic homework structure
    if week_num not in hw_content:
        hw_content[week_num] = {
            "review": f'# Review: Week {week_num} Concepts\n\n# 1. What was the main concept this week?\n# Answer: \n\n# 2. How does it connect to your pipeline?\n# Answer: \n\n# 3. Write one example using this concept.\n\n',
            "practice": [
                f'# Practice 1: Apply this week\'s concept to a simple example\n# (Use the examples from the core notebook as a starting point)\n\n',
                f'# Practice 2: Modify the core notebook example to handle\n# a different dataset\n\n',
                f'# Practice 3: Write a function that demonstrates\n# this week\'s main concept\n\n',
                f'# Practice 4: Test your function with at least 3 different inputs\n# including edge cases (empty data, invalid data)\n\n',
                f'# Practice 5: Integrate this week\'s concept into your\n# pipeline code\n\n',
            ],
            "challenge": [
                f'# Challenge 1: Extend this week\'s concept in a creative way\n# (e.g., handle more edge cases, add more features)\n\n',
                f'# Challenge 2: Research one related Python feature online\n# and demonstrate it with an example\n\n',
            ],
            "mini_project": f'# Mini-Project: Build a standalone tool using Week {week_num} concepts\n# Requirements:\n# - Uses at least 3 concepts from this week\n# - Works with sample data\n# - Prints clear, formatted output\n# - Handles at least 2 edge cases\n\n',
        }

    hw = hw_content[week_num]

    cells = [
        md(f"# CP1 Week {week_num} Homework — {title}\n\n**Due:** Before next week's session\n**Estimated time:** 2-4 hours\n\nComplete all Review and Practice exercises. Challenge and Mini-Project are optional but highly recommended."),
        md("---\n## Review Exercises\nThese check your understanding of the concepts:"),
        code(hw["review"]),
        md("---\n## Practice Exercises\nApply the concepts to solve problems:"),
    ]

    for p in hw["practice"]:
        cells.append(code(p))

    cells.append(md("---\n## Challenge Exercises (Optional but Recommended)"))
    for c in hw["challenge"]:
        cells.append(code(c))

    cells.append(md("---\n## Mini-Project"))
    cells.append(code(hw["mini_project"]))

    cells.append(md("---\n## Self-Check\nBefore submitting, verify:"))
    cells.append(code(f'# Self-check: Did you complete everything?\nchecklist = [\n    "All Review exercises answered",\n    "All 5 Practice exercises completed",\n    "Code runs without errors",\n    "Output is clear and formatted",\n    "Edge cases considered",\n]\n\nprint("=== Homework {week_num} Self-Check ===")\nfor item in checklist:\n    print(f"  [ ] {{item}}")\nprint("\\nMark each item [x] when done!")'))

    return cells


# ============================================================
# GENERATE ALL NOTEBOOKS
# ============================================================

print("Generating CP1 notebooks...")

# Special core notebooks (detailed content)
core_generators = {
    1: make_core_w01,
    2: make_core_w02,
    3: make_core_w03,
    4: make_core_w04,
    5: make_core_w05,
}

for week_num, title, concepts, focus in WEEKS:
    wk = f"W{week_num:02d}"

    # Core notebook
    if week_num in core_generators:
        cells = core_generators[week_num]()
    else:
        cells = make_core_generic(week_num, title, concepts, focus)

    nb = notebook(cells, f"CP1 {wk} Core — {title}")
    save_notebook(nb, os.path.join(BASE, f"{wk}_core.ipynb"))
    print(f"  {wk}_core.ipynb")

    # Studio notebooks (5 tracks)
    for track_key in TRACK_DATA:
        cells = make_studio(week_num, track_key)
        nb = notebook(cells, f"CP1 {wk} Studio — {TRACK_DATA[track_key]['name']}")
        save_notebook(nb, os.path.join(BASE, f"{wk}_studio_{track_key}.ipynb"))
    print(f"  {wk}_studio_*.ipynb (5 tracks)")

    # Check notebook
    cells = make_check(week_num)
    nb = notebook(cells, f"CP1 {wk} Universal Check")
    save_notebook(nb, os.path.join(BASE, f"{wk}_check.ipynb"))
    print(f"  {wk}_check.ipynb")

    # Homework notebook
    cells = make_homework(week_num, title)
    nb = notebook(cells, f"CP1 {wk} Homework — {title}")
    save_notebook(nb, os.path.join(BASE, f"{wk}_homework.ipynb"))
    print(f"  {wk}_homework.ipynb")

total = 14 * (1 + 5 + 1 + 1)  # core + 5 studios + check + homework
print(f"\nCP1 complete: {total} notebooks generated!")
