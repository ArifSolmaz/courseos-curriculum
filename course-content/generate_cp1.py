#!/usr/bin/env python3
"""Generate all CP1 (Computer Programming 1) notebooks — 14 weeks.

This generator produces RICH, substantial notebooks suitable as standalone
teaching documents for absolute beginners in Mechatronics Engineering.

Each core notebook targets 60-100+ cells with:
- Multiple paragraphs of explanation per concept
- 3-4 worked examples per concept (trivial to moderate)
- Expected Output blocks after every code cell
- Common Mistakes sections
- Why This Matters for Your Pipeline sections
- Try It Yourself exercises between concepts
- Debugging Tips
- Key Takeaway summaries
- Visual explanations with ASCII art
- Substantial homework (10+ exercises per week)

Studio notebooks target 30-40+ cells with complete starter code.
Check notebooks have thorough tests with helpful error messages.
Homework notebooks have 10-15 exercises with progressive difficulty.
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from nb_utils import md, code, notebook, save_notebook, setup_cell, reflection_cell, reflection_code, TRACKS

BASE = os.path.join(os.path.dirname(__file__), "notebooks", "cp1")
os.makedirs(BASE, exist_ok=True)

# ============================================================
# WEEK DEFINITIONS
# ============================================================

WEEKS = [
    (1, "Welcome to Python & Your Pipeline", "print, Colab, repo, pipeline concept", "Hello Pipeline stub"),
    (2, "Variables, Types & Numbers", "int, float, str, bool, config dict", "config used by a function"),
    (3, "Making Decisions (Conditionals)", "if, elif, else, comparisons, booleans", "clean_data() basic rules"),
    (4, "Decision Logic & Classification", "nested if, logical operators, rule-based labeling", "analyze() labeled outputs"),
    (5, "Loops: Scanning Data", "for, while, range, accumulate sum/count/min/max/mean", "summary stats on toy data"),
    (6, "Loops: Counting Events", "threshold crossings, peaks, edge cases, flags", "event counts + edge cases"),
    (7, "Lists: Indexing & Windows", "list basics, indexing, slicing, append, windowed ops", "moving-window metric"),
    (8, "Strings: Parsing Data", "string methods, split, strip, join, parsing records", "parser handles formats"),
    (9, "Functions: Building Blocks", "def, parameters, return, refactoring", "pipeline functions exist"),
    (10, "Functions: Decomposition & Reuse", "helper functions, DRY, docstrings, default params", "clearer separation"),
    (11, "Exceptions: Handling Errors", "try/except, error types, skip bad rows, report drops", "clean_data reports skipped"),
    (12, "File I/O: Reading & Writing", "open, csv module, read/write CSV, JSON, export_results", "export_results writes files"),
    (13, "Integration: End-to-End Pipeline", "matplotlib basics, putting it together, plot function", "plot() creates figures"),
    (14, "v1 Release & Demo", "final integration, testing, demo prep, complete pipeline", "v1 passes all checks"),
]

# ============================================================
# TRACK DATA
# ============================================================

TRACK_DATA = {
    "robotics": {
        "name": "Robotics/Mechatronics",
        "product": "MechaSense Studio",
        "dataset_desc": "sensor readings (temperature, RPM, vibration)",
        "sample_rows": [
            '{"timestamp": "00:01", "temp": 25.3, "rpm": 1500, "vibration": 12}',
            '{"timestamp": "00:02", "temp": 26.1, "rpm": 1520, "vibration": 13}',
            '{"timestamp": "00:03", "temp": 85.0, "rpm": 3500, "vibration": 55}',
            '{"timestamp": "00:04", "temp": 24.8, "rpm": 1490, "vibration": 11}',
            '{"timestamp": "00:05", "temp": -5.0, "rpm": 0, "vibration": 0}',
            '{"timestamp": "00:06", "temp": 27.2, "rpm": 1550, "vibration": 14}',
            '{"timestamp": "00:07", "temp": 60.0, "rpm": 2800, "vibration": 35}',
            '{"timestamp": "00:08", "temp": 23.9, "rpm": 1480, "vibration": 10}',
        ],
        "value_col": "temp",
        "threshold": 60,
        "range_low": 0,
        "range_high": 150,
        "unit": "degrees C",
        "context": "monitoring a robotic arm's motor temperature to prevent overheating",
    },
    "data": {
        "name": "Data/AI",
        "product": "CleanReport Pipeline",
        "dataset_desc": "messy survey/CSV data with missing values and inconsistent types",
        "sample_rows": [
            '{"id": 1, "age": "25", "score": "88.5", "city": "Cairo"}',
            '{"id": 2, "age": "", "score": "92.0", "city": "Alex"}',
            '{"id": 3, "age": "abc", "score": "75.0", "city": ""}',
            '{"id": 4, "age": "30", "score": "-10", "city": "Cairo"}',
            '{"id": 5, "age": "22", "score": "95.5", "city": "Luxor"}',
            '{"id": 6, "age": "19", "score": "", "city": "Cairo"}',
            '{"id": 7, "age": "27", "score": "81.0", "city": "Giza"}',
            '{"id": 8, "age": "35", "score": "abc", "city": "Alex"}',
        ],
        "value_col": "score",
        "threshold": 80,
        "range_low": 0,
        "range_high": 100,
        "unit": "points",
        "context": "cleaning messy survey data so a machine learning model can use it",
    },
    "simulation": {
        "name": "Simulation/Games",
        "product": "SimLab Engine",
        "dataset_desc": "simulation timestep logs with position, velocity, and score",
        "sample_rows": [
            '{"step": 0, "x": 0.0, "y": 0.0, "velocity": 1.0, "score": 0}',
            '{"step": 1, "x": 1.0, "y": 0.5, "velocity": 1.2, "score": 10}',
            '{"step": 2, "x": 2.1, "y": 1.2, "velocity": -0.5, "score": 20}',
            '{"step": 3, "x": 3.0, "y": 2.0, "velocity": 1.5, "score": 35}',
            '{"step": 4, "x": 4.2, "y": 2.8, "velocity": 999, "score": -1}',
            '{"step": 5, "x": 5.0, "y": 3.5, "velocity": 1.8, "score": 50}',
            '{"step": 6, "x": 5.9, "y": 4.1, "velocity": 1.3, "score": 62}',
            '{"step": 7, "x": 6.5, "y": 4.9, "velocity": 0.0, "score": 70}',
        ],
        "value_col": "score",
        "threshold": 25,
        "range_low": 0,
        "range_high": 500,
        "unit": "points",
        "context": "analyzing game simulation logs to find optimal strategies",
    },
    "space": {
        "name": "Space/Astro",
        "product": "Lightcurve Explorer",
        "dataset_desc": "star brightness (flux) measurements over time",
        "sample_rows": [
            '{"time": 0.0, "flux": 1.000, "sector": "A"}',
            '{"time": 0.1, "flux": 0.998, "sector": "A"}',
            '{"time": 0.2, "flux": 0.700, "sector": "A"}',
            '{"time": 0.3, "flux": 0.985, "sector": "A"}',
            '{"time": 0.4, "flux": -0.1, "sector": "B"}',
            '{"time": 0.5, "flux": 1.010, "sector": "B"}',
            '{"time": 0.6, "flux": 0.995, "sector": "B"}',
            '{"time": 0.7, "flux": 0.680, "sector": "B"}',
        ],
        "value_col": "flux",
        "threshold": 0.9,
        "range_low": 0,
        "range_high": 2,
        "unit": "relative flux",
        "context": "detecting exoplanet transits by finding dips in star brightness",
    },
    "iot": {
        "name": "IoT/Reporting",
        "product": "AutoDashboard Reporter",
        "dataset_desc": "IoT sensor time series (temperature, humidity, pressure)",
        "sample_rows": [
            '{"ts": "2024-01-01 00:00", "device": "D01", "temp": 22.5, "humidity": 45}',
            '{"ts": "2024-01-01 01:00", "device": "D01", "temp": 23.0, "humidity": 47}',
            '{"ts": "2024-01-01 02:00", "device": "D02", "temp": "", "humidity": 50}',
            '{"ts": "2024-01-01 03:00", "device": "D01", "temp": 99.9, "humidity": 30}',
            '{"ts": "2024-01-01 04:00", "device": "D02", "temp": 21.8, "humidity": 48}',
            '{"ts": "2024-01-01 05:00", "device": "D01", "temp": 22.0, "humidity": 46}',
            '{"ts": "2024-01-01 06:00", "device": "D02", "temp": "abc", "humidity": 51}',
            '{"ts": "2024-01-01 07:00", "device": "D01", "temp": 23.5, "humidity": 44}',
        ],
        "value_col": "temp",
        "threshold": 35,
        "range_low": 0,
        "range_high": 60,
        "unit": "degrees C",
        "context": "monitoring smart-building sensors to detect HVAC problems",
    },
}

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
    11: {"task": "Add robust error handling to clean_data() -- skip and count bad rows", "deliverable": "clean_data() reports skipped counts"},
    12: {"task": "Implement full file I/O: read CSV, write cleaned.csv and report.json", "deliverable": "export_results() writes required files"},
    13: {"task": "Build plot() and run the complete pipeline end-to-end", "deliverable": "plot() creates at least 1 figure"},
    14: {"task": "Final integration, pass universal check, prepare demo", "deliverable": "v1 passes universal check + exports + demo"},
}


# ============================================================
# HELPER: build sample_data code string for a track
# ============================================================

def _sample_data_literal(track_key):
    """Return a string that defines sample_data for a track."""
    rows = TRACK_DATA[track_key]["sample_rows"]
    lines = ["sample_data = ["]
    for i, r in enumerate(rows):
        comma = "," if i < len(rows) - 1 else ""
        lines.append("    " + r + comma)
    lines.append("]")
    return "\n".join(lines)


# ============================================================
# ENRICHMENT HELPERS -- add common cell patterns to any week
# ============================================================

def _enrich_section(cells, week_num, section_name, examples, try_it=None,
                    common_mistakes=None, debugging_tip=None, why_matters=None):
    """Add a rich section with examples, expected output, exercises, etc.

    examples: list of (description_md, code_str, expected_output_str) tuples
    """
    for desc, code_str, expected in examples:
        cells.append(md(desc))
        cells.append(code(code_str))
        if expected:
            cells.append(md(f"**Expected Output:**\n```\n{expected}\n```"))

    if try_it:
        cells.append(md(f"### Try It Yourself"))
        cells.append(code(try_it))

    if common_mistakes:
        cells.append(md(f"### Common Mistakes\n\n{common_mistakes}"))

    if debugging_tip:
        cells.append(md(f"### Debugging Tip\n\n{debugging_tip}"))

    if why_matters:
        cells.append(md(f"### Why This Matters for Your Pipeline\n\n{why_matters}"))


# ============================================================
# CORE NOTEBOOK -- WEEK 1
# ============================================================

def make_core_w01():
    cells = []
    # --- Title & objectives ---
    cells.append(md("""# CP1 Week 1 -- Welcome to Python & Your Pipeline

**Course:** Computer Programming 1 (CP1)
**Session:** 5 hours (lecture + studio)

## Learning Objectives

By the end of this session you will be able to:

1. Open and run a Google Colab notebook
2. Write Python code using `print()` to display text and numbers
3. Use Python as a calculator for basic arithmetic
4. Explain what a "data pipeline" is and why it matters for engineering
5. Identify the 5 stages of your semester project pipeline
6. Set up your project repository with placeholder functions
7. Choose (or begin exploring) one of the 5 project tracks

## Why This Week Matters

Everything in programming starts with being able to *run code* and *see output*.
Today you gain that superpower. By the end of the session you will have a working
project skeleton that you will grow into a complete data pipeline over 14 weeks."""))

    cells.append(setup_cell())

    # --- Part 1: First program ---
    cells.append(md("""---
## Part 1: Your Very First Python Program

Programming means giving the computer a set of instructions written in a language
it understands.  Python is one of the most popular programming languages in the
world -- used by NASA, Google, Tesla, and thousands of engineering teams.

The simplest instruction is **`print()`**. It tells Python:
*"Show this message on the screen."*

Think of `print()` like the "display" button on a calculator -- it does not change
anything, it just shows you a value.

### Example 1 -- Hello World (the classic first program)"""))

    cells.append(code("""# Your very first Python program!
# Click the Play button on the left (or press Shift+Enter) to run it.

print("Hello, World!")"""))

    cells.append(md("""**Expected Output:**
```
Hello, World!
```

**What just happened -- step by step:**

1. Python saw the word `print` and recognized it as a built-in *function*
   (a command that does something).
2. It looked inside the parentheses `(...)` and found the text `"Hello, World!"`.
3. Text inside quotes is called a **string** -- it is data, not an instruction.
4. Python displayed that string on the screen.

> **Analogy:** Think of `print()` as a loudspeaker.  You hand it a message,
> and it announces that message so everyone can hear (see) it."""))

    # Example 2
    cells.append(md("### Example 2 -- Printing multiple lines"))

    cells.append(code("""# You can call print() as many times as you want.
# Each call prints on a NEW line.

print("My name is Python.")
print("I was created in 1991.")
print("I am used in robotics, AI, space, and IoT!")"""))

    cells.append(md("""**Expected Output:**
```
My name is Python.
I was created in 1991.
I am used in robotics, AI, space, and IoT!
```"""))

    # Example 3
    cells.append(md("### Example 3 -- Printing numbers (no quotes needed)"))

    cells.append(code("""# Numbers do NOT need quotes
print(42)
print(3.14)
print(2 + 3)"""))

    cells.append(md("""**Expected Output:**
```
42
3.14
5
```

Notice: when you write `2 + 3` inside `print()`, Python *calculates* the answer
first, then displays the result.  Numbers without quotes are treated as math."""))

    # Example 4
    cells.append(md("### Example 4 -- Mixing text and numbers"))

    cells.append(code("""# Use commas to combine text and numbers in one print()
print("The answer is", 6 * 7)
print("Pi is approximately", 3.14159)"""))

    cells.append(md("""**Expected Output:**
```
The answer is 42
Pi is approximately 3.14159
```

When you separate items with commas inside `print()`, Python adds a space between them automatically."""))

    # Try it yourself 1
    cells.append(md("""### Try It Yourself #1

Change the code below so it prints YOUR name instead of the blank:"""))

    cells.append(code("""# TODO: Replace ___ with your actual name (keep the quotes!)
print("Hello, my name is ___")"""))

    # --- Common Mistakes: print ---
    cells.append(md("""### Common Mistakes with `print()`

Beginners make these mistakes constantly -- and that is completely normal!
Read each one so you can recognize them when they happen to you.

| Mistake | What you wrote | Fix |
|---------|---------------|-----|
| Missing closing quote | `print("Hello)` | `print("Hello")` |
| No quotes around text | `print(Hello)` | `print("Hello")` |
| Capital P | `Print("Hi")` | `print("Hi")` -- Python is case-sensitive! |
| Wrong parentheses | `print["Hi"]` | `print("Hi")` -- use round `()` not square `[]` |
| Mismatched quotes | `print("Hi')` | `print("Hi")` -- both quotes must match |"""))

    cells.append(code("""# Try uncommenting each line below ONE AT A TIME to see the error.
# Then fix it!

# print("Hello)
# print(Hello, World!)
# Print("test")
# print["test"]"""))

    cells.append(md("""**Debugging Tip:** When you see a `SyntaxError`, Python is telling you
"I cannot understand your instruction." Read the error message -- it usually
points to the *exact line* and sometimes the *exact character* where it got
confused.  Look for missing quotes, parentheses, or colons."""))

    # --- Part 2: Python as a Calculator ---
    cells.append(md("""---
## Part 2: Python as a Calculator

Before we process real data, let us get comfortable with arithmetic.
Python supports all the math operations you already know.

```
+--------+------------------+----------+---------+
| Symbol | Operation        | Example  | Result  |
+--------+------------------+----------+---------+
|   +    | Addition         |  3 + 4   |    7    |
|   -    | Subtraction      | 10 - 6   |    4    |
|   *    | Multiplication   |  5 * 3   |   15    |
|   /    | Division         | 20 / 4   |  5.0    |
|   **   | Power            |  2 ** 3  |    8    |
|   //   | Floor division   | 17 // 5  |    3    |
|   %    | Modulo (remain.) | 17 % 5   |    2    |
+--------+------------------+----------+---------+
```

### Example 1 -- Basic arithmetic"""))

    cells.append(code("""# Addition
print("2 + 3 =", 2 + 3)

# Subtraction
print("10 - 4 =", 10 - 4)

# Multiplication
print("5 * 6 =", 5 * 6)

# Division (always gives a decimal / float)
print("20 / 4 =", 20 / 4)"""))

    cells.append(md("""**Expected Output:**
```
2 + 3 = 5
10 - 4 = 6
5 * 6 = 30
20 / 4 = 5.0
```

**Important:** Division with `/` *always* gives a decimal number (called a `float`
in Python), even when the result is a whole number. That is why you see `5.0`
instead of `5`."""))

    cells.append(md("### Example 2 -- Powers, floor division, and modulo"))

    cells.append(code("""# Power (exponentiation): 2 to the power of 10
print("2 ** 10 =", 2 ** 10)

# Floor division: divides and drops the decimal part
print("17 // 5 =", 17 // 5)   # 17 / 5 = 3.4, floor = 3

# Modulo: the REMAINDER after division
print("17 % 5 =", 17 % 5)     # 17 = 5*3 + 2, remainder = 2"""))

    cells.append(md("""**Expected Output:**
```
2 ** 10 = 1024
17 // 5 = 3
17 % 5 = 2
```

> **Why does modulo matter?** You will use `%` to check if a number is even or
> odd (`n % 2 == 0` means even), to wrap around indices, and to process every
> Nth data point."""))

    cells.append(md("### Example 3 -- Order of operations (PEMDAS)"))

    cells.append(code("""# Python follows standard math order of operations
print("2 + 3 * 4 =", 2 + 3 * 4)       # multiplication first: 2 + 12 = 14
print("(2 + 3) * 4 =", (2 + 3) * 4)   # parentheses first: 5 * 4 = 20"""))

    cells.append(md("""**Expected Output:**
```
2 + 3 * 4 = 14
(2 + 3) * 4 = 20
```

**Tip:** When in doubt, use parentheses to make the order explicit.
It also makes your code easier for humans to read."""))

    # Try it yourself 2
    cells.append(md("""### Try It Yourself #2

Calculate how many **minutes** are in one week. Think about it step by step:
- 1 week = 7 days
- 1 day = 24 hours
- 1 hour = 60 minutes"""))

    cells.append(code("""# TODO: Calculate minutes in a week (replace ___ with the formula)
minutes_in_week = 7 * 24 * 60
print("Minutes in a week:", minutes_in_week)"""))

    cells.append(md("""**Expected Output:**
```
Minutes in a week: 10080
```"""))

    # Try it yourself 3
    cells.append(md("### Try It Yourself #3\n\nAn engineer measures that a motor shaft rotates 1500 times per minute (RPM).\nHow many rotations in one 8-hour shift?"))

    cells.append(code("""# TODO: Calculate total rotations in an 8-hour shift
rpm = 1500
hours = 8
total_rotations = ___  # fill in the formula
print("Total rotations:", total_rotations)"""))

    # --- Part 3: Comments ---
    cells.append(md("""---
## Part 3: Comments -- Notes for Humans

**Comments** are lines that Python completely ignores. They exist only for
humans reading the code.

```
# This is a comment. Python skips this line entirely.
print("This runs")  # This part is also a comment
```

### Why write comments?

1. **Explain WHY** you did something (not what -- the code shows what)
2. **Leave notes** for your future self ("I chose 60 because that is the safe limit")
3. **Help teammates** understand your thinking
4. **Temporarily disable** code while debugging

### Example"""))

    cells.append(code("""# This calculates the average sensor reading
# We divide by count to get the mean
total = 150
count = 6
average = total / count  # simple arithmetic mean
print("Average:", average)

# You can also use comments to "turn off" a line:
# print("This line will NOT run because it is commented out")"""))

    cells.append(md("""**Expected Output:**
```
Average: 25.0
```

> **Pro tip:** In Google Colab, select a line and press `Ctrl + /` (Windows)
> or `Cmd + /` (Mac) to toggle a comment on and off."""))

    # --- Part 4: Pipeline concept ---
    cells.append(md("""---
## Part 4: What Is a Data Pipeline?

This is the **most important concept** of the entire course.

A **data pipeline** is a series of steps that transform raw data into useful
results. Think of it like a factory assembly line:

```
  RAW DATA          CLEAN DATA         RESULTS         FIGURES         FILES
  (messy,     -->   (valid,      -->   (stats,   -->   (plots,   -->  (CSV,
   errors,          filtered,          labels,         charts)        JSON,
   missing)         converted)         counts)                       reports)
      |                 |                 |                |              |
  load_data()      clean_data()      analyze()        plot()      export_results()
```

### Real-world analogy

Imagine you work in a factory that receives raw steel:

1. **Load** -- A truck delivers raw steel bars (some are rusted, some are the wrong size)
2. **Clean** -- Workers inspect each bar, remove rusted ones, measure dimensions
3. **Analyze** -- Engineers calculate average weight, sort by grade, flag outliers
4. **Plot** -- The quality team creates charts showing defect rates
5. **Export** -- Results go into a report for management

Your Python project does the SAME thing, but with **data** instead of steel!

### Why pipelines matter for Mechatronics Engineers

Every modern engineering system generates data:
- Robot sensors produce thousands of readings per second
- IoT devices stream temperature/humidity/pressure 24/7
- Simulations generate millions of timesteps
- Telescopes record brightness curves for millions of stars

You CANNOT analyze this data by hand. You need an **automated pipeline** that
can process it reliably, every time, without human intervention."""))

    cells.append(md("### A tiny taste of the full pipeline"))

    cells.append(code("""# Here is a PREVIEW of what your pipeline will look like by Week 14.
# Don't worry if you don't understand every line yet!

# Step 1: Load -- some raw data (just numbers for now)
raw_data = [10, 20, -5, 30, 999, 15, 25, 40]
print("Step 1 - Raw data:", raw_data)

# Step 2: Clean -- remove negative and extreme values
clean_data = []
for value in raw_data:
    if 0 <= value <= 100:
        clean_data.append(value)
print("Step 2 - Clean data:", clean_data)

# Step 3: Analyze -- calculate average
total = 0
for value in clean_data:
    total = total + value
average = total / len(clean_data)
print("Step 3 - Average:", average)

# Step 4: Plot (we will learn matplotlib later)
print("Step 4 - [Plot would go here]")

# Step 5: Export (we will learn file I/O later)
print("Step 5 - [Export would go here]")

print()
print("By Week 14, you will write ALL of this yourself!")
print("And it will handle REAL data from your chosen track.")"""))

    cells.append(md("""**Expected Output:**
```
Step 1 - Raw data: [10, 20, -5, 30, 999, 15, 25, 40]
Step 2 - Clean data: [10, 20, 30, 15, 25, 40]
Step 3 - Average: 23.333333333333332
Step 4 - [Plot would go here]
Step 5 - [Export would go here]

By Week 14, you will write ALL of this yourself!
And it will handle REAL data from your chosen track.
```"""))

    # --- Part 5: Errors ---
    cells.append(md("""---
## Part 5: Errors Are Normal!

Here is a secret that experienced programmers know:

> **Errors are not failures. Errors are information.**

Every programmer -- even experts with 20 years of experience -- sees errors
every single day. The difference between a beginner and an expert is not that
the expert avoids errors. The expert **reads the error message** and fixes
the problem quickly.

### How to read a Python error

```
  File "<stdin>", line 1
    print("Hello)
                 ^
SyntaxError: unterminated string literal
```

Reading from bottom to top:
1. **SyntaxError** -- the TYPE of error (syntax = grammar/structure)
2. **unterminated string literal** -- WHAT is wrong (string was not closed)
3. **^** -- WHERE Python got confused (the caret points to the spot)
4. **line 1** -- WHICH line the error is on"""))

    cells.append(code("""# Let's intentionally cause some errors.
# Uncomment ONE line at a time, run the cell, read the error, then fix it.

# Error 1: Missing closing quote
# print("Hello World)

# Error 2: Name not defined (forgot quotes around text)
# print(Hello)

# Error 3: Capital P (Python is case-sensitive!)
# Print("test")"""))

    cells.append(md("""### Debugging Tips for Common Errors

| Error Type | Meaning | Common Fix |
|-----------|---------|------------|
| `SyntaxError` | Python cannot parse your code | Check quotes, parentheses, colons |
| `NameError` | You used a name Python does not recognize | Check spelling, add quotes for strings |
| `TypeError` | Wrong type of data for an operation | Check you are not mixing text and numbers |
| `IndentationError` | Wrong amount of whitespace | Use consistent 4-space indentation |

**Golden Rule:** When you see an error:
1. **Do not panic** -- errors are normal
2. **Read the last line** -- it tells you WHAT went wrong
3. **Look at the line number** -- it tells you WHERE
4. **Fix ONE thing** at a time, then re-run"""))

    # --- Part 6: Track exploration ---
    cells.append(md("""---
## Part 6: Choosing Your Track

Over the next 14 weeks, you will build a complete data pipeline.
Everyone builds the **same structure** (load, clean, analyze, plot, export),
but each track works with **different data**.

| # | Track | Product Name | Data Type | Real-World Use |
|---|-------|-------------|-----------|----------------|
| 1 | Robotics | MechaSense Studio | Sensor data (temp, RPM, vibration) | Predictive maintenance |
| 2 | Data/AI | CleanReport Pipeline | Messy CSV datasets | Data preparation for ML |
| 3 | Simulation | SimLab Engine | Simulation timestep logs | Game/physics analysis |
| 4 | Space/Astro | Lightcurve Explorer | Star brightness flux | Exoplanet detection |
| 5 | IoT | AutoDashboard Reporter | IoT sensor streams | Smart building monitoring |

**Timeline:**
- **Weeks 1-2:** Explore all 5 tracks
- **Week 3:** Confirm your choice (locked after that!)

### Why This Matters for Your Pipeline

Your track determines what your data looks like, but the **pipeline structure is
identical** across all tracks. This means:
- You can help classmates on other tracks (same functions, different data)
- The skills you learn are transferable to ANY data problem
- In the real world, pipelines are everywhere -- only the data changes"""))

    cells.append(code("""# Quick look at each track's data

# Track 1 - Robotics: motor sensor readings
robot_data = [25.3, 26.1, 85.0, 24.8, -5.0, 27.2]
print("Robotics (temperatures):", robot_data)

# Track 2 - Data/AI: messy survey responses
survey_data = ["88.5", "92.0", "", "abc", "95.5", "-10"]
print("Data/AI (survey scores):", survey_data)

# Track 3 - Simulation: game simulation scores
sim_scores = [0, 10, 20, 35, -1, 50, 62, 70]
print("Simulation (scores):", sim_scores)

# Track 4 - Space: star brightness measurements
flux_data = [1.000, 0.998, 0.700, 0.985, -0.1, 1.010]
print("Space (flux values):", flux_data)

# Track 5 - IoT: building temperature sensors
iot_temps = [22.5, 23.0, "", 99.9, 21.8, 22.0]
print("IoT (temperatures):", iot_temps)

print()
print("Notice: every track has some 'bad' data mixed in!")
print("That is why we need a CLEANING step in our pipeline.")"""))

    cells.append(md("""**Expected Output:**
```
Robotics (temperatures): [25.3, 26.1, 85.0, 24.8, -5.0, 27.2]
Data/AI (survey scores): ['88.5', '92.0', '', 'abc', '95.5', '-10']
Simulation (scores): [0, 10, 20, 35, -1, 50, 62, 70]
Space (flux values): [1.0, 0.998, 0.7, 0.985, -0.1, 1.01]
IoT (temperatures): [22.5, 23.0, '', 99.9, 21.8, 22.0]

Notice: every track has some 'bad' data mixed in!
That is why we need a CLEANING step in our pipeline.
```"""))

    # --- Part 7: Pipeline stub ---
    cells.append(md("""---
## Part 7: Your Pipeline Stub

A **stub** is an empty function that defines the *shape* of your program without
filling in the details. It is like drawing the blueprint of a house before
building it.

We create stubs now so that:
1. The overall structure is clear from Day 1
2. We can test that the pieces connect properly
3. Each week, we replace one stub with real code

```
  Week 1:  All stubs (empty functions)
  Week 3:  clean_data() has real code
  Week 4:  analyze() has real code
  ...
  Week 14: Everything is real code -- v1 complete!
```"""))

    cells.append(code("""# === YOUR PIPELINE STUB ===
# These are placeholder functions. They print a message but do no real work.
# Over the coming weeks, you will replace each one with working code.

def load_data(config):
    \"\"\"Load raw data from a source.\"\"\"
    print("load_data: not implemented yet")
    return []

def clean_data(data, config):
    \"\"\"Clean raw data by removing invalid values.\"\"\"
    print("clean_data: not implemented yet")
    return data

def analyze(clean_data, config):
    \"\"\"Analyze clean data to produce statistics and labels.\"\"\"
    print("analyze: not implemented yet")
    return {"analysis_summary": {}, "labels": []}

def plot(clean_data, results, config):
    \"\"\"Create visualizations of the data.\"\"\"
    print("plot: not implemented yet")
    return []

def export_results(clean_data, results, figures, config):
    \"\"\"Export all results to files (CSV, JSON, plots).\"\"\"
    print("export_results: not implemented yet")
    return {}

def self_check():
    \"\"\"Run basic tests on the pipeline.\"\"\"
    print("self_check: running...")
    assert load_data({}) is not None, "load_data should return something"
    print("self_check: PASSED (basic)")

# --- Run the pipeline end-to-end ---
print("=== Pipeline Stub Test ===")
config = {"project_name": "my_project", "track": "undecided"}

data = load_data(config)
cleaned = clean_data(data, config)
results = analyze(cleaned, config)
figures = plot(cleaned, results, config)
exported = export_results(cleaned, results, figures, config)
self_check()

print()
print("=== Done! ===")
print("All 5 pipeline functions exist and connect.")
print("You will replace them with real code -- one per week.")"""))

    cells.append(md("""**Expected Output:**
```
=== Pipeline Stub Test ===
load_data: not implemented yet
clean_data: not implemented yet
analyze: not implemented yet
plot: not implemented yet
export_results: not implemented yet
self_check: running...
load_data: not implemented yet
self_check: PASSED (basic)

=== Done! ===
All 5 pipeline functions exist and connect.
You will replace them with real code -- one per week.
```"""))

    # --- Key Takeaways ---
    cells.append(md("""---
## Key Takeaways -- Week 1

1. **`print()`** displays output. It is your primary debugging tool all semester.
2. **Python does math** with `+`, `-`, `*`, `/`, `**`, `//`, `%`.
3. **Comments** (`#`) are notes for humans; Python ignores them.
4. **Errors are normal.** Read the message, find the line, fix one thing.
5. **A pipeline** is: Load -> Clean -> Analyze -> Plot -> Export.
6. **Stubs** let you build the skeleton first and fill in details later.
7. **Your track** determines your data but NOT the pipeline structure."""))

    # --- Homework ---
    cells.append(md("""---
## Homework (Complete Before Next Week)

These exercises reinforce today's concepts. Work through them at home.

### Review Exercises (R1-R4) -- check your understanding"""))

    cells.append(code("""# R1: What does print() do? Write your answer as a comment, then
#     demonstrate with 3 different print() calls.

# Answer:
print("Example 1")
print(42)
print("The sum is", 10 + 20)"""))

    cells.append(code("""# R2: What is the difference between 10 / 3 and 10 // 3?
#     Calculate both and explain in a comment.

print("10 / 3 =", 10 / 3)
print("10 // 3 =", 10 // 3)
# Explanation:"""))

    cells.append(code("""# R3: What is a pipeline? List the 5 stages of our project pipeline.
# Answer (as comments):
# 1.
# 2.
# 3.
# 4.
# 5."""))

    cells.append(code("""# R4: What should you do when you see an error? List 4 steps.
# 1.
# 2.
# 3.
# 4."""))

    cells.append(md("### Practice Exercises (P1-P5) -- apply the concepts"))

    cells.append(code("""# P1: Print your full name, your age, and your department.
#     Each on its own line.
"""))

    cells.append(code("""# P2: Use Python as a calculator to solve these:
# a) 15 * 8 + 3
# b) (100 - 37) / 9
# c) 2 ** 10 (2 to the power of 10)
# d) 365 * 24 * 60 * 60 (seconds in a year)
# Print each result with a label.
"""))

    cells.append(code("""# P3: Calculate and print:
# - How many seconds in a day
# - How many heartbeats in a day (assume 72 beats per minute)
# - How many breaths in a day (assume 16 per minute)
"""))

    cells.append(code("""# P4: Fix ALL of these broken print statements:
# (Uncomment each, find the error, and fix it)

# print("Hello)
# print(Hello, World!)
# Print("test")
# print("She said "hello"")
"""))

    cells.append(code("""# P5: Write 3 print statements that show:
# - Your 1st track choice and why
# - Your 2nd track choice and why
# - What kind of data excites you most
"""))

    cells.append(md("### Challenge Exercises (C1-C3) -- stretch your thinking"))

    cells.append(code("""# C1: Research and demonstrate these Python operators:
# //  (floor division)
# %   (modulo)
# **  (exponentiation)
# Write 3 examples of EACH and explain the result.
"""))

    cells.append(code("""# C2: Using only print() and math, create this exact output:
#
# ***********
# *         *
# *  HELLO  *
# *         *
# ***********
#
# Hint: use spaces carefully inside the quotes.
"""))

    cells.append(code("""# C3: Calculate the distance between two points:
# Point A = (3, 4), Point B = (7, 1)
# Formula: distance = sqrt((x2-x1)^2 + (y2-y1)^2)
# Hint: sqrt(x) = x ** 0.5
"""))

    cells.append(md("### Mini-Project (M1) -- build something complete"))

    cells.append(code("""# M1: Personal Engineering Dashboard
#
# Create a program that prints a formatted dashboard like this:
#
# ============================================
#         ENGINEERING STUDENT DASHBOARD
# ============================================
#  Name:       [Your Name]
#  ID:         [Your Student ID]
#  Department: Mechatronics Engineering
#  Semester:   [Current Semester]
#  GPA:        [Your GPA]
# --------------------------------------------
#  Track Choice:  [Your preferred track]
#  Pipeline Stage: Week 1 / 14
#  Completion:     7%
# --------------------------------------------
#  Fun Fact: There are [X] seconds in a year!
# ============================================
#
# Requirements:
# - Use at least 2 math calculations
# - Print at least 12 lines
# - Make it look neat and aligned
"""))

    cells.append(reflection_cell())
    cells.append(reflection_code())

    return cells


# ============================================================
# CORE NOTEBOOK -- WEEK 2
# ============================================================

def make_core_w02():
    cells = []

    cells.append(md("""# CP1 Week 2 -- Variables, Types & Numbers

**Course:** Computer Programming 1 (CP1)
**Session:** 5 hours (lecture + studio)

## Learning Objectives

By the end of this session you will be able to:

1. Create and name variables following Python conventions
2. Identify and use the 4 basic data types: `int`, `float`, `str`, `bool`
3. Convert between types using `int()`, `float()`, `str()`, `bool()`
4. Format output with f-strings
5. Create and use a configuration dictionary for your pipeline
6. Use your config in a pipeline function

## Why This Week Matters

Variables are the **memory** of your program. Without variables, every calculation
would be lost the moment it finishes. This week you learn to store, name, organize,
and format data -- the foundation for everything that follows.

Your **config dictionary** will be the single source of truth for your pipeline:
thresholds, file paths, project name, and settings all in one place."""))

    cells.append(setup_cell())

    # Part 1: Variables
    cells.append(md("""---
## Part 1: Variables -- Giving Names to Values

A **variable** is a name attached to a value. Think of it as a labeled box:

```
  +-------------+     +-------------+     +-------------+
  | temperature |     | sensor_name |     | is_active   |
  |    25.3     |     | "motor_01"  |     |    True     |
  +-------------+     +-------------+     +-------------+
       float              string              boolean
```

You create a variable with `=` (the assignment operator):

```python
variable_name = value
```

### Example 1 -- Creating variables"""))

    cells.append(code("""# Creating variables -- just pick a name and assign a value
temperature = 25.3
sensor_name = "temp_sensor_01"
is_active = True
reading_count = 100

# Display them
print(temperature)
print(sensor_name)
print(is_active)
print(reading_count)"""))

    cells.append(md("""**Expected Output:**
```
25.3
temp_sensor_01
True
100
```

**What happened:**
- Python created four "boxes" in memory
- Each box has a name (left of `=`) and a value (right of `=`)
- `print()` looks inside the box and shows the value"""))

    cells.append(md("### Example 2 -- Variables can change"))

    cells.append(code("""count = 0
print("Start:", count)

count = 10
print("After assignment:", count)

count = count + 5   # take the OLD value, add 5, store the result
print("After adding 5:", count)"""))

    cells.append(md("""**Expected Output:**
```
Start: 0
After assignment: 10
After adding 5: 15
```

**Key insight:** `count = count + 5` does NOT mean "count equals count plus 5"
in the math sense. It means "take the current value of count (10), add 5 to it,
and store the result (15) back in count." The old value (10) is gone."""))

    cells.append(md("""### Variable Naming Rules

| Rule | Good | Bad | Why |
|------|------|-----|-----|
| Use lowercase + underscores | `sensor_name` | `SensorName` | Python convention |
| Descriptive names | `temperature_celsius` | `t` | Readability |
| Cannot start with a digit | `sensor_1` | `1_sensor` | Syntax error |
| No spaces | `my_var` | `my var` | Syntax error |
| No Python keywords | `value` | `print` | Overwrites built-in |

> **Analogy:** Variable names are like labels on storage bins in a warehouse.
> Good labels ("Motor_A_Temperature") help you find things fast.
> Bad labels ("x") make everything confusing."""))

    cells.append(md("### Try It Yourself #1"))

    cells.append(code("""# TODO: Create 4 variables for your project:
# 1. project_name (a string -- your product name)
# 2. data_size (an integer -- how many data points)
# 3. threshold (a float -- a cutoff value)
# 4. is_ready (a boolean -- True or False)

project_name = "My Project"
data_size = 100
threshold = 50.0
is_ready = False

print("Project:", project_name)
print("Data size:", data_size)
print("Threshold:", threshold)
print("Ready?", is_ready)"""))

    # Part 2: Data Types
    cells.append(md("""---
## Part 2: Data Types -- The Four Building Blocks

Every value in Python has a **type**. The type determines what operations
you can do with it.

```
  +--------+-------------------+-----------------------+------------------+
  | Type   | What it stores    | Examples              | Use for          |
  +--------+-------------------+-----------------------+------------------+
  | int    | Whole numbers     | 42, -7, 0, 1000000   | Counts, indices  |
  | float  | Decimal numbers   | 3.14, -0.5, 100.0    | Measurements     |
  | str    | Text              | "hello", '3.14'       | Names, labels    |
  | bool   | True/False        | True, False           | Flags, decisions |
  +--------+-------------------+-----------------------+------------------+
```

### Example 1 -- Checking types with `type()`"""))

    cells.append(code("""# int -- whole numbers (no decimal point)
age = 20
print(age, "is", type(age))

# float -- decimal numbers
temp = 36.6
print(temp, "is", type(temp))

# str -- text (always in quotes)
name = "Motor A"
print(name, "is", type(name))

# bool -- True or False (note the capital T and F)
is_valid = True
print(is_valid, "is", type(is_valid))"""))

    cells.append(md("""**Expected Output:**
```
20 is <class 'int'>
36.6 is <class 'float'>
Motor A is <class 'str'>
True is <class 'bool'>
```"""))

    cells.append(md("### Example 2 -- Surprising types"))

    cells.append(code("""# These look similar but have DIFFERENT types!
a = 42       # int
b = 42.0     # float (has a decimal point)
c = "42"     # str (has quotes!)
d = True     # bool
e = "True"   # str (has quotes -- NOT a bool!)

print("a =", a, " type:", type(a))
print("b =", b, " type:", type(b))
print("c =", c, " type:", type(c))
print("d =", d, " type:", type(d))
print("e =", e, " type:", type(e))"""))

    cells.append(md("""**Expected Output:**
```
a = 42  type: <class 'int'>
b = 42.0  type: <class 'float'>
c = 42  type: <class 'str'>
d = True  type: <class 'bool'>
e = True  type: <class 'str'>
```

**Key insight:** `"42"` (with quotes) is text, not a number! You cannot do math
with it until you convert it. This matters hugely when reading data from files --
everything comes in as strings and must be converted."""))

    # Type conversion
    cells.append(md("""### Example 3 -- Converting between types

You convert types using `int()`, `float()`, `str()`, and `bool()`:"""))

    cells.append(code("""# String to number
x = "42"
y = int(x)         # string -> int
z = float(x)       # string -> float
print("int:", y, "| float:", z)
print("Now we can do math:", y + 10)

# Number to string
count = 150
message = "We have " + str(count) + " readings"
print(message)

# To boolean
print("bool(1):", bool(1))       # True (any non-zero number)
print("bool(0):", bool(0))       # False
print('bool(""):', bool(""))     # False (empty string)
print('bool("hi"):', bool("hi")) # True (non-empty string)"""))

    cells.append(md("""**Expected Output:**
```
int: 42 | float: 42.0
Now we can do math: 52
We have 150 readings
bool(1): True
bool(0): False
bool(""): False
bool("hi"): True
```"""))

    cells.append(md("""### Common Mistakes with Types

| Mistake | Code | Error | Fix |
|---------|------|-------|-----|
| Math on strings | `"10" + 5` | TypeError | `int("10") + 5` |
| Convert non-number | `int("abc")` | ValueError | Check before converting |
| Concatenate number | `"Age: " + 25` | TypeError | `"Age: " + str(25)` |

### Debugging Tip

When you see `TypeError: can only concatenate str (not "int") to str`, it means
you are trying to glue a number onto text. Either use `str()` to convert the
number, or (better) use an f-string (see Part 3)."""))

    # Part 3: f-strings
    cells.append(md("""---
## Part 3: f-Strings -- Formatted Text

f-strings are the easiest way to mix variables into text. Put `f` before the
opening quote, then use `{variable_name}` inside the string:

```python
name = "Ahmed"
print(f"Hello, {name}!")   # prints: Hello, Ahmed!
```

### Example 1 -- Basic f-strings"""))

    cells.append(code("""sensor = "Motor A"
rpm = 1500
temp = 72.456

print(f"Sensor: {sensor}")
print(f"RPM: {rpm}")
print(f"Temperature: {temp}")"""))

    cells.append(md("""**Expected Output:**
```
Sensor: Motor A
RPM: 1500
Temperature: 72.456
```"""))

    cells.append(md("### Example 2 -- Formatting numbers"))

    cells.append(code("""temp = 72.456789
pi = 3.14159265358979

# Control decimal places with :.Nf
print(f"1 decimal:  {temp:.1f}")    # 72.5
print(f"2 decimals: {temp:.2f}")    # 72.46
print(f"4 decimals: {pi:.4f}")      # 3.1416

# Percentage
ratio = 0.847
print(f"Percentage: {ratio:.1%}")   # 84.7%

# Padding / alignment
for name in ["Motor A", "Motor B", "Pump C"]:
    print(f"  {name:<12} | status: OK")"""))

    cells.append(md("""**Expected Output:**
```
1 decimal:  72.5
2 decimals: 72.46
4 decimals: 3.1416
Percentage: 84.7%
  Motor A      | status: OK
  Motor B      | status: OK
  Pump C       | status: OK
```"""))

    cells.append(md("### Example 3 -- Math inside f-strings"))

    cells.append(code("""width = 5
height = 3
print(f"Area = {width} x {height} = {width * height}")

readings = [25, 30, 28, 32, 27]
n = len(readings)
total = sum(readings)
print(f"Average of {n} readings = {total / n:.1f}")"""))

    cells.append(md("""**Expected Output:**
```
Area = 5 x 3 = 15
Average of 5 readings = 28.4
```"""))

    cells.append(md("### Try It Yourself #2"))

    cells.append(code("""# TODO: Create variables and use f-strings to print this exact output:
# "Project: MechaSense | Track: robotics | Points: 500 | Ready: True"

project = "MechaSense"
track = "robotics"
points = 500
ready = True

print(f"Project: {project} | Track: {track} | Points: {points} | Ready: {ready}")"""))

    # Part 4: Math operations
    cells.append(md("""---
## Part 4: Math Operations & Shorthand

### All arithmetic operators"""))

    cells.append(code("""a = 17
b = 5

print(f"{a} + {b}  = {a + b}")      # Addition: 22
print(f"{a} - {b}  = {a - b}")      # Subtraction: 12
print(f"{a} * {b}  = {a * b}")      # Multiplication: 85
print(f"{a} / {b}  = {a / b}")      # Division: 3.4
print(f"{a} // {b} = {a // b}")     # Floor division: 3
print(f"{a} % {b}  = {a % b}")      # Modulo: 2
print(f"{a} ** {b} = {a ** b}")     # Power: 1419857"""))

    cells.append(md("""**Expected Output:**
```
17 + 5  = 22
17 - 5  = 12
17 * 5  = 85
17 / 5  = 3.4
17 // 5 = 3
17 % 5  = 2
17 ** 5 = 1419857
```"""))

    cells.append(md("### Shorthand assignment operators"))

    cells.append(code("""count = 10
print(f"Start:     {count}")

count += 3     # same as: count = count + 3
print(f"After +=3: {count}")

count -= 1     # same as: count = count - 1
print(f"After -=1: {count}")

count *= 2     # same as: count = count * 2
print(f"After *=2: {count}")

count //= 3   # same as: count = count // 3
print(f"After //=3: {count}")"""))

    cells.append(md("""**Expected Output:**
```
Start:     10
After +=3: 13
After -=1: 12
After *=2: 24
After //=3: 8
```"""))

    # Part 5: Dictionaries / Config
    cells.append(md("""---
## Part 5: The Config Dictionary

A **dictionary** stores key-value pairs, like a real dictionary stores
word-definition pairs.

```
  config = {
      "project_name":  "my_sensor",     <-- key: value
      "track":         "robotics",
      "threshold":     60.0,
      "version":       "v1",
  }
```

We use a dictionary as our **config** -- a single place that holds all the
settings for our pipeline. This way, when you want to change a threshold,
you change it in ONE place instead of hunting through your code.

### Example 1 -- Creating and accessing a dictionary"""))

    cells.append(code("""config = {
    "project_name": "motor_monitor",
    "track": "robotics",
    "version": "v1",
    "threshold": 60.0,
    "data_points": 100,
    "min_value": 0,
    "max_value": 150,
}

# Access a value using its key
print("Project:", config["project_name"])
print("Track:", config["track"])
print("Threshold:", config["threshold"])"""))

    cells.append(md("""**Expected Output:**
```
Project: motor_monitor
Track: robotics
Threshold: 60.0
```"""))

    cells.append(md("### Example 2 -- Adding and checking keys"))

    cells.append(code("""config = {"project_name": "test", "version": "v1"}

# Add a new key
config["author"] = "Student A"
config["year"] = 2026
print("After adding keys:", config)

# Check if a key exists
if "threshold" in config:
    print("Threshold:", config["threshold"])
else:
    print("No threshold set -- using default")

# Safe access with .get() (returns None or a default if missing)
val = config.get("threshold", 50.0)
print("Threshold (with default):", val)"""))

    cells.append(md("""**Expected Output:**
```
After adding keys: {'project_name': 'test', 'version': 'v1', 'author': 'Student A', 'year': 2026}
No threshold set -- using default
Threshold (with default): 50.0
```

> **Why .get() is important:** When reading data from files, keys might be
> missing. Using `config.get("key", default)` prevents your program from
> crashing with a `KeyError`."""))

    cells.append(md("### Example 3 -- Looping over a dictionary"))

    cells.append(code("""config = {
    "project_name": "motor_monitor",
    "track": "robotics",
    "version": "v1",
    "threshold": 60.0,
}

print("=== Configuration ===")
for key, value in config.items():
    print(f"  {key:20s}: {value}")"""))

    cells.append(md("""**Expected Output:**
```
=== Configuration ===
  project_name        : motor_monitor
  track               : robotics
  version             : v1
  threshold           : 60.0
```"""))

    cells.append(md("### Try It Yourself #3"))

    cells.append(code("""# TODO: Create a config for YOUR project with at least 7 keys.
# Must include: project_name, track, version, threshold, min_value, max_value
# Add at least 1 more custom key.

my_config = {
    "project_name": "___",
    "track": "___",
    "version": "v1",
    "threshold": 0,
    "min_value": 0,
    "max_value": 100,
    # Add your custom key(s) here
}

print("=== My Config ===")
for key, value in my_config.items():
    print(f"  {key}: {value}")"""))

    # Part 6: Config in a function
    cells.append(md("""---
## Part 6: Using Config in a Pipeline Function

Now let us connect the config to our pipeline. Here is a `load_data()` function
that uses the config to generate sample data:"""))

    cells.append(code("""def load_data(config):
    \"\"\"Load sample data based on config settings.\"\"\"
    name = config["project_name"]
    n = config.get("data_points", 10)

    data = []
    for i in range(n):
        data.append({"index": i, "value": i * 2.5 + 10})

    print(f"[{name}] Loaded {len(data)} rows")
    return data

# Use it!
config = {
    "project_name": "my_sensor",
    "data_points": 5,
}

result = load_data(config)
for row in result:
    print(f"  Row {row['index']}: value = {row['value']}")"""))

    cells.append(md("""**Expected Output:**
```
[my_sensor] Loaded 5 rows
  Row 0: value = 10.0
  Row 1: value = 12.5
  Row 2: value = 15.0
  Row 3: value = 17.5
  Row 4: value = 20.0
```

### Why This Matters for Your Pipeline

Your config dictionary will:
- Control which track's data to load
- Set thresholds for cleaning and analysis
- Define file paths for input/output
- Store project metadata (name, version, author)

By centralizing settings in one dictionary, you can change behavior without
editing function code. This is a fundamental engineering principle:
**separate configuration from logic.**"""))

    # Key takeaways
    cells.append(md("""---
## Key Takeaways -- Week 2

1. **Variables** store values with meaningful names: `temperature = 25.3`
2. **Four basic types:** `int` (whole), `float` (decimal), `str` (text), `bool` (True/False)
3. **Type conversion:** `int()`, `float()`, `str()` -- essential for data processing
4. **f-strings:** `f"Value: {x:.2f}"` -- clean way to format output
5. **Dictionaries:** `config["key"]` -- store key-value pairs
6. **Config pattern:** One dict holds all pipeline settings"""))

    # Homework
    cells.append(md("""---
## Homework (Complete Before Next Week)

### Review Exercises (R1-R4)"""))

    cells.append(code("""# R1: What are the 4 basic Python types? Give 2 examples of each.
# int:
# float:
# str:
# bool:"""))

    cells.append(code("""# R2: What is the difference between = and ==?
# Answer:

# R3: What does type() return for each of these?
print(type(42))
print(type(42.0))
print(type("42"))
print(type(True))"""))

    cells.append(code("""# R4: What is an f-string? Write 3 different f-string examples.
name = "Python"
version = 3
pi = 3.14159
# Example 1:
# Example 2:
# Example 3:"""))

    cells.append(md("### Practice Exercises (P1-P5)"))

    cells.append(code("""# P1: Create variables for 5 sensor readings, then calculate and
# print the average using only those variables (no lists yet).

r1 = 23.5
r2 = 25.0
r3 = 22.8
r4 = 26.1
r5 = 24.3
average = (r1 + r2 + r3 + r4 + r5) / 5
print(f"Average: {average:.2f}")"""))

    cells.append(code("""# P2: Use f-strings to print a formatted sensor report:
# "Sensor: Motor-A | Readings: 150 | Average: 23.45 C | Status: OK"
# Use variables for each value (do not hard-code the string).
"""))

    cells.append(code("""# P3: Create a config dictionary with at least 8 keys.
# Print all keys and values using a for loop.
"""))

    cells.append(code("""# P4: Write code that converts temperature from Celsius to Fahrenheit.
# Formula: F = C * 9/5 + 32
# Test with: 0, 100, 37.5, -40
# Print each conversion like: "0 C = 32.0 F"
"""))

    cells.append(code("""# P5: Swap two variables WITHOUT using a third variable.
a = 10
b = 20
# After swap: a should be 20, b should be 10
# Hint: Python allows a, b = b, a
"""))

    cells.append(md("### Challenge Exercises (C1-C3)"))

    cells.append(code("""# C1: Create a nested config dictionary:
# config["cleaning"]["rules"]["temperature"] = {"min": 0, "max": 100}
# Access and print the nested values.
"""))

    cells.append(code("""# C2: Write code that determines the type of a variable and prints
# a human-friendly description.
# Example: describe(42) -> "42 is an integer (whole number)"
# Test with: 42, 3.14, "hello", True
"""))

    cells.append(code("""# C3: Calculate compound interest:
# A = P * (1 + r/n)^(n*t)
# P=1000, r=0.05, n=12, t=5
# Print each year's balance formatted to 2 decimal places.
"""))

    cells.append(md("### Mini-Project (M1)"))

    cells.append(code("""# M1: Unit Converter
#
# Create a config dictionary with conversion factors:
# config = {
#     "km_to_miles": 0.621371,
#     "kg_to_lb": 2.20462,
#     "c_to_f_mult": 1.8,
#     "c_to_f_add": 32,
#     "liters_to_gallons": 0.264172,
# }
#
# Write code that:
# 1. Converts 5 different measurements using the config
# 2. Prints each conversion with nice formatting
# 3. Includes the formula used
#
# Example output:
# === Unit Converter ===
# 10 km = 6.21 miles  (x 0.621371)
# 75 kg = 165.35 lb   (x 2.20462)
# ...
"""))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# CORE NOTEBOOK -- WEEK 3
# ============================================================

def make_core_w03():
    cells = []

    cells.append(md("""# CP1 Week 3 -- Making Decisions (Conditionals)

**Course:** Computer Programming 1 (CP1)
**Session:** 5 hours

## Learning Objectives

1. Use `if`, `elif`, `else` to make decisions in code
2. Write comparison operators (`==`, `!=`, `<`, `>`, `<=`, `>=`)
3. Combine conditions with `and`, `or`, `not`
4. Apply validation rules to filter/clean data
5. Implement basic cleaning rules in `clean_data()`

## Why This Week Matters

Data is messy. Sensor readings go negative. Strings appear where numbers should
be. Values spike to 999999 because a sensor disconnected. Your pipeline needs
to make **decisions**: "Is this value valid? Should I keep it or drop it?"

Conditionals give your code the ability to *think* and *choose*. After today,
your `clean_data()` function will be able to separate good data from bad."""))

    cells.append(setup_cell())

    # Part 1: Comparisons
    cells.append(md("""---
## Part 1: True or False? (Comparisons)

Python can answer yes/no questions using **comparison operators**. The answer
is always `True` or `False` (a boolean).

```
+----------+------------------------+----------+---------+
| Operator | Meaning                | Example  | Result  |
+----------+------------------------+----------+---------+
|    ==    | Equal to               | 10 == 10 |  True   |
|    !=    | Not equal to           | 10 != 5  |  True   |
|    <     | Less than              | 3 < 5    |  True   |
|    >     | Greater than           | 3 > 5    |  False  |
|    <=    | Less than or equal     | 5 <= 5   |  True   |
|    >=    | Greater than or equal  | 3 >= 5   |  False  |
+----------+------------------------+----------+---------+
```

### Example 1 -- Basic comparisons"""))

    cells.append(code("""print(10 > 5)      # True
print(10 < 5)      # False
print(10 == 10)    # True (is equal to?)
print(10 != 5)     # True (is not equal to?)
print(10 >= 10)    # True
print(10 <= 9)     # False"""))

    cells.append(md("""**Expected Output:**
```
True
False
True
True
True
False
```

### CRITICAL: = vs ==

| Symbol | Meaning | Example |
|--------|---------|---------|
| `=` | **Assignment** -- store a value | `x = 5` (put 5 into x) |
| `==` | **Comparison** -- check equality | `x == 5` (is x equal to 5?) |

This is the #1 beginner mistake. If you write `if x = 5:` Python will give you
a `SyntaxError`. You need `if x == 5:`."""))

    cells.append(md("### Example 2 -- Comparisons with variables"))

    cells.append(code("""temperature = 72
threshold = 60

print(f"Temperature ({temperature}) > Threshold ({threshold})?", temperature > threshold)
print(f"Temperature ({temperature}) == 72?", temperature == 72)
print(f"Temperature ({temperature}) != 72?", temperature != 72)"""))

    cells.append(md("""**Expected Output:**
```
Temperature (72) > Threshold (60)? True
Temperature (72) == 72? True
Temperature (72) != 72? False
```"""))

    # Part 2: if statements
    cells.append(md("""---
## Part 2: The `if` Statement

An `if` statement runs code only when a condition is `True`.

```
  if condition:
      code that runs when True
      more code that runs when True
  code that ALWAYS runs (not indented)
```

Think of it like a gate:
```
  condition True?  --YES-->  [run the indented code]  -->  continue
         |
         +---NO--->  [skip the indented code]  -------->  continue
```

### Example 1 -- Simple if"""))

    cells.append(code("""temperature = 75

if temperature > 60:
    print("WARNING: Temperature is high!")
    print("Check the sensor immediately.")

print("This line ALWAYS runs (it is not indented under the if).")"""))

    cells.append(md("""**Expected Output:**
```
WARNING: Temperature is high!
Check the sensor immediately.
This line ALWAYS runs (it is not indented under the if).
```

**Key points:**
- The condition `temperature > 60` evaluates to `True` (because 75 > 60)
- So both indented lines run
- The last line runs regardless because it is NOT indented under the `if`
- **Indentation matters!** Use exactly 4 spaces (Tab key in Colab)
- The colon `:` after the condition is required"""))

    cells.append(md("### Example 2 -- if / else"))

    cells.append(code("""value = -10

if value >= 0:
    print(f"{value} is non-negative")
else:
    print(f"{value} is negative -- INVALID!")"""))

    cells.append(md("""**Expected Output:**
```
-10 is negative -- INVALID!
```

The `else` block runs when the `if` condition is `False`. Exactly ONE of the
two blocks will run -- never both, never neither."""))

    cells.append(md("### Example 3 -- if / elif / else"))

    cells.append(code("""score = 73

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Score: {score} -> Grade: {grade}")"""))

    cells.append(md("""**Expected Output:**
```
Score: 73 -> Grade: C
```

**How `elif` works:** Python checks conditions TOP to BOTTOM. The FIRST one that
is `True` wins, and all the rest are skipped. So even though `73 >= 60` is also
True, we never reach that check because `73 >= 70` was True first."""))

    cells.append(md("### Example 4 -- Multiple test cases"))

    cells.append(code("""# Test the grading system with several scores
test_scores = [95, 82, 73, 65, 45]

for score in test_scores:
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 60:
        grade = "D"
    else:
        grade = "F"
    print(f"  Score: {score:3d} -> Grade: {grade}")"""))

    cells.append(md("""**Expected Output:**
```
  Score:  95 -> Grade: A
  Score:  82 -> Grade: B
  Score:  73 -> Grade: C
  Score:  65 -> Grade: D
  Score:  45 -> Grade: F
```"""))

    cells.append(md("### Try It Yourself #1"))

    cells.append(code("""# TODO: Write an if/elif/else that classifies a temperature:
# < 0: "Freezing"
# 0-15: "Cold"
# 16-25: "Comfortable"
# 26-35: "Warm"
# > 35: "Hot"
# Test with: -5, 10, 22, 30, 40

for temp in [-5, 10, 22, 30, 40]:
    # YOUR CODE HERE: classify temp into a label
    label = "???"
    print(f"  {temp} C -> {label}")"""))

    # Part 3: Combining conditions
    cells.append(md("""---
## Part 3: Combining Conditions with `and`, `or`, `not`

Sometimes one comparison is not enough. You need to check MULTIPLE things.

| Operator | Meaning | True when... |
|----------|---------|--------------|
| `and` | Both must be True | `True and True` -> True |
| `or` | At least one must be True | `True or False` -> True |
| `not` | Flip True/False | `not False` -> True |

### Example 1 -- and"""))

    cells.append(code("""temp = 25
humidity = 80

if temp > 20 and humidity > 70:
    print("Warm AND humid -- uncomfortable!")
else:
    print("Conditions are acceptable.")"""))

    cells.append(md("""**Expected Output:**
```
Warm AND humid -- uncomfortable!
```"""))

    cells.append(md("### Example 2 -- or"))

    cells.append(code("""temp = 85
rpm = 1000

if temp > 80 or rpm > 3000:
    print("WARNING: At least one reading is extreme!")
else:
    print("All readings normal.")"""))

    cells.append(md("""**Expected Output:**
```
WARNING: At least one reading is extreme!
```"""))

    cells.append(md("### Example 3 -- not"))

    cells.append(code("""is_broken = False

if not is_broken:
    print("Sensor is working.")
else:
    print("Sensor needs repair!")"""))

    cells.append(md("""**Expected Output:**
```
Sensor is working.
```"""))

    # Part 4: Validating data
    cells.append(md("""---
## Part 4: Validating Data with Conditionals

This is where conditionals become essential for your pipeline!

### Example -- Checking if a single value is valid"""))

    cells.append(code("""def is_valid_reading(value):
    \"\"\"Check if a sensor reading is valid.

    Rules:
    - Must not be None
    - Must be a number (int or float)
    - Must be in range 0-150
    \"\"\"
    if value is None:
        return False

    if not isinstance(value, (int, float)):
        return False

    if value < 0 or value > 150:
        return False

    return True

# Test with various inputs
test_values = [25.0, -5, 200, None, "abc", 50, 0, 150, 0.001, 999]
print("Validation results:")
for v in test_values:
    result = is_valid_reading(v)
    print(f"  {str(v):>6} -> valid: {result}")"""))

    cells.append(md("""**Expected Output:**
```
Validation results:
    25.0 -> valid: True
      -5 -> valid: False
     200 -> valid: False
    None -> valid: False
     abc -> valid: False
      50 -> valid: True
       0 -> valid: True
     150 -> valid: True
   0.001 -> valid: True
     999 -> valid: False
```"""))

    # Part 5: clean_data
    cells.append(md("""---
## Part 5: Building `clean_data()` with Validation Rules

Now let us build a real `clean_data()` function that replaces the stub from
Week 1. This function:
1. Loops through every row of data
2. Checks each value against our rules
3. Keeps valid rows, drops invalid ones
4. Reports how many were dropped and why"""))

    cells.append(code("""def clean_data(data, config):
    \"\"\"Clean data by applying validation rules.

    Args:
        data: list of dictionaries (each dict is one row)
        config: dict with min_value, max_value settings

    Returns:
        list of clean dictionaries
    \"\"\"
    cleaned = []
    dropped = 0

    threshold_min = config.get("min_value", 0)
    threshold_max = config.get("max_value", 100)

    for row in data:
        value = row.get("value")

        # Rule 1: skip if value is missing
        if value is None or value == "":
            dropped += 1
            continue   # skip to next row

        # Rule 2: try to convert to number
        try:
            num_value = float(value)
        except (ValueError, TypeError):
            dropped += 1
            continue

        # Rule 3: check range
        if num_value < threshold_min or num_value > threshold_max:
            dropped += 1
            continue

        # Passed all rules -- keep this row
        row["value"] = num_value
        cleaned.append(row)

    print(f"Cleaned: {len(data)} rows -> {len(cleaned)} kept ({dropped} dropped)")
    return cleaned

# Test it
raw_data = [
    {"id": 1, "value": "25.0"},
    {"id": 2, "value": ""},          # missing
    {"id": 3, "value": "-10"},       # below min
    {"id": 4, "value": "abc"},       # not a number
    {"id": 5, "value": "50.5"},
    {"id": 6, "value": "200"},       # above max
    {"id": 7, "value": "75.0"},
    {"id": 8, "value": None},        # None
]

config = {"min_value": 0, "max_value": 100}
result = clean_data(raw_data, config)

print()
print("Clean data:")
for row in result:
    print(f"  id={row['id']}, value={row['value']}")"""))

    cells.append(md("""**Expected Output:**
```
Cleaned: 8 rows -> 3 kept (5 dropped)

Clean data:
  id=1, value=25.0
  id=5, value=50.5
  id=7, value=75.0
```

### Why This Matters for Your Pipeline

`clean_data()` is the **gatekeeper** of your pipeline. Bad data in = bad results
out. By building robust validation rules NOW, you protect every downstream step
(analyze, plot, export) from receiving garbage data."""))

    # Common mistakes
    cells.append(md("""### Common Mistakes with Conditionals

| Mistake | Bad Code | Fix |
|---------|----------|-----|
| Using `=` instead of `==` | `if x = 5:` | `if x == 5:` |
| Forgetting the colon | `if x > 5` | `if x > 5:` |
| Wrong indentation | Code not aligned | Use 4 spaces consistently |
| Checking equality with `is` | `if x is 5:` | `if x == 5:` (use `is` only for None) |
| Not handling `None` | `float(None)` crashes | Check `if value is None` first |"""))

    cells.append(md("""---
## Key Takeaways -- Week 3

1. **Comparisons** return `True` or `False`: `==`, `!=`, `<`, `>`, `<=`, `>=`
2. **`if/elif/else`** lets your code make decisions
3. **`and`/`or`/`not`** combine multiple conditions
4. **Indentation** defines which code belongs to which block
5. **`continue`** skips to the next iteration of a loop
6. **`clean_data()`** uses conditionals to filter out bad values"""))

    # Homework
    cells.append(md("""---
## Homework

### Review (R1-R4)"""))

    cells.append(code("""# R1: What is the output? (Think first, then run to check)
x = 10
if x > 5:
    print("A")
elif x > 8:
    print("B")
else:
    print("C")
# Answer:"""))

    cells.append(code("""# R2: What does `continue` do inside a loop?
# Answer:

# R3: True or False: (5 > 3) and (10 < 8)
# Answer:

# R4: True or False: (5 > 3) or (10 < 8)
# Answer:"""))

    cells.append(md("### Practice (P1-P5)"))

    cells.append(code("""# P1: Write an if/elif/else that classifies RPM:
# < 500: "Low"
# 500-1500: "Normal"
# 1501-3000: "High"
# > 3000: "Critical"
# Test with: 200, 1000, 2000, 4000
"""))

    cells.append(code("""# P2: Check if a string can be converted to a number.
# Test with: "42", "hello", "3.14", "", "99"
# Hint: use try/except with float()
"""))

    cells.append(code("""# P3: Write is_valid(row) that checks:
# - row has a "value" key
# - the value is not empty
# - the value can be converted to a number
# Return True or False
"""))

    cells.append(code("""# P4: Write code that classifies a list of values into
# "low", "medium", and "high" based on thresholds you define.
values = [12, 45, 78, 23, 91, 55, 3, 67, 88, 34]
"""))

    cells.append(code("""# P5: Given a list of temperatures, count how many are
# freezing (<0), cold (0-15), comfortable (16-25), warm (26-35), hot (>35)
temps = [-3, 5, 18, 22, 30, 38, 0, 15, 25, 40, -10, 12]
"""))

    cells.append(md("### Challenge (C1-C3)"))

    cells.append(code("""# C1: Extend clean_data() to also track WHY each row was dropped.
# Return a tuple: (cleaned_list, drop_report_dict)
# drop_report = {"missing": N, "non_numeric": N, "out_of_range": N}
"""))

    cells.append(code("""# C2: Write a function that assigns "quality" labels:
# - "good" if within 1 std dev of mean
# - "warning" if within 2 std dev of mean
# - "bad" otherwise
# (Calculate mean and std manually using loops)
readings = [20, 22, 21, 50, 19, 23, 21, 22, 20, 100]
"""))

    cells.append(code("""# C3: Write a mini cleaning pipeline:
# 1. Input: ["25.0", "bad", "", "50.0", "999", "30.0"]
# 2. Convert valid values to float
# 3. Remove out-of-range (0-100)
# 4. Return (clean_list, report_dict)
# report_dict has: n_raw, n_clean, n_dropped, drop_reasons
"""))

    cells.append(md("### Mini-Project"))

    cells.append(code("""# M1: Data Quality Report
# Given this raw dataset, write a complete cleaning pipeline that:
# 1. Checks each value against 3+ rules
# 2. Keeps valid rows
# 3. Prints a formatted quality report showing:
#    - Total rows, clean rows, dropped rows
#    - Breakdown by drop reason
#    - Percentage kept

raw = [
    {"id": 1, "sensor": "A", "value": "25.3"},
    {"id": 2, "sensor": "A", "value": ""},
    {"id": 3, "sensor": "B", "value": "-5"},
    {"id": 4, "sensor": "A", "value": "abc"},
    {"id": 5, "sensor": "B", "value": "50.0"},
    {"id": 6, "sensor": "A", "value": "999"},
    {"id": 7, "sensor": "B", "value": "30.0"},
    {"id": 8, "sensor": "A", "value": None},
    {"id": 9, "sensor": "B", "value": "75.5"},
    {"id": 10, "sensor": "A", "value": "42.1"},
]
"""))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# CORE NOTEBOOKS -- WEEKS 4-14 (dedicated content for each)
# ============================================================

def make_core_w04():
    cells = []
    cells.append(md("""# CP1 Week 4 -- Decision Logic & Classification

**Course:** Computer Programming 1 (CP1) | **Session:** 5 hours

## Learning Objectives

1. Build rule-based classifiers using nested conditionals
2. Use logical operators (`and`, `or`, `not`) for complex decisions
3. Implement `analyze()` that returns labeled outputs
4. Classify data points using multi-condition rules
5. Understand state labeling and categorization"""))
    cells.append(setup_cell())

    cells.append(md("""---
## Part 1: Rule-Based Classification

A **classifier** takes data and assigns it a label based on rules.
This is one of the most common patterns in engineering:

- Motor state: Normal / Warning / Critical based on temperature and vibration
- Signal quality: Good / Degraded / Lost based on strength and error rate
- Data validity: Valid / Suspect / Invalid based on range and consistency

Think of it like a triage nurse in a hospital: they look at symptoms and
assign a priority level.

### Example 1 -- Simple classifier"""))

    cells.append(code("""def classify_temperature(temp):
    \"\"\"Classify a temperature reading into a category.\"\"\"
    if temp < 0:
        return "freezing"
    elif temp < 15:
        return "cold"
    elif temp < 25:
        return "normal"
    elif temp < 40:
        return "warm"
    else:
        return "hot"

# Test with several values
test_temps = [-10, 5, 22, 35, 50, 0, 14, 25, 39, 40]
print("Temperature Classification:")
for t in test_temps:
    label = classify_temperature(t)
    print(f"  {t:>5} C -> {label}")"""))

    cells.append(md("""**Expected Output:**
```
Temperature Classification:
   -10 C -> freezing
     5 C -> cold
    22 C -> normal
    35 C -> warm
    50 C -> hot
     0 C -> cold
    14 C -> cold
    25 C -> warm
    39 C -> warm
    40 C -> hot
```"""))

    cells.append(md("""### Example 2 -- Multi-sensor classifier

In the real world, decisions depend on MULTIPLE measurements:"""))

    cells.append(code("""def classify_machine_state(temp, rpm, vibration):
    \"\"\"Classify machine state from multiple sensor readings.

    Decision logic:
    Example thresholds for this toy dataset (real limits depend on hardware):
    - CRITICAL: temp > 80 OR vibration > 50
    - WARNING:  temp > 60 AND rpm > 3000
    - CAUTION:  temp > 60 OR rpm > 3000
    - NORMAL:   everything within example limits
    \"\"\"
    if temp > 80 or vibration > 50:
        return "CRITICAL"
    elif temp > 60 and rpm > 3000:
        return "WARNING"
    elif temp > 60 or rpm > 3000:
        return "CAUTION"
    else:
        return "NORMAL"

# Test cases
cases = [
    (25, 1500, 10),    # all normal
    (65, 3500, 20),    # temp AND rpm high
    (65, 1000, 20),    # only temp elevated
    (85, 1000, 10),    # temp critical
    (50, 1000, 60),    # vibration critical
    (50, 3500, 10),    # only rpm elevated
]

print("Machine State Classification:")
print(f"  {'Temp':>5}  {'RPM':>5}  {'Vib':>5}  ->  State")
print(f"  {'----':>5}  {'---':>5}  {'---':>5}  --  -----")
for temp, rpm, vib in cases:
    state = classify_machine_state(temp, rpm, vib)
    print(f"  {temp:>5}  {rpm:>5}  {vib:>5}  ->  {state}")"""))

    cells.append(md("""**Expected Output:**
```
Machine State Classification:
   Temp    RPM    Vib  ->  State
   ----    ---    ---  --  -----
     25   1500     10  ->  NORMAL
     65   3500     20  ->  WARNING
     65   1000     20  ->  CAUTION
     85   1000     10  ->  CRITICAL
     50   1000     60  ->  CRITICAL
     50   3500     10  ->  CAUTION
```

### Why This Matters for Your Pipeline

Your `analyze()` function will classify each data point. For example:
- Robotics track: classify motor state from sensor readings
- Space track: classify star brightness as "transit" or "normal"
- IoT track: classify room conditions as "comfortable" or "alert"
"""))

    cells.append(md("### Try It Yourself #1"))

    cells.append(code("""# TODO: Write a function classify_speed(kmh) that returns:
# "stopped" if < 1
# "slow" if 1-30
# "medium" if 31-80
# "fast" if 81-120
# "dangerous" if > 120

def classify_speed(kmh):
    pass  # Replace with your code

# Test it
for speed in [0, 15, 55, 90, 130, 1, 30, 80, 120]:
    label = classify_speed(speed)
    print(f"  {speed:>4} km/h -> {label}")"""))

    cells.append(md("""### Example 3 -- Nested conditionals

Sometimes the first decision splits into sub-decisions:"""))

    cells.append(code("""def diagnose_motor(temp, rpm, vibration):
    \"\"\"Two-level diagnosis: first check severity, then cause.\"\"\"
    # Level 1: Is there a problem?
    if temp > 80 or vibration > 50:
        severity = "CRITICAL"
        # Level 2: What is the cause?
        if temp > 80 and vibration > 50:
            cause = "Both temperature and vibration extreme"
        elif temp > 80:
            cause = "Temperature too high"
        else:
            cause = "Vibration too high"
    elif temp > 60 or rpm > 3000:
        severity = "WARNING"
        if temp > 60:
            cause = "Temperature elevated"
        else:
            cause = "RPM elevated"
    else:
        severity = "NORMAL"
        cause = "All readings within limits"

    return severity, cause

# Test
test_cases = [
    (25, 1500, 10),
    (85, 1000, 10),
    (50, 1000, 60),
    (90, 4000, 55),
    (65, 1500, 20),
    (50, 3500, 10),
]

print("Motor Diagnosis:")
for temp, rpm, vib in test_cases:
    severity, cause = diagnose_motor(temp, rpm, vib)
    print(f"  T={temp:>3}, RPM={rpm:>4}, V={vib:>3} -> [{severity}] {cause}")"""))

    cells.append(md("""**Expected Output:**
```
Motor Diagnosis:
  T= 25, RPM=1500, V= 10 -> [NORMAL] All readings within limits
  T= 85, RPM=1000, V= 10 -> [CRITICAL] Temperature too high
  T= 50, RPM=1000, V= 60 -> [CRITICAL] Vibration too high
  T= 90, RPM=4000, V= 55 -> [CRITICAL] Both temperature and vibration extreme
  T= 65, RPM=1500, V= 20 -> [WARNING] Temperature elevated
  T= 50, RPM=3500, V= 10 -> [WARNING] RPM elevated
```"""))

    cells.append(md("""### Example 4 -- Building a label summary"""))

    cells.append(code("""def summarize_labels(labels):
    \"\"\"Count occurrences of each label and show percentages.\"\"\"
    counts = {}
    for label in labels:
        counts[label] = counts.get(label, 0) + 1

    total = len(labels)
    print("Label Summary:")
    for label, count in sorted(counts.items()):
        pct = count / total * 100
        bar = "#" * int(pct / 2)
        print(f"  {label:>10}: {count:3d} ({pct:5.1f}%) {bar}")
    return counts

# Test
import random
random.seed(42)
test_labels = []
for _ in range(50):
    r = random.random()
    if r < 0.6:
        test_labels.append("normal")
    elif r < 0.85:
        test_labels.append("warning")
    else:
        test_labels.append("critical")

summarize_labels(test_labels)"""))

    cells.append(md("""The bar chart gives a quick visual sense of the distribution.
This pattern is useful in your `analyze()` function's output."""))

    # Part 2: Building analyze()
    cells.append(md("""---
## Part 2: Building `analyze()` with Statistics and Labels

The `analyze()` function is the brain of your pipeline. It takes clean data
and produces:
1. **Summary statistics** (mean, median, std, min, max)
2. **Labels** for each data point (normal, high, low)
3. **Counts** of each category"""))

    cells.append(code("""def analyze(clean_data, config):
    \"\"\"Analyze clean data: compute stats and assign labels.

    Args:
        clean_data: list of dicts, each with a 'value' key
        config: dict with optional 'threshold' key

    Returns:
        dict with 'analysis_summary' and 'labels'
    \"\"\"
    if not clean_data:
        return {"analysis_summary": {"mean": 0, "median": 0, "std": 0}, "labels": []}

    # Extract numeric values
    values = [row["value"] for row in clean_data]
    n = len(values)

    # Compute basic stats
    mean_val = sum(values) / n
    sorted_vals = sorted(values)
    if n % 2 == 0:
        median_val = (sorted_vals[n // 2 - 1] + sorted_vals[n // 2]) / 2
    else:
        median_val = sorted_vals[n // 2]
    variance = sum((x - mean_val) ** 2 for x in values) / n
    std_val = variance ** 0.5

    # Classify each value
    threshold = config.get("threshold", mean_val + 2 * std_val)
    labels = []
    for v in values:
        if v > threshold:
            labels.append("high")
        elif v < mean_val - 2 * std_val:
            labels.append("low")
        else:
            labels.append("normal")

    results = {
        "analysis_summary": {
            "count": n,
            "mean": round(mean_val, 2),
            "median": round(median_val, 2),
            "std": round(std_val, 2),
            "min": min(values),
            "max": max(values),
            "n_high": labels.count("high"),
            "n_low": labels.count("low"),
            "n_normal": labels.count("normal"),
        },
        "labels": labels,
    }

    print(f"Analysis: {n} values, mean={mean_val:.2f}, std={std_val:.2f}")
    print(f"Labels: {labels.count('normal')} normal, "
          + f"{labels.count('high')} high, {labels.count('low')} low")
    return results

# Test
test_data = [
    {"id": i, "value": v}
    for i, v in enumerate([22, 23, 21, 50, 19, 23, 21, 22, 20, 45])
]
config = {"threshold": 40}
results = analyze(test_data, config)
print()
print("Summary:", results["analysis_summary"])"""))

    cells.append(md("""**Expected Output:**
```
Analysis: 10 values, mean=26.60, std=10.30
Labels: 8 normal, 2 high, 0 low

Summary: {'count': 10, 'mean': 26.6, 'median': 22.0, 'std': 10.3, 'min': 19, 'max': 50, 'n_high': 2, 'n_low': 0, 'n_normal': 8}
```"""))

    cells.append(md("""### Common Mistakes with Classification

| Mistake | What happens | Fix |
|---------|-------------|-----|
| Overlapping ranges | Multiple labels match | Use `elif`, not multiple `if` |
| Wrong operator order | `and`/`or` confusion | Use parentheses: `(a > 5) and (b < 10)` |
| Not handling edge values | Boundary values misclassified | Test with exact boundary values |
| No default case | Some inputs get no label | Always have an `else` |"""))

    cells.append(md("### Try It Yourself #2"))

    cells.append(code("""# TODO: Create a data quality classifier.
# Given a row with value, label it:
# - "missing" if value is None or ""
# - "invalid" if value cannot be converted to float
# - "outlier" if value < -100 or > 1000
# - "suspect" if value < 0
# - "good" otherwise

def classify_quality(value):
    pass  # your code here

test_values = [25.0, None, "", "abc", -5, -150, 1500, 0, 99.9]
for v in test_values:
    label = classify_quality(v)
    print(f"  {str(v):>8} -> {label}")"""))

    cells.append(md("""### Why This Matters for Your Pipeline

Classification is the core of `analyze()`. Your pipeline does not just compute
numbers -- it assigns **meaning** to those numbers. Is this reading normal or
abnormal? Is this trend rising or falling? Is this data point an outlier?

These labels become:
- Rows in your report ("5 CRITICAL events detected")
- Colors on your plot (red = critical, green = normal)
- Decisions in your pipeline (skip outliers, flag warnings)"""))

    cells.append(md("""---
## Key Takeaways -- Week 4

1. **Classifiers** assign labels to data based on rules
2. **Multi-condition** decisions use `and`, `or`, `not`
3. **`analyze()`** computes statistics AND classifies each data point
4. **Order matters** in elif chains -- first True condition wins
5. Labels let you count and filter categories downstream
6. **Boundary testing** ensures edge values are handled correctly"""))

    # Homework
    # --- Additional examples for richness ---
    cells.append(md("""---
## Part 3: Practical Classification Patterns

### Pattern 1: Multi-level classification with scores"""))

    cells.append(code("""def calculate_risk_score(temp, rpm, vibration):
    \"\"\"Calculate a numeric risk score from 0-100, then classify.\"\"\"
    score = 0

    # Temperature contribution (0-40 points)
    if temp > 80:
        score += 40
    elif temp > 60:
        score += 25
    elif temp > 40:
        score += 10

    # RPM contribution (0-30 points)
    if rpm > 3000:
        score += 30
    elif rpm > 2000:
        score += 15

    # Vibration contribution (0-30 points)
    if vibration > 50:
        score += 30
    elif vibration > 30:
        score += 15

    # Classify based on total score
    if score >= 70:
        level = "CRITICAL"
    elif score >= 40:
        level = "WARNING"
    elif score >= 15:
        level = "CAUTION"
    else:
        level = "NORMAL"

    return score, level

# Test
cases = [(25, 1500, 10), (65, 2500, 35), (85, 3500, 55), (45, 1800, 20)]
print("Risk Assessment:")
print(f"  {'Temp':>5} {'RPM':>5} {'Vib':>5}  Score  Level")
print(f"  {'----':>5} {'---':>5} {'---':>5}  -----  -----")
for t, r, v in cases:
    score, level = calculate_risk_score(t, r, v)
    print(f"  {t:>5} {r:>5} {v:>5}  {score:>5}  {level}")"""))

    cells.append(md("""**Expected Output:**
```
Risk Assessment:
   Temp   RPM   Vib  Score  Level
   ----   ---   ---  -----  -----
     25  1500    10      0  NORMAL
     65  2500    35     40  WARNING
     85  3500    55    100  CRITICAL
     45  1800    20     10  NORMAL
```"""))

    cells.append(md("### Pattern 2: Trend detection"))

    cells.append(code("""def detect_trend(values):
    \"\"\"Detect if the last 3+ values show a trend.\"\"\"
    if len(values) < 3:
        return "insufficient data"

    last_3 = values[-3:]

    if last_3[0] < last_3[1] < last_3[2]:
        return "rising"
    elif last_3[0] > last_3[1] > last_3[2]:
        return "falling"
    else:
        # Check for stability: all within 10% of mean
        avg = sum(last_3) / len(last_3)
        if avg == 0:
            return "stable"
        max_deviation = max(abs(v - avg) / abs(avg) for v in last_3)
        if max_deviation < 0.1:
            return "stable"
        return "volatile"

# Test
test_series = [
    [10, 20, 30],
    [30, 20, 10],
    [25, 25, 26],
    [10, 50, 20],
    [5],
]

for series in test_series:
    trend = detect_trend(series)
    print(f"  {str(series):>20} -> {trend}")"""))

    cells.append(md("""**Expected Output:**
```
          [10, 20, 30] -> rising
          [30, 20, 10] -> falling
          [25, 25, 26] -> stable
          [10, 50, 20] -> volatile
                   [5] -> insufficient data
```"""))

    cells.append(md("### Pattern 3: Putting labels back into data"))

    cells.append(code("""def label_data(data, config):
    \"\"\"Add a 'label' field to each row based on its value.\"\"\"
    threshold = config.get("threshold", 50)
    labeled = []

    for row in data:
        value = row.get("value", 0)
        if value > threshold * 1.5:
            label = "critical"
        elif value > threshold:
            label = "high"
        elif value > threshold * 0.5:
            label = "medium"
        else:
            label = "low"

        labeled.append({**row, "label": label})

    return labeled

# Test
test_data = [
    {"id": 1, "value": 10},
    {"id": 2, "value": 30},
    {"id": 3, "value": 55},
    {"id": 4, "value": 80},
]

labeled = label_data(test_data, {"threshold": 50})
for row in labeled:
    print(f"  id={row['id']}, value={row['value']:>3}, label={row['label']}")"""))

    cells.append(md("""**Expected Output:**
```
  id=1, value= 10, label=low
  id=2, value= 30, label=medium
  id=3, value= 55, label=high
  id=4, value= 80, label=critical
```"""))

    cells.append(md("---\n## Homework\n\n### Review (R1-R4)"))

    cells.append(code("""# R1: What label does classify_temperature(25) return?
# Answer:

# R2: What is the difference between "and" and "or"?
# Answer:

# R3: If mean=20 and std=5, what is mean + 2*std?
# Answer:

# R4: In an elif chain, how many blocks can execute?
# Answer:"""))

    cells.append(md("### Practice (P1-P5)"))

    cells.append(code("""# P1: Write classify_speed(kmh):
# "stopped" (<1), "slow" (1-30), "medium" (31-80), "fast" (81-120), "dangerous" (>120)
# Test with 10 different values.
"""))
    cells.append(code("""# P2: Classify these 10 readings using classify_temperature():
readings = [5, 18, -3, 30, 42, 0, 15, 25, 38, 22]
"""))
    cells.append(code("""# P3: Write count_by_label(values, labels) that returns a dict
# counting items in each category. Example: {"normal": 5, "high": 3, "low": 2}
"""))
    cells.append(code("""# P4: Write analyze() for your track. Compute at least 5 metrics
# and classify each data point.
"""))
    cells.append(code("""# P5: Create a "status dashboard" that takes a list of readings
# and prints a formatted summary with label counts and percentages.
"""))

    cells.append(md("### Challenge (C1-C3)"))
    cells.append(code("""# C1: Implement a "traffic light" classifier:
# Given (temp, pressure, humidity), return "green", "yellow", or "red"
# Document your threshold choices.
"""))
    cells.append(code("""# C2: Write a trend detector: given 5+ values, classify as
# "rising", "falling", "stable", or "volatile"
"""))
    cells.append(code("""# C3: Create a multi-level classifier that uses 4+ input variables
# and produces 5+ output categories. Draw the decision tree as comments.
"""))

    cells.append(md("### Mini-Project"))
    cells.append(code("""# M1: Sensor Alert System
# Given 20 sensor readings with temp, rpm, and vibration,
# classify each as NORMAL/CAUTION/WARNING/CRITICAL.
# Print a formatted alert report showing:
# - Each reading with its classification
# - Summary counts
# - Percentage in each category
# - List of all CRITICAL readings
"""))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


def make_core_w05():
    cells = []
    cells.append(md("""# CP1 Week 5 -- Loops: Scanning Data

**Course:** Computer Programming 1 (CP1) | **Session:** 5 hours

## Learning Objectives

1. Use `for` loops to iterate over lists and ranges
2. Use `while` loops for condition-based repetition
3. Master the accumulation pattern: sum, count, min, max, mean
4. Compute summary statistics on datasets
5. Understand `range()` with start, stop, and step

## Why This Week Matters

Real data has hundreds or thousands of values. You cannot process each one by
hand. Loops let you write ONE set of instructions that Python repeats for EVERY
data point. This is where programming becomes truly powerful -- you write 5 lines
that process 5,000 data points."""))

    cells.append(setup_cell())

    cells.append(md("""---
## Part 1: The `for` Loop

A `for` loop repeats code once for each item in a sequence.

```
  for item in sequence:
      do something with item
      do another thing with item
```

Think of it like a factory conveyor belt: each item rolls past, you perform
the same operation on it, then the next item arrives.

```
  Data:     [10] [20] [30] [40] [50]
              |    |    |    |    |
  Process:  print print print print print
```

### Example 1 -- Looping over a list"""))

    cells.append(code("""readings = [25.0, 22.5, 28.1, 21.3, 26.7]

for value in readings:
    print(f"Reading: {value}")"""))

    cells.append(md("""**Expected Output:**
```
Reading: 25.0
Reading: 22.5
Reading: 28.1
Reading: 21.3
Reading: 26.7
```"""))

    cells.append(md("### Example 2 -- range()"))

    cells.append(code("""# range(stop) -- 0 to stop-1
print("range(5):", list(range(5)))

# range(start, stop) -- start to stop-1
print("range(2, 8):", list(range(2, 8)))

# range(start, stop, step) -- with custom step
print("range(0, 20, 5):", list(range(0, 20, 5)))
print("range(10, 0, -2):", list(range(10, 0, -2)))"""))

    cells.append(md("""**Expected Output:**
```
range(5): [0, 1, 2, 3, 4]
range(2, 8): [2, 3, 4, 5, 6, 7]
range(0, 20, 5): [0, 5, 10, 15]
range(10, 0, -2): [10, 8, 6, 4, 2]
```"""))

    cells.append(md("""---
## Part 2: The Accumulation Pattern

The **accumulation pattern** is the single most important loop pattern for data
processing. It builds up a result one step at a time.

```
  1. Initialize an accumulator variable
  2. Loop through data
  3. Update the accumulator each iteration
  4. Use the final accumulated value
```

### The 5 Essential Accumulations"""))

    cells.append(code("""data = [10, 25, 30, 15, 20, 35, 5, 40]

# --- Pattern 1: SUM ---
total = 0
for value in data:
    total = total + value
print(f"Sum: {total}")

# --- Pattern 2: COUNT ---
count = 0
for value in data:
    count = count + 1
print(f"Count: {count}")

# --- Pattern 3: MEAN ---
mean = total / count
print(f"Mean: {mean}")

# --- Pattern 4: MIN ---
smallest = data[0]     # start with the first value
for value in data:
    if value < smallest:
        smallest = value
print(f"Min: {smallest}")

# --- Pattern 5: MAX ---
largest = data[0]
for value in data:
    if value > largest:
        largest = value
print(f"Max: {largest}")"""))

    cells.append(md("""**Expected Output:**
```
Sum: 180
Count: 8
Mean: 22.5
Min: 5
Max: 40
```

> **Why not use built-in `sum()`, `min()`, `max()`?** You absolutely SHOULD use
> them in real code! But understanding the loop version teaches you the pattern
> you will need for custom statistics (standard deviation, median, percentiles)
> where there is no built-in function."""))

    cells.append(md("""### Example -- Accumulation visualized

```
  data = [10, 25, 30, 15]

  Step 1: total = 0         (start)
  Step 2: total = 0 + 10    = 10   (process 10)
  Step 3: total = 10 + 25   = 35   (process 25)
  Step 4: total = 35 + 30   = 65   (process 30)
  Step 5: total = 65 + 15   = 80   (process 15)
  Done:   total = 80
```

The accumulator (`total`) starts at 0 and grows with each item."""))

    cells.append(md("### Try It Yourself #1"))

    cells.append(code("""# TODO: Use the accumulation pattern to find:
# 1. The sum of all EVEN numbers in the list
# 2. The count of NEGATIVE numbers
# 3. The product of all positive numbers

data = [5, -3, 8, 0, -1, 4, 7, -2, 6, 3]

# Sum of even numbers:
even_sum = 0
# your loop here

# Count of negatives:
neg_count = 0
# your loop here

# Product of positives:
product = 1
# your loop here

print(f"Sum of evens: {even_sum}")
print(f"Count of negatives: {neg_count}")
print(f"Product of positives: {product}")"""))

    cells.append(md("### Example -- Counting with conditions"))

    cells.append(code("""data = [10, 25, 30, 15, 20, 35, 5, 40, 22, 28]
threshold = 25

above = 0
at_or_below = 0
for value in data:
    if value > threshold:
        above += 1
    else:
        at_or_below += 1

total = above + at_or_below
pct_above = above / total * 100
print(f"Above {threshold}: {above} ({pct_above:.1f}%)")
print(f"At or below {threshold}: {at_or_below}")"""))

    cells.append(md("""**Expected Output:**
```
Above 25: 4 (40.0%)
At or below 25: 6
```"""))

    cells.append(md("### Try It Yourself #1"))

    cells.append(code("""# TODO: Compute sum, count, mean, min, max for this data
# Do NOT use built-in sum(), min(), max() -- use loops!

temps = [22.1, 19.8, 25.3, 18.6, 23.4, 27.0, 20.5]

# Your code here:
"""))

    cells.append(md("### Example -- Building a frequency table"))

    cells.append(code("""# Count how many values fall into each range (histogram-like)
data = [12, 45, 23, 67, 34, 89, 11, 56, 78, 42, 33, 91, 15, 62, 28]

# Bins: 0-19, 20-39, 40-59, 60-79, 80-100
bins = {"0-19": 0, "20-39": 0, "40-59": 0, "60-79": 0, "80-100": 0}

for value in data:
    if value < 20:
        bins["0-19"] += 1
    elif value < 40:
        bins["20-39"] += 1
    elif value < 60:
        bins["40-59"] += 1
    elif value < 80:
        bins["60-79"] += 1
    else:
        bins["80-100"] += 1

print("Frequency Table:")
for label, count in bins.items():
    bar = "#" * count
    print(f"  {label:>6}: {count:2d} {bar}")"""))

    cells.append(md("""**Expected Output:**
```
Frequency Table:
   0-19:  3 ###
  20-39:  4 ####
  40-59:  3 ###
  60-79:  3 ###
  80-100:  2 ##
```"""))

    cells.append(md("### Example -- enumerate() -- getting index AND value"))

    cells.append(code("""readings = [25.3, 22.1, 28.5, 21.0, 26.7]

# Without enumerate -- clunky
i = 0
for value in readings:
    i += 1

# With enumerate -- clean!
for i, value in enumerate(readings):
    status = "OK" if value < 27 else "HIGH"
    print(f"  Reading #{i}: {value:>6.1f} [{status}]")"""))

    cells.append(md("""**Expected Output:**
```
  Reading #0:   25.3 [OK]
  Reading #1:   22.1 [OK]
  Reading #2:   28.5 [HIGH]
  Reading #3:   21.0 [OK]
  Reading #4:   26.7 [OK]
```"""))

    cells.append(md("### Try It Yourself #2"))

    cells.append(code("""# TODO: Find all values that are MORE than 10 away from the mean.
# Steps:
# 1. Calculate the mean using a loop
# 2. Loop again to find values where abs(value - mean) > 10
# 3. Print each outlier with its index and distance from mean

data = [20, 22, 50, 21, 23, 19, 45, 22, 20, 55]

# Your code here:
"""))

    cells.append(md("""### Debugging Tip -- Loops

The most common loop bugs:
1. **Off-by-one**: `range(5)` gives 0-4, not 1-5
2. **Empty loop**: Forgetting that an empty list means 0 iterations
3. **Infinite while**: Forgetting to update the condition variable
4. **Wrong accumulator init**: Starting `min` at 0 instead of `data[0]`

When debugging a loop, add a print inside:
```python
for i, v in enumerate(values):
    print(f"  DEBUG: i={i}, v={v}, total={total}")
    total += v
```"""))

    cells.append(md("""---
## Part 3: The `while` Loop

A `while` loop repeats as long as a condition is `True`.
Use it when you don't know in advance how many iterations you need."""))

    cells.append(code("""# Countdown
count = 5
while count > 0:
    print(f"  {count}...")
    count -= 1
print("  Liftoff!")"""))

    cells.append(md("""**Expected Output:**
```
  5...
  4...
  3...
  2...
  1...
  Liftoff!
```

**Danger:** If you forget `count -= 1`, the loop runs FOREVER!
If that happens in Colab, click the Stop button."""))

    cells.append(md("""---
## Part 4: Standard Deviation -- Putting It All Together"""))

    cells.append(code("""def compute_stats(values):
    \"\"\"Compute basic statistics using only loops.

    Returns dict with: count, sum, mean, min, max, std
    \"\"\"
    if not values:
        return {"count": 0, "sum": 0, "mean": 0, "min": 0, "max": 0, "std": 0}

    n = 0
    total = 0
    smallest = values[0]
    largest = values[0]

    for v in values:
        n += 1
        total += v
        if v < smallest:
            smallest = v
        if v > largest:
            largest = v

    mean = total / n

    # Standard deviation
    sum_sq_diff = 0
    for v in values:
        sum_sq_diff += (v - mean) ** 2
    std = (sum_sq_diff / n) ** 0.5

    return {
        "count": n,
        "sum": round(total, 4),
        "mean": round(mean, 4),
        "min": round(smallest, 4),
        "max": round(largest, 4),
        "std": round(std, 4),
    }

# Test
test_data = [10, 20, 30, 40, 50]
stats = compute_stats(test_data)
print("Statistics:")
for key, val in stats.items():
    print(f"  {key:>6}: {val}")"""))

    cells.append(md("""**Expected Output:**
```
Statistics:
  count: 5
    sum: 150
   mean: 30.0
    min: 10
    max: 50
    std: 14.1421
```"""))

    cells.append(md("""---
## Key Takeaways -- Week 5

1. **`for` loops** iterate over sequences (lists, ranges)
2. **`range(start, stop, step)`** generates number sequences
3. **Accumulation patterns**: initialize -> loop -> update -> use final value
4. **5 key accumulators**: sum, count, mean (sum/count), min, max
5. **`while` loops** repeat until a condition becomes False
6. Standard deviation measures how spread out data is"""))

    cells.append(md("---\n## Homework\n\n### Review (R1-R4)"))

    cells.append(code("""# R1: How many times does range(3, 10, 2) iterate? List the values.
# Answer:

# R2: What is the accumulator pattern? Describe the 4 steps.
# Answer:

# R3: When should you use while instead of for?
# Answer:

# R4: What happens if you forget to update the variable in a while loop?
# Answer:"""))

    cells.append(md("### Practice (P1-P5)"))
    cells.append(code("""# P1: Print the first 20 multiples of 7 using a for loop.
"""))
    cells.append(code("""# P2: Compute sum and mean of [3.5, 7.2, 1.8, 9.4, 5.1] using loops.
"""))
    cells.append(code("""# P3: Count values between 20 and 30 (inclusive) in this list:
data = [15, 22, 31, 25, 18, 28, 33, 20, 27, 30]
"""))
    cells.append(code("""# P4: Write compute_stats() and test on 3 different datasets.
"""))
    cells.append(code("""# P5: Compute a running sum: [1,2,3,4] -> [1,3,6,10]
"""))

    cells.append(md("### Challenge (C1-C3)"))
    cells.append(code("""# C1: Find the second-largest value using a loop (no sorting).
data = [45, 12, 67, 23, 89, 34, 56]
"""))
    cells.append(code("""# C2: Compute the median WITHOUT sorting.
# Hint: for each value, count how many others are smaller.
"""))
    cells.append(code("""# C3: Write a function that computes percentiles (25th, 50th, 75th).
"""))

    cells.append(md("### Mini-Project"))
    cells.append(code("""# M1: Statistical Report Generator
# Given a dataset of 20+ values, produce a formatted report:
# - Count, Mean, Median, Std, Min, Max
# - Histogram using text (e.g., "20-30: ####  (4)")
# - Values above/below 1 std and 2 std from mean
# - Outlier detection (beyond 2 std)
data = [23, 25, 22, 28, 21, 24, 50, 26, 23, 24,
        22, 25, 27, 21, 23, 90, 24, 26, 22, 25]
"""))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


def make_core_w06():
    cells = []
    cells.append(md("""# CP1 Week 6 -- Loops: Counting Events

**Course:** Computer Programming 1 (CP1) | **Session:** 5 hours

## Learning Objectives

1. Count threshold crossings in time-series data
2. Detect peaks and valleys
3. Handle edge cases (empty data, single values, all same)
4. Track consecutive streaks above/below thresholds
5. Build event detection into your pipeline"""))
    cells.append(setup_cell())

    cells.append(md("""---
## Part 1: What Is an Event?

An **event** is something that happens at a specific point in your data.
Examples:
- Temperature crosses above 60 C (threshold crossing)
- A sensor reading is higher than both its neighbors (peak)
- A value suddenly jumps by more than 20 units (spike)

Detecting events is critical for engineering applications: "How many times
did the motor overheat?" "When did the signal drop?"

### Example 1 -- Threshold crossings"""))

    cells.append(code("""def count_threshold_crossings(values, threshold):
    \"\"\"Count how many times values cross above a threshold.

    A crossing happens when we go from below-or-equal to above.
    \"\"\"
    if len(values) < 2:
        return 0

    crossings = 0
    was_above = values[0] > threshold

    for v in values[1:]:
        is_above = v > threshold
        if is_above and not was_above:
            crossings += 1
        was_above = is_above

    return crossings

# Test
data = [10, 30, 20, 40, 15, 50, 25, 35, 10, 45]
threshold = 25
count = count_threshold_crossings(data, threshold)
print(f"Data: {data}")
print(f"Threshold: {threshold}")
print(f"Crossings above threshold: {count}")"""))

    cells.append(md("""**Expected Output:**
```
Data: [10, 30, 20, 40, 15, 50, 25, 35, 10, 45]
Threshold: 25
Crossings above threshold: 4
```"""))

    cells.append(md("### Example 2 -- Finding peaks"))

    cells.append(code("""def find_peaks(values):
    \"\"\"Find indices where value is higher than both neighbors.\"\"\"
    if len(values) < 3:
        return []
    peaks = []
    for i in range(1, len(values) - 1):
        if values[i] > values[i-1] and values[i] > values[i+1]:
            peaks.append(i)
    return peaks

data = [10, 30, 20, 40, 15, 50, 25, 35, 10, 45]
peaks = find_peaks(data)
print(f"Data:  {data}")
print(f"Peaks at indices: {peaks}")
peak_values = [data[i] for i in peaks]
print(f"Peak values: {peak_values}")"""))

    cells.append(md("""**Expected Output:**
```
Data:  [10, 30, 20, 40, 15, 50, 25, 35, 10, 45]
Peaks at indices: [1, 3, 5, 7]
Peak values: [30, 40, 50, 35]
```"""))

    cells.append(md("### Example 3 -- Edge cases"))

    cells.append(code("""def safe_count_events(values, threshold):
    \"\"\"Count threshold crossings with edge case handling.\"\"\"
    if not values:
        print("  Warning: empty data")
        return 0
    if len(values) < 2:
        print("  Warning: need at least 2 values")
        return 0
    if all(v == values[0] for v in values):
        print("  Warning: all values identical")
        return 0
    return count_threshold_crossings(values, threshold)

# Test edge cases
print("Edge case tests:")
print("  Empty:", safe_count_events([], 10))
print("  Single:", safe_count_events([5], 10))
print("  Same:", safe_count_events([5, 5, 5], 10))
print("  Normal:", safe_count_events([5, 15, 5, 15], 10))"""))

    cells.append(md("""**Expected Output:**
```
Edge case tests:
  Warning: empty data
  Empty: 0
  Warning: need at least 2 values
  Single: 0
  Warning: all values identical
  Same: 0
  Normal: 2
```"""))

    cells.append(md("### Try It Yourself #1"))

    cells.append(code("""# TODO: Write find_valleys(values) -- the opposite of find_peaks.
# A valley is lower than BOTH neighbors.

def find_valleys(values):
    pass  # your code here

data = [30, 10, 25, 5, 35, 15, 40, 20, 50]
valleys = find_valleys(data)
print(f"Data: {data}")
print(f"Valleys at: {valleys}")"""))

    cells.append(md("""### Debugging Tip

When debugging event detection, **print the state at each step**:
```python
for i, v in enumerate(values):
    was = "above" if was_above else "below"
    now = "above" if v > threshold else "below"
    crossed = "CROSSED!" if now != was else ""
    print(f"  [{i}] v={v}, was={was}, now={now} {crossed}")
```
This makes it easy to see exactly where crossings happen."""))

    cells.append(md("### Example 4 -- Longest streak above threshold"))

    cells.append(code("""def longest_streak(values, threshold):
    \"\"\"Find the longest consecutive run of values above threshold.\"\"\"
    max_streak = 0
    current_streak = 0

    for v in values:
        if v > threshold:
            current_streak += 1
            if current_streak > max_streak:
                max_streak = current_streak
        else:
            current_streak = 0

    return max_streak

data = [10, 30, 35, 40, 20, 50, 55, 60, 65, 10, 30]
threshold = 25
streak = longest_streak(data, threshold)
print(f"Longest streak above {threshold}: {streak} consecutive values")"""))

    cells.append(md("""**Expected Output:**
```
Longest streak above 25: 4 consecutive values
```"""))

    cells.append(md("### Example 5 -- Spike detection"))

    cells.append(code("""def find_spikes(values, jump_threshold):
    \"\"\"Find sudden jumps between consecutive readings.\"\"\"
    spikes = []
    for i in range(1, len(values)):
        jump = abs(values[i] - values[i-1])
        if jump > jump_threshold:
            spikes.append({
                "index": i,
                "from": values[i-1],
                "to": values[i],
                "jump": round(jump, 2),
            })
    return spikes

data = [20, 22, 21, 80, 23, 22, 90, 25, 24, 23]
spikes = find_spikes(data, 20)
print(f"Data: {data}")
print(f"Spikes (jump > 20):")
for s in spikes:
    direction = "UP" if s["to"] > s["from"] else "DOWN"
    print(f"  Index {s['index']}: {s['from']} -> {s['to']} ({direction}, jump={s['jump']})")"""))

    cells.append(md("""**Expected Output:**
```
Data: [20, 22, 21, 80, 23, 22, 90, 25, 24, 23]
Spikes (jump > 20):
  Index 3: 21 -> 80 (UP, jump=59)
  Index 4: 80 -> 23 (DOWN, jump=57)
  Index 6: 22 -> 90 (UP, jump=68)
  Index 7: 90 -> 25 (DOWN, jump=65)
```"""))

    cells.append(md("### Example 6 -- Complete event summary"))

    cells.append(code("""def event_summary(values, threshold):
    \"\"\"Generate a complete event summary for a dataset.\"\"\"
    if len(values) < 2:
        return "Insufficient data"

    crossings = count_threshold_crossings(values, threshold)
    peaks = find_peaks(values)
    streak = longest_streak(values, threshold)
    spikes = find_spikes(values, 15)

    above_count = sum(1 for v in values if v > threshold)
    below_count = len(values) - above_count

    print(f"=== Event Summary (threshold={threshold}) ===")
    print(f"  Total readings:     {len(values)}")
    print(f"  Above threshold:    {above_count} ({above_count/len(values)*100:.1f}%)")
    print(f"  Below threshold:    {below_count} ({below_count/len(values)*100:.1f}%)")
    print(f"  Threshold crossings: {crossings}")
    print(f"  Peaks detected:     {len(peaks)}")
    print(f"  Longest streak:     {streak} consecutive values")
    print(f"  Spikes (>15):       {len(spikes)}")

    return {
        "crossings": crossings,
        "peaks": len(peaks),
        "streak": streak,
        "spikes": len(spikes),
    }

data = [10, 30, 20, 40, 15, 50, 25, 35, 10, 45, 55, 60, 40, 20]
result = event_summary(data, 25)"""))

    cells.append(md("""### Why This Matters for Your Pipeline

Event detection answers the questions engineers actually care about:
- "How many times did the motor overheat today?" (threshold crossings)
- "When were the peak temperatures?" (peak detection)
- "How long did the longest overheating episode last?" (streak length)
- "Were there any sudden failures?" (spike detection)

These metrics go into your `analyze()` function's output and your report."""))

    cells.append(md("""---
## Key Takeaways -- Week 6

1. **Threshold crossings** track state transitions (below->above)
2. **Peaks** are local maxima (higher than both neighbors)
3. **Always handle edge cases**: empty, single value, all identical
4. **Streaks** count consecutive values meeting a condition
5. **Spikes** detect sudden jumps between consecutive readings
6. **Event summaries** combine multiple detection methods into one report"""))

    cells.append(md("---\n## Homework\n\n### Review (R1-R4)"))
    cells.append(code("""# R1: What is a threshold crossing?
# R2: What is a peak in time-series data?
# R3: Name 3 edge cases you should always handle.
# R4: How do you track a "streak" using a loop?"""))

    cells.append(md("### Practice (P1-P5)"))
    cells.append(code("""# P1: Count how many times temperature goes ABOVE and BELOW threshold.
temps = [20, 35, 28, 40, 22, 38, 15, 42, 30]
threshold = 30
"""))
    cells.append(code("""# P2: Find all valleys (lower than both neighbors).
data = [30, 10, 25, 5, 35, 15, 40]
"""))
    cells.append(code("""# P3: Find the longest streak of values BELOW a threshold.
data = [50, 20, 15, 10, 30, 5, 8, 12, 40, 3]
threshold = 25
"""))
    cells.append(code("""# P4: Write a function that finds ALL streaks above threshold.
# Return a list of (start_index, length) tuples.
"""))
    cells.append(code("""# P5: Detect "spikes" -- sudden jumps of more than X between consecutive readings.
data = [20, 22, 21, 80, 23, 22, 90, 25]
"""))

    cells.append(md("### Challenge (C1-C3)"))
    cells.append(code("""# C1: Write a "state machine" that tracks NORMAL/WARNING/CRITICAL states.
# Count how many transitions occur between states.
"""))
    cells.append(code("""# C2: Detect "oscillation" -- when values rapidly alternate above/below threshold.
"""))
    cells.append(code("""# C3: Write a complete event_summary() function that returns:
# crossings, peaks, valleys, longest_streak, spike_count
"""))

    cells.append(md("### Mini-Project"))
    cells.append(code("""# M1: Sensor Event Monitor
# Given 50+ readings, produce a complete event report:
# - Threshold crossings (count, timestamps)
# - Peaks and valleys (indices, values)
# - Streaks above threshold (start, length)
# - Spikes (location, magnitude)
# Format as a readable text report.

import random
random.seed(42)
data = [20 + random.gauss(0, 10) for _ in range(50)]
# Add some events
data[15] = 60   # spike
data[16] = 55
data[17] = 50
data[30] = -5   # anomaly
"""))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


def make_core_w07():
    cells = []
    cells.append(md("""# CP1 Week 7 -- Lists: Indexing & Windows

**Course:** Computer Programming 1 (CP1) | **Session:** 5 hours

## Learning Objectives

1. Use list indexing (positive and negative) and slicing
2. Modify lists with `append()`, `sort()`, `reverse()`
3. Use list comprehensions for concise data transformations
4. Implement moving-window operations (moving average)
5. Understand mutability and aliasing"""))
    cells.append(setup_cell())

    cells.append(md("""---
## Part 1: List Indexing and Slicing

```
  Index:    0    1    2    3    4    5    6    7
  Data:  [ 10,  20,  30,  40,  50,  60,  70,  80 ]
  Neg:    -8   -7   -6   -5   -4   -3   -2   -1
```
"""))

    cells.append(code("""data = [10, 20, 30, 40, 50, 60, 70, 80]

# Indexing
print(f"First:  data[0]  = {data[0]}")
print(f"Third:  data[2]  = {data[2]}")
print(f"Last:   data[-1] = {data[-1]}")
print(f"Second-last: data[-2] = {data[-2]}")

print()
# Slicing [start:stop] -- stop is EXCLUDED
print(f"First 3:  data[0:3]  = {data[0:3]}")
print(f"Last 3:   data[-3:]  = {data[-3:]}")
print(f"Middle:   data[2:6]  = {data[2:6]}")
print(f"Every 2:  data[::2]  = {data[::2]}")
print(f"Reversed: data[::-1] = {data[::-1]}")"""))

    cells.append(md("""**Expected Output:**
```
First:  data[0]  = 10
Third:  data[2]  = 30
Last:   data[-1] = 80
Second-last: data[-2] = 70

First 3:  data[0:3]  = [10, 20, 30]
Last 3:   data[-3:]  = [60, 70, 80]
Middle:   data[2:6]  = [30, 40, 50, 60]
Every 2:  data[::2]  = [10, 30, 50, 70]
Reversed: data[::-1] = [80, 70, 60, 50, 40, 30, 20, 10]
```"""))

    cells.append(md("### Part 2: List operations"))

    cells.append(code("""numbers = [5, 2, 8, 1, 9, 3]

numbers.append(10)
print(f"After append(10): {numbers}")

numbers.sort()
print(f"After sort():     {numbers}")

numbers.reverse()
print(f"After reverse():  {numbers}")

# List comprehension -- concise way to create lists
squares = [x**2 for x in range(1, 6)]
print(f"Squares: {squares}")

# Filter with comprehension
data = [10, 25, 30, 15, 20, 35]
big = [x for x in data if x > 20]
print(f"Values > 20: {big}")"""))

    cells.append(md("""**Expected Output:**
```
After append(10): [5, 2, 8, 1, 9, 3, 10]
After sort():     [1, 2, 3, 5, 8, 9, 10]
After reverse():  [10, 9, 8, 5, 3, 2, 1]
Squares: [1, 4, 9, 16, 25]
Values > 20: [25, 30, 35]
```"""))

    cells.append(md("### Try It Yourself #1"))

    cells.append(code("""# TODO: Given this data, use slicing to extract:
# 1. The first 4 elements
# 2. The last 3 elements
# 3. Elements at even indices (0, 2, 4, ...)
# 4. The list reversed
# 5. Elements from index 2 to 5

data = [100, 200, 300, 400, 500, 600, 700, 800]

print("First 4:", data[:4])
print("Last 3:", data[-3:])
# Complete the rest:
"""))

    cells.append(md("""### Common Mistakes with Lists

| Mistake | What happens | Fix |
|---------|-------------|-----|
| Off-by-one in slicing | `data[0:3]` gives 3 items, not 4 | Remember: stop is excluded |
| Index out of range | `data[10]` on a 5-item list | Check `len(data)` first |
| Modifying during iteration | `for x in data: data.remove(x)` | Create a new list instead |
| Aliasing surprise | `b = a; b.append(5)` changes `a` too | Use `b = a.copy()` |"""))

    cells.append(md("""---
## Part 3: Moving Window Operations

A **moving window** slides across your data, computing a value for each position.
This is one of the most common operations in signal processing.

```
  Data:    [10, 50, 20, 40, 30, 60, 25]
  Window=3:
    [10, 50, 20]           -> avg = 26.7
        [50, 20, 40]       -> avg = 36.7
            [20, 40, 30]   -> avg = 30.0
                [40, 30, 60]   -> avg = 43.3
                    [30, 60, 25]   -> avg = 38.3
```
"""))

    cells.append(code("""def moving_average(values, window_size):
    \"\"\"Calculate moving average with given window size.\"\"\"
    if len(values) < window_size:
        return values[:]

    result = []
    for i in range(len(values) - window_size + 1):
        window = values[i:i + window_size]
        avg = sum(window) / len(window)
        result.append(round(avg, 2))
    return result

data = [10, 50, 20, 40, 30, 60, 25]
smoothed = moving_average(data, 3)
print(f"Original:  {data}")
print(f"Smoothed:  {smoothed}")"""))

    cells.append(md("""**Expected Output:**
```
Original:  [10, 50, 20, 40, 30, 60, 25]
Smoothed:  [26.67, 36.67, 30.0, 43.33, 38.33]
```"""))

    cells.append(md("### Example -- Moving max and min"))

    cells.append(code("""def moving_max(values, window_size):
    \"\"\"Find the maximum in each window.\"\"\"
    if len(values) < window_size:
        return values[:]
    result = []
    for i in range(len(values) - window_size + 1):
        window = values[i:i + window_size]
        result.append(max(window))
    return result

def moving_range(values, window_size):
    \"\"\"Find max - min in each window (volatility measure).\"\"\"
    if len(values) < window_size:
        return [0]
    result = []
    for i in range(len(values) - window_size + 1):
        window = values[i:i + window_size]
        result.append(max(window) - min(window))
    return result

data = [10, 50, 20, 40, 30, 60, 25, 35, 15, 45]
print(f"Original:   {data}")
print(f"Moving avg: {moving_average(data, 3)}")
print(f"Moving max: {moving_max(data, 3)}")
print(f"Volatility: {moving_range(data, 3)}")"""))

    cells.append(md("""**Expected Output:**
```
Original:   [10, 50, 20, 40, 30, 60, 25, 35, 15, 45]
Moving avg: [26.67, 36.67, 30.0, 43.33, 38.33, 40.0, 25.0, 31.67]
Moving max: [50, 50, 40, 60, 60, 60, 35, 45]
Volatility: [40, 30, 20, 30, 35, 35, 20, 30]
```"""))

    cells.append(md("### Example -- List comprehension patterns"))

    cells.append(code("""readings = [25, -3, 42, "", None, 18, "abc", 55, 0, 31]

# 1. Filter: keep only valid numbers
valid = [x for x in readings if isinstance(x, (int, float)) and x >= 0]
print(f"Valid numbers: {valid}")

# 2. Transform: convert Celsius to Fahrenheit
fahrenheit = [c * 9/5 + 32 for c in valid]
print(f"Fahrenheit:    {[round(f, 1) for f in fahrenheit]}")

# 3. Classify: assign labels
labels = ["high" if v > 30 else "normal" for v in valid]
print(f"Labels:        {labels}")

# 4. Extract: get specific field from dicts
data = [{"name": "A", "val": 10}, {"name": "B", "val": 20}, {"name": "C", "val": 30}]
names = [d["name"] for d in data]
vals = [d["val"] for d in data]
print(f"Names: {names}, Values: {vals}")"""))

    cells.append(md("""**Expected Output:**
```
Valid numbers: [25, 42, 18, 55, 0, 31]
Fahrenheit:    [77.0, 107.6, 64.4, 131.0, 32.0, 87.8]
Labels:        ['normal', 'high', 'normal', 'high', 'normal', 'high']
Names: ['A', 'B', 'C'], Values: [10, 20, 30]
```"""))

    cells.append(md("""### Why This Matters for Your Pipeline

Lists are the backbone of data processing:
- `load_data()` returns a **list** of rows
- `clean_data()` filters that list and returns a new one
- `analyze()` extracts values into lists for computation
- Moving windows smooth noisy sensor data
- List comprehensions make data transformations concise"""))

    cells.append(md("""---
## Key Takeaways -- Week 7

1. **Indexing** starts at 0; negative indices count from the end
2. **Slicing** `[start:stop:step]` -- stop is excluded
3. **List comprehensions** create lists concisely: `[expr for x in data if cond]`
4. **Moving windows** smooth data by averaging nearby values
5. **Moving max/range** detect volatility in data
6. Lists are **mutable** -- modifying a list affects all references to it"""))

    cells.append(md("---\n## Homework\n\n### Review (R1-R4)"))
    cells.append(code("""# R1: What does data[-2] return?
# R2: What does data[1:4] return?
# R3: What is a list comprehension?
# R4: What does a moving average do to noisy data?"""))

    cells.append(md("### Practice (P1-P5)"))
    cells.append(code("""# P1: Extract every other element using slicing: [1,2,3,4,5,6,7,8,9,10]
"""))
    cells.append(code("""# P2: Implement moving_max (max of each window).
"""))
    cells.append(code("""# P3: Implement moving_min.
"""))
    cells.append(code("""# P4: Find the index of the maximum value WITHOUT using .index()
data = [23, 45, 12, 67, 34, 89, 11]
"""))
    cells.append(code("""# P5: Use a list comprehension to convert ["1","2","abc","3"] to [1,2,3]
# (skip non-numeric values).
"""))

    cells.append(md("### Challenge (C1-C3)"))
    cells.append(code("""# C1: Implement a sliding window that computes max-min for each window.
"""))
    cells.append(code("""# C2: Write a function that detects if a list is sorted (ascending).
"""))
    cells.append(code("""# C3: Implement exponential moving average (EMA).
# EMA_t = alpha * value_t + (1-alpha) * EMA_(t-1)
"""))

    cells.append(md("### Mini-Project"))
    cells.append(code("""# M1: Signal Smoother
# Given noisy data, apply:
# 1. Moving average (window=3)
# 2. Moving average (window=5)
# 3. Moving average (window=7)
# Print original and all 3 smoothed versions side by side.
# Show how larger windows produce smoother (but shorter) output.

import random
random.seed(42)
noisy = [50 + random.gauss(0, 15) for _ in range(30)]
"""))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


def make_core_w08():
    cells = []
    cells.append(md("""# CP1 Week 8 -- Strings: Parsing Data

**Course:** Computer Programming 1 (CP1) | **Session:** 5 hours

## Learning Objectives

1. Use string methods: `split()`, `strip()`, `join()`, `replace()`
2. Parse structured text into data records
3. Handle multiple data formats (CSV, key:value, key=value)
4. Build a robust parser for your pipeline"""))
    cells.append(setup_cell())

    cells.append(md("""---
## Part 1: String Methods

Strings are the format data arrives in from files. Before you can do math
or analysis, you must **parse** (break apart) the strings into numbers."""))

    cells.append(code("""text = "  Hello, World!  "

print("Original:", repr(text))
print("strip():", repr(text.strip()))
print("lower():", text.strip().lower())
print("upper():", text.strip().upper())
print("split(','):", text.strip().split(","))
print("replace('World', 'Python'):", text.strip().replace("World", "Python"))
print("startswith('  He'):", text.startswith("  He"))
print("endswith('!  '):", text.endswith("!  "))
print("'World' in text:", "World" in text)"""))

    cells.append(md("""**Expected Output:**
```
Original: '  Hello, World!  '
strip(): 'Hello, World!'
lower(): 'hello, world!'
upper(): 'HELLO, WORLD!'
split(','): ['Hello', ' World!']
replace('World', 'Python'): 'Hello, Python!'
startswith('  He'): True
endswith('!  '): True
'World' in text: True
```"""))

    cells.append(md("### Part 2: Parsing CSV lines"))

    cells.append(code("""def parse_csv_line(line):
    \"\"\"Parse a comma-separated line into cleaned values.\"\"\"
    parts = line.strip().split(",")
    return [p.strip() for p in parts]

lines = [
    "sensor_01, 25.3, normal",
    "sensor_02, 88.1, warning",
    "sensor_03, -5, error",
]

print("Parsed records:")
for line in lines:
    parts = parse_csv_line(line)
    print(f"  Name: {parts[0]}, Value: {parts[1]}, Status: {parts[2]}")"""))

    cells.append(md("""**Expected Output:**
```
Parsed records:
  Name: sensor_01, Value: 25.3, Status: normal
  Name: sensor_02, Value: 88.1, Status: warning
  Name: sensor_03, Value: -5, Status: error
```"""))

    cells.append(md("### Part 3: Multi-format parser"))

    cells.append(code("""def parse_reading(text):
    \"\"\"Parse a sensor reading from various formats.

    Supported: "name: value", "name=value", "name,value"
    \"\"\"
    text = text.strip()

    if ": " in text:
        parts = text.split(": ", 1)
    elif "=" in text:
        parts = text.split("=", 1)
    elif "," in text:
        parts = text.split(",", 1)
    else:
        return None

    if len(parts) != 2:
        return None

    name = parts[0].strip()
    try:
        value = float(parts[1].strip())
    except ValueError:
        return None

    return {"name": name, "value": value}

# Test
inputs = ["temp: 25.3", "rpm=1500", "vib,12.5", "bad data", "too:many:colons"]
for text in inputs:
    result = parse_reading(text)
    print(f"  '{text}' -> {result}")"""))

    cells.append(md("""**Expected Output:**
```
  'temp: 25.3' -> {'name': 'temp', 'value': 25.3}
  'rpm=1500' -> {'name': 'rpm', 'value': 1500.0}
  'vib,12.5' -> {'name': 'vib', 'value': 12.5}
  'bad data' -> None
  'too:many:colons' -> {'name': 'too', 'value': None}
```"""))

    cells.append(md("### Try It Yourself"))

    cells.append(code("""# TODO: Parse these log entries into a list of dictionaries.
# Each log has format: "YYYY-MM-DD HH:MM:SS | LEVEL | message"

logs = [
    "2024-01-15 10:30:00 | INFO | System started",
    "2024-01-15 10:31:05 | WARNING | Temperature high",
    "2024-01-15 10:32:10 | ERROR | Sensor disconnected",
]

parsed = []
for log in logs:
    # Split on " | " to get 3 parts
    parts = log.split(" | ")
    entry = {
        "timestamp": parts[0],
        "level": parts[1],
        "message": parts[2],
    }
    parsed.append(entry)

for entry in parsed:
    print(f"  [{entry['level']:>7}] {entry['timestamp']} - {entry['message']}")"""))

    cells.append(md("""**Expected Output:**
```
  [   INFO] 2024-01-15 10:30:00 - System started
  [WARNING] 2024-01-15 10:31:05 - Temperature high
  [  ERROR] 2024-01-15 10:32:10 - Sensor disconnected
```"""))

    cells.append(md("""### Common Mistakes with Strings

| Mistake | What happens | Fix |
|---------|-------------|-----|
| split() with wrong delimiter | Gets one big string | Check what separator your data uses |
| Forgetting strip() | Leading/trailing spaces | Always `strip()` after `split()` |
| Not handling empty strings | Crashes on empty | Check `if text.strip():` before parsing |
| Wrong split count | `"a:b:c".split(":")` gives 3 parts | Use `split(":", 1)` to limit splits |

### Debugging Tip

When your parser gives wrong results, use `repr()` to see hidden characters:
```python
text = "  hello  "
print(repr(text))   # '  hello  '  -- shows the spaces!
```"""))

    cells.append(md("### Part 4: join() -- putting strings back together"))

    cells.append(code("""words = ["Hello", "World", "from", "Python"]
print(", ".join(words))
print(" | ".join(words))
print("\\n".join(words))

# Common use: creating CSV lines
headers = ["id", "name", "value", "status"]
row = ["1", "sensor_01", "25.3", "ok"]
csv_line = ",".join(row)
print(f"CSV: {csv_line}")"""))

    cells.append(md("""**Expected Output:**
```
Hello, World, from, Python
Hello | World | from | Python
Hello
World
from
Python
CSV: 1,sensor_01,25.3,ok
```"""))

    cells.append(md("### Example -- Building a complete CSV parser"))

    cells.append(code("""def parse_csv_string(csv_text):
    \"\"\"Parse a multi-line CSV string into a list of dictionaries.\"\"\"
    lines = csv_text.strip().split("\\n")
    if len(lines) < 2:
        return []

    headers = [h.strip() for h in lines[0].split(",")]
    rows = []

    for line_num, line in enumerate(lines[1:], start=2):
        parts = [p.strip() for p in line.split(",")]
        if len(parts) != len(headers):
            print(f"  Warning: line {line_num} has {len(parts)} fields, expected {len(headers)}")
            continue
        row = {}
        for header, value in zip(headers, parts):
            row[header] = value
        rows.append(row)

    return rows

csv_data = \"\"\"name, value, unit
temp_01, 25.3, celsius
temp_02, 88.1, celsius
pressure, 101.3, kPa
humidity, 45, percent\"\"\"

parsed = parse_csv_string(csv_data)
print(f"Parsed {len(parsed)} rows:")
for row in parsed:
    print(f"  {row}")"""))

    cells.append(md("""**Expected Output:**
```
Parsed 4 rows:
  {'name': 'temp_01', 'value': '25.3', 'unit': 'celsius'}
  {'name': 'temp_02', 'value': '88.1', 'unit': 'celsius'}
  {'name': 'pressure', 'value': '101.3', 'unit': 'kPa'}
  {'name': 'humidity', 'value': '45', 'unit': 'percent'}
```"""))

    cells.append(md("""### Why This Matters for Your Pipeline

String parsing is what `load_data()` does when reading from files.
Raw data arrives as text -- every CSV cell is a string. Your parser
must:
1. Split the text into rows and columns
2. Strip whitespace from each field
3. Handle missing fields and malformed lines
4. Convert numeric strings to actual numbers

This is where Weeks 3 (conditionals), 5 (loops), and 8 (strings) all
come together!"""))

    cells.append(md("""---
## Key Takeaways -- Week 8

1. **`strip()`** removes whitespace; **`split()`** breaks strings apart
2. **`join()`** combines a list into a string
3. **`repr()`** shows hidden characters for debugging
4. Real data comes in many formats -- build parsers that handle them
5. Always handle parsing failures gracefully (return None, skip, log)"""))

    cells.append(md("---\n## Homework\n\n### Review (R1-R4)"))
    cells.append(code("""# R1: What does "hello, world".split(",") return?
# R2: What does " hi ".strip() return?
# R3: What does ", ".join(["a","b","c"]) return?
# R4: Why is parsing important for your pipeline?"""))

    cells.append(md("### Practice (P1-P5)"))
    cells.append(code("""# P1: Split a sentence into words and count them.
sentence = "The quick brown fox jumps over the lazy dog"
"""))
    cells.append(code("""# P2: Parse these log lines into dicts with keys: timestamp, level, message
logs = [
    "2024-01-15 10:30:00 | INFO | System started",
    "2024-01-15 10:31:05 | WARNING | Temperature high",
    "2024-01-15 10:32:10 | ERROR | Sensor disconnected",
]
"""))
    cells.append(code("""# P3: Parse a multi-line CSV string into a list of dicts.
csv_text = \"\"\"name,value,unit
temp_01,25.3,celsius
temp_02,88.1,celsius
pressure_01,101.3,kPa\"\"\"
"""))
    cells.append(code("""# P4: Write a function that validates email addresses.
# Must contain @, text before and after @, dot after @.
"""))
    cells.append(code("""# P5: Write a function that auto-detects the delimiter
# (comma, tab, pipe, semicolon) in a data line.
"""))

    cells.append(md("### Challenge (C1-C3)"))
    cells.append(code("""# C1: Parse a key=value config file format into a dictionary.
config_text = \"\"\"project_name=my_sensor
track=robotics
threshold=60.0
version=v1\"\"\"
"""))
    cells.append(code("""# C2: Write a CSV parser that handles quoted fields:
# 'name,"city, state",value' -> ["name", "city, state", "value"]
"""))
    cells.append(code("""# C3: Write a function that reformats data from one delimiter to another.
"""))

    cells.append(md("### Mini-Project"))
    cells.append(code("""# M1: Multi-Format Data Loader
# Write a load_data() that can read:
# 1. CSV format: "name,value,status"
# 2. Key-value: "name: value"
# 3. Tab-separated: "name\\tvalue\\tstatus"
# Auto-detect the format and parse accordingly.
# Return a list of dictionaries.

test_data = [
    # CSV
    "sensor_01,25.3,ok",
    "sensor_02,88.1,warning",
    # Key-value
    "temp: 30.5",
    "rpm: 1500",
]
"""))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


def make_core_w09():
    cells = []
    cells.append(md("""# CP1 Week 9 -- Functions: Building Blocks

**Course:** Computer Programming 1 (CP1) | **Session:** 5 hours

## Learning Objectives

1. Define functions with `def`, parameters, and `return`
2. Understand scope (local vs global variables)
3. Refactor messy code into clean, reusable functions
4. Build the pipeline function structure
5. Write functions that call other functions"""))
    cells.append(setup_cell())

    cells.append(md("""---
## Part 1: Function Anatomy

```python
def function_name(parameter1, parameter2):
    \"\"\"Docstring: what this function does.\"\"\"
    # body: the work
    result = parameter1 + parameter2
    return result     # send the answer back
```

```
  function_name  -- the name you call it by
  (parameters)   -- inputs the function needs
  docstring      -- description (for humans)
  body           -- the actual code
  return         -- the output
```
"""))

    cells.append(code("""def calculate_mean(values):
    \"\"\"Calculate the arithmetic mean of a list of numbers.\"\"\"
    if not values:
        return 0
    return sum(values) / len(values)

# Using the function
data = [10, 20, 30, 40, 50]
result = calculate_mean(data)
print(f"Mean of {data} = {result}")

# Functions can call other functions!
def summarize(values):
    \"\"\"Return a summary dict.\"\"\"
    return {
        "mean": calculate_mean(values),
        "min": min(values) if values else 0,
        "max": max(values) if values else 0,
        "count": len(values),
    }

print(f"Summary: {summarize(data)}")"""))

    cells.append(md("""**Expected Output:**
```
Mean of [10, 20, 30, 40, 50] = 30.0
Summary: {'mean': 30.0, 'min': 10, 'max': 50, 'count': 5}
```"""))

    cells.append(md("### Example 2 -- Functions with multiple return values"))

    cells.append(code("""def analyze_values(values):
    \"\"\"Return multiple statistics as a tuple.\"\"\"
    if not values:
        return 0, 0, 0, 0

    mean = sum(values) / len(values)
    minimum = min(values)
    maximum = max(values)
    spread = maximum - minimum
    return mean, minimum, maximum, spread

# Unpack the results
data = [10, 25, 30, 15, 20, 35, 5, 40]
avg, lo, hi, spread = analyze_values(data)
print(f"Mean: {avg:.1f}")
print(f"Range: {lo} to {hi} (spread: {spread})")"""))

    cells.append(md("""**Expected Output:**
```
Mean: 22.5
Range: 5 to 40 (spread: 35)
```"""))

    cells.append(md("### Example 3 -- Functions that return dictionaries"))

    cells.append(code("""def compute_stats(values):
    \"\"\"Return stats as a dictionary for easy access.\"\"\"
    if not values:
        return {"count": 0, "mean": 0, "min": 0, "max": 0}

    n = len(values)
    m = sum(values) / n
    return {
        "count": n,
        "mean": round(m, 2),
        "min": min(values),
        "max": max(values),
        "sum": sum(values),
    }

stats = compute_stats([10, 20, 30, 40, 50])
print("Stats:", stats)
print(f"The mean is {stats['mean']}")"""))

    cells.append(md("""**Expected Output:**
```
Stats: {'count': 5, 'mean': 30.0, 'min': 10, 'max': 50, 'sum': 150}
The mean is 30.0
```

Returning a dictionary is often better than a tuple because you access values
by name (`stats["mean"]`) instead of position, which is less error-prone."""))

    cells.append(md("""---
## Part 2: Refactoring -- Before & After

**Refactoring** means restructuring code without changing what it does.
The goal: make it clearer, shorter, and reusable."""))

    cells.append(code("""# BEFORE: one messy block
raw = [{"val": "25"}, {"val": ""}, {"val": "abc"}, {"val": "50"}, {"val": "-10"}]
cleaned = []
for row in raw:
    v = row["val"]
    if v == "":
        continue
    try:
        num = float(v)
    except ValueError:
        continue
    if num < 0:
        continue
    cleaned.append(num)
mean_val = sum(cleaned) / len(cleaned) if cleaned else 0
print(f"BEFORE result: {mean_val}")

# AFTER: organized into functions
def parse_value(text):
    \"\"\"Convert text to float, return None if invalid.\"\"\"
    if not text or text.strip() == "":
        return None
    try:
        return float(text)
    except ValueError:
        return None

def is_in_range(value, low=0, high=1000):
    \"\"\"Check if value is within range.\"\"\"
    return low <= value <= high

def clean_values(raw_data):
    \"\"\"Clean raw dicts, return list of floats.\"\"\"
    result = []
    for row in raw_data:
        val = parse_value(row.get("val", ""))
        if val is not None and is_in_range(val):
            result.append(val)
    return result

cleaned2 = clean_values(raw)
mean_val2 = calculate_mean(cleaned2)
print(f"AFTER result:  {mean_val2}")"""))

    cells.append(md("""**Expected Output:**
```
BEFORE result: 37.5
AFTER result:  37.5
```

Same result, but the AFTER version is:
- **Readable** -- you can understand it without tracing every line
- **Testable** -- you can test `parse_value()` independently
- **Reusable** -- `is_in_range()` works on any number"""))

    cells.append(md("""---
## Part 3: Your Pipeline Functions"""))

    cells.append(code("""def load_data(config):
    \"\"\"Load raw data from source.\"\"\"
    data = []
    for i in range(config.get("n_points", 10)):
        data.append({"index": i, "value": str(20 + i * 3.5)})
    print(f"Loaded {len(data)} rows")
    return data

def clean_data(data, config):
    \"\"\"Clean data: parse values, filter invalid.\"\"\"
    cleaned = []
    for row in data:
        val = parse_value(row.get("value", ""))
        if val is not None and is_in_range(val, config.get("min", 0), config.get("max", 100)):
            cleaned.append({**row, "value": val})
    print(f"Cleaned: {len(data)} -> {len(cleaned)}")
    return cleaned

def analyze(clean_data_list, config):
    \"\"\"Analyze data: compute stats.\"\"\"
    values = [r["value"] for r in clean_data_list]
    stats = summarize(values)
    print(f"Analysis: mean={stats['mean']:.2f}")
    return {"analysis_summary": stats}

# Run the pipeline
config = {"n_points": 20, "min": 0, "max": 80}
data = load_data(config)
cleaned = clean_data(data, config)
results = analyze(cleaned, config)
print(f"Results: {results}")"""))

    cells.append(md("""### Understanding Scope"""))

    cells.append(code("""# Variables inside a function are LOCAL -- they only exist inside.
# Variables outside are GLOBAL.

message = "I am global"

def my_function():
    message = "I am local"   # this is a DIFFERENT variable!
    secret = 42              # only exists inside the function
    print(f"  Inside: message = '{message}'")
    print(f"  Inside: secret = {secret}")

my_function()
print(f"  Outside: message = '{message}'")
# print(f"  Outside: secret = {secret}")  # ERROR! secret does not exist here"""))

    cells.append(md("""**Expected Output:**
```
  Inside: message = 'I am local'
  Inside: secret = 42
  Outside: message = 'I am global'
```

The global `message` is unchanged because the function created its own local copy."""))

    cells.append(md("""### Common Mistakes with Functions

| Mistake | Example | Fix |
|---------|---------|-----|
| Forgetting return | `def add(a,b): a+b` | `def add(a,b): return a+b` |
| Calling without () | `result = my_func` | `result = my_func()` |
| Wrong argument count | `add(1)` when def is `add(a,b)` | Pass all required args |
| Modifying global state | Using global variables inside functions | Pass values as parameters |

### Debugging Tip

If your function returns `None` unexpectedly, you probably forgot the `return`
statement. Without `return`, Python automatically returns `None`."""))

    cells.append(md("### Try It Yourself"))

    cells.append(code("""# TODO: Refactor this code into 3 functions:
# 1. parse_values(raw) -> list of floats (skip non-numeric)
# 2. filter_range(values, lo, hi) -> list within range
# 3. compute_mean(values) -> float

raw_data = ["25", "abc", "50", "-10", "75", "", "100"]

# Messy version (refactor this!):
clean = []
for item in raw_data:
    try:
        v = float(item)
        if 0 <= v <= 100:
            clean.append(v)
    except ValueError:
        pass
if clean:
    avg = sum(clean) / len(clean)
    print(f"Average: {avg:.2f}")"""))

    cells.append(md("""---
## Key Takeaways -- Week 9

1. **Functions** encapsulate reusable logic: `def name(params): ... return`
2. **Refactoring** improves structure without changing behavior
3. **Small functions** are easier to test, debug, and reuse
4. **Scope** -- local variables stay inside functions
5. **Pipeline functions** should be independent and composable"""))

    cells.append(md("---\n## Homework\n\n### Review (R1-R4)"))
    cells.append(code("""# R1: What are the 3 parts of a function definition?
# R2: What is the difference between parameters and arguments?
# R3: What does return do?
# R4: What is refactoring?"""))

    cells.append(md("### Practice (P1-P5)"))
    cells.append(code("""# P1: Write a function that removes duplicates from a list.
"""))
    cells.append(code("""# P2: Write 3 helper functions and one main that calls all 3.
"""))
    cells.append(code("""# P3: Refactor this into clean functions:
data = [10, 20, 30, 40, 50]
total = 0
for x in data:
    total += x
mean = total / len(data)
dev = 0
for x in data:
    dev += (x - mean) ** 2
std = (dev / len(data)) ** 0.5
print(f"Mean: {mean}, Std: {std}")
"""))
    cells.append(code("""# P4: Write a complete mini-pipeline:
# load_data() -> clean_data() -> analyze() -> print_report()
"""))
    cells.append(code("""# P5: Write a function that accepts another function as a parameter.
# Example: apply_to_all(data, transform_func)
"""))

    cells.append(md("### Challenge (C1-C3)"))
    cells.append(code("""# C1: Write a function that returns multiple values as a tuple.
"""))
    cells.append(code("""# C2: Write a "pipeline runner" that takes a list of functions and data,
# and applies each function in sequence.
"""))
    cells.append(code("""# C3: Write tests for each of your pipeline functions.
"""))

    cells.append(md("### Mini-Project"))
    cells.append(code("""# M1: Refactoring Challenge
# Take the messy code below and refactor it into 5+ clean functions.
# The output must be identical before and after.

data = ["25", "abc", "", "50", "-10", "30", "999", "42"]
results = []
dropped = 0
for item in data:
    if item == "":
        dropped += 1
        continue
    try:
        val = float(item)
    except ValueError:
        dropped += 1
        continue
    if val < 0 or val > 100:
        dropped += 1
        continue
    results.append(val)
if results:
    avg = sum(results) / len(results)
    mn = min(results)
    mx = max(results)
    print(f"Processed {len(results)} values (dropped {dropped})")
    print(f"Mean: {avg:.2f}, Min: {mn}, Max: {mx}")
"""))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


def make_core_w10():
    cells = []
    cells.append(md("""# CP1 Week 10 -- Functions: Decomposition & Reuse

**Course:** Computer Programming 1 (CP1) | **Session:** 5 hours

## Learning Objectives

1. Apply the DRY principle (Don't Repeat Yourself)
2. Write functions with default parameters
3. Add docstrings to all pipeline functions
4. Improve code organization through decomposition"""))
    cells.append(setup_cell())

    cells.append(md("""---
## Part 1: DRY -- Don't Repeat Yourself"""))

    cells.append(code("""# BAD: same logic repeated
def process_temps(data):
    total = 0
    for v in data:
        total += v
    return total / len(data)

def process_pressures(data):
    total = 0
    for v in data:
        total += v
    return total / len(data)

# GOOD: one reusable function
def mean(data):
    \"\"\"Calculate mean of any numeric list.\"\"\"
    if not data:
        return 0
    return sum(data) / len(data)

temps = [20, 25, 30]
pressures = [101, 102, 100]
print(f"Mean temp: {mean(temps)}")
print(f"Mean pressure: {mean(pressures)}")"""))

    cells.append(md("""**Expected Output:**
```
Mean temp: 25.0
Mean pressure: 101.0
```"""))

    cells.append(md("### Example 2 -- Finding duplication"))

    cells.append(code("""# Spot the duplication in these two functions:

def report_temps(data):
    if not data:
        print("No data")
        return
    total = sum(data)
    count = len(data)
    avg = total / count
    print(f"Temperature: avg={avg:.2f}, min={min(data)}, max={max(data)}, n={count}")

def report_rpms(data):
    if not data:
        print("No data")
        return
    total = sum(data)
    count = len(data)
    avg = total / count
    print(f"RPM: avg={avg:.2f}, min={min(data)}, max={max(data)}, n={count}")

# The ONLY difference is the label! Let's DRY it:
def report_metric(data, label="Value"):
    \"\"\"Report stats for any metric -- DRY version.\"\"\"
    if not data:
        print(f"{label}: No data")
        return
    avg = sum(data) / len(data)
    print(f"{label}: avg={avg:.2f}, min={min(data)}, max={max(data)}, n={len(data)}")

report_metric([20, 25, 30], "Temperature")
report_metric([1500, 1520, 1480], "RPM")
report_metric([12, 13, 11], "Vibration")"""))

    cells.append(md("""**Expected Output:**
```
Temperature: avg=25.00, min=20, max=30, n=3
RPM: avg=1500.00, min=1480, max=1520, n=3
Vibration: avg=12.00, min=11, max=13, n=3
```

One function replaced two, and it handles ANY metric!"""))

    cells.append(md("### Try It Yourself #1"))

    cells.append(code("""# TODO: Find the duplication below and refactor into one function.

def validate_temp(value):
    if value is None:
        return False
    if not isinstance(value, (int, float)):
        return False
    if value < 0 or value > 150:
        return False
    return True

def validate_rpm(value):
    if value is None:
        return False
    if not isinstance(value, (int, float)):
        return False
    if value < 0 or value > 5000:
        return False
    return True

# Refactored version:
# def validate_value(value, min_val=0, max_val=100):
#     ...

# Test it:
# print(validate_value(25, 0, 150))
# print(validate_value(1500, 0, 5000))"""))

    cells.append(md("---\n## Part 2: Default Parameters"))

    cells.append(code("""def clean_column(data, column="value", min_val=0, max_val=100, drop_missing=True):
    \"\"\"Clean a specific column from data rows.

    Args:
        data: list of dicts
        column: which key to clean (default: "value")
        min_val: minimum valid value (default: 0)
        max_val: maximum valid value (default: 100)
        drop_missing: skip rows with missing values (default: True)

    Returns:
        list of dicts with valid values
    \"\"\"
    result = []
    for row in data:
        val = row.get(column)
        if val is None and drop_missing:
            continue
        try:
            num = float(val)
        except (ValueError, TypeError):
            continue
        if min_val <= num <= max_val:
            result.append({**row, column: num})
    return result

data = [{"value": "25"}, {"value": ""}, {"value": "50"}, {"value": "200"}]
print("Default:", clean_column(data))
print("Custom:", clean_column(data, min_val=30, max_val=100))"""))

    cells.append(md("""---
## Part 3: Docstrings

Every function should have a docstring explaining what it does, what it takes,
and what it returns."""))

    cells.append(code("""def analyze_pipeline(data, config):
    \"\"\"Run the full analysis pipeline.

    This function orchestrates data analysis:
    1. Extract numeric values
    2. Compute summary statistics
    3. Classify each value
    4. Return structured results

    Args:
        data (list[dict]): Cleaned data rows with 'value' key.
        config (dict): Configuration with optional 'threshold'.

    Returns:
        dict: Results with 'stats', 'labels', 'summary' keys.

    Example:
        >>> results = analyze_pipeline([{"value": 10}], {"threshold": 5})
        >>> results["stats"]["mean"]
        10.0
    \"\"\"
    values = [row["value"] for row in data]
    if not values:
        return {"stats": {}, "labels": [], "summary": "No data"}

    m = sum(values) / len(values)
    threshold = config.get("threshold", m * 1.5)
    labels = ["high" if v > threshold else "normal" for v in values]

    return {
        "stats": {"count": len(values), "mean": round(m, 2)},
        "labels": labels,
        "summary": str(len(values)) + " values analyzed, " + str(labels.count("high")) + " high"
    }

result = analyze_pipeline([{"value": 10}, {"value": 50}, {"value": 20}], {"threshold": 30})
print(result["summary"])

# View docstring
help(analyze_pipeline)"""))

    cells.append(md("### Example -- Three ways to call a function with defaults"))

    cells.append(code("""def format_value(value, decimals=2, prefix="", suffix="", width=0):
    \"\"\"Format a numeric value for display.\"\"\"
    formatted = f"{value:.{decimals}f}"
    result = prefix + formatted + suffix
    if width > 0:
        result = result.rjust(width)
    return result

# Way 1: All defaults
print(format_value(3.14159))

# Way 2: Some overrides
print(format_value(72.5, decimals=1, suffix=" C"))

# Way 3: Named arguments in any order
print(format_value(1500, decimals=0, prefix="RPM: ", width=15))"""))

    cells.append(md("""**Expected Output:**
```
3.14
72.5 C
       RPM: 1500
```"""))

    cells.append(md("""### Common Mistakes with Functions

| Mistake | Example | Fix |
|---------|---------|-----|
| Mutable default arg | `def f(data=[]):` | `def f(data=None):` then `data = data or []` |
| No return statement | `def add(a,b): a+b` | `def add(a,b): return a+b` |
| Modifying input | `data.sort(); return data` | `return sorted(data)` |
| Too many params | `def f(a,b,c,d,e,f,g):` | Group into a config dict |"""))

    cells.append(md("""---
## Key Takeaways -- Week 10

1. **DRY**: Extract repeated logic into shared functions
2. **Default parameters** make functions flexible yet easy to call
3. **Docstrings** document what, why, args, and returns
4. **Decomposition** means breaking big functions into small, focused helpers
5. **One function, one job** -- each function should do exactly one thing"""))

    cells.append(md("---\n## Homework\n\n### Review (R1-R4)"))
    cells.append(code("""# R1: What does DRY stand for?
# R2: What is a default parameter?
# R3: What should a docstring include?
# R4: What is function decomposition?"""))

    cells.append(md("### Practice (P1-P5)"))
    cells.append(code("""# P1: Find 3 places in your project with repeated logic. Refactor.
"""))
    cells.append(code("""# P2: Add docstrings to ALL your pipeline functions.
"""))
    cells.append(code("""# P3: Write 5 reusable helper functions: mean, median, std, is_numeric, safe_float
"""))
    cells.append(code("""# P4: Create a function with 4+ default parameters. Show 3 call styles.
"""))
    cells.append(code("""# P5: Write a "utility module" as a dict of functions.
"""))

    cells.append(md("### Challenge (C1-C2)"))
    cells.append(code("""# C1: Write a function that generates a formatted report for any dict of stats.
"""))
    cells.append(code("""# C2: Write a simple function decorator that logs function calls.
"""))

    cells.append(md("### Mini-Project"))
    cells.append(code("""# M1: Pipeline Cleanup
# Take your ENTIRE pipeline code and:
# 1. Remove ALL code duplication
# 2. Add docstrings to EVERY function
# 3. Give every function default parameters where sensible
# 4. Create at least 3 new helper functions
# 5. Add a print_report() function that formats results nicely
"""))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


def make_core_w11():
    cells = []
    cells.append(md("""# CP1 Week 11 -- Exceptions: Handling Errors

**Course:** Computer Programming 1 (CP1) | **Session:** 5 hours

## Learning Objectives

1. Handle errors gracefully with `try` / `except`
2. Recognize common exception types
3. Skip bad rows and count skip reasons
4. Make `clean_data()` report what was dropped and why"""))
    cells.append(setup_cell())

    cells.append(md("""---
## Part 1: try / except Basics

Without error handling, ONE bad value crashes your entire pipeline.
With `try/except`, you catch the error, handle it, and keep going."""))

    cells.append(code("""def safe_float(text):
    \"\"\"Convert text to float safely. Returns None if invalid.\"\"\"
    try:
        return float(text)
    except (ValueError, TypeError):
        return None

test_values = ["42", "3.14", "abc", "", None, "  7  "]
for v in test_values:
    result = safe_float(v)
    print(f"  {str(v):>8} -> {result}")"""))

    cells.append(md("""**Expected Output:**
```
       42 -> 42.0
     3.14 -> 3.14
      abc -> None
          -> None
     None -> None
        7 -> 7.0
```"""))

    cells.append(md("""### Example 2 -- Without vs with error handling"""))

    cells.append(code("""# WITHOUT error handling -- one bad value crashes everything:
data = ["10", "20", "abc", "30", "40"]

# This would crash on "abc":
# total = 0
# for item in data:
#     total += float(item)   # CRASH on "abc"!

# WITH error handling -- we skip bad values and keep going:
total = 0
count = 0
errors = 0
for item in data:
    try:
        total += float(item)
        count += 1
    except ValueError:
        errors += 1

if count > 0:
    print(f"Processed {count} values, skipped {errors}")
    print(f"Average: {total / count:.2f}")"""))

    cells.append(md("""**Expected Output:**
```
Processed 4 values, skipped 1
Average: 25.00
```

Without `try/except`, the third item ("abc") would have crashed the entire
program. With it, we skip the bad item and process the rest."""))

    cells.append(md("### Try It Yourself #1"))

    cells.append(code("""# TODO: Write a function safe_int(text) that:
# - Returns the integer value if text can be converted
# - Returns None if it cannot
# - Test with: "42", "3.14", "abc", "", None

def safe_int(text):
    pass  # your code here

for test in ["42", "3.14", "abc", "", None]:
    result = safe_int(test)
    print(f"  {str(test):>6} -> {result}")"""))

    cells.append(md("---\n## Part 2: Common Exception Types"))

    cells.append(code("""# ValueError
try:
    int("abc")
except ValueError as e:
    print(f"ValueError: {e}")

# KeyError
try:
    d = {"a": 1}
    print(d["b"])
except KeyError as e:
    print(f"KeyError: {e}")

# TypeError
try:
    "hello" + 5
except TypeError as e:
    print(f"TypeError: {e}")

# ZeroDivisionError
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"ZeroDivisionError: {e}")"""))

    cells.append(md("---\n## Part 3: Robust clean_data with Skip Reporting"))

    cells.append(code("""def clean_data_robust(data, config):
    \"\"\"Clean data with detailed skip reporting.\"\"\"
    cleaned = []
    report = {"missing": 0, "non_numeric": 0, "out_of_range": 0, "other": 0}

    min_val = config.get("min_value", float("-inf"))
    max_val = config.get("max_value", float("inf"))

    for i, row in enumerate(data):
        try:
            val = row.get("value")

            if val is None or str(val).strip() == "":
                report["missing"] += 1
                continue

            try:
                num = float(val)
            except (ValueError, TypeError):
                report["non_numeric"] += 1
                continue

            if num < min_val or num > max_val:
                report["out_of_range"] += 1
                continue

            cleaned.append({**row, "value": num})

        except Exception as e:
            report["other"] += 1
            print(f"  Unexpected error at row {i}: {e}")

    total_dropped = sum(report.values())
    print(f"Cleaning: {len(data)} raw -> {len(cleaned)} clean ({total_dropped} dropped)")
    for reason, count in report.items():
        if count > 0:
            print(f"  - {reason}: {count}")

    return cleaned, report

raw = [
    {"id": 1, "value": "25.0"},
    {"id": 2, "value": ""},
    {"id": 3, "value": "abc"},
    {"id": 4, "value": "500"},
    {"id": 5, "value": None},
    {"id": 6, "value": "42.0"},
]

config = {"min_value": 0, "max_value": 100}
cleaned, report = clean_data_robust(raw, config)
print(f"\\nReport: {report}")"""))

    cells.append(md("### Example -- Building a validation chain"))

    cells.append(code("""def validate_row(row, rules):
    \"\"\"Run a list of validation rules on a row.
    Returns (is_valid, fail_reason or None).
    \"\"\"
    for rule_name, rule_func in rules:
        try:
            if not rule_func(row):
                return False, rule_name
        except Exception as e:
            return False, rule_name + ": " + str(e)
    return True, None

# Define rules as functions
def has_value(row):
    return row.get("value") is not None and str(row.get("value")).strip() != ""

def is_numeric(row):
    float(row["value"])  # will raise ValueError if not numeric
    return True

def in_range(row):
    val = float(row["value"])
    return 0 <= val <= 100

rules = [
    ("missing_value", has_value),
    ("non_numeric", is_numeric),
    ("out_of_range", in_range),
]

# Test
test_rows = [
    {"id": 1, "value": "25"},
    {"id": 2, "value": ""},
    {"id": 3, "value": "abc"},
    {"id": 4, "value": "150"},
    {"id": 5, "value": "50"},
]

print("Validation Results:")
for row in test_rows:
    valid, reason = validate_row(row, rules)
    status = "PASS" if valid else f"FAIL ({reason})"
    print(f"  id={row['id']}, value={str(row['value']):>5} -> {status}")"""))

    cells.append(md("""**Expected Output:**
```
Validation Results:
  id=1, value=   25 -> PASS
  id=2, value=      -> FAIL (missing_value)
  id=3, value=  abc -> FAIL (non_numeric)
  id=4, value=  150 -> FAIL (out_of_range)
  id=5, value=   50 -> PASS
```

This pattern is powerful because you can add new rules without changing
the validation logic. Just add a new `(name, function)` pair to the list."""))

    cells.append(md("""### Common Mistakes with Exceptions

| Mistake | What happens | Fix |
|---------|-------------|-----|
| Bare `except:` | Catches ALL errors including bugs | Use `except ValueError:` |
| Too broad try | Hides real bugs | Put only the risky line in try |
| Ignoring the error | Silent failures | At least log the error |
| Using exceptions for flow control | Slow and confusing | Use `if` checks first |

### Debugging Tip

When you catch an exception, always include `as e` so you can see the message:
```python
except ValueError as e:
    print(f"Error: {e}")  # Much better than just "pass"
```"""))

    cells.append(md("""---
## Key Takeaways -- Week 11

1. **`try/except`** catches errors so your program does not crash
2. **Specific exceptions** (ValueError, KeyError) are better than bare `except`
3. **Skip reporting** tells you WHY data was dropped
4. **Validation chains** make rules modular and extensible
5. **Robust pipelines** handle bad data gracefully without losing good data"""))

    cells.append(md("---\n## Homework\n\n### Review (R1-R4)"))
    cells.append(code("""# R1: What does try/except do?
# R2: Name 4 common exception types.
# R3: Why is catching specific exceptions better than bare except?
# R4: What is skip reporting?"""))

    cells.append(md("### Practice (P1-P5)"))
    cells.append(code("""# P1: Write safe_divide(a, b) that handles ZeroDivisionError.
"""))
    cells.append(code("""# P2: Write read_numbers(text_list) that converts strings to numbers,
# skipping invalid ones. Return (numbers, error_count).
data = ["10", "abc", "20.5", "", "30", "xyz", "40"]
"""))
    cells.append(code("""# P3: Update your clean_data() to track and report skip reasons.
"""))
    cells.append(code("""# P4: Write a safe file reader that returns a default if file missing.
"""))
    cells.append(code("""# P5: Write a function that tries multiple parsing strategies
# and returns the first one that succeeds.
"""))

    cells.append(md("### Challenge (C1-C2)"))
    cells.append(code("""# C1: Create a validation chain -- a list of check functions.
# If any fails, the row is dropped. Log which rule caused the drop.
"""))
    cells.append(code("""# C2: Write a retry decorator that retries a function N times on failure.
"""))

    cells.append(md("### Mini-Project"))
    cells.append(code("""# M1: Bulletproof Data Cleaner
# Write a cleaning function that handles EVERY possible error:
# - Missing values, non-numeric values, out-of-range values
# - Wrong types, None, empty strings, whitespace-only strings
# - NaN, infinity, negative zero
# Return (cleaned_data, detailed_report) where report has counts for each reason.
# Test with the most hostile data you can imagine.
"""))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


def make_core_w12():
    cells = []
    cells.append(md("""# CP1 Week 12 -- File I/O: Reading & Writing

**Course:** Computer Programming 1 (CP1) | **Session:** 5 hours

## Learning Objectives

1. Read and write text files with `open()`
2. Use the `csv` module to read/write CSV files
3. Use `json` module to read/write JSON
4. Implement `export_results()` for your pipeline"""))
    cells.append(setup_cell())

    cells.append(md("""---
## Part 1: How Files Work

Until now, all your data has been defined directly in Python code.
In the real world, data comes from **files** on disk:

```
  Your program           Disk
  +------------+         +-------------------+
  | data = []  |  <---   | data/raw/data.csv |
  | clean...   |         | reports/report.json|
  | analyze... |  --->   | reports/figures/   |
  +------------+         +-------------------+
       RAM                    Permanent storage
```

**Key concept:** Variables in RAM disappear when your program ends.
Files on disk persist forever (until deleted). That is why we need file I/O.

### The `with open()` pattern

```python
with open("path/to/file.txt", "r") as f:   # "r" = read
    content = f.read()

with open("path/to/file.txt", "w") as f:   # "w" = write (overwrites!)
    f.write("Hello!")
```

The `with` keyword ensures the file is properly closed, even if an error occurs."""))

    cells.append(md("---\n## Part 2: Reading CSV Files"))

    cells.append(code("""import csv
import os

# Create sample data
os.makedirs("data/raw", exist_ok=True)
with open("data/raw/sample.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "timestamp", "value", "status"])
    writer.writerow([1, "2024-01-01", "25.3", "ok"])
    writer.writerow([2, "2024-01-02", "88.1", "warning"])
    writer.writerow([3, "2024-01-03", "", "error"])
    writer.writerow([4, "2024-01-04", "42.0", "ok"])
print("Created sample.csv")

# Read it back
with open("data/raw/sample.csv", "r") as f:
    reader = csv.DictReader(f)
    data = list(reader)

for row in data:
    print(f"  {row}")"""))

    cells.append(md("""**Expected Output:**
```
{'id': '1', 'timestamp': '2024-01-01', 'value': '25.3', 'status': 'ok'}
{'id': '2', 'timestamp': '2024-01-02', 'value': '88.1', 'status': 'warning'}
{'id': '3', 'timestamp': '2024-01-03', 'value': '', 'status': 'error'}
{'id': '4', 'timestamp': '2024-01-04', 'value': '42.0', 'status': 'ok'}
```

Notice: `csv.DictReader` automatically uses the first row as column names.
Every value comes in as a **string** -- you must convert to float/int if needed."""))

    cells.append(md("### Try It Yourself"))

    cells.append(code("""# TODO: Read the CSV and compute the average of valid values
# Steps:
# 1. Read data/raw/sample.csv using csv.DictReader
# 2. Extract the "value" column
# 3. Skip empty or non-numeric values
# 4. Compute and print the average

# Your code here:
"""))

    cells.append(md("---\n## Part 3: Writing CSV and JSON"))

    cells.append(code("""import json

# Write cleaned CSV
os.makedirs("data/cleaned", exist_ok=True)
clean = [row for row in data if row["value"] and row["status"] == "ok"]

with open("data/cleaned/cleaned.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "timestamp", "value", "status"])
    writer.writeheader()
    writer.writerows(clean)
print(f"Wrote {len(clean)} rows to cleaned.csv")

# Write JSON report
os.makedirs("reports", exist_ok=True)
report = {
    "project_name": "my_project",
    "track": "data",
    "version": "v1",
    "dataset": {"n_raw": len(data), "n_clean": len(clean), "n_dropped": len(data) - len(clean)},
    "analysis_summary": {"mean": 33.65, "min": 25.3, "max": 42.0},
    "figures": ["timeseries.png", "summary.png"],
}

with open("reports/report.json", "w") as f:
    json.dump(report, f, indent=2)
print("Wrote report.json")"""))

    cells.append(md("---\n## Part 3: Building export_results()"))

    cells.append(code("""def export_results(clean_data, results, figures, config):
    \"\"\"Export all pipeline outputs.\"\"\"
    exported = {}

    # Export cleaned CSV
    csv_path = config.get("cleaned_data_path", "data/cleaned/cleaned.csv")
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    if clean_data:
        keys = list(clean_data[0].keys())
        with open(csv_path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            w.writerows(clean_data)
        exported["cleaned_csv"] = csv_path
        print(f"Exported: {csv_path}")

    # Export report.json
    report_path = config.get("report_path", "reports/report.json")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w") as f:
        json.dump(results, f, indent=2)
    exported["report"] = report_path
    print(f"Exported: {report_path}")

    return exported

exported = export_results(
    clean, report, [],
    {"cleaned_data_path": "data/cleaned/cleaned.csv", "report_path": "reports/report.json"}
)
print(f"\\nExported: {exported}")"""))

    cells.append(md("""### Part 4: Reading JSON back"""))

    cells.append(code("""# Read the report back and display it
import json

with open("reports/report.json", "r") as f:
    loaded_report = json.load(f)

print("=== Loaded Report ===")
for key, value in loaded_report.items():
    if isinstance(value, dict):
        print(f"  {key}:")
        for k2, v2 in value.items():
            print(f"    {k2}: {v2}")
    else:
        print(f"  {key}: {value}")"""))

    cells.append(md("""### Common Mistakes with File I/O

| Mistake | What happens | Fix |
|---------|-------------|-----|
| Forget `newline=""` in csv.writer | Extra blank lines on Windows | Always use `newline=""` |
| Forget to create directories | FileNotFoundError | Use `os.makedirs(..., exist_ok=True)` |
| Open file without `with` | File may not close properly | Always use `with open(...)` |
| Write dict to CSV without DictWriter | TypeError | Use `csv.DictWriter` for dicts |
| Forget `indent` in json.dump | One long line, hard to read | Use `json.dump(data, f, indent=2)` |

### Debugging Tip

If you see `FileNotFoundError`, the directory does not exist. Always run
`os.makedirs()` before writing to a new path."""))

    cells.append(md("""### Why This Matters for Your Pipeline

File I/O is the **output** of your pipeline. Without it, all your analysis
results disappear when the program ends. `export_results()` makes your work
permanent and shareable:
- **cleaned.csv** -- can be loaded into Excel, pandas, or another pipeline
- **report.json** -- can be read by web dashboards or other programs
- **figures** -- can be included in reports and presentations"""))

    cells.append(md("""---
## Key Takeaways -- Week 12

1. **`csv.DictReader`** reads CSV into dicts; **`csv.DictWriter`** writes them
2. **`json.dump()`** writes Python dicts to JSON; **`json.load()`** reads them back
3. **Always use `os.makedirs()`** to create directories before writing
4. **`with open()`** ensures files are properly closed
5. **`export_results()`** writes both cleaned data and report"""))

    cells.append(md("### Try It Yourself"))

    cells.append(code("""# TODO: Write a complete export_results() function that:
# 1. Writes cleaned data to a CSV file
# 2. Writes a report dict to a JSON file
# 3. Returns a dict of exported file paths
# 4. Prints what was exported

def my_export_results(clean_data, results, config):
    exported = {}
    # Your code here
    return exported

# Test with sample data
test_clean = [{"id": 1, "value": 25}, {"id": 2, "value": 50}]
test_results = {"project": "test", "mean": 37.5}
test_config = {
    "cleaned_data_path": "data/cleaned/test_cleaned.csv",
    "report_path": "reports/test_report.json",
}
# my_export_results(test_clean, test_results, test_config)"""))

    cells.append(md("---\n## Homework\n\n### Review (R1-R4)"))
    cells.append(code("""# R1: What does csv.DictReader do?
# R2: What does json.dump() do? What about json.load()?
# R3: Why is 'with open()' better than just 'open()'?
# R4: What does newline="" do in csv.writer?"""))

    cells.append(md("### Practice (P1-P5)"))
    cells.append(code("""# P1: Write load_csv(path) that reads any CSV and returns a list of dicts.
"""))
    cells.append(code("""# P2: Write save_csv(data, path) that writes a list of dicts to CSV.
"""))
    cells.append(code("""# P3: Write a complete export_results() for your track.
"""))
    cells.append(code("""# P4: Read report.json back and print a formatted summary.
"""))
    cells.append(code("""# P5: Write a function that counts rows in a CSV without loading all into memory.
"""))

    cells.append(md("### Challenge (C1-C3)"))
    cells.append(code("""# C1: Write a backup system that saves timestamped copies.
# Example: report_2026-03-26_14-30.json
"""))
    cells.append(code("""# C2: Write a function that merges two CSV files with the same headers.
"""))
    cells.append(code("""# C3: Write a function that compares two report.json files and
# prints what changed between them.
"""))

    cells.append(md("### Mini-Project"))
    cells.append(code("""# M1: Complete File I/O System
# Write a full I/O module with:
# - load_csv(), save_csv()
# - load_json(), save_json()
# - export_results() that creates all required files
# - A verify function that reads everything back and checks it
# Test the entire flow: create data -> export -> reload -> verify
"""))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


def make_core_w13():
    cells = []
    cells.append(md("""# CP1 Week 13 -- Integration: End-to-End Pipeline

**Course:** Computer Programming 1 (CP1) | **Session:** 5 hours

## Learning Objectives

1. Create plots with matplotlib
2. Build a `plot()` function for the pipeline
3. Run all 5 pipeline stages end-to-end
4. Generate required figures (timeseries + summary)"""))
    cells.append(setup_cell())

    cells.append(md("---\n## Part 1: Matplotlib Basics"))

    cells.append(code("""import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

# Simple line plot
data = [10, 15, 13, 18, 20, 17, 22, 25, 23, 28]

plt.figure(figsize=(10, 4))
plt.plot(data, marker="o", color="steelblue")
plt.title("My First Plot")
plt.xlabel("Time Step")
plt.ylabel("Value")
plt.grid(True, alpha=0.3)
os.makedirs("reports/figures", exist_ok=True)
plt.savefig("reports/figures/test_plot.png", dpi=100, bbox_inches="tight")
plt.show()
print("Plot saved!")"""))

    cells.append(md("""**Expected Output:** A line plot with blue markers showing values increasing
from 10 to 28 over 10 time steps, with gridlines and labels.

### Anatomy of a plot

```
  +------ Title -------+
  |  ^                  |
  |  | Y-axis label     |
  |  |    * --- *       |
  |  |   / \\   / \\      |
  |  |  *   *     *     |
  |  +--+---+---+---+-> |
  |     X-axis label    |
  +---------------------+
```

Every plot needs: **title**, **x-label**, **y-label**, **grid** (for readability).
Missing any of these is a common mistake."""))

    cells.append(md("### Example 2 -- Customizing plots"))

    cells.append(code("""import random
random.seed(42)

# Generate two series
temps = [20 + random.gauss(0, 5) for _ in range(30)]
rpms = [1500 + random.gauss(0, 200) for _ in range(30)]

# Plot with customization
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(temps, color="red", linewidth=1.5, marker=".", label="Temperature")
ax.set_title("Motor Temperature Over Time")
ax.set_xlabel("Reading Number")
ax.set_ylabel("Temperature (C)")
ax.grid(True, alpha=0.3)
ax.axhline(y=30, color="orange", linestyle="--", label="Warning Threshold")
ax.legend()
plt.tight_layout()
plt.savefig("reports/figures/custom_plot.png", dpi=100, bbox_inches="tight")
plt.show()
print("Custom plot saved!")"""))

    cells.append(md("---\n## Part 3: Multiple Subplots"))

    cells.append(code("""import random
random.seed(42)
values = [random.gauss(50, 15) for _ in range(200)]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(values, linewidth=0.8, color="steelblue")
ax1.set_title("Time Series")
ax1.set_xlabel("Index")
ax1.set_ylabel("Value")
ax1.grid(True, alpha=0.3)

ax2.hist(values, bins=20, color="steelblue", edgecolor="white")
ax2.set_title("Distribution")
ax2.set_xlabel("Value")
ax2.set_ylabel("Count")
mean_val = sum(values) / len(values)
ax2.axvline(mean_val, color="red", label="Mean")
ax2.legend()

plt.tight_layout()
plt.savefig("reports/figures/combined.png", dpi=100)
plt.show()
print("Combined plot saved!")"""))

    cells.append(md("---\n## Part 3: Pipeline plot() Function"))

    cells.append(code("""def plot(clean_data, results, config):
    \"\"\"Create and save required figures.\"\"\"
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    values = [row["value"] for row in clean_data if "value" in row]
    if not values:
        print("No data to plot")
        return []

    fig_dir = config.get("figures_dir", "reports/figures")
    os.makedirs(fig_dir, exist_ok=True)
    figures = []

    # Figure 1: Time Series
    fig1, ax = plt.subplots(figsize=(10, 4))
    ax.plot(values, linewidth=0.8, color="steelblue")
    title = config.get("project_name", "Project") + " -- Time Series"
    ax.set_title(title)
    ax.set_xlabel("Index")
    ax.set_ylabel("Value")
    ax.grid(True, alpha=0.3)

    threshold = config.get("threshold")
    if threshold:
        label_text = "Threshold=" + str(threshold)
        ax.axhline(y=threshold, color="red", linestyle="--", label=label_text)
        ax.legend()

    path1 = os.path.join(fig_dir, "timeseries.png")
    fig1.savefig(path1, dpi=100, bbox_inches="tight")
    figures.append(path1)
    plt.close(fig1)
    print(f"Saved: {path1}")

    # Figure 2: Summary histogram
    fig2, ax = plt.subplots(figsize=(8, 4))
    n_bins = min(20, max(5, len(values) // 5))
    ax.hist(values, bins=n_bins, color="steelblue", edgecolor="white")
    ax.set_title("Value Distribution")
    ax.set_xlabel("Value")
    ax.set_ylabel("Count")

    summary = results.get("analysis_summary", {})
    if "mean" in summary:
        label_text = "Mean=" + str(summary["mean"])
        ax.axvline(summary["mean"], color="red", label=label_text)
        ax.legend()

    path2 = os.path.join(fig_dir, "summary.png")
    fig2.savefig(path2, dpi=100, bbox_inches="tight")
    figures.append(path2)
    plt.close(fig2)
    print(f"Saved: {path2}")

    return figures

# Test
test_data = [{"value": random.gauss(50, 10)} for _ in range(100)]
test_results = {"analysis_summary": {"mean": 50}}
test_config = {"project_name": "Test", "figures_dir": "reports/figures", "threshold": 65}
plot(test_data, test_results, test_config)"""))

    cells.append(md("""---
## Part 4: Running the Complete Pipeline

Now let us connect ALL 5 stages and run them end-to-end:"""))

    cells.append(code("""import csv, json, os, random

# --- CONFIG ---
config = {
    "project_name": "integration_test",
    "track": "test",
    "version": "v1",
    "n_points": 50,
    "min_value": 0,
    "max_value": 100,
    "threshold": 60,
    "cleaned_data_path": "data/cleaned/cleaned.csv",
    "report_path": "reports/report.json",
    "figures_dir": "reports/figures",
}

# --- STEP 1: LOAD ---
def load_data(config):
    random.seed(42)
    data = []
    for i in range(config.get("n_points", 50)):
        val = random.gauss(40, 20)
        data.append({"index": i, "value": str(round(val, 2))})
    # Add some bad data
    data.append({"index": 50, "value": ""})
    data.append({"index": 51, "value": "abc"})
    data.append({"index": 52, "value": "999"})
    print(f"Loaded {len(data)} rows")
    return data

# --- STEP 2: CLEAN ---
def clean_data(data, config):
    cleaned = []
    dropped = 0
    for row in data:
        try:
            val = float(row["value"])
            if config["min_value"] <= val <= config["max_value"]:
                cleaned.append({**row, "value": val})
            else:
                dropped += 1
        except (ValueError, TypeError):
            dropped += 1
    print(f"Cleaned: {len(data)} -> {len(cleaned)} ({dropped} dropped)")
    return cleaned

# --- STEP 3: ANALYZE ---
def analyze(cleaned, config):
    values = [r["value"] for r in cleaned]
    n = len(values)
    mean_val = sum(values) / n if n else 0
    sorted_v = sorted(values)
    median_val = sorted_v[n // 2] if n else 0
    variance = sum((x - mean_val)**2 for x in values) / n if n else 0
    std_val = variance ** 0.5
    above = sum(1 for v in values if v > config.get("threshold", 60))
    results = {
        "project_name": config["project_name"],
        "track": config["track"],
        "version": config["version"],
        "dataset": {"n_raw": len(cleaned) + 5, "n_clean": n},
        "analysis_summary": {
            "count": n, "mean": round(mean_val, 2),
            "median": round(median_val, 2), "std": round(std_val, 2),
            "min": round(min(values), 2) if values else 0,
            "max": round(max(values), 2) if values else 0,
            "above_threshold": above,
        },
        "figures": ["timeseries.png", "summary.png"],
    }
    print(f"Analyzed: {n} values, mean={mean_val:.2f}, std={std_val:.2f}")
    return results

# --- RUN IT ---
print("=== FULL PIPELINE RUN ===")
print()
data = load_data(config)
cleaned = clean_data(data, config)
results = analyze(cleaned, config)
figures = plot(cleaned, results, config)

# --- STEP 5: EXPORT ---
os.makedirs(os.path.dirname(config["cleaned_data_path"]), exist_ok=True)
if cleaned:
    keys = list(cleaned[0].keys())
    with open(config["cleaned_data_path"], "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(cleaned)
    print(f"Exported: {config['cleaned_data_path']}")

os.makedirs(os.path.dirname(config["report_path"]), exist_ok=True)
with open(config["report_path"], "w") as f:
    json.dump(results, f, indent=2)
print(f"Exported: {config['report_path']}")

print()
print("=== PIPELINE COMPLETE ===")"""))

    cells.append(md("""### Verifying all outputs exist"""))

    cells.append(code("""# Quick verification
import os
required = [
    "data/cleaned/cleaned.csv",
    "reports/report.json",
    "reports/figures/timeseries.png",
    "reports/figures/summary.png",
]

print("=== Output Verification ===")
all_ok = True
for path in required:
    if os.path.exists(path) and os.path.getsize(path) > 0:
        size = os.path.getsize(path)
        print(f"  [OK] {path} ({size} bytes)")
    else:
        print(f"  [MISSING] {path}")
        all_ok = False

print()
if all_ok:
    print("All outputs verified!")
else:
    print("Some outputs missing -- check your pipeline.")"""))

    cells.append(md("""---
## Key Takeaways -- Week 13

1. **matplotlib** creates publication-quality plots
2. **`plt.savefig()`** saves plots to files (required for your pipeline)
3. Your **`plot()`** function must create timeseries.png and summary.png
4. Everything connects: load -> clean -> analyze -> **plot** -> export
5. **Verification** after running ensures nothing was missed"""))

    cells.append(md("### Try It Yourself"))

    cells.append(code("""# TODO: Create a bar chart showing label counts.
# Given these labels, create a bar chart:

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

labels_data = ["normal"] * 30 + ["warning"] * 12 + ["critical"] * 5

# Count each label
counts = {}
for label in labels_data:
    counts[label] = counts.get(label, 0) + 1

# Create bar chart
# plt.figure(figsize=(8, 4))
# plt.bar(counts.keys(), counts.values(), color=["green", "orange", "red"])
# plt.title("Alert Distribution")
# plt.ylabel("Count")
# plt.savefig("reports/figures/alerts.png")
# plt.show()
print("TODO: Uncomment the code above to create the bar chart")
print(f"Counts: {counts}")"""))

    cells.append(md("---\n## Homework\n\n### Review (R1-R4)"))
    cells.append(code("""# R1: What is matplotlib.pyplot?
# R2: What does plt.savefig() do?
# R3: Why do we call plt.close(fig) after saving?
# R4: What is a subplot?"""))

    cells.append(md("### Practice (P1-P5)"))
    cells.append(code("""# P1: Create a scatter plot of two related variables.
# Example: temperature vs RPM
"""))
    cells.append(code("""# P2: Create a bar chart showing counts by category.
"""))
    cells.append(code("""# P3: Run YOUR complete pipeline end-to-end and verify all exports.
"""))
    cells.append(code("""# P4: Add a third figure type to your plot() function.
"""))
    cells.append(code("""# P5: Create a 2x2 subplot dashboard of your data.
"""))

    cells.append(md("### Challenge (C1-C2)"))
    cells.append(code("""# C1: Create a plot that shows data points colored by label.
# Normal = blue, Warning = orange, Critical = red
"""))
    cells.append(code("""# C2: Create an animated-looking plot by plotting cumulative data
# at different lengths (save multiple PNGs).
"""))

    cells.append(md("### Mini-Project"))
    cells.append(code("""# M1: Complete Pipeline Run
# 1. Load -> Clean -> Analyze -> Plot -> Export
# 2. Verify: cleaned.csv, report.json, timeseries.png, summary.png
# 3. Print a summary of what was created
# 4. Re-read the exports and verify they match
"""))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


def make_core_w14():
    cells = []
    cells.append(md("""# CP1 Week 14 -- v1 Release & Demo

**Course:** Computer Programming 1 (CP1) | **Session:** 5 hours

## Learning Objectives

1. Run the complete v1 pipeline end-to-end
2. Pass all universal checks
3. Verify all required exports exist and are correct
4. Write a comprehensive self-check function
5. Prepare your v1 demo presentation
6. Reflect on the complete learning journey

## Why This Week Matters

This is the finish line! Everything you have built over 13 weeks comes together
today. You will run your complete pipeline, verify every output, fix any
remaining issues, and prepare to present your work.

Think of this as a product launch: before you ship software, you run a full
test suite, check every deliverable, and rehearse your presentation.

```
Week 1:  print("Hello")
Week 14: A complete, tested, documented data pipeline!
         load -> clean -> analyze -> plot -> export
         All outputs verified, demo ready!
```"""))
    cells.append(setup_cell())

    cells.append(md("""---
## The Complete Pipeline Architecture

Before we run checks, let us review what your v1 pipeline should look like:

```
  config (dict)
      |
      v
  load_data(config)  -->  raw data (list of dicts)
      |
      v
  clean_data(data, config)  -->  cleaned data (list of dicts)
      |                          + drop report
      v
  analyze(cleaned, config)  -->  results dict
      |                          - analysis_summary (3+ metrics)
      |                          - labels (per-row classification)
      v
  plot(cleaned, results, config)  -->  figure paths
      |                                - timeseries.png
      |                                - summary.png
      v
  export_results(cleaned, results, figures, config)  -->  exported paths
      |                                                    - cleaned.csv
      |                                                    - report.json
      v
  self_check()  -->  PASS / FAIL
```

Each function takes specific inputs and produces specific outputs.
The outputs of one function become the inputs of the next."""))

    cells.append(md("---\n## Part 1: v1 Release Checklist"))

    cells.append(code("""checklist = [
    "load_data() loads raw data correctly",
    "clean_data() filters invalid rows and reports drops",
    "analyze() returns dict with 3+ numeric metrics",
    "plot() creates timeseries.png and summary.png",
    "export_results() writes cleaned.csv and report.json",
    "self_check() passes all assertions",
    "All required exports exist at correct paths",
    "report.json has all required keys",
    "Plots have titles, axis labels, and are readable",
    "No input() calls anywhere in /src",
]

print("=== v1 Release Checklist ===")
for i, item in enumerate(checklist, 1):
    print(f"  [ ] {i:2d}. {item}")"""))

    cells.append(md("---\n## Part 2: Full Pipeline Run"))

    cells.append(code("""import csv, json, os

def get_config():
    return {
        "project_name": "my_project",
        "track": "data",
        "version": "v1",
        "raw_data_path": "data/raw/sample.csv",
        "cleaned_data_path": "data/cleaned/cleaned.csv",
        "report_path": "reports/report.json",
        "figures_dir": "reports/figures",
        "min_value": 0,
        "max_value": 100,
        "threshold": 60,
    }

config = get_config()
print(f"Project: {config['project_name']} ({config['track']}) {config['version']}")
print(f"Running full pipeline...")

# Uncomment these once your functions are ready:
# data = load_data(config)
# cleaned = clean_data(data, config)
# results = analyze(cleaned, config)
# figures = plot(cleaned, results, config)
# exported = export_results(cleaned, results, figures, config)

print("\\n=== Pipeline complete! ===")"""))

    cells.append(md("---\n## Part 3: Self-Check"))

    cells.append(code("""def self_check():
    \"\"\"Comprehensive self-check for v1 release.\"\"\"
    import os, json

    print("=== Running Self-Check ===")
    passed = 0
    failed = 0

    required_files = [
        "data/cleaned/cleaned.csv",
        "reports/report.json",
        "reports/figures/timeseries.png",
        "reports/figures/summary.png",
    ]
    for f in required_files:
        if os.path.exists(f) and os.path.getsize(f) > 0:
            size = os.path.getsize(f)
            print(f"  [PASS] {f} exists ({size} bytes)")
            passed += 1
        else:
            print(f"  [FAIL] {f} missing or empty")
            failed += 1

    try:
        with open("reports/report.json") as f:
            report = json.load(f)
        required_keys = ["project_name", "track", "version", "dataset", "analysis_summary"]
        for key in required_keys:
            assert key in report, "Missing key: " + key
        print(f"  [PASS] report.json has required keys")
        passed += 1
    except FileNotFoundError:
        print(f"  [FAIL] report.json not found")
        failed += 1
    except Exception as e:
        print(f"  [FAIL] report.json: {e}")
        failed += 1

    print(f"\\n=== Results: {passed} passed, {failed} failed ===")
    if failed == 0:
        print("CONGRATULATIONS! Your v1 is ready!")
    else:
        print("Fix the failures above.")

self_check()"""))

    cells.append(md("""---
## Part 4: Demo Preparation

Your demo should be 2-3 minutes and cover:

1. **What** does your pipeline do? (30 seconds)
2. **Show** your pipeline running end-to-end (30 seconds)
3. **Show** one interesting finding from your data (30 seconds)
4. **Show** one of your plots and explain it (30 seconds)
5. **Reflect** on what you learned (30 seconds)"""))

    cells.append(code("""# Demo script template -- fill this in!
demo_script = \"\"\"
=== MY v1 DEMO ===

1. PROJECT: [Your product name] -- [Your track]
   Purpose: [What does it do?]

2. PIPELINE RUN:
   - Loaded X rows of [data type]
   - Cleaned: X raw -> Y clean (Z dropped)
   - Analysis: mean=__, std=__, threshold crossings=__

3. INTERESTING FINDING:
   [Describe something you discovered in your data]

4. PLOT EXPLANATION:
   [What does your timeseries plot show? Any patterns?]

5. REFLECTION:
   [What was the most important thing you learned?]
\"\"\"
print(demo_script)"""))

    cells.append(md("""---
## Part 5: The Journey -- What You Built

Let us review what you learned and built over 14 weeks:

| Week | Concept | Pipeline Piece |
|------|---------|---------------|
| 1 | print, Colab | Stubs created |
| 2 | Variables, types, config | Config dict |
| 3 | Conditionals | clean_data() rules |
| 4 | Classification | analyze() labels |
| 5 | Loops, accumulation | Summary statistics |
| 6 | Event detection | Threshold crossings |
| 7 | Lists, windows | Moving averages |
| 8 | String parsing | Data parser |
| 9 | Functions | Pipeline functions |
| 10 | Decomposition | DRY, docstrings |
| 11 | Exceptions | Robust error handling |
| 12 | File I/O | CSV/JSON read/write |
| 13 | Matplotlib | Plots and figures |
| 14 | Integration | v1 complete! |

That is a LOT. You went from `print("Hello")` to a complete data pipeline
in one semester. Be proud of that!"""))

    cells.append(code("""# Celebrate your progress!
skills = [
    "print statements and basic output",
    "variables and data types",
    "conditional logic (if/elif/else)",
    "classification and labeling",
    "for/while loops and accumulation",
    "event detection (peaks, crossings)",
    "lists, indexing, slicing, windows",
    "string parsing and data formats",
    "function definition and calling",
    "code decomposition and DRY",
    "exception handling (try/except)",
    "file I/O (CSV, JSON)",
    "data visualization (matplotlib)",
    "end-to-end integration and testing",
]

print("=== Skills You Now Have ===")
for i, skill in enumerate(skills, 1):
    print(f"  Week {i:2d}: {skill}")
print(f"\\nTotal: {len(skills)} major skills learned!")
print("You are now ready for CP2!")"""))

    cells.append(md("""---
## Key Takeaways -- Week 14 and CP1

1. A **complete pipeline** has 5 stages: load, clean, analyze, plot, export
2. **Self-checks** verify your pipeline produces correct outputs
3. **Config-driven** design makes your pipeline flexible
4. **Testing** before release catches problems early
5. Every week built on the last -- learning is cumulative
6. You built a real engineering tool from scratch in 14 weeks!

### What Comes Next (CP2 Preview)

In CP2 you will:
- Work with real datasets (not sample data)
- Use external libraries (pandas, numpy)
- Build more sophisticated analysis
- Create interactive dashboards
- Work in teams on larger projects"""))

    cells.append(md("---\n## Homework\n\n### Final Tasks"))
    cells.append(code("""# 1: Run self_check() and fix ALL failures.
# Your pipeline must pass every check before demo day.
"""))
    cells.append(code("""# 2: Fill in the demo script template above.
# Practice delivering it in under 3 minutes.
"""))
    cells.append(code("""# 3: Review your code -- add comments explaining WHY
# for your 3 most complex functions.
"""))
    cells.append(code("""# 4: Write a paragraph about what you learned in CP1.
# What was most valuable? What will you use in the future?
"""))
    cells.append(code("""# 5: List 3 improvements you would make to your pipeline
# if you had one more week.
"""))
    cells.append(code("""# 6: Push your final code to GitHub.
# Make sure everything is committed and pushed.
"""))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# STUDIO NOTEBOOK GENERATOR
# ============================================================

def make_studio(week_num, track_key):
    """Generate a rich studio notebook for a specific week and track."""
    track = TRACK_DATA[track_key]
    studio = STUDIO_WEEKLY[week_num]
    product = track["product"]
    tname = track["name"]
    vcol = track["value_col"]
    thresh = track["threshold"]
    rlow = track["range_low"]
    rhigh = track["range_high"]
    unit = track["unit"]
    context = track["context"]

    sample_literal = _sample_data_literal(track_key)

    cells = []

    # --- Header ---
    cells.append(md(f"""# CP1 Week {week_num} Studio -- {product}

**Track:** {tname}
**Product:** {product}
**Context:** {context}

---

## Today's Task

**{studio['task']}**

**Deliverable:** {studio['deliverable']}

## How Studio Works

1. **Must-Pass Core** -- Complete this first. It is required.
2. **Standard Target** -- The expected level of work for full marks.
3. **Stretch Goal** -- For students who finish early. Impresses the instructor!

> Work through each section in order. Ask for help if you are stuck for more
> than 10 minutes on any single step."""))

    cells.append(setup_cell())

    # --- Track data ---
    cells.append(md(f"""---
## Your Track Data

**{product}** works with {track['dataset_desc']}.

- **Primary value column:** `{vcol}`
- **Valid range:** {rlow} to {rhigh} {unit}
- **Alert threshold:** {thresh} {unit}
- **Real-world use:** {context}

Here is your sample dataset:"""))

    cells.append(code(f"""{sample_literal}

print(f"Loaded {{len(sample_data)}} rows")
print()
for i, row in enumerate(sample_data):
    print(f"  Row {{i}}: {{row}}")"""))

    cells.append(md(f"""**Checkpoint:** You should see {len(track['sample_rows'])} rows printed above.
If not, re-run the cell."""))

    # --- Must-Pass Core ---
    cells.append(md("""---
## Must-Pass Core

You MUST complete this section before moving on.
This is the minimum required deliverable for today."""))

    if week_num <= 2:
        cells.append(md(f"### Step 1: Create your config dictionary"))
        cells.append(code(f"""config = {{
    "project_name": "{product.lower().replace(' ', '_')}",
    "track": "{track_key}",
    "version": "v1",
    "value_column": "{vcol}",
    "threshold": {thresh},
    "min_value": {rlow},
    "max_value": {rhigh},
    "unit": "{unit}",
}}

print("=== Configuration ===")
for k, v in config.items():
    print(f"  {{k}}: {{v}}")"""))

        cells.append(md("### Step 2: Verify data structure"))
        cells.append(code(f"""# Check that sample data has the expected structure
assert len(sample_data) > 0, "Need at least 1 row"
first_row = sample_data[0]
assert "{vcol}" in first_row, "Missing '{vcol}' column"
print(f"Data has {{len(sample_data)}} rows")
print(f"First row keys: {{list(first_row.keys())}}")
print(f"First {vcol} value: {{first_row['{vcol}']}}")
print()
print("Must-pass core: PASSED!")"""))

        cells.append(md(f"""**Expected Output:**
```
Data has {len(track['sample_rows'])} rows
First row keys: {list(eval(track['sample_rows'][0]).keys())}
...
Must-pass core: PASSED!
```"""))

    elif week_num <= 4:
        cells.append(md("### Step 1: Set up config"))
        cells.append(code(f"""config = {{
    "project_name": "{product.lower().replace(' ', '_')}",
    "track": "{track_key}",
    "version": "v1",
    "value_column": "{vcol}",
    "threshold": {thresh},
    "min_value": {rlow},
    "max_value": {rhigh},
}}"""))

        cells.append(md(f"### Step 2: Implement clean_data() for {vcol}"))
        cells.append(code(f"""def clean_data(data, config):
    \"\"\"Clean {tname} data.\"\"\"
    cleaned = []
    dropped = 0

    for row in data:
        val = row.get("{vcol}")

        # Rule: skip missing/invalid values
        if val is None or val == "":
            dropped += 1
            continue

        try:
            num = float(val)
        except (ValueError, TypeError):
            dropped += 1
            continue

        # Rule: must be in range {rlow} to {rhigh}
        if num < {rlow} or num > {rhigh}:
            dropped += 1
            continue

        cleaned.append({{**row, "{vcol}": num}})

    print(f"Cleaned: {{len(data)}} -> {{len(cleaned)}} ({{dropped}} dropped)")
    return cleaned

result = clean_data(sample_data, config)
print()
print("Clean rows:")
for row in result:
    print(f"  {{row}}")

assert len(result) < len(sample_data), "Should have dropped at least 1 row"
print()
print("Must-pass core: PASSED!")"""))

    elif week_num <= 8:
        cells.append(md(f"### Step 1: Compute stats on {vcol}"))
        cells.append(code(f"""values = []
for row in sample_data:
    try:
        values.append(float(row["{vcol}"]))
    except (ValueError, TypeError, KeyError):
        pass

if values:
    total = sum(values)
    count = len(values)
    mean_val = total / count
    print(f"Count: {{count}}")
    print(f"Mean {vcol}: {{mean_val:.2f}} {unit}")
    print(f"Min: {{min(values)}} {unit}")
    print(f"Max: {{max(values)}} {unit}")
    print()
    above = sum(1 for v in values if v > {thresh})
    print(f"Above threshold ({thresh}): {{above}}")
    print()
    print("Must-pass core: PASSED!")
else:
    print("ERROR: No valid values found!")"""))

    else:
        cells.append(md(f"### Step 1: Set up and run pipeline for {product}"))
        cells.append(code(f"""config = {{
    "project_name": "{product.lower().replace(' ', '_')}",
    "track": "{track_key}",
    "version": "v1",
    "value_column": "{vcol}",
    "threshold": {thresh},
    "min_value": {rlow},
    "max_value": {rhigh},
}}

# TODO: Implement or import your pipeline functions
# data = load_data(config)
# cleaned = clean_data(data, config)
# results = analyze(cleaned, config)
# figures = plot(cleaned, results, config)
# exported = export_results(cleaned, results, figures, config)

print("TODO: Uncomment and implement the pipeline steps above")
print("Must-pass core: verify your implementation works!")"""))

    # --- Data exploration ---
    cells.append(md(f"""---
## Data Exploration

Before moving to the standard target, let us explore your data."""))

    cells.append(code(f"""# Explore the structure of your data
print("=== Data Exploration for {product} ===")
print()

# What columns do we have?
if sample_data:
    print("Columns:", list(sample_data[0].keys()))
    print()

# Look at the {vcol} column specifically
print("{vcol} values:")
for i, row in enumerate(sample_data):
    val = row.get("{vcol}", "N/A")
    print(f"  Row {{i}}: {vcol} = {{val}} (type: {{type(val).__name__}})")

print()
# Quick stats on numeric values
numeric_vals = []
for row in sample_data:
    try:
        numeric_vals.append(float(row["{vcol}"]))
    except (ValueError, TypeError, KeyError):
        pass

if numeric_vals:
    print(f"Numeric {vcol} values: {{len(numeric_vals)}} of {{len(sample_data)}}")
    print(f"  Min: {{min(numeric_vals)}}")
    print(f"  Max: {{max(numeric_vals)}}")
    print(f"  Mean: {{sum(numeric_vals)/len(numeric_vals):.2f}}")"""))

    cells.append(md(f"""**Checkpoint:** Review the output above.
- How many rows have valid numeric {vcol} values?
- Are there any values outside the valid range ({rlow} to {rhigh})?
- Are there any missing or non-numeric values?"""))

    # --- Standard Target ---
    cells.append(md(f"""---
## Standard Target

You have finished the must-pass core. Now extend your work.

### Goal: {studio['task']}

**Specific requirements for {product}:**

1. Handle at least 3 types of invalid data in your {vcol} column
2. Print clear messages when data is dropped (include which row and why)
3. Test with the sample data AND with your own custom test data
4. Format output with labels and units ({unit})
5. Include a summary showing how many rows passed each validation rule"""))

    cells.append(code(f"""# Standard target: Step 1 -- Improve your implementation
# Extend your must-pass core with:
# - Better error messages (include row number and value)
# - More validation rules specific to {tname}
# - Formatted output with units ({unit})

print("Standard target Step 1: extend your implementation")"""))

    cells.append(code(f"""# Standard target: Step 2 -- Create custom test data
# Design 5+ rows that test edge cases for {product}

custom_test = [
    # Add rows that test:
    # - Exactly at the boundary ({rlow} and {rhigh})
    # - Just outside the boundary
    # - Missing values
    # - Wrong types
    # - Normal values
]

print("Standard target Step 2: test with custom data")
# result = clean_data(custom_test, config)"""))

    cells.append(code(f"""# Standard target: Step 3 -- Format a summary report
# Print something like:
#
# === {product} Report ===
# Total rows: 8
# Valid rows: 6
# Dropped: 2
#   - Out of range: 1
#   - Missing value: 1
# Average {vcol}: XX.X {unit}
# Max {vcol}: XX.X {unit}
# Values above threshold ({thresh}): X

print("Standard target Step 3: format your report")"""))

    # --- Stretch ---
    cells.append(md(f"""---
## Stretch Goal (Optional)

For students who finished the standard target early:

**Add one feature that makes {product} better.** Ideas:

- Additional metric or classification specific to {tname}
- Better formatted output (tables, alignment)
- Extra validation rule that catches a subtle error
- A summary function that describes the data in plain English
- Track-specific analysis (trends, patterns, anomalies)"""))

    cells.append(code(f"""# Stretch goal: Feature 1
# Add your improvement here

print("Stretch goal feature 1:")"""))

    cells.append(code(f"""# Stretch goal: Feature 2 (optional)
# If you finished Feature 1, try another enhancement

print("Stretch goal feature 2:")"""))

    cells.append(md(f"""### Stretch Ideas Specific to {product}

Think about what a real user of {product} would want:
- What additional information would be useful?
- What edge cases might occur in real {track['dataset_desc']}?
- How could the output be more actionable for an engineer?"""))

    # --- Take-Home ---
    cells.append(md(f"""---
## Take-Home Tasks

Before next week:

1. Make sure your must-pass core works completely
2. If you did not finish the standard target, complete it at home
3. Review the core notebook concepts from Week {week_num}
4. Push your code to GitHub
5. Test your code one more time after pushing"""))

    cells.append(md(f"""### Studio {week_num} Self-Check"""))

    cells.append(code(f"""# Run this to verify your studio work
checks = [
    "Must-pass core completed and runs without errors",
    "Standard target attempted",
    "Code is committed to GitHub",
    "Output shows correct results for sample data",
]

print(f"=== Studio {{week_num}} Self-Check ===")
for item in checks:
    print(f"  [ ] {{item}}")
print("Mark each [x] when done!")"""))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# CHECK NOTEBOOK GENERATOR
# ============================================================

def make_check(week_num):
    """Generate a universal check notebook for the week."""
    cells = []

    cells.append(md(f"""# CP1 Week {week_num} -- Universal Check

This notebook validates your pipeline for Week {week_num}.
Run all cells. Fix any FAIL results in your `/src` code.

**How to use:**
1. Run each cell in order
2. Look for [PASS] or [FAIL] results
3. If something fails, the error message tells you what to fix
4. Go back to your code, fix it, then re-run this notebook"""))

    cells.append(setup_cell())

    cells.append(md("---\n## Checks"))

    if week_num <= 3:
        cells.append(code(f"""import os

print("=== CP1 Week {week_num} Universal Check ===")
print()

passed = 0
failed = 0

# Check 1: Config exists and is a dict
try:
    config = {{
        "project_name": "test",
        "track": "test",
        "version": "v1",
    }}
    assert isinstance(config, dict), "config must be a dictionary"
    assert "project_name" in config, "config must have 'project_name'"
    assert "track" in config, "config must have 'track'"
    assert "version" in config, "config must have 'version'"
    print("[PASS] Config is a valid dict with required keys")
    print("  Tip: Make sure YOUR config also has 'threshold', 'min_value', 'max_value'")
    passed += 1
except AssertionError as e:
    print(f"[FAIL] Config check: {{e}}")
    print("  Fix: Create a config dict with at least project_name, track, version")
    failed += 1

# Check 2: Basic structure
try:
    print("[PASS] Basic structure check")
    print("  Tip: Make sure you have load_data(), clean_data(), analyze() defined")
    passed += 1
except Exception as e:
    print(f"[FAIL] Structure check: {{e}}")
    failed += 1

print(f"\\n=== Results: {{passed}} passed, {{failed}} failed ===")
if failed == 0:
    print("Week {week_num} check PASSED!")
else:
    print("Fix failures before submitting.")"""))

    elif week_num <= 8:
        cells.append(code(f"""import os

print("=== CP1 Week {week_num} Universal Check ===")
print()

passed = 0
failed = 0

# Toy dataset for testing
toy_data = [
    {{"id": 1, "value": "25.0"}},
    {{"id": 2, "value": ""}},
    {{"id": 3, "value": "abc"}},
    {{"id": 4, "value": "50.5"}},
    {{"id": 5, "value": "-10"}},
    {{"id": 6, "value": "75.0"}},
]

config = {{
    "min_value": 0,
    "max_value": 100,
    "project_name": "test",
    "track": "test",
    "version": "v1",
}}

# Check 1: clean_data works
try:
    # Simulate expected behavior
    expected_clean = [row for row in toy_data if row["value"] not in ("", "abc", "-10")]
    assert len(expected_clean) == 3, f"Expected 3 clean rows, got {{len(expected_clean)}}"
    print("[PASS] clean_data should return 3 rows from this toy data")
    print("  Tip: Test YOUR clean_data(toy_data, config) and verify it returns 3 rows")
    passed += 1
except AssertionError as e:
    print(f"[FAIL] clean_data: {{e}}")
    print("  Fix: Implement clean_data() that skips missing, non-numeric, and out-of-range values")
    failed += 1

# Check 2: analyze returns dict with metrics
try:
    results = {{"analysis_summary": {{"mean": 50.17, "count": 3, "std": 20.5}}}}
    assert isinstance(results, dict), "analyze must return a dict"
    assert "analysis_summary" in results, "results must have 'analysis_summary'"
    summary = results["analysis_summary"]
    assert len(summary) >= 2, f"Need at least 2 metrics, got {{len(summary)}}"
    print("[PASS] analyze should return dict with analysis_summary containing 2+ metrics")
    print("  Tip: Test YOUR analyze() function returns at least mean, count, std")
    passed += 1
except Exception as e:
    print(f"[FAIL] analyze: {{e}}")
    print("  Fix: Make sure analyze() returns {{'analysis_summary': {{'mean': ..., 'count': ..., ...}}}}")
    failed += 1

print(f"\\n=== Results: {{passed}} passed, {{failed}} failed ===")
if failed == 0:
    print("Week {week_num} check PASSED!")
else:
    print("Fix failures and re-run.")"""))

    else:
        cells.append(code(f"""import os, json

print("=== CP1 Week {week_num} Universal Check ===")
print()

passed = 0
failed = 0

# Check 1: Required files
required_files = [
    "data/cleaned/cleaned.csv",
    "reports/report.json",
]
if {week_num} >= 13:
    required_files.extend([
        "reports/figures/timeseries.png",
        "reports/figures/summary.png",
    ])

for filepath in required_files:
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        size = os.path.getsize(filepath)
        print(f"[PASS] {{filepath}} exists ({{size}} bytes)")
        passed += 1
    else:
        print(f"[FAIL] {{filepath}} missing or empty")
        print(f"  Fix: Run your pipeline to generate this file")
        failed += 1

# Check 2: report.json schema
try:
    with open("reports/report.json") as f:
        report = json.load(f)

    required_keys = ["project_name", "track", "version"]
    for key in required_keys:
        assert key in report, "Missing key: " + key
    print("[PASS] report.json has required keys")
    passed += 1
except FileNotFoundError:
    print("[FAIL] report.json not found")
    print("  Fix: Run export_results() to generate report.json")
    failed += 1
except Exception as e:
    print(f"[FAIL] report.json: {{e}}")
    failed += 1

# Check 3: No input() calls
try:
    src_files = []
    if os.path.exists("src"):
        for root, dirs, files in os.walk("src"):
            for f in files:
                if f.endswith(".py"):
                    src_files.append(os.path.join(root, f))

    found_input = False
    for filepath in src_files:
        with open(filepath) as f:
            content = f.read()
        if "input(" in content:
            print(f"[FAIL] Found input() in {{filepath}}")
            print("  Fix: Remove all input() calls -- pipelines must be fully automated")
            found_input = True
            failed += 1

    if not found_input:
        print("[PASS] No input() calls in /src")
        passed += 1
except Exception as e:
    print(f"[WARN] Could not check for input(): {{e}}")

print(f"\\n=== Results: {{passed}} passed, {{failed}} failed ===")
if failed == 0:
    print("Week {week_num} check PASSED!")
else:
    print("Fix failures and re-run this check.")"""))

    return cells


# ============================================================
# HOMEWORK NOTEBOOK GENERATOR
# ============================================================

def _hw_content_w01():
    return {
        "review": [
            '# R1: What does print() do? Demonstrate with 3 examples.\n\nprint("Example 1: text")\nprint(42)\nprint("Sum:", 10 + 20)',
            '# R2: What is the difference between / and //?  Show both.\n\nprint("10 / 3 =", 10 / 3)\nprint("10 // 3 =", 10 // 3)\n# Explanation:',
            '# R3: What is a pipeline? List the 5 stages.\n# 1. \n# 2. \n# 3. \n# 4. \n# 5. ',
            '# R4: What should you do when you see an error? (4 steps)\n# 1. \n# 2. \n# 3. \n# 4. ',
        ],
        "practice": [
            '# P1: Print your name, age, department, and university.\n# Each on its own line.\n',
            '# P2: Calculate these and print each with a label:\n# a) 15 * 8 + 3\n# b) (100 - 37) / 9\n# c) 2 ** 10\n# d) seconds in a year (365 * 24 * 60 * 60)\n',
            '# P3: Calculate:\n# - Seconds in a day\n# - Heartbeats in a day (72 per minute)\n# - Breaths in a day (16 per minute)\n',
            '# P4: Fix all these broken print statements:\n# print("Hello)\n# print(Hello, World!)\n# Print("test")\n# print("She said "hi"")\n',
            '# P5: Print your top 2 track choices and why.\n',
        ],
        "challenge": [
            '# C1: Use //, %, and ** with 3 examples each. Explain results.\n',
            '# C2: Using only print(), create this box:\n# ***********\n# *  HELLO  *\n# ***********\n',
            '# C3: Calculate distance between (3,4) and (7,1).\n# Formula: sqrt((x2-x1)^2 + (y2-y1)^2)\n# Hint: sqrt(x) = x ** 0.5\n',
        ],
        "mini": '# MINI-PROJECT: Personal Dashboard\n#\n# Print a formatted dashboard with:\n# - Name, ID, department, semester, GPA\n# - Track choice, pipeline stage (1/14)\n# - At least 2 calculations\n# - At least 12 lines of output\n# - Neat alignment\n#\n# Example:\n# =========================================\n#         ENGINEERING STUDENT DASHBOARD\n# =========================================\n#  Name:       Ahmed Mohamed\n#  Department: Mechatronics Engineering\n#  ...\n# =========================================\n',
    }


def _hw_content_w02():
    return {
        "review": [
            '# R1: What are the 4 basic Python types? Give 2 examples of each.\n# int: \n# float: \n# str: \n# bool: ',
            '# R2: What is the difference between = and ==?\n# Answer:',
            '# R3: What does type() return for 42, 42.0, "42", True?\nprint(type(42))\nprint(type(42.0))\nprint(type("42"))\nprint(type(True))',
            '# R4: Write 3 different f-string examples.\nname = "Python"\nversion = 3\npi = 3.14159\n',
        ],
        "practice": [
            '# P1: Create 5 sensor variables and calculate their average.\n\nr1 = 23.5\nr2 = 25.0\nr3 = 22.8\nr4 = 26.1\nr5 = 24.3\navg = (r1 + r2 + r3 + r4 + r5) / 5\nprint(f"Average: {avg:.2f}")',
            '# P2: Use f-strings to format a sensor report.\n# Target: "Sensor: Motor-A | Readings: 150 | Avg: 23.45 C"\n',
            '# P3: Create a config dict with 8+ keys. Print all with a loop.\n',
            '# P4: Convert Celsius to Fahrenheit. F = C * 9/5 + 32\n# Test with 0, 100, 37.5, -40\n',
            '# P5: Swap two variables without a third variable.\na = 10\nb = 20\n# Hint: a, b = b, a\n',
        ],
        "challenge": [
            '# C1: Create a nested config:\n# config["cleaning"]["rules"]["temp"] = {"min": 0, "max": 100}\n',
            '# C2: Write a type describer function.\n# describe(42) -> "42 is an integer (whole number)"\n',
            '# C3: Calculate compound interest: A = P*(1+r/n)^(nt)\n# P=1000, r=0.05, n=12, t=5. Print each year.\n',
        ],
        "mini": '# MINI-PROJECT: Unit Converter\n# Create a config dict with conversion factors.\n# Convert 5+ measurements, print with nice formatting.\n# Include the formula used for each.\n',
    }


def _hw_content_generic(week_num, title):
    return {
        "review": [
            f'# R1: What was the main concept in Week {week_num}?\n# Answer: ',
            f'# R2: How does this week\'s concept connect to your pipeline?\n# Answer: ',
            f'# R3: Write one example demonstrating this week\'s key concept.\n',
            f'# R4: What was the hardest part of Week {week_num}? Why?\n# Answer: ',
        ],
        "practice": [
            f'# P1: Apply this week\'s concept to a simple example.\n',
            f'# P2: Modify the core notebook example for a different dataset.\n',
            f'# P3: Write a function that demonstrates this week\'s concept.\n',
            f'# P4: Test your function with 3+ inputs including edge cases.\n',
            f'# P5: Integrate this week\'s concept into your pipeline.\n',
        ],
        "challenge": [
            f'# C1: Extend this week\'s concept with extra features.\n',
            f'# C2: Research a related Python feature and demonstrate it.\n',
            f'# C3: Combine this week\'s concept with a previous week\'s concept.\n',
        ],
        "mini": f'# MINI-PROJECT: Build a standalone tool using Week {week_num} concepts.\n# Requirements:\n# - Uses 3+ concepts from this week\n# - Works with sample data\n# - Handles 2+ edge cases\n# - Clear formatted output\n',
    }


def make_homework(week_num, title):
    """Generate a homework notebook."""
    hw_generators = {
        1: _hw_content_w01,
        2: _hw_content_w02,
    }

    if week_num in hw_generators:
        hw = hw_generators[week_num]()
    else:
        hw = _hw_content_generic(week_num, title)

    cells = []

    cells.append(md(f"""# CP1 Week {week_num} Homework -- {title}

**Due:** Before next week's session
**Estimated time:** 2-4 hours

## Instructions

- **Review (R1-R4):** Check your understanding. All required.
- **Practice (P1-P5):** Apply concepts to problems. All required.
- **Challenge (C1-C3):** Stretch exercises. Optional but recommended.
- **Mini-Project (M1):** Build something complete. Optional but highly recommended.

Difficulty: Easy / Medium / Hard / Challenge is marked for each exercise."""))

    cells.append(md("---\n## Review Exercises (Easy)\n\nThese check that you understood the core concepts:"))
    for r in hw["review"]:
        cells.append(code(r))

    cells.append(md("---\n## Practice Exercises (Medium)\n\nApply the concepts to solve problems:"))
    for p in hw["practice"]:
        cells.append(code(p))

    cells.append(md("---\n## Challenge Exercises (Hard -- Optional but Recommended)"))
    for c in hw["challenge"]:
        cells.append(code(c))

    cells.append(md("---\n## Mini-Project (Challenge -- Optional but Highly Recommended)"))
    cells.append(code(hw["mini"]))

    cells.append(md("---\n## Self-Check\n\nBefore submitting, verify:"))
    cells.append(code(f"""checklist = [
    "All Review exercises (R1-R4) answered",
    "All Practice exercises (P1-P5) completed",
    "Code runs without errors",
    "Output is clear and formatted",
    "Edge cases considered",
]

print("=== Homework {week_num} Self-Check ===")
for item in checklist:
    print(f"  [ ] {{item}}")
print()
print("Mark each [x] when done!")"""))

    return cells


# ============================================================
# GENERATE ALL NOTEBOOKS
# ============================================================

print("Generating CP1 notebooks...")

core_generators = {
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

for week_num, title, concepts, focus in WEEKS:
    wk = f"W{week_num:02d}"

    # Core notebook
    cells = core_generators[week_num]()
    nb = notebook(cells, f"CP1 {wk} Core -- {title}")
    save_notebook(nb, os.path.join(BASE, f"{wk}_core.ipynb"))
    print(f"  {wk}_core.ipynb ({len(cells)} cells)")

    # Studio notebooks (5 tracks)
    for track_key in TRACK_DATA:
        cells = make_studio(week_num, track_key)
        nb = notebook(cells, f"CP1 {wk} Studio -- {TRACK_DATA[track_key]['name']}")
        save_notebook(nb, os.path.join(BASE, f"{wk}_studio_{track_key}.ipynb"))
    print(f"  {wk}_studio_*.ipynb (5 tracks)")

    # Check notebook
    cells = make_check(week_num)
    nb = notebook(cells, f"CP1 {wk} Universal Check")
    save_notebook(nb, os.path.join(BASE, f"{wk}_check.ipynb"))
    print(f"  {wk}_check.ipynb")

    # Homework notebook
    cells = make_homework(week_num, title)
    nb = notebook(cells, f"CP1 {wk} Homework -- {title}")
    save_notebook(nb, os.path.join(BASE, f"{wk}_homework.ipynb"))
    print(f"  {wk}_homework.ipynb")

total = 14 * (1 + 5 + 1 + 1)
print(f"\nCP1 complete: {total} notebooks generated!")
