#!/usr/bin/env python3
"""Generate all OOP (Object-Oriented Programming) notebooks -- 14 weeks.

Produces rich, substantial notebooks with:
- 60-100+ cells per core notebook
- Multiple paragraphs of explanation per concept
- 3-4 worked examples per concept progressing in complexity
- Expected Output after every code cell
- Common Mistakes sections with broken code + fix
- Procedural vs OOP comparison sections
- Design Decisions sections
- Try It exercises between sections
- Debugging Tips for OOP-specific errors
- UML-like ASCII class diagrams
- 10+ homework exercises including design exercises
- 30-40+ cell studio notebooks
- 10-15 exercise homework notebooks
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from nb_utils import (
    md, code, notebook, save_notebook, setup_cell,
    reflection_cell, reflection_code,
)

BASE = os.path.join(os.path.dirname(__file__), "notebooks", "oop")
os.makedirs(BASE, exist_ok=True)

TRACKS = {
    "robotics": {
        "name": "Robotics/Mechatronics",
        "product": "MechaSense Studio",
        "domain_object": "Sensor",
        "domain_data": "sensor readings (temperature, RPM, vibration)",
        "example_class": "SensorArray",
        "example_method": "read_sensors",
        "example_attr": "sensor_id",
        "example_value": "temperature in Celsius",
        "example_threshold": 80,
        "example_unit": "degrees C",
    },
    "data": {
        "name": "Data/AI",
        "product": "CleanReport Pipeline",
        "domain_object": "DataRecord",
        "domain_data": "CSV rows (numeric columns, labels, timestamps)",
        "example_class": "DataPipeline",
        "example_method": "transform",
        "example_attr": "column_name",
        "example_value": "numeric measurement",
        "example_threshold": 100,
        "example_unit": "units",
    },
    "simulation": {
        "name": "Simulation/Games",
        "product": "SimLab Engine",
        "domain_object": "Particle",
        "domain_data": "particle positions, velocities, forces",
        "example_class": "Simulation",
        "example_method": "step",
        "example_attr": "particle_id",
        "example_value": "velocity magnitude",
        "example_threshold": 50,
        "example_unit": "m/s",
    },
    "space": {
        "name": "Space/Astro",
        "product": "Lightcurve Explorer",
        "domain_object": "Star",
        "domain_data": "brightness measurements over time (lightcurves)",
        "example_class": "LightcurveAnalyzer",
        "example_method": "detect_transit",
        "example_attr": "star_id",
        "example_value": "brightness in flux",
        "example_threshold": 0.98,
        "example_unit": "relative flux",
    },
    "iot": {
        "name": "IoT/Reporting",
        "product": "AutoDashboard Reporter",
        "domain_object": "Device",
        "domain_data": "device telemetry (uptime, signal strength, battery)",
        "example_class": "Dashboard",
        "example_method": "refresh",
        "example_attr": "device_id",
        "example_value": "signal strength in dBm",
        "example_threshold": -70,
        "example_unit": "dBm",
    },
}

WEEKS = [
    (1, "OOP Kickoff: Classes & Objects",
     "classes, __init__, methods, state vs behavior"),
    (2, "Composition: DataSource & Dataset",
     "composition, has-a relationships, wrapping data in objects"),
    (3, "Cleaner Component",
     "strategy selection, composing cleaners"),
    (4, "Analyzer Component",
     "analysis as an object, stable results schema"),
    (5, "Plotter & Reporter Components",
     "component architecture, unified exports"),
    (6, "Domain Exceptions & Validation",
     "custom exception hierarchy, validation flow"),
    (7, "SOLID Principles: SRP & OCP",
     "Single Responsibility Principle, Open/Closed Principle"),
    (8, "Strategy Pattern",
     "interchangeable algorithms, config-driven selection"),
    (9, "Factory & Registry Pattern",
     "creating objects from config, plugin architecture"),
    (10, "Testing with pytest",
     "test organization, fixtures, parametrize, TDD"),
    (11, "Package Hygiene",
     "module boundaries, __init__.py, clean imports"),
    (12, "Plugin Exercise",
     "add new analyzer WITHOUT touching core code"),
    (13, "Architecture Freeze",
     "API stability, documentation, interface contracts"),
    (14, "v3 Architecture Demo",
     "final tests, architecture review, release"),
]


# ============================================================
# HELPER: expected output markdown cell
# ============================================================
def expected_output(text):
    """Create an 'Expected Output' markdown cell."""
    return md("**Expected Output:**\n```\n" + text + "\n```")


def common_mistake(title, broken, fix, explanation):
    """Create a Common Mistakes section: broken code, explanation, fix."""
    cells = [
        md("---\n### Common Mistake: " + title + "\n\n"
           "The code below has a bug. Can you spot it before reading the fix?"),
        code(broken),
        md("**What goes wrong:** " + explanation),
        md("**The fix:**"),
        code(fix),
    ]
    return cells


def try_it(prompt):
    """A 'Try It' exercise cell pair."""
    return [
        md("---\n### Try It!\n\n" + prompt),
        code("# YOUR CODE HERE\n"),
    ]


def design_decision(title, text):
    """A Design Decisions explanation cell."""
    return md("---\n### Design Decision: " + title + "\n\n" + text)


def debugging_tip(title, text):
    """A Debugging Tip cell."""
    return md("---\n### Debugging Tip: " + title + "\n\n" + text)


def ascii_diagram(title, diagram):
    """An ASCII class/UML diagram."""
    return md("---\n### " + title + "\n\n```\n" + diagram + "\n```")


def procedural_vs_oop(title, procedural_code, oop_code, explanation):
    """Side-by-side procedural vs OOP comparison."""
    cells = [
        md("---\n### Procedural vs OOP: " + title + "\n\n" + explanation),
        md("**Procedural approach (what you did in CP1/CP2):**"),
        code(procedural_code),
        md("**OOP approach (what we are learning now):**"),
        code(oop_code),
    ]
    return cells


# ============================================================
# WEEK 1: Classes & Objects
# ============================================================
def week01_core():
    cells = []

    # --- Title ---
    cells.append(md(
        "# OOP Week 1 -- Classes & Objects\n\n"
        "**Course:** Object-Oriented Programming (Year 2)\n"
        "**Session:** 3 hours\n"
        "**Prerequisites:** CP1 + CP2 complete (v2 pipeline working)\n"
        "**Focus:** classes, `__init__`, attributes, methods, instances, "
        "state vs behavior\n\n"
        "---\n\n"
        "## Learning Objectives\n\n"
        "By the end of this session you will be able to:\n\n"
        "1. Define a class with `__init__`, attributes, and methods\n"
        "2. Create multiple instances (objects) from one class\n"
        "3. Explain the difference between **state** (attributes) and "
        "**behavior** (methods)\n"
        "4. Explain why `self` is needed in every method\n"
        "5. Compare procedural code to OOP code and articulate the benefits"
    ))
    cells.append(setup_cell())

    # --- Section 1: What is OOP? ---
    cells.append(md(
        "---\n## Section 1: What is OOP?\n\n"
        "### The Kitchen Analogy\n\n"
        "Think of your v2 pipeline as a **kitchen with scattered tools** on "
        "the counter. Each function works, but everything is loose -- you "
        "need to remember which tool goes with which recipe, which variable "
        "holds which data, and what order to call things in.\n\n"
        "**OOP** is like organizing the kitchen into **stations**:\n\n"
        "- The **Prep Station** (DataSource) knows how to get ingredients\n"
        "- The **Cleaning Station** (Cleaner) knows how to wash and validate\n"
        "- The **Cooking Station** (Analyzer) knows how to process\n"
        "- The **Plating Station** (Plotter) knows how to present\n"
        "- The **Delivery Station** (Reporter) knows how to export\n\n"
        "Each station **owns its tools and knows its job**. That is OOP!\n\n"
        "### The Car Analogy\n\n"
        "A **class** is a blueprint -- like the engineering drawings for a "
        "Toyota Camry. An **object** is an actual car built from that "
        "blueprint. You can build many cars (objects) from the same blueprint "
        "(class), each with its own color, mileage, and fuel level.\n\n"
        "### The Robot Analogy\n\n"
        "A **class** is the design spec for a robot model. Each physical "
        "robot built from that spec is an **object**. Every robot has its "
        "own battery level, position, and sensor readings -- but they all "
        "share the same capabilities defined in the spec."
    ))

    # --- Section 2: Your First Class ---
    cells.append(md(
        "---\n## Section 2: Your First Class\n\n"
        "A class is created with the `class` keyword. The special method "
        "`__init__` is called automatically whenever you create a new object. "
        "The parameter `self` refers to the specific object being created or "
        "used -- it is how the object talks about itself.\n\n"
        "Let us build a `Sensor` class step by step."
    ))

    # Example 1: Minimal class
    cells.append(md("### Example 1: The Simplest Possible Class"))
    cells.append(code(
        "class Sensor:\n"
        "    \"\"\"A sensor with a name.\"\"\"\n"
        "    pass  # empty class -- valid but useless\n"
        "\n"
        "s = Sensor()\n"
        "print(type(s))\n"
        "print(s)"
    ))
    cells.append(expected_output(
        "<class '__main__.Sensor'>\n"
        "<__main__.Sensor object at 0x...>"
    ))

    # Example 2: Adding __init__
    cells.append(md(
        "### Example 2: Adding `__init__` (the Constructor)\n\n"
        "`__init__` runs automatically when you create an object. It sets up "
        "the object's initial state (its attributes). Think of it as filling "
        "out the 'birth certificate' for the object."
    ))
    cells.append(code(
        "class Sensor:\n"
        "    \"\"\"A sensor with a name and unit.\"\"\"\n"
        "\n"
        "    def __init__(self, name, unit):\n"
        "        self.name = name    # attribute: the sensor's name\n"
        "        self.unit = unit    # attribute: what it measures\n"
        "\n"
        "# Create two sensor objects\n"
        "temp = Sensor(\"Temperature\", \"Celsius\")\n"
        "rpm = Sensor(\"RPM\", \"revolutions/min\")\n"
        "\n"
        "print(temp.name, temp.unit)\n"
        "print(rpm.name, rpm.unit)"
    ))
    cells.append(expected_output(
        "Temperature Celsius\n"
        "RPM revolutions/min"
    ))

    # Example 3: Adding methods
    cells.append(md(
        "### Example 3: Adding Methods (Behavior)\n\n"
        "Methods are functions that belong to a class. They always take "
        "`self` as the first parameter, which gives them access to the "
        "object's attributes."
    ))
    cells.append(code(
        "class Sensor:\n"
        "    \"\"\"A sensor that collects readings.\"\"\"\n"
        "\n"
        "    def __init__(self, name, unit):\n"
        "        self.name = name\n"
        "        self.unit = unit\n"
        "        self.readings = []   # starts empty\n"
        "\n"
        "    def add_reading(self, value):\n"
        "        \"\"\"Add a new reading.\"\"\"\n"
        "        self.readings.append(value)\n"
        "\n"
        "    def get_mean(self):\n"
        "        \"\"\"Return the average reading.\"\"\"\n"
        "        if not self.readings:\n"
        "            return 0.0\n"
        "        return sum(self.readings) / len(self.readings)\n"
        "\n"
        "    def __str__(self):\n"
        "        \"\"\"Human-readable string representation.\"\"\"\n"
        "        count = len(self.readings)\n"
        "        return \"Sensor(\" + self.name + \", \" + str(count) + \" readings)\"\n"
        "\n"
        "\n"
        "# Create and use\n"
        "temp = Sensor(\"Temperature\", \"Celsius\")\n"
        "temp.add_reading(22.5)\n"
        "temp.add_reading(23.1)\n"
        "temp.add_reading(21.8)\n"
        "\n"
        "print(temp)\n"
        "print(\"Mean:\", round(temp.get_mean(), 2), temp.unit)\n"
        "print(\"All readings:\", temp.readings)"
    ))
    cells.append(expected_output(
        "Sensor(Temperature, 3 readings)\n"
        "Mean: 22.47 Celsius\n"
        "All readings: [22.5, 23.1, 21.8]"
    ))

    # Example 4: Multiple objects, separate state
    cells.append(md(
        "### Example 4: Multiple Objects Have Separate State\n\n"
        "This is one of the most important ideas in OOP: each object has "
        "its **own** copy of the attributes. Changing one object does NOT "
        "change another."
    ))
    cells.append(code(
        "temp = Sensor(\"Temperature\", \"C\")\n"
        "rpm = Sensor(\"RPM\", \"rpm\")\n"
        "\n"
        "temp.add_reading(22.5)\n"
        "temp.add_reading(23.0)\n"
        "\n"
        "rpm.add_reading(1500)\n"
        "rpm.add_reading(1520)\n"
        "rpm.add_reading(1510)\n"
        "\n"
        "# Each has its OWN readings\n"
        "print(\"temp readings:\", temp.readings)\n"
        "print(\"rpm  readings:\", rpm.readings)\n"
        "print()\n"
        "print(\"temp mean:\", round(temp.get_mean(), 1))\n"
        "print(\"rpm  mean:\", round(rpm.get_mean(), 1))"
    ))
    cells.append(expected_output(
        "temp readings: [22.5, 23.0]\n"
        "rpm  readings: [1500, 1520, 1510]\n\n"
        "temp mean: 22.8\n"
        "rpm  mean: 1510.0"
    ))

    # --- ASCII diagram ---
    cells.append(ascii_diagram(
        "Class Diagram: Sensor",
        "+---------------------------+\n"
        "|         Sensor            |\n"
        "+---------------------------+\n"
        "| - name: str               |\n"
        "| - unit: str               |\n"
        "| - readings: list[float]   |\n"
        "+---------------------------+\n"
        "| + __init__(name, unit)    |\n"
        "| + add_reading(value)      |\n"
        "| + get_mean() -> float     |\n"
        "| + __str__() -> str        |\n"
        "+---------------------------+\n"
        "\n"
        "  temp : Sensor          rpm : Sensor\n"
        "  name = 'Temperature'   name = 'RPM'\n"
        "  unit = 'C'             unit = 'rpm'\n"
        "  readings = [22.5,23]   readings = [1500,1520,1510]"
    ))

    # --- Section 3: State vs Behavior ---
    cells.append(md(
        "---\n## Section 3: State vs Behavior\n\n"
        "Every object has two aspects:\n\n"
        "| Aspect | What it means | Example (Sensor) |\n"
        "|--------|--------------|-------------------|\n"
        "| **State** (attributes) | The data the object holds | "
        "`name`, `unit`, `readings` |\n"
        "| **Behavior** (methods) | What the object can do | "
        "`add_reading()`, `get_mean()` |\n\n"
        "**State** is stored in attributes (variables attached to `self`).\n"
        "**Behavior** is defined by methods (functions inside the class).\n\n"
        "Think of a robot:\n"
        "- **State:** battery_level=87, position=(3,5), is_moving=True\n"
        "- **Behavior:** move_forward(), turn_left(), pick_up()\n\n"
        "The key insight: **methods can read and change the state**. "
        "The `add_reading` method changes the `readings` attribute. "
        "The `get_mean` method reads the `readings` attribute."
    ))

    cells.append(code(
        "# Demonstrating state change\n"
        "s = Sensor(\"Vibration\", \"mm/s\")\n"
        "print(\"Before:\", s.readings, \"-- mean:\", s.get_mean())\n"
        "\n"
        "s.add_reading(0.5)\n"
        "s.add_reading(1.2)\n"
        "print(\"After: \", s.readings, \"-- mean:\", round(s.get_mean(), 2))\n"
        "\n"
        "# The method changed the state!\n"
        "print(\"Number of readings:\", len(s.readings))"
    ))
    cells.append(expected_output(
        "Before: [] -- mean: 0.0\n"
        "After:  [0.5, 1.2] -- mean: 0.85\n"
        "Number of readings: 2"
    ))

    # --- Section 4: Procedural vs OOP ---
    cells.append(md("---\n## Section 4: Procedural vs OOP -- Side by Side"))

    cells.extend(procedural_vs_oop(
        "Managing Sensor Data",
        (
            "# PROCEDURAL: functions + dictionaries\n"
            "\n"
            "def create_sensor(name, unit):\n"
            "    return {\"name\": name, \"unit\": unit, \"readings\": []}\n"
            "\n"
            "def add_reading(sensor, value):\n"
            "    sensor[\"readings\"].append(value)\n"
            "\n"
            "def get_mean(sensor):\n"
            "    r = sensor[\"readings\"]\n"
            "    return sum(r) / len(r) if r else 0\n"
            "\n"
            "# Usage\n"
            "s = create_sensor(\"Temp\", \"C\")\n"
            "add_reading(s, 22.5)\n"
            "add_reading(s, 23.0)\n"
            "print(get_mean(s))"
        ),
        (
            "# OOP: class bundles data + functions\n"
            "\n"
            "class Sensor:\n"
            "    def __init__(self, name, unit):\n"
            "        self.name = name\n"
            "        self.unit = unit\n"
            "        self.readings = []\n"
            "\n"
            "    def add_reading(self, value):\n"
            "        self.readings.append(value)\n"
            "\n"
            "    def get_mean(self):\n"
            "        return sum(self.readings) / len(self.readings) if self.readings else 0\n"
            "\n"
            "# Usage\n"
            "s = Sensor(\"Temp\", \"C\")\n"
            "s.add_reading(22.5)\n"
            "s.add_reading(23.0)\n"
            "print(s.get_mean())"
        ),
        "**Why is the OOP version better?**\n\n"
        "1. **Encapsulation**: Data and functions that operate on it are "
        "bundled together. You cannot accidentally pass the wrong dictionary "
        "to the wrong function.\n"
        "2. **Discoverability**: Type `s.` and your IDE shows you everything "
        "a Sensor can do.\n"
        "3. **Safety**: In the procedural version, nothing stops you from "
        "writing `s[\"readnigs\"]` (typo) -- you get a silent KeyError at "
        "runtime. With OOP, `s.readnigs` gives an immediate AttributeError.\n"
        "4. **Reusability**: One class definition creates unlimited sensors, "
        "each with its own state."
    ))

    # --- Section 5: self explained ---
    cells.append(md(
        "---\n## Section 5: Understanding `self`\n\n"
        "`self` is the **most confusing part** of Python OOP for beginners. "
        "Let us demystify it.\n\n"
        "When you write `temp.add_reading(22.5)`, Python translates it to "
        "`Sensor.add_reading(temp, 22.5)`. The object before the dot is "
        "automatically passed as the first argument -- that is `self`.\n\n"
        "**Rule:** Every method in a class must have `self` as its first "
        "parameter. Inside the method, `self.something` accesses or creates "
        "an attribute on that specific object.\n\n"
        "**Analogy:** `self` is like saying 'my' -- when a sensor says "
        "`self.name`, it means 'my name'. When you have two sensors, each "
        "one's `self` refers to itself."
    ))
    cells.append(code(
        "# Python translates method calls like this:\n"
        "# temp.add_reading(22.5)  -->  Sensor.add_reading(temp, 22.5)\n"
        "\n"
        "# We can prove it:\n"
        "temp = Sensor(\"Temp\", \"C\")\n"
        "\n"
        "# Normal way\n"
        "temp.add_reading(100)\n"
        "\n"
        "# Explicit way (same thing!)\n"
        "Sensor.add_reading(temp, 200)\n"
        "\n"
        "print(temp.readings)  # both 100 and 200 are there"
    ))
    cells.append(expected_output("[100, 200]"))

    # --- Common Mistakes ---
    cells.append(md("---\n## Section 6: Common Mistakes\n\n"
                     "OOP introduces new error patterns. Let us see the most "
                     "common ones and learn to fix them."))

    cells.extend(common_mistake(
        "Forgetting `self` in method definition",
        (
            "class Broken:\n"
            "    def __init__(self, name):\n"
            "        self.name = name\n"
            "\n"
            "    def greet():  # BUG: missing self!\n"
            "        print(\"Hello from \" + self.name)\n"
            "\n"
            "b = Broken(\"test\")\n"
            "try:\n"
            "    b.greet()\n"
            "except TypeError as e:\n"
            "    print(\"ERROR:\", e)"
        ),
        (
            "class Fixed:\n"
            "    def __init__(self, name):\n"
            "        self.name = name\n"
            "\n"
            "    def greet(self):  # FIXED: added self\n"
            "        print(\"Hello from \" + self.name)\n"
            "\n"
            "f = Fixed(\"test\")\n"
            "f.greet()"
        ),
        "Python passes the object as the first argument automatically. "
        "If you do not have `self` in the parameter list, Python tries to "
        "pass the object but there is no parameter to receive it. You get: "
        "`TypeError: greet() takes 0 positional arguments but 1 was given`."
    ))

    cells.extend(common_mistake(
        "Forgetting `self.` when accessing attributes",
        (
            "class Broken2:\n"
            "    def __init__(self, name):\n"
            "        self.name = name\n"
            "        self.count = 0\n"
            "\n"
            "    def increment(self):\n"
            "        count += 1  # BUG: this is a local variable, not self.count!\n"
            "\n"
            "b = Broken2(\"test\")\n"
            "try:\n"
            "    b.increment()\n"
            "except UnboundLocalError as e:\n"
            "    print(\"ERROR:\", e)"
        ),
        (
            "class Fixed2:\n"
            "    def __init__(self, name):\n"
            "        self.name = name\n"
            "        self.count = 0\n"
            "\n"
            "    def increment(self):\n"
            "        self.count += 1  # FIXED: use self.count\n"
            "\n"
            "f = Fixed2(\"test\")\n"
            "f.increment()\n"
            "f.increment()\n"
            "print(\"count:\", f.count)"
        ),
        "Without `self.`, Python thinks `count` is a local variable inside "
        "the method. It has never been assigned locally, so you get an "
        "`UnboundLocalError`. Always use `self.attribute` to access object state."
    ))

    cells.extend(common_mistake(
        "Creating attributes outside __init__",
        (
            "class Risky:\n"
            "    def __init__(self, name):\n"
            "        self.name = name\n"
            "        # Oops -- forgot to initialize self.data here\n"
            "\n"
            "    def load(self):\n"
            "        self.data = [1, 2, 3]  # created here instead\n"
            "\n"
            "    def process(self):\n"
            "        return sum(self.data)  # crashes if load() not called first!\n"
            "\n"
            "r = Risky(\"test\")\n"
            "try:\n"
            "    r.process()  # AttributeError!\n"
            "except AttributeError as e:\n"
            "    print(\"ERROR:\", e)"
        ),
        (
            "class Safe:\n"
            "    def __init__(self, name):\n"
            "        self.name = name\n"
            "        self.data = []  # FIXED: always initialize in __init__\n"
            "\n"
            "    def load(self):\n"
            "        self.data = [1, 2, 3]\n"
            "\n"
            "    def process(self):\n"
            "        if not self.data:\n"
            "            print(\"No data loaded yet!\")\n"
            "            return 0\n"
            "        return sum(self.data)\n"
            "\n"
            "s = Safe(\"test\")\n"
            "print(s.process())  # safe: returns 0\n"
            "s.load()\n"
            "print(s.process())  # 6"
        ),
        "**Best practice:** Always initialize ALL attributes in `__init__`. "
        "Use `None`, `[]`, or a sensible default. This way, every object is "
        "in a valid state from the moment it is created."
    ))

    # --- Debugging Tips ---
    cells.append(debugging_tip(
        "AttributeError: object has no attribute ...",
        "This is the #1 OOP error. It means you tried to access an "
        "attribute that does not exist on the object. Common causes:\n\n"
        "1. **Typo** in the attribute name (`self.naem` instead of `self.name`)\n"
        "2. **Forgot to initialize** the attribute in `__init__`\n"
        "3. **Forgot `self.`** when setting the attribute (wrote `name = x` "
        "instead of `self.name = x`)\n\n"
        "**Fix:** Check `__init__` -- is the attribute there? Check spelling. "
        "Use `print(dir(obj))` to see all attributes an object has."
    ))

    cells.append(debugging_tip(
        "TypeError: __init__() takes N positional arguments but M were given",
        "This means you are passing the wrong number of arguments when "
        "creating an object.\n\n"
        "```python\n"
        "class Sensor:\n"
        "    def __init__(self, name, unit):  # expects 2 args\n"
        "        ...\n"
        "\n"
        "s = Sensor(\"Temp\")  # only 1 arg -> TypeError!\n"
        "```\n\n"
        "**Fix:** Count the parameters in `__init__` (excluding `self`). "
        "Pass exactly that many arguments."
    ))

    # --- Try It exercises ---
    cells.extend(try_it(
        "Create a `BankAccount` class with:\n"
        "- Attributes: `owner` (str), `balance` (float, starts at 0)\n"
        "- Methods: `deposit(amount)`, `withdraw(amount)`, `get_balance()`\n"
        "- `withdraw` should print a warning if balance would go negative\n\n"
        "Test it by creating two accounts and making several transactions."
    ))

    cells.extend(try_it(
        "Create a `Counter` class with:\n"
        "- An attribute `count` that starts at 0\n"
        "- Methods: `increment()`, `decrement()`, `reset()`, `get_count()`\n"
        "- Add a `__str__` method that returns something like `Counter(5)`\n\n"
        "Create two separate counters and verify they track independently."
    ))

    # --- Design Decisions ---
    cells.append(design_decision(
        "When to use a class vs a function",
        "**Use a function** when:\n"
        "- You have a single operation with no state to remember\n"
        "- The operation is simple and self-contained\n"
        "- Example: `def celsius_to_fahrenheit(temp): return temp * 9/5 + 32`\n\n"
        "**Use a class** when:\n"
        "- You have data AND operations that go together\n"
        "- You need to remember state between calls\n"
        "- You want to create multiple instances with different configurations\n"
        "- Example: A `Sensor` that accumulates readings over time\n\n"
        "**Rule of thumb:** If you find yourself passing the same dictionary "
        "to multiple functions, those functions and that dictionary probably "
        "want to be a class."
    ))

    # --- Section 7: Building a Bigger Example ---
    cells.append(md(
        "---\n## Section 7: Putting It All Together -- Pipeline Preview\n\n"
        "Let us build a tiny version of what your v3 pipeline will look like. "
        "This previews the next 13 weeks."
    ))
    cells.append(code(
        "class DataSource:\n"
        "    \"\"\"Loads raw data from a path.\"\"\"\n"
        "\n"
        "    def __init__(self, path):\n"
        "        self.path = path\n"
        "        self.raw_data = None\n"
        "\n"
        "    def load(self):\n"
        "        # Simulate loading\n"
        "        self.raw_data = [\n"
        "            {\"id\": 1, \"value\": 25.0, \"status\": \"ok\"},\n"
        "            {\"id\": 2, \"value\": 30.0, \"status\": \"ok\"},\n"
        "            {\"id\": 3, \"value\": -5.0, \"status\": \"error\"},\n"
        "        ]\n"
        "        print(\"Loaded \" + str(len(self.raw_data)) + \" rows from \" + self.path)\n"
        "        return self.raw_data\n"
        "\n"
        "\n"
        "class Cleaner:\n"
        "    \"\"\"Cleans data by removing invalid rows.\"\"\"\n"
        "\n"
        "    def __init__(self, min_val=0, max_val=100):\n"
        "        self.min_val = min_val\n"
        "        self.max_val = max_val\n"
        "        self.dropped = 0\n"
        "\n"
        "    def clean(self, data):\n"
        "        result = []\n"
        "        self.dropped = 0\n"
        "        for row in data:\n"
        "            val = row.get(\"value\")\n"
        "            if isinstance(val, (int, float)) and self.min_val <= val <= self.max_val:\n"
        "                result.append(row)\n"
        "            else:\n"
        "                self.dropped += 1\n"
        "        print(\"Cleaned: kept \" + str(len(result)) + \", dropped \" + str(self.dropped))\n"
        "        return result\n"
        "\n"
        "\n"
        "class Analyzer:\n"
        "    \"\"\"Computes statistics on clean data.\"\"\"\n"
        "\n"
        "    def __init__(self, column=\"value\"):\n"
        "        self.column = column\n"
        "        self.results = {}\n"
        "\n"
        "    def analyze(self, data):\n"
        "        values = [row[self.column] for row in data if self.column in row]\n"
        "        if not values:\n"
        "            self.results = {\"count\": 0}\n"
        "            return self.results\n"
        "        self.results = {\n"
        "            \"count\": len(values),\n"
        "            \"mean\": round(sum(values) / len(values), 2),\n"
        "            \"min\": min(values),\n"
        "            \"max\": max(values),\n"
        "        }\n"
        "        print(\"Analysis: \" + str(self.results))\n"
        "        return self.results\n"
        "\n"
        "\n"
        "# Wire them together\n"
        "source = DataSource(\"data/raw/sensors.csv\")\n"
        "cleaner = Cleaner(min_val=0, max_val=100)\n"
        "analyzer = Analyzer(\"value\")\n"
        "\n"
        "raw = source.load()\n"
        "clean = cleaner.clean(raw)\n"
        "results = analyzer.analyze(clean)\n"
        "\n"
        "print()\n"
        "print(\"Each component has ONE job.\")\n"
        "print(\"Each component remembers its own state.\")\n"
        "print(\"Components are INDEPENDENT -- swap one without touching others.\")"
    ))
    cells.append(expected_output(
        "Loaded 3 rows from data/raw/sensors.csv\n"
        "Cleaned: kept 2, dropped 1\n"
        "Analysis: {'count': 2, 'mean': 27.5, 'min': 25.0, 'max': 30.0}\n\n"
        "Each component has ONE job.\n"
        "Each component remembers its own state.\n"
        "Components are INDEPENDENT -- swap one without touching others."
    ))

    # --- Mini-Quiz ---
    cells.append(md(
        "---\n## Mini-Quiz\n\n"
        "Answer these in the code cell below. No peeking!"
    ))
    cells.append(code(
        "# Q1: What keyword creates a class?\n"
        "# Answer: \n"
        "\n"
        "# Q2: What special method runs when you create an object?\n"
        "# Answer: \n"
        "\n"
        "# Q3: What is 'self'?\n"
        "# Answer: \n"
        "\n"
        "# Q4: What is the difference between a class and an object?\n"
        "# Answer: \n"
        "\n"
        "# Q5: Name two benefits of OOP over procedural code.\n"
        "# Answer: "
    ))

    # --- Homework Preview ---
    cells.append(md(
        "---\n## Homework Preview\n\n"
        "This week's homework has **12 exercises**. You will:\n\n"
        "1. Create classes from scratch\n"
        "2. Add methods that modify state\n"
        "3. Write `__str__` methods\n"
        "4. Compare procedural vs OOP implementations\n"
        "5. Design a class diagram before writing code\n\n"
        "See the homework notebook for full details."
    ))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# WEEK 2: Composition -- DataSource & Dataset
# ============================================================
def week02_core():
    cells = []
    cells.append(md(
        "# OOP Week 2 -- Composition: DataSource & Dataset\n\n"
        "**Course:** Object-Oriented Programming (Year 2)\n"
        "**Session:** 3 hours\n"
        "**Prerequisites:** Week 1 (Classes & Objects)\n"
        "**Focus:** composition, has-a relationships, wrapping data in objects\n\n"
        "---\n\n"
        "## Learning Objectives\n\n"
        "1. Explain composition ('has-a') relationships\n"
        "2. Build a `Dataset` class that wraps raw data with metadata\n"
        "3. Build a `DataSource` that creates `Dataset` objects\n"
        "4. Understand why we wrap data in objects instead of using raw dicts/lists\n"
        "5. Draw composition diagrams"
    ))
    cells.append(setup_cell())

    # Section 1: What is Composition?
    cells.append(md(
        "---\n## Section 1: What is Composition?\n\n"
        "**Composition** means one object **contains** another object. "
        "We say object A 'has-a' object B.\n\n"
        "### Real-World Examples\n\n"
        "- A **Car** has-a Engine, has-a Transmission, has-a Battery\n"
        "- A **Kitchen** has-a Oven, has-a Refrigerator, has-a Sink\n"
        "- A **Robot** has-a MotorController, has-a SensorArray, has-a Battery\n"
        "- A **Pipeline** has-a DataSource, has-a Cleaner, has-a Analyzer\n\n"
        "Composition is the **most common** relationship in OOP. It is how "
        "you build complex systems from simple parts.\n\n"
        "### Composition vs Inheritance\n\n"
        "| Composition (has-a) | Inheritance (is-a) |\n"
        "|--------------------|-----------------|\n"
        "| Car HAS-A Engine | ElectricCar IS-A Car |\n"
        "| Pipeline HAS-A Cleaner | RangeCleaner IS-A Cleaner |\n"
        "| Flexible, easy to swap parts | Rigid hierarchy |\n"
        "| **Preferred in modern Python** | Use sparingly |\n\n"
        "We will focus on composition for the next several weeks."
    ))

    cells.append(ascii_diagram(
        "Composition: Pipeline has-a DataSource, Cleaner, Analyzer",
        "+------------------+       +------------------+\n"
        "|    Pipeline      |       |    DataSource     |\n"
        "+------------------+  has  +------------------+\n"
        "| - source --------+------>| - path: str      |\n"
        "| - cleaner -------+--+    | + load() -> Dataset\n"
        "| - analyzer ------+-+|    +------------------+\n"
        "+------------------+ ||    \n"
        "| + run()          | ||    +------------------+\n"
        "+------------------+ |+--->|    Cleaner        |\n"
        "                     |     +------------------+\n"
        "                     |     | - min_val: float |\n"
        "                     |     | + clean(data)    |\n"
        "                     |     +------------------+\n"
        "                     |     \n"
        "                     +---->+------------------+\n"
        "                           |    Analyzer       |\n"
        "                           +------------------+\n"
        "                           | - column: str    |\n"
        "                           | + analyze(data)  |\n"
        "                           +------------------+"
    ))

    # Section 2: The Dataset Class
    cells.append(md(
        "---\n## Section 2: The Dataset Class\n\n"
        "Right now your data is a plain list of dictionaries. That works, "
        "but it has problems:\n\n"
        "- No metadata (where did it come from? how many rows?)\n"
        "- No helper methods (want column names? write code every time)\n"
        "- No validation (is the data even valid?)\n\n"
        "A `Dataset` class wraps the raw data and adds all of this."
    ))

    # Example 1: Basic Dataset
    cells.append(md("### Example 1: Basic Dataset"))
    cells.append(code(
        "class Dataset:\n"
        "    \"\"\"A structured container for tabular data.\"\"\"\n"
        "\n"
        "    def __init__(self, rows, source_path=\"unknown\"):\n"
        "        self.rows = rows\n"
        "        self.source_path = source_path\n"
        "        self.n_rows = len(rows)\n"
        "        self.columns = list(rows[0].keys()) if rows else []\n"
        "\n"
        "    def get_column(self, name):\n"
        "        \"\"\"Extract all values for a given column.\"\"\"\n"
        "        return [row.get(name) for row in self.rows]\n"
        "\n"
        "    def head(self, n=5):\n"
        "        \"\"\"Return first n rows.\"\"\"\n"
        "        return self.rows[:n]\n"
        "\n"
        "    def describe(self):\n"
        "        \"\"\"Print a summary of the dataset.\"\"\"\n"
        "        print(\"Dataset Summary\")\n"
        "        print(\"  Source:  \" + self.source_path)\n"
        "        print(\"  Rows:   \" + str(self.n_rows))\n"
        "        print(\"  Columns: \" + str(self.columns))\n"
        "\n"
        "    def __len__(self):\n"
        "        return self.n_rows\n"
        "\n"
        "    def __str__(self):\n"
        "        return \"Dataset(\" + str(self.n_rows) + \" rows, columns=\" + str(self.columns) + \")\"\n"
        "\n"
        "\n"
        "# Create a Dataset\n"
        "raw = [\n"
        "    {\"id\": 1, \"value\": 25.0, \"status\": \"ok\"},\n"
        "    {\"id\": 2, \"value\": 30.0, \"status\": \"ok\"},\n"
        "    {\"id\": 3, \"value\": 88.0, \"status\": \"warning\"},\n"
        "    {\"id\": 4, \"value\": -5.0, \"status\": \"error\"},\n"
        "]\n"
        "ds = Dataset(raw, \"data/raw/sensors.csv\")\n"
        "\n"
        "print(ds)\n"
        "ds.describe()\n"
        "print(\"Values:\", ds.get_column(\"value\"))\n"
        "print(\"First 2:\", ds.head(2))"
    ))
    cells.append(expected_output(
        "Dataset(4 rows, columns=['id', 'value', 'status'])\n"
        "Dataset Summary\n"
        "  Source:  data/raw/sensors.csv\n"
        "  Rows:   4\n"
        "  Columns: ['id', 'value', 'status']\n"
        "Values: [25.0, 30.0, 88.0, -5.0]\n"
        "First 2: [{'id': 1, 'value': 25.0, 'status': 'ok'}, "
        "{'id': 2, 'value': 30.0, 'status': 'ok'}]"
    ))

    # Example 2: Dataset with filtering
    cells.append(md("### Example 2: Adding Filtering to Dataset"))
    cells.append(code(
        "class Dataset:\n"
        "    \"\"\"Enhanced Dataset with filtering.\"\"\"\n"
        "\n"
        "    def __init__(self, rows, source_path=\"unknown\"):\n"
        "        self.rows = rows\n"
        "        self.source_path = source_path\n"
        "        self.n_rows = len(rows)\n"
        "        self.columns = list(rows[0].keys()) if rows else []\n"
        "\n"
        "    def get_column(self, name):\n"
        "        return [row.get(name) for row in self.rows]\n"
        "\n"
        "    def filter_rows(self, column, condition):\n"
        "        \"\"\"Return a NEW Dataset with only rows meeting condition.\n"
        "\n"
        "        Does NOT modify the original dataset.\n"
        "        \"\"\"\n"
        "        kept = [row for row in self.rows if condition(row.get(column))]\n"
        "        return Dataset(kept, self.source_path)\n"
        "\n"
        "    def __len__(self):\n"
        "        return self.n_rows\n"
        "\n"
        "    def __str__(self):\n"
        "        return \"Dataset(\" + str(self.n_rows) + \" rows)\"\n"
        "\n"
        "\n"
        "ds = Dataset(raw, \"sensors.csv\")\n"
        "print(\"Original:\", ds)\n"
        "\n"
        "# Filter: keep only positive values\n"
        "positive = ds.filter_rows(\"value\", lambda v: isinstance(v, (int, float)) and v > 0)\n"
        "print(\"Positive:\", positive)\n"
        "print(\"Positive values:\", positive.get_column(\"value\"))\n"
        "\n"
        "# Original is unchanged!\n"
        "print(\"Original still has:\", len(ds), \"rows\")"
    ))
    cells.append(expected_output(
        "Original: Dataset(4 rows)\n"
        "Positive: Dataset(3 rows)\n"
        "Positive values: [25.0, 30.0, 88.0]\n"
        "Original still has: 4 rows"
    ))

    cells.append(design_decision(
        "Why filter_rows returns a NEW Dataset",
        "Notice that `filter_rows` does not modify `self.rows`. It creates "
        "and returns a **new** Dataset. This is called being **immutable** "
        "(or at least non-destructive).\n\n"
        "Why? Because you might want to:\n"
        "- Apply different filters to the same original data\n"
        "- Compare before and after\n"
        "- Debug by looking at the original\n\n"
        "**Rule of thumb:** Methods that transform data should return new "
        "objects, not modify the original. Methods that update state (like "
        "`add_reading`) are the exception."
    ))

    # Section 3: The DataSource Class
    cells.append(md(
        "---\n## Section 3: The DataSource Class\n\n"
        "The DataSource is responsible for loading data from an external "
        "source and returning a Dataset. This separates the 'where data "
        "comes from' logic from the 'what data looks like' logic."
    ))
    cells.append(code(
        "class DataSource:\n"
        "    \"\"\"Loads raw data and returns a Dataset.\"\"\"\n"
        "\n"
        "    def __init__(self, path, required_columns=None):\n"
        "        self.path = path\n"
        "        self.required_columns = required_columns or []\n"
        "\n"
        "    def load(self):\n"
        "        \"\"\"Load data and return as a Dataset.\"\"\"\n"
        "        # Simulate loading from file\n"
        "        raw = [\n"
        "            {\"id\": 1, \"value\": 25.0, \"status\": \"ok\"},\n"
        "            {\"id\": 2, \"value\": 30.0, \"status\": \"ok\"},\n"
        "            {\"id\": 3, \"value\": 88.0, \"status\": \"warning\"},\n"
        "            {\"id\": 4, \"value\": -5.0, \"status\": \"error\"},\n"
        "        ]\n"
        "\n"
        "        # Validate required columns\n"
        "        if raw and self.required_columns:\n"
        "            actual = set(raw[0].keys())\n"
        "            missing = set(self.required_columns) - actual\n"
        "            if missing:\n"
        "                raise ValueError(\"Missing columns: \" + str(missing))\n"
        "\n"
        "        dataset = Dataset(raw, self.path)\n"
        "        print(\"Loaded: \" + str(dataset))\n"
        "        return dataset\n"
        "\n"
        "\n"
        "# DataSource CREATES a Dataset (composition in action)\n"
        "source = DataSource(\"data/raw/sensors.csv\", required_columns=[\"id\", \"value\"])\n"
        "dataset = source.load()\n"
        "\n"
        "print(\"Rows:\", len(dataset))\n"
        "print(\"Columns:\", dataset.columns)\n"
        "print(\"Values:\", dataset.get_column(\"value\"))"
    ))
    cells.append(expected_output(
        "Loaded: Dataset(4 rows)\n"
        "Rows: 4\n"
        "Columns: ['id', 'value', 'status']\n"
        "Values: [25.0, 30.0, 88.0, -5.0]"
    ))

    # Section 4: Composing Components
    cells.append(md(
        "---\n## Section 4: Composing Components Together\n\n"
        "Now let us compose DataSource, Dataset, and a simple Cleaner into "
        "a mini-pipeline. Each component does one job and passes its output "
        "to the next."
    ))
    cells.append(code(
        "class SimpleCleaner:\n"
        "    \"\"\"Cleans a Dataset by filtering rows.\"\"\"\n"
        "\n"
        "    def __init__(self, value_column, min_val, max_val):\n"
        "        self.value_column = value_column\n"
        "        self.min_val = min_val\n"
        "        self.max_val = max_val\n"
        "        self.drop_count = 0\n"
        "\n"
        "    def clean(self, dataset):\n"
        "        \"\"\"Return a new clean Dataset.\"\"\"\n"
        "        clean_rows = []\n"
        "        self.drop_count = 0\n"
        "        for row in dataset.rows:\n"
        "            val = row.get(self.value_column)\n"
        "            if isinstance(val, (int, float)) and self.min_val <= val <= self.max_val:\n"
        "                clean_rows.append(row)\n"
        "            else:\n"
        "                self.drop_count += 1\n"
        "        result = Dataset(clean_rows, dataset.source_path)\n"
        "        print(\"Cleaned: \" + str(len(dataset)) + \" -> \" + str(len(result))\n"
        "              + \" (dropped \" + str(self.drop_count) + \")\")\n"
        "        return result\n"
        "\n"
        "\n"
        "# Compose the pipeline\n"
        "source = DataSource(\"data/raw/sensors.csv\")\n"
        "cleaner = SimpleCleaner(\"value\", min_val=0, max_val=100)\n"
        "\n"
        "# Run\n"
        "dataset = source.load()\n"
        "clean_dataset = cleaner.clean(dataset)\n"
        "\n"
        "print()\n"
        "print(\"Original values:\", dataset.get_column(\"value\"))\n"
        "print(\"Clean values:   \", clean_dataset.get_column(\"value\"))"
    ))
    cells.append(expected_output(
        "Loaded: Dataset(4 rows)\n"
        "Cleaned: 4 -> 3 (dropped 1)\n\n"
        "Original values: [25.0, 30.0, 88.0, -5.0]\n"
        "Clean values:    [25.0, 30.0, 88.0]"
    ))

    # Procedural vs OOP
    cells.extend(procedural_vs_oop(
        "Loading and Cleaning Data",
        (
            "# PROCEDURAL\n"
            "def load_data(path):\n"
            "    return [{\"id\": 1, \"value\": 25}, {\"id\": 2, \"value\": -5}]\n"
            "\n"
            "def clean_data(data, col, lo, hi):\n"
            "    return [r for r in data if lo <= r.get(col, 0) <= hi]\n"
            "\n"
            "raw = load_data(\"data.csv\")\n"
            "clean = clean_data(raw, \"value\", 0, 100)\n"
            "print(len(clean), \"rows\")\n"
            "# No metadata! Where did it come from? What columns?"
        ),
        (
            "# OOP\n"
            "source = DataSource(\"data.csv\")\n"
            "dataset = source.load()   # returns a Dataset object\n"
            "print(dataset)            # knows its own metadata\n"
            "print(dataset.columns)    # self-documenting\n"
            "\n"
            "clean = cleaner.clean(dataset)  # returns new Dataset\n"
            "print(clean)              # metadata preserved"
        ),
        "The OOP version is **self-documenting**. The Dataset object knows "
        "where it came from, what columns it has, and how many rows. In the "
        "procedural version, that metadata is lost -- it is just a plain list."
    ))

    # Common Mistake
    cells.extend(common_mistake(
        "Modifying the original dataset",
        (
            "class BadCleaner:\n"
            "    def clean(self, dataset):\n"
            "        # BUG: modifies the original!\n"
            "        i = 0\n"
            "        while i < len(dataset.rows):\n"
            "            if dataset.rows[i].get(\"value\", 0) < 0:\n"
            "                dataset.rows.pop(i)\n"
            "            else:\n"
            "                i += 1\n"
            "        return dataset\n"
            "\n"
            "ds = Dataset([{\"value\": 10}, {\"value\": -5}, {\"value\": 20}])\n"
            "print(\"Before:\", len(ds), \"rows\")\n"
            "cleaned = BadCleaner().clean(ds)\n"
            "print(\"After: \", len(ds), \"rows\")  # OOPS: original changed!"
        ),
        (
            "class GoodCleaner:\n"
            "    def clean(self, dataset):\n"
            "        # FIXED: create new list, do not modify original\n"
            "        kept = [r for r in dataset.rows if r.get(\"value\", 0) >= 0]\n"
            "        return Dataset(kept, dataset.source_path)\n"
            "\n"
            "ds = Dataset([{\"value\": 10}, {\"value\": -5}, {\"value\": 20}])\n"
            "print(\"Before:\", len(ds), \"rows\")\n"
            "cleaned = GoodCleaner().clean(ds)\n"
            "print(\"After: \", len(ds), \"rows\")  # Original unchanged!\n"
            "print(\"Clean: \", len(cleaned), \"rows\")"
        ),
        "The BadCleaner uses `pop()` to remove items from the original list. "
        "Since lists are mutable, this modifies the original Dataset. Always "
        "create a NEW list/Dataset when cleaning."
    ))

    # Try It
    cells.extend(try_it(
        "Create a `Dataset` that holds student grade data:\n"
        "```python\n"
        "grades = [\n"
        "    {\"name\": \"Alice\", \"score\": 92},\n"
        "    {\"name\": \"Bob\", \"score\": 67},\n"
        "    {\"name\": \"Charlie\", \"score\": 45},\n"
        "    {\"name\": \"Diana\", \"score\": 88},\n"
        "]\n"
        "```\n"
        "1. Create the Dataset\n"
        "2. Use `get_column` to extract all scores\n"
        "3. Create a `GradeCleaner` that drops scores below 50\n"
        "4. Verify the original dataset is unchanged"
    ))

    cells.append(md(
        "---\n## Mini-Quiz"
    ))
    cells.append(code(
        "# Q1: What is composition?\n"
        "# Answer: \n"
        "\n"
        "# Q2: What is the difference between 'has-a' and 'is-a'?\n"
        "# Answer: \n"
        "\n"
        "# Q3: Why should clean() return a NEW dataset instead of modifying the original?\n"
        "# Answer: \n"
        "\n"
        "# Q4: What does the DataSource create and return?\n"
        "# Answer: \n"
        "\n"
        "# Q5: Draw (in comments) a composition diagram for a school:\n"
        "#      School has-a ... has-a ... \n"
        "# Answer: "
    ))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# WEEK 3: Cleaner Component
# ============================================================
def week03_core():
    cells = []
    cells.append(md(
        "# OOP Week 3 -- Cleaner Component\n\n"
        "**Course:** Object-Oriented Programming (Year 2)\n"
        "**Session:** 3 hours\n"
        "**Prerequisites:** Weeks 1-2 (Classes, Composition)\n"
        "**Focus:** strategy selection, composing cleaners, "
        "method overriding\n\n"
        "---\n\n"
        "## Learning Objectives\n\n"
        "1. Build a base cleaner class with a template method\n"
        "2. Create specialized cleaner subclasses\n"
        "3. Compose multiple cleaners into a pipeline\n"
        "4. Understand method overriding (polymorphism preview)\n"
        "5. Track cleaning metadata (drop counts, reasons)"
    ))
    cells.append(setup_cell())

    # Redefine Dataset for this notebook
    cells.append(md("---\n## Setup: Dataset Class (from Week 2)"))
    cells.append(code(
        "class Dataset:\n"
        "    \"\"\"Data container from Week 2.\"\"\"\n"
        "    def __init__(self, rows, source_path=\"unknown\"):\n"
        "        self.rows = rows\n"
        "        self.source_path = source_path\n"
        "        self.n_rows = len(rows)\n"
        "        self.columns = list(rows[0].keys()) if rows else []\n"
        "\n"
        "    def get_column(self, name):\n"
        "        return [row.get(name) for row in self.rows]\n"
        "\n"
        "    def __len__(self):\n"
        "        return self.n_rows\n"
        "\n"
        "    def __str__(self):\n"
        "        return \"Dataset(\" + str(self.n_rows) + \" rows)\"\n"
        "\n"
        "\n"
        "# Sample data for this session\n"
        "sample_data = Dataset([\n"
        "    {\"id\": 1, \"value\": 25.0, \"status\": \"ok\"},\n"
        "    {\"id\": 2, \"value\": 30.0, \"status\": \"ok\"},\n"
        "    {\"id\": 3, \"value\": 88.0, \"status\": \"warning\"},\n"
        "    {\"id\": 4, \"value\": -5.0, \"status\": \"error\"},\n"
        "    {\"id\": 5, \"value\": None, \"status\": \"ok\"},\n"
        "    {\"id\": 6, \"value\": 200.0, \"status\": \"ok\"},\n"
        "    {\"id\": 7, \"value\": 42.0, \"status\": \"\"},\n"
        "], \"sensors.csv\")\n"
        "print(\"Sample:\", sample_data)"
    ))
    cells.append(expected_output("Sample: Dataset(7 rows)"))

    # Section 1: Base Cleaner
    cells.append(md(
        "---\n## Section 1: The Base Cleaner Pattern\n\n"
        "Instead of writing one giant cleaning function, we define a "
        "**base class** that provides the cleaning loop, and **subclasses** "
        "that define specific cleaning rules.\n\n"
        "This is called the **Template Method** pattern: the base class "
        "defines the algorithm skeleton, and subclasses fill in the details."
    ))
    cells.append(code(
        "class BaseCleaner:\n"
        "    \"\"\"Base cleaner with template method pattern.\n"
        "\n"
        "    Subclasses override check() to define their cleaning rule.\n"
        "    The clean() method handles the loop and tracking.\n"
        "    \"\"\"\n"
        "\n"
        "    def __init__(self, name=\"base\"):\n"
        "        self.name = name\n"
        "        self.drop_reasons = {}\n"
        "        self.n_checked = 0\n"
        "        self.n_dropped = 0\n"
        "\n"
        "    def clean(self, dataset):\n"
        "        \"\"\"Clean a dataset. Returns a NEW Dataset.\"\"\"\n"
        "        clean_rows = []\n"
        "        self.drop_reasons = {}\n"
        "        self.n_checked = 0\n"
        "        self.n_dropped = 0\n"
        "\n"
        "        for row in dataset.rows:\n"
        "            self.n_checked += 1\n"
        "            reason = self.check(row)\n"
        "            if reason is None:\n"
        "                clean_rows.append(row)\n"
        "            else:\n"
        "                self.n_dropped += 1\n"
        "                self.drop_reasons[reason] = self.drop_reasons.get(reason, 0) + 1\n"
        "\n"
        "        return Dataset(clean_rows, dataset.source_path)\n"
        "\n"
        "    def check(self, row):\n"
        "        \"\"\"Check one row. Return reason string if invalid, None if ok.\n"
        "\n"
        "        Override this in subclasses!\n"
        "        \"\"\"\n"
        "        return None  # base class accepts everything\n"
        "\n"
        "    def report(self):\n"
        "        \"\"\"Print a cleaning report.\"\"\"\n"
        "        print(\"Cleaner: \" + self.name)\n"
        "        print(\"  Checked: \" + str(self.n_checked))\n"
        "        print(\"  Dropped: \" + str(self.n_dropped))\n"
        "        for reason, count in self.drop_reasons.items():\n"
        "            print(\"    - \" + reason + \": \" + str(count))\n"
        "\n"
        "\n"
        "# The base cleaner accepts everything\n"
        "base = BaseCleaner()\n"
        "result = base.clean(sample_data)\n"
        "print(\"Base cleaner kept:\", len(result), \"of\", len(sample_data))\n"
        "base.report()"
    ))
    cells.append(expected_output(
        "Base cleaner kept: 7 of 7\n"
        "Cleaner: base\n"
        "  Checked: 7\n"
        "  Dropped: 0"
    ))

    # Section 2: Specialized Cleaners
    cells.append(md(
        "---\n## Section 2: Specialized Cleaners\n\n"
        "Now we create cleaners that override `check()` with specific rules."
    ))
    cells.append(md("### RangeCleaner -- drops values outside a range"))
    cells.append(code(
        "class RangeCleaner(BaseCleaner):\n"
        "    \"\"\"Drop rows where a numeric column is outside a range.\"\"\"\n"
        "\n"
        "    def __init__(self, column, low, high):\n"
        "        super().__init__(\"range_\" + column)\n"
        "        self.column = column\n"
        "        self.low = low\n"
        "        self.high = high\n"
        "\n"
        "    def check(self, row):\n"
        "        val = row.get(self.column)\n"
        "        if isinstance(val, (int, float)):\n"
        "            if val < self.low or val > self.high:\n"
        "                return \"out_of_range_\" + self.column\n"
        "        return None\n"
        "\n"
        "\n"
        "rc = RangeCleaner(\"value\", 0, 100)\n"
        "result = rc.clean(sample_data)\n"
        "rc.report()\n"
        "print(\"Kept values:\", result.get_column(\"value\"))"
    ))
    cells.append(expected_output(
        "Cleaner: range_value\n"
        "  Checked: 7\n"
        "  Dropped: 2\n"
        "    - out_of_range_value: 2\n"
        "Kept values: [25.0, 30.0, 88.0, None, 42.0]"
    ))

    cells.append(md("### MissingCleaner -- drops rows with None or empty strings"))
    cells.append(code(
        "class MissingCleaner(BaseCleaner):\n"
        "    \"\"\"Drop rows with missing values in specified columns.\"\"\"\n"
        "\n"
        "    def __init__(self, columns):\n"
        "        super().__init__(\"missing\")\n"
        "        self.columns = columns\n"
        "\n"
        "    def check(self, row):\n"
        "        for col in self.columns:\n"
        "            val = row.get(col)\n"
        "            if val is None:\n"
        "                return \"missing_\" + col\n"
        "            if isinstance(val, str) and val.strip() == \"\":\n"
        "                return \"empty_\" + col\n"
        "        return None\n"
        "\n"
        "\n"
        "mc = MissingCleaner([\"value\", \"status\"])\n"
        "result = mc.clean(sample_data)\n"
        "mc.report()\n"
        "print(\"Kept:\", len(result), \"rows\")"
    ))
    cells.append(expected_output(
        "Cleaner: missing\n"
        "  Checked: 7\n"
        "  Dropped: 2\n"
        "    - missing_value: 1\n"
        "    - empty_status: 1\n"
        "Kept: 5 rows"
    ))

    # Section 3: Composing Cleaners
    cells.append(md(
        "---\n## Section 3: Composing Cleaners\n\n"
        "The power of this design is that you can **chain** multiple "
        "cleaners. Each one applies its own rule. The output of one "
        "becomes the input of the next."
    ))
    cells.append(code(
        "class CleaningPipeline:\n"
        "    \"\"\"Applies multiple cleaners in sequence.\"\"\"\n"
        "\n"
        "    def __init__(self, cleaners=None):\n"
        "        self.cleaners = cleaners or []\n"
        "\n"
        "    def add(self, cleaner):\n"
        "        self.cleaners.append(cleaner)\n"
        "        return self  # allows chaining: pipeline.add(a).add(b)\n"
        "\n"
        "    def clean(self, dataset):\n"
        "        \"\"\"Apply all cleaners in sequence.\"\"\"\n"
        "        current = dataset\n"
        "        for cleaner in self.cleaners:\n"
        "            current = cleaner.clean(current)\n"
        "        return current\n"
        "\n"
        "    def report(self):\n"
        "        \"\"\"Print reports for all cleaners.\"\"\"\n"
        "        total_dropped = 0\n"
        "        for c in self.cleaners:\n"
        "            c.report()\n"
        "            total_dropped += c.n_dropped\n"
        "        print(\"Total dropped: \" + str(total_dropped))\n"
        "\n"
        "\n"
        "# Build the pipeline\n"
        "pipeline = CleaningPipeline()\n"
        "pipeline.add(MissingCleaner([\"value\", \"status\"]))\n"
        "pipeline.add(RangeCleaner(\"value\", 0, 100))\n"
        "\n"
        "# Run it\n"
        "print(\"Input:\", sample_data)\n"
        "clean = pipeline.clean(sample_data)\n"
        "print(\"Output:\", clean)\n"
        "print(\"Clean values:\", clean.get_column(\"value\"))\n"
        "print()\n"
        "pipeline.report()"
    ))
    cells.append(expected_output(
        "Input: Dataset(7 rows)\n"
        "Output: Dataset(3 rows)\n"
        "Clean values: [25.0, 30.0, 88.0]\n\n"
        "Cleaner: missing\n"
        "  Checked: 7\n"
        "  Dropped: 2\n"
        "    - missing_value: 1\n"
        "    - empty_status: 1\n"
        "Cleaner: range_value\n"
        "  Checked: 5\n"
        "  Dropped: 2\n"
        "    - out_of_range_value: 2\n"
        "Total dropped: 4"
    ))

    cells.append(ascii_diagram(
        "Cleaner Class Hierarchy",
        "    +------------------+\n"
        "    |   BaseCleaner    |\n"
        "    +------------------+\n"
        "    | - name           |\n"
        "    | - drop_reasons   |\n"
        "    +------------------+\n"
        "    | + clean(dataset) |\n"
        "    | + check(row)     |  <-- override this\n"
        "    | + report()       |\n"
        "    +------------------+\n"
        "         /          \\\\\n"
        "        /            \\\\\n"
        "+---------------+  +------------------+\n"
        "| RangeCleaner  |  | MissingCleaner   |\n"
        "+---------------+  +------------------+\n"
        "| - column      |  | - columns        |\n"
        "| - low, high   |  +------------------+\n"
        "+---------------+  | + check(row)     |\n"
        "| + check(row)  |  +------------------+\n"
        "+---------------+"
    ))

    # Try It
    cells.extend(try_it(
        "Create a `StatusCleaner(BaseCleaner)` that drops rows where "
        "`status` is `\"error\"`. Then add it to the pipeline and run again."
    ))

    # Common Mistake
    cells.extend(common_mistake(
        "Forgetting super().__init__() in subclass",
        (
            "class BrokenCleaner(BaseCleaner):\n"
            "    def __init__(self, threshold):\n"
            "        # BUG: forgot super().__init__()!\n"
            "        self.threshold = threshold\n"
            "\n"
            "bc = BrokenCleaner(50)\n"
            "try:\n"
            "    bc.clean(sample_data)\n"
            "except AttributeError as e:\n"
            "    print(\"ERROR:\", e)"
        ),
        (
            "class FixedCleaner(BaseCleaner):\n"
            "    def __init__(self, threshold):\n"
            "        super().__init__(\"threshold\")  # FIXED!\n"
            "        self.threshold = threshold\n"
            "\n"
            "fc = FixedCleaner(50)\n"
            "result = fc.clean(sample_data)\n"
            "print(\"Works! Kept\", len(result), \"rows\")"
        ),
        "`super().__init__()` calls the parent class constructor. Without it, "
        "the BaseCleaner attributes (`name`, `drop_reasons`, etc.) are never "
        "created, causing AttributeError when `clean()` tries to use them."
    ))

    cells.append(md("---\n## Mini-Quiz"))
    cells.append(code(
        "# Q1: What does the BaseCleaner.check() method return for valid rows?\n"
        "# Answer: \n"
        "\n"
        "# Q2: Why do we use super().__init__() in subclass constructors?\n"
        "# Answer: \n"
        "\n"
        "# Q3: What is the Template Method pattern?\n"
        "# Answer: \n"
        "\n"
        "# Q4: What advantage does a CleaningPipeline have over one big cleaner?\n"
        "# Answer: "
    ))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# WEEK 4: Analyzer Component
# ============================================================
def week04_core():
    cells = []
    cells.append(md(
        "# OOP Week 4 -- Analyzer Component\n\n"
        "**Course:** Object-Oriented Programming (Year 2)\n"
        "**Session:** 3 hours\n"
        "**Prerequisites:** Weeks 1-3\n"
        "**Focus:** analysis as an object, stable results schema, "
        "composable analyzers\n\n"
        "---\n\n"
        "## Learning Objectives\n\n"
        "1. Build an Analyzer class with a stable output schema\n"
        "2. Understand why analysis results should follow a fixed structure\n"
        "3. Create multiple analyzer types (mean, std, event detection)\n"
        "4. Compose analyzers to produce a combined report\n"
        "5. Add threshold-based event detection"
    ))
    cells.append(setup_cell())

    # Dataset setup
    cells.append(md("---\n## Setup: Dataset from previous weeks"))
    cells.append(code(
        "class Dataset:\n"
        "    def __init__(self, rows, source_path=\"unknown\"):\n"
        "        self.rows = rows\n"
        "        self.source_path = source_path\n"
        "        self.n_rows = len(rows)\n"
        "        self.columns = list(rows[0].keys()) if rows else []\n"
        "    def get_column(self, name):\n"
        "        return [row.get(name) for row in self.rows]\n"
        "    def __len__(self):\n"
        "        return self.n_rows\n"
        "    def __str__(self):\n"
        "        return \"Dataset(\" + str(self.n_rows) + \" rows)\"\n"
        "\n"
        "# Clean sample data\n"
        "clean_data = Dataset([\n"
        "    {\"id\": 1, \"value\": 25.0, \"status\": \"ok\"},\n"
        "    {\"id\": 2, \"value\": 30.0, \"status\": \"ok\"},\n"
        "    {\"id\": 3, \"value\": 88.0, \"status\": \"warning\"},\n"
        "    {\"id\": 4, \"value\": 42.0, \"status\": \"ok\"},\n"
        "    {\"id\": 5, \"value\": 67.0, \"status\": \"ok\"},\n"
        "    {\"id\": 6, \"value\": 15.0, \"status\": \"ok\"},\n"
        "], \"sensors.csv\")\n"
        "print(\"Clean data:\", clean_data)"
    ))
    cells.append(expected_output("Clean data: Dataset(6 rows)"))

    # Section 1: Why wrap analysis in a class?
    cells.append(md(
        "---\n## Section 1: Why Wrap Analysis in a Class?\n\n"
        "In your v2 pipeline, analysis was probably a function that returned "
        "a dictionary. That works, but:\n\n"
        "1. **No guaranteed structure** -- different functions return "
        "different keys\n"
        "2. **No metadata** -- when was the analysis run? On what data?\n"
        "3. **No composition** -- hard to combine multiple analyses\n"
        "4. **No state** -- cannot inspect what happened after the fact\n\n"
        "An Analyzer class solves all of these."
    ))

    cells.extend(procedural_vs_oop(
        "Data Analysis",
        (
            "# PROCEDURAL\n"
            "def analyze_mean(data, column):\n"
            "    vals = [r[column] for r in data if isinstance(r.get(column), (int, float))]\n"
            "    return {\"mean\": sum(vals) / len(vals)} if vals else {}\n"
            "\n"
            "def analyze_std(data, column):\n"
            "    vals = [r[column] for r in data if isinstance(r.get(column), (int, float))]\n"
            "    if not vals:\n"
            "        return {}\n"
            "    m = sum(vals) / len(vals)\n"
            "    return {\"std\": (sum((x-m)**2 for x in vals) / len(vals)) ** 0.5}\n"
            "\n"
            "# Different functions, different return shapes, no guarantees\n"
            "r1 = analyze_mean([{\"value\": 10}, {\"value\": 20}], \"value\")\n"
            "r2 = analyze_std([{\"value\": 10}, {\"value\": 20}], \"value\")\n"
            "print(r1, r2)"
        ),
        (
            "# OOP -- consistent interface\n"
            "# (defined below)\n"
            "print(\"All analyzers will have: .analyze(dataset) -> dict\")\n"
            "print(\"All results will have: column, count, result keys\")"
        ),
        "With OOP, every analyzer follows the same interface: call "
        "`.analyze(dataset)` and get back a dictionary with a guaranteed "
        "structure. This makes it easy to combine, test, and swap analyzers."
    ))

    # Section 2: Building the Analyzer
    cells.append(md("---\n## Section 2: The Analyzer Class"))
    cells.append(code(
        "class Analyzer:\n"
        "    \"\"\"Analyzes a Dataset and produces structured results.\"\"\"\n"
        "\n"
        "    def __init__(self, config):\n"
        "        self.config = config\n"
        "        self.results = {}\n"
        "\n"
        "    def analyze(self, dataset):\n"
        "        \"\"\"Run analysis and return results dict.\"\"\"\n"
        "        col = self.config.get(\"value_column\", \"value\")\n"
        "        values = []\n"
        "        for row in dataset.rows:\n"
        "            val = row.get(col)\n"
        "            if isinstance(val, (int, float)):\n"
        "                values.append(val)\n"
        "\n"
        "        if not values:\n"
        "            self.results = {\"analysis_summary\": {\"count\": 0}}\n"
        "            return self.results\n"
        "\n"
        "        n = len(values)\n"
        "        mean_val = sum(values) / n\n"
        "        sorted_vals = sorted(values)\n"
        "        median_val = sorted_vals[n // 2]\n"
        "        variance = sum((x - mean_val) ** 2 for x in values) / n\n"
        "        std_val = variance ** 0.5\n"
        "\n"
        "        self.results = {\n"
        "            \"analysis_summary\": {\n"
        "                \"column\": col,\n"
        "                \"count\": n,\n"
        "                \"mean\": round(mean_val, 4),\n"
        "                \"median\": round(median_val, 4),\n"
        "                \"std\": round(std_val, 4),\n"
        "                \"min\": round(min(values), 4),\n"
        "                \"max\": round(max(values), 4),\n"
        "            }\n"
        "        }\n"
        "\n"
        "        # Optional: event detection\n"
        "        threshold = self.config.get(\"threshold\")\n"
        "        if threshold is not None:\n"
        "            events = sum(1 for v in values if v > threshold)\n"
        "            self.results[\"analysis_summary\"][\"events_above_threshold\"] = events\n"
        "            self.results[\"analysis_summary\"][\"threshold\"] = threshold\n"
        "\n"
        "        return self.results\n"
        "\n"
        "\n"
        "# Test\n"
        "analyzer = Analyzer({\"value_column\": \"value\", \"threshold\": 50})\n"
        "results = analyzer.analyze(clean_data)\n"
        "\n"
        "import json\n"
        "print(json.dumps(results, indent=2))"
    ))
    cells.append(expected_output(
        "{\n"
        "  \"analysis_summary\": {\n"
        "    \"column\": \"value\",\n"
        "    \"count\": 6,\n"
        "    \"mean\": 44.5,\n"
        "    \"median\": 42.0,\n"
        "    \"std\": 25.1330,\n"
        "    \"min\": 15.0,\n"
        "    \"max\": 88.0,\n"
        "    \"events_above_threshold\": 2,\n"
        "    \"threshold\": 50\n"
        "  }\n"
        "}"
    ))

    # Section 3: Composable Analyzers
    cells.append(md(
        "---\n## Section 3: Composable Analyzers\n\n"
        "Like cleaners, we can create specialized analyzers and combine them."
    ))
    cells.append(code(
        "class AnalyzerBase:\n"
        "    \"\"\"Base class for all analyzers.\"\"\"\n"
        "    def analyze(self, values):\n"
        "        raise NotImplementedError(\"Subclasses must implement analyze()\")\n"
        "\n"
        "class MeanAnalyzer(AnalyzerBase):\n"
        "    def analyze(self, values):\n"
        "        if not values:\n"
        "            return {}\n"
        "        return {\"mean\": round(sum(values) / len(values), 4)}\n"
        "\n"
        "class StdAnalyzer(AnalyzerBase):\n"
        "    def analyze(self, values):\n"
        "        if not values:\n"
        "            return {}\n"
        "        m = sum(values) / len(values)\n"
        "        var = sum((x - m) ** 2 for x in values) / len(values)\n"
        "        return {\"std\": round(var ** 0.5, 4)}\n"
        "\n"
        "class EventAnalyzer(AnalyzerBase):\n"
        "    def __init__(self, threshold):\n"
        "        self.threshold = threshold\n"
        "    def analyze(self, values):\n"
        "        events = sum(1 for v in values if v > self.threshold)\n"
        "        return {\"events_above\": events, \"threshold\": self.threshold}\n"
        "\n"
        "class RangeAnalyzer(AnalyzerBase):\n"
        "    def analyze(self, values):\n"
        "        if not values:\n"
        "            return {}\n"
        "        return {\"min\": min(values), \"max\": max(values), \"range\": max(values) - min(values)}\n"
        "\n"
        "\n"
        "# Compose and run all\n"
        "values = clean_data.get_column(\"value\")\n"
        "values = [v for v in values if isinstance(v, (int, float))]\n"
        "\n"
        "analyzers = [\n"
        "    MeanAnalyzer(),\n"
        "    StdAnalyzer(),\n"
        "    EventAnalyzer(threshold=50),\n"
        "    RangeAnalyzer(),\n"
        "]\n"
        "\n"
        "combined = {}\n"
        "for a in analyzers:\n"
        "    result = a.analyze(values)\n"
        "    combined.update(result)\n"
        "    print(type(a).__name__ + \":\", result)\n"
        "\n"
        "print()\n"
        "print(\"Combined:\", combined)"
    ))
    cells.append(expected_output(
        "MeanAnalyzer: {'mean': 44.5}\n"
        "StdAnalyzer: {'std': 25.133}\n"
        "EventAnalyzer: {'events_above': 2, 'threshold': 50}\n"
        "RangeAnalyzer: {'min': 15.0, 'max': 88.0, 'range': 73.0}\n\n"
        "Combined: {'mean': 44.5, 'std': 25.133, 'events_above': 2, "
        "'threshold': 50, 'min': 15.0, 'max': 88.0, 'range': 73.0}"
    ))

    cells.append(design_decision(
        "Stable Results Schema",
        "Notice that every analyzer returns a dictionary with predictable keys. "
        "This is crucial because:\n\n"
        "1. **The Reporter** can always find the data it needs\n"
        "2. **Tests** can assert specific keys exist\n"
        "3. **New analyzers** can be added without breaking existing code\n"
        "4. **JSON export** just works\n\n"
        "A stable schema is a **contract** between components. Break it and "
        "everything downstream breaks."
    ))

    cells.extend(try_it(
        "Create a `PercentileAnalyzer(AnalyzerBase)` that computes the "
        "25th, 50th, and 75th percentiles. Add it to the list and run again."
    ))

    cells.extend(common_mistake(
        "Not handling empty input",
        (
            "class BadAnalyzer:\n"
            "    def analyze(self, values):\n"
            "        # BUG: crashes on empty list!\n"
            "        return {\"mean\": sum(values) / len(values)}\n"
            "\n"
            "try:\n"
            "    BadAnalyzer().analyze([])\n"
            "except ZeroDivisionError as e:\n"
            "    print(\"ERROR:\", e)"
        ),
        (
            "class SafeAnalyzer:\n"
            "    def analyze(self, values):\n"
            "        if not values:          # FIXED: guard clause\n"
            "            return {\"mean\": 0}  # or return {}\n"
            "        return {\"mean\": sum(values) / len(values)}\n"
            "\n"
            "print(SafeAnalyzer().analyze([]))  # safe!\n"
            "print(SafeAnalyzer().analyze([10, 20]))  # normal case"
        ),
        "Always handle edge cases first (empty list, None, etc). "
        "This is called a **guard clause** pattern."
    ))

    cells.append(md("---\n## Mini-Quiz"))
    cells.append(code(
        "# Q1: Why do we wrap analysis in a class instead of a plain function?\n"
        "# Answer: \n"
        "\n"
        "# Q2: What does 'stable schema' mean?\n"
        "# Answer: \n"
        "\n"
        "# Q3: What does AnalyzerBase.analyze() raise if not overridden?\n"
        "# Answer: "
    ))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# WEEK 5: Plotter & Reporter
# ============================================================
def week05_core():
    cells = []
    cells.append(md(
        "# OOP Week 5 -- Plotter & Reporter Components\n\n"
        "**Course:** Object-Oriented Programming (Year 2)\n"
        "**Session:** 3 hours\n"
        "**Prerequisites:** Weeks 1-4\n"
        "**Focus:** component architecture, unified exports, "
        "visualization objects\n\n"
        "---\n\n"
        "## Learning Objectives\n\n"
        "1. Build a Plotter class that creates figures from analysis results\n"
        "2. Build a Reporter class that exports all outputs\n"
        "3. Understand the full component pipeline: Source -> Clean -> Analyze -> Plot -> Report\n"
        "4. Design classes that produce file outputs"
    ))
    cells.append(setup_cell())

    cells.append(md("---\n## Setup: Previous components"))
    cells.append(code(
        "import os, json\n"
        "\n"
        "class Dataset:\n"
        "    def __init__(self, rows, source_path=\"unknown\"):\n"
        "        self.rows = rows\n"
        "        self.source_path = source_path\n"
        "        self.n_rows = len(rows)\n"
        "        self.columns = list(rows[0].keys()) if rows else []\n"
        "    def get_column(self, name):\n"
        "        return [row.get(name) for row in self.rows]\n"
        "    def __len__(self):\n"
        "        return self.n_rows\n"
        "\n"
        "# Sample clean data and analysis results\n"
        "clean_data = Dataset([\n"
        "    {\"id\": i, \"value\": v, \"status\": \"ok\"}\n"
        "    for i, v in enumerate([25, 30, 88, 42, 67, 15, 55, 73, 38, 91], 1)\n"
        "], \"sensors.csv\")\n"
        "\n"
        "sample_results = {\n"
        "    \"analysis_summary\": {\n"
        "        \"column\": \"value\",\n"
        "        \"count\": 10,\n"
        "        \"mean\": 52.4,\n"
        "        \"std\": 25.5,\n"
        "        \"min\": 15.0,\n"
        "        \"max\": 91.0,\n"
        "    }\n"
        "}\n"
        "print(\"Setup complete. Clean data:\", len(clean_data), \"rows\")"
    ))
    cells.append(expected_output("Setup complete. Clean data: 10 rows"))

    # Section 1: Plotter
    cells.append(md(
        "---\n## Section 1: The Plotter Component\n\n"
        "The Plotter creates visualizations from analysis results. It:\n"
        "- Takes a Dataset and results dictionary as input\n"
        "- Creates matplotlib figures\n"
        "- Saves them to disk\n"
        "- Returns the list of created figures\n\n"
        "Note: If matplotlib is not available, the Plotter gracefully "
        "degrades (prints a message instead of crashing)."
    ))
    cells.append(code(
        "class Plotter:\n"
        "    \"\"\"Creates and saves figures from analysis results.\"\"\"\n"
        "\n"
        "    def __init__(self, config):\n"
        "        self.config = config\n"
        "        self.figures = []\n"
        "        self.saved_paths = []\n"
        "\n"
        "    def plot(self, dataset, results):\n"
        "        \"\"\"Create all required plots.\"\"\"\n"
        "        try:\n"
        "            import matplotlib\n"
        "            matplotlib.use(\"Agg\")\n"
        "            import matplotlib.pyplot as plt\n"
        "        except ImportError:\n"
        "            print(\"matplotlib not available -- skipping plots\")\n"
        "            return []\n"
        "\n"
        "        self.figures = []\n"
        "        self.saved_paths = []\n"
        "        fig_dir = self.config.get(\"figures_dir\", \"reports/figures\")\n"
        "        os.makedirs(fig_dir, exist_ok=True)\n"
        "\n"
        "        col = self.config.get(\"value_column\", \"value\")\n"
        "        values = dataset.get_column(col)\n"
        "        values = [v for v in values if isinstance(v, (int, float))]\n"
        "\n"
        "        if not values:\n"
        "            print(\"No numeric values to plot\")\n"
        "            return []\n"
        "\n"
        "        # Figure 1: Time series\n"
        "        fig1, ax = plt.subplots(figsize=(10, 4))\n"
        "        ax.plot(values, color=\"#2196F3\", linewidth=0.8, marker=\"o\", markersize=3)\n"
        "        title = self.config.get(\"project_name\", \"\") + \" -- Time Series\"\n"
        "        ax.set_title(title)\n"
        "        ax.set_xlabel(\"Index\")\n"
        "        ax.set_ylabel(col)\n"
        "        ax.grid(True, alpha=0.3)\n"
        "        path1 = os.path.join(fig_dir, \"timeseries.png\")\n"
        "        fig1.savefig(path1, dpi=100, bbox_inches=\"tight\")\n"
        "        self.figures.append(fig1)\n"
        "        self.saved_paths.append(path1)\n"
        "        plt.close(fig1)\n"
        "\n"
        "        # Figure 2: Histogram\n"
        "        fig2, ax = plt.subplots(figsize=(8, 4))\n"
        "        ax.hist(values, bins=20, color=\"#2196F3\", edgecolor=\"white\")\n"
        "        ax.set_title(\"Distribution of \" + col)\n"
        "        ax.set_xlabel(col)\n"
        "        ax.set_ylabel(\"Count\")\n"
        "        ax.grid(True, alpha=0.3)\n"
        "        path2 = os.path.join(fig_dir, \"histogram.png\")\n"
        "        fig2.savefig(path2, dpi=100, bbox_inches=\"tight\")\n"
        "        self.figures.append(fig2)\n"
        "        self.saved_paths.append(path2)\n"
        "        plt.close(fig2)\n"
        "\n"
        "        print(\"Created \" + str(len(self.figures)) + \" figures\")\n"
        "        for p in self.saved_paths:\n"
        "            print(\"  Saved: \" + p)\n"
        "        return self.figures\n"
        "\n"
        "\n"
        "# Test\n"
        "plotter = Plotter({\n"
        "    \"project_name\": \"SensorDemo\",\n"
        "    \"value_column\": \"value\",\n"
        "    \"figures_dir\": \"/tmp/oop_demo/figures\",\n"
        "})\n"
        "figs = plotter.plot(clean_data, sample_results)\n"
        "print(\"Figures created:\", len(figs))"
    ))
    cells.append(expected_output(
        "Created 2 figures\n"
        "  Saved: /tmp/oop_demo/figures/timeseries.png\n"
        "  Saved: /tmp/oop_demo/figures/histogram.png\n"
        "Figures created: 2"
    ))

    # Section 2: Reporter
    cells.append(md(
        "---\n## Section 2: The Reporter Component\n\n"
        "The Reporter is the final stage. It collects everything and "
        "exports it to the required formats (CSV, JSON, etc)."
    ))
    cells.append(code(
        "import csv\n"
        "\n"
        "class Reporter:\n"
        "    \"\"\"Generates and exports reports.\"\"\"\n"
        "\n"
        "    def __init__(self, config):\n"
        "        self.config = config\n"
        "        self.exported = {}\n"
        "\n"
        "    def export(self, dataset, results, figure_paths=None):\n"
        "        \"\"\"Export all outputs to configured paths.\"\"\"\n"
        "        self.exported = {}\n"
        "\n"
        "        # 1. Export cleaned CSV\n"
        "        csv_path = self.config.get(\"cleaned_data_path\", \"data/cleaned/cleaned.csv\")\n"
        "        os.makedirs(os.path.dirname(csv_path), exist_ok=True)\n"
        "        if dataset.rows:\n"
        "            cols = list(dataset.rows[0].keys())\n"
        "            with open(csv_path, \"w\", newline=\"\") as f:\n"
        "                w = csv.DictWriter(f, fieldnames=cols)\n"
        "                w.writeheader()\n"
        "                w.writerows(dataset.rows)\n"
        "            self.exported[\"cleaned_csv\"] = csv_path\n"
        "            print(\"Exported CSV: \" + csv_path)\n"
        "\n"
        "        # 2. Export report JSON\n"
        "        report_path = self.config.get(\"report_path\", \"reports/report.json\")\n"
        "        os.makedirs(os.path.dirname(report_path), exist_ok=True)\n"
        "        report = {\n"
        "            \"project_name\": self.config.get(\"project_name\"),\n"
        "            \"track\": self.config.get(\"track\"),\n"
        "            \"version\": \"v3\",\n"
        "            \"dataset\": {\"n_clean\": len(dataset)},\n"
        "            \"analysis_summary\": results.get(\"analysis_summary\", {}),\n"
        "            \"figures\": figure_paths or [],\n"
        "        }\n"
        "        with open(report_path, \"w\") as f:\n"
        "            json.dump(report, f, indent=2)\n"
        "        self.exported[\"report\"] = report_path\n"
        "        print(\"Exported report: \" + report_path)\n"
        "\n"
        "        print(\"Total exports: \" + str(len(self.exported)))\n"
        "        return self.exported\n"
        "\n"
        "\n"
        "# Test\n"
        "reporter = Reporter({\n"
        "    \"project_name\": \"SensorDemo\",\n"
        "    \"track\": \"robotics\",\n"
        "    \"cleaned_data_path\": \"/tmp/oop_demo/data/cleaned.csv\",\n"
        "    \"report_path\": \"/tmp/oop_demo/reports/report.json\",\n"
        "})\n"
        "exports = reporter.export(clean_data, sample_results, plotter.saved_paths)"
    ))
    cells.append(expected_output(
        "Exported CSV: /tmp/oop_demo/data/cleaned.csv\n"
        "Exported report: /tmp/oop_demo/reports/report.json\n"
        "Total exports: 2"
    ))

    # Full pipeline
    cells.append(md(
        "---\n## Section 3: The Full Pipeline\n\n"
        "Now let us see all 5 components working together. This is the "
        "architecture you will build over the next weeks."
    ))
    cells.append(ascii_diagram(
        "Full v3 Pipeline Architecture",
        "DataSource --> Dataset --> Cleaner --> Dataset --> Analyzer --> results\n"
        "                                                      |          |\n"
        "                                                      v          v\n"
        "                                                   Plotter   Reporter\n"
        "                                                      |          |\n"
        "                                                  figures/    reports/\n"
        "                                                   *.png     report.json\n"
        "                                                             cleaned.csv"
    ))

    cells.extend(try_it(
        "Add a third plot type to the Plotter: a box plot of the values. "
        "Hint: use `ax.boxplot(values)`."
    ))

    cells.append(md("---\n## Mini-Quiz"))
    cells.append(code(
        "# Q1: What are the 5 components of the v3 pipeline?\n"
        "# Answer: \n"
        "\n"
        "# Q2: Why does the Plotter use try/except for matplotlib?\n"
        "# Answer: \n"
        "\n"
        "# Q3: What files does the Reporter produce?\n"
        "# Answer: "
    ))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# WEEK 6: Domain Exceptions
# ============================================================
def week06_core():
    cells = []
    cells.append(md(
        "# OOP Week 6 -- Domain Exceptions & Validation\n\n"
        "**Course:** Object-Oriented Programming (Year 2)\n"
        "**Session:** 3 hours\n"
        "**Prerequisites:** Weeks 1-5\n"
        "**Focus:** custom exception hierarchy, validation flow, "
        "error messages that help\n\n"
        "---\n\n"
        "## Learning Objectives\n\n"
        "1. Explain why custom exceptions are better than generic ones\n"
        "2. Build an exception hierarchy for a data pipeline\n"
        "3. Add validation that raises informative exceptions\n"
        "4. Use try/except to handle exceptions gracefully\n"
        "5. Design exceptions that carry useful context"
    ))
    cells.append(setup_cell())

    cells.append(md(
        "---\n## Section 1: Why Custom Exceptions?\n\n"
        "In your v2 code, errors probably looked like:\n"
        "```python\n"
        "raise ValueError(\"bad data\")\n"
        "```\n\n"
        "This is unhelpful because:\n"
        "- **Which** data was bad? Which row? Which column?\n"
        "- **Why** was it bad? Missing? Out of range? Wrong type?\n"
        "- **What should the user do** about it?\n\n"
        "Custom exceptions solve all of these problems. They carry "
        "context-specific information and have descriptive names."
    ))

    cells.append(md("### Example: Generic vs Custom Exceptions"))
    cells.append(code(
        "# GENERIC (unhelpful)\n"
        "try:\n"
        "    raise ValueError(\"bad data\")\n"
        "except ValueError as e:\n"
        "    print(\"Generic:\", e)\n"
        "    # What data? What was bad? What do I do?\n"
        "\n"
        "print()\n"
        "\n"
        "# CUSTOM (informative)\n"
        "class SchemaError(Exception):\n"
        "    def __init__(self, missing_columns, actual_columns):\n"
        "        self.missing = missing_columns\n"
        "        self.actual = actual_columns\n"
        "        msg = (\"Schema mismatch: missing \" + str(missing_columns)\n"
        "               + \". Available: \" + str(actual_columns))\n"
        "        super().__init__(msg)\n"
        "\n"
        "try:\n"
        "    raise SchemaError([\"value\", \"timestamp\"], [\"id\", \"status\"])\n"
        "except SchemaError as e:\n"
        "    print(\"Custom:\", e)\n"
        "    print(\"Missing:\", e.missing)\n"
        "    print(\"Actual: \", e.actual)"
    ))
    cells.append(expected_output(
        "Generic: bad data\n\n"
        "Custom: Schema mismatch: missing ['value', 'timestamp']. "
        "Available: ['id', 'status']\n"
        "Missing: ['value', 'timestamp']\n"
        "Actual:  ['id', 'status']"
    ))

    # Section 2: Exception Hierarchy
    cells.append(md(
        "---\n## Section 2: Building an Exception Hierarchy\n\n"
        "We create a **base** exception for our pipeline, then specific "
        "exceptions for each type of error. This lets us catch all pipeline "
        "errors at once or handle specific ones."
    ))
    cells.append(ascii_diagram(
        "Exception Hierarchy",
        "Exception (built-in)\n"
        "  |\n"
        "  +-- PipelineError (our base)\n"
        "        |\n"
        "        +-- SchemaError (missing/wrong columns)\n"
        "        |\n"
        "        +-- CleaningError (too much data dropped)\n"
        "        |\n"
        "        +-- EmptyDataError (no data at a stage)\n"
        "        |\n"
        "        +-- ConfigError (bad configuration)"
    ))
    cells.append(code(
        "class PipelineError(Exception):\n"
        "    \"\"\"Base exception for all pipeline errors.\"\"\"\n"
        "    pass\n"
        "\n"
        "\n"
        "class SchemaError(PipelineError):\n"
        "    \"\"\"Data schema does not match expectations.\"\"\"\n"
        "    def __init__(self, missing_columns, actual_columns):\n"
        "        self.missing = missing_columns\n"
        "        self.actual = actual_columns\n"
        "        msg = (\"Schema mismatch: missing \" + str(missing_columns)\n"
        "               + \". Available: \" + str(actual_columns))\n"
        "        super().__init__(msg)\n"
        "\n"
        "\n"
        "class CleaningError(PipelineError):\n"
        "    \"\"\"Too many rows dropped during cleaning.\"\"\"\n"
        "    def __init__(self, n_raw, n_clean, threshold=0.5):\n"
        "        self.n_raw = n_raw\n"
        "        self.n_clean = n_clean\n"
        "        self.threshold = threshold\n"
        "        if n_raw > 0:\n"
        "            self.drop_rate = 1 - (n_clean / n_raw)\n"
        "        else:\n"
        "            self.drop_rate = 1.0\n"
        "        pct = str(round(self.drop_rate * 100)) + \"%\"\n"
        "        thr = str(round(threshold * 100)) + \"%\"\n"
        "        msg = (\"Cleaning dropped \" + pct + \" of data (\"\n"
        "               + str(n_raw) + \" -> \" + str(n_clean)\n"
        "               + \"). Threshold: \" + thr)\n"
        "        super().__init__(msg)\n"
        "\n"
        "\n"
        "class EmptyDataError(PipelineError):\n"
        "    \"\"\"Pipeline received empty data.\"\"\"\n"
        "    def __init__(self, stage):\n"
        "        self.stage = stage\n"
        "        super().__init__(\"Empty data at stage: \" + stage)\n"
        "\n"
        "\n"
        "class ConfigError(PipelineError):\n"
        "    \"\"\"Invalid configuration.\"\"\"\n"
        "    def __init__(self, key, message):\n"
        "        self.key = key\n"
        "        super().__init__(\"Config error [\" + key + \"]: \" + message)\n"
        "\n"
        "\n"
        "print(\"Exception hierarchy defined!\")\n"
        "print(\"All inherit from PipelineError -> Exception\")"
    ))
    cells.append(expected_output(
        "Exception hierarchy defined!\n"
        "All inherit from PipelineError -> Exception"
    ))

    # Section 3: Using Exceptions
    cells.append(md("---\n## Section 3: Using Custom Exceptions"))
    cells.append(code(
        "def validate_and_clean(data, config):\n"
        "    \"\"\"Full validation pipeline with custom exceptions.\"\"\"\n"
        "\n"
        "    # 1. Check for empty data\n"
        "    if not data:\n"
        "        raise EmptyDataError(\"load\")\n"
        "\n"
        "    # 2. Check schema\n"
        "    required = config.get(\"required_columns\", [])\n"
        "    actual = list(data[0].keys())\n"
        "    missing = set(required) - set(actual)\n"
        "    if missing:\n"
        "        raise SchemaError(list(missing), actual)\n"
        "\n"
        "    # 3. Clean\n"
        "    cleaned = [r for r in data if r.get(\"value\") is not None]\n"
        "\n"
        "    # 4. Check drop rate\n"
        "    if len(data) > 0 and len(cleaned) < len(data) * 0.5:\n"
        "        raise CleaningError(len(data), len(cleaned))\n"
        "\n"
        "    return cleaned\n"
        "\n"
        "\n"
        "# Test 1: Empty data\n"
        "try:\n"
        "    validate_and_clean([], {})\n"
        "except EmptyDataError as e:\n"
        "    print(\"Caught EmptyDataError:\", e)\n"
        "\n"
        "# Test 2: Schema mismatch\n"
        "try:\n"
        "    validate_and_clean([{\"a\": 1}], {\"required_columns\": [\"value\"]})\n"
        "except SchemaError as e:\n"
        "    print(\"Caught SchemaError:\", e)\n"
        "\n"
        "# Test 3: Too much dropped\n"
        "try:\n"
        "    data = [{\"value\": None}] * 8 + [{\"value\": 10}] * 2\n"
        "    validate_and_clean(data, {})\n"
        "except CleaningError as e:\n"
        "    print(\"Caught CleaningError:\", e)\n"
        "\n"
        "# Test 4: Catch ALL pipeline errors\n"
        "try:\n"
        "    validate_and_clean([], {})\n"
        "except PipelineError as e:\n"
        "    print(\"Caught PipelineError (catches all subtypes):\", type(e).__name__)"
    ))
    cells.append(expected_output(
        "Caught EmptyDataError: Empty data at stage: load\n"
        "Caught SchemaError: Schema mismatch: missing ['value']. Available: ['a']\n"
        "Caught CleaningError: Cleaning dropped 80% of data (10 -> 2). Threshold: 50%\n"
        "Caught PipelineError (catches all subtypes): EmptyDataError"
    ))

    cells.append(design_decision(
        "When to raise vs when to handle",
        "**Raise** an exception when:\n"
        "- The error makes it impossible to continue\n"
        "- The caller needs to know something went wrong\n"
        "- You want to prevent bad data from propagating silently\n\n"
        "**Handle** (try/except) when:\n"
        "- You can recover from the error\n"
        "- You want to log it and continue\n"
        "- You are at the 'top level' and need to show the user a message\n\n"
        "**Rule of thumb:** Low-level components RAISE. High-level "
        "orchestrators HANDLE."
    ))

    cells.extend(common_mistake(
        "Catching too broadly",
        (
            "# BAD: catches EVERYTHING, including bugs!\n"
            "try:\n"
            "    result = 1 / 0  # this is a bug, not a data error\n"
            "except Exception:\n"
            "    print(\"Something went wrong\")  # hides the real problem!"
        ),
        (
            "# GOOD: catch only what you expect\n"
            "try:\n"
            "    validate_and_clean([], {})\n"
            "except PipelineError as e:\n"
            "    print(\"Data error:\", e)  # only catches our errors\n"
            "# ZeroDivisionError would still crash (good! it's a bug)"
        ),
        "Catching `Exception` hides bugs. Only catch specific exceptions "
        "that you know how to handle. Let unexpected errors crash -- they "
        "reveal bugs that need fixing."
    ))

    cells.extend(try_it(
        "Add a `ConfigError` validation: before running the pipeline, check "
        "that the config has a `value_column` key. Raise `ConfigError` if missing."
    ))

    cells.append(md("---\n## Mini-Quiz"))
    cells.append(code(
        "# Q1: Why is raise ValueError('bad') worse than raise SchemaError(...)?\n"
        "# Answer: \n"
        "\n"
        "# Q2: What does 'except PipelineError' catch?\n"
        "# Answer: \n"
        "\n"
        "# Q3: When should you raise vs handle an exception?\n"
        "# Answer: "
    ))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# WEEK 7: SOLID -- SRP & OCP
# ============================================================
def week07_core():
    cells = []
    cells.append(md(
        "# OOP Week 7 -- SOLID Principles: SRP & OCP\n\n"
        "**Course:** Object-Oriented Programming (Year 2)\n"
        "**Session:** 3 hours\n"
        "**Prerequisites:** Weeks 1-6\n"
        "**Focus:** Single Responsibility Principle, Open/Closed Principle\n\n"
        "---\n\n"
        "## Learning Objectives\n\n"
        "1. State the Single Responsibility Principle (SRP) in your own words\n"
        "2. Identify SRP violations and refactor them\n"
        "3. State the Open/Closed Principle (OCP)\n"
        "4. Design classes that can be extended without modification\n"
        "5. Recognize these principles in the pipeline architecture"
    ))
    cells.append(setup_cell())

    # SRP
    cells.append(md(
        "---\n## Section 1: Single Responsibility Principle (SRP)\n\n"
        "**\"A class should have one, and only one, reason to change.\"**\n"
        "-- Robert C. Martin\n\n"
        "In plain English: **each class should do ONE job**.\n\n"
        "### The Restaurant Analogy\n\n"
        "Imagine a restaurant where one person is the chef, the waiter, "
        "the cashier, AND the dishwasher. If you need to change how "
        "dishes are washed, you have to modify the same person who cooks. "
        "That is fragile and confusing.\n\n"
        "Better: separate roles. The Chef cooks. The Waiter serves. "
        "The Cashier handles payments. Change one without affecting others."
    ))

    cells.append(md("### SRP Violation: The God Class"))
    cells.append(code(
        "# BAD: One class does EVERYTHING\n"
        "class GodPipeline:\n"
        "    def __init__(self, path, config):\n"
        "        self.path = path\n"
        "        self.config = config\n"
        "\n"
        "    def load(self):\n"
        "        self.data = [{\"value\": 25}, {\"value\": -5}, {\"value\": 30}]\n"
        "        print(\"Loaded\")\n"
        "\n"
        "    def clean(self):\n"
        "        self.data = [r for r in self.data if r.get(\"value\", 0) >= 0]\n"
        "        print(\"Cleaned\")\n"
        "\n"
        "    def analyze(self):\n"
        "        vals = [r[\"value\"] for r in self.data]\n"
        "        self.results = {\"mean\": sum(vals) / len(vals)}\n"
        "        print(\"Analyzed\")\n"
        "\n"
        "    def plot(self):\n"
        "        print(\"Plotted\")\n"
        "\n"
        "    def export(self):\n"
        "        print(\"Exported\")\n"
        "\n"
        "    def send_email(self):     # NOT its job!\n"
        "        print(\"Email sent\")\n"
        "\n"
        "    def backup_database(self):  # DEFINITELY not its job!\n"
        "        print(\"Database backed up\")\n"
        "\n"
        "\n"
        "# Problems:\n"
        "print(\"GodPipeline has 7 reasons to change!\")\n"
        "print(\"Change email format? Modify GodPipeline.\")\n"
        "print(\"Change analysis? Modify GodPipeline.\")\n"
        "print(\"Change plotting? Modify GodPipeline.\")\n"
        "print(\"Everything is tangled together.\")"
    ))
    cells.append(expected_output(
        "GodPipeline has 7 reasons to change!\n"
        "Change email format? Modify GodPipeline.\n"
        "Change analysis? Modify GodPipeline.\n"
        "Change plotting? Modify GodPipeline.\n"
        "Everything is tangled together."
    ))

    cells.append(md("### SRP Applied: Separate Components"))
    cells.append(code(
        "# GOOD: Each class has ONE responsibility\n"
        "\n"
        "class DataLoader:\n"
        "    \"\"\"ONLY loads data.\"\"\"\n"
        "    def load(self, path):\n"
        "        return [{\"value\": 25}, {\"value\": -5}, {\"value\": 30}]\n"
        "\n"
        "class DataCleaner:\n"
        "    \"\"\"ONLY cleans data.\"\"\"\n"
        "    def clean(self, data):\n"
        "        return [r for r in data if r.get(\"value\", 0) >= 0]\n"
        "\n"
        "class DataAnalyzer:\n"
        "    \"\"\"ONLY analyzes data.\"\"\"\n"
        "    def analyze(self, data):\n"
        "        vals = [r[\"value\"] for r in data]\n"
        "        return {\"mean\": sum(vals) / len(vals)} if vals else {}\n"
        "\n"
        "class DataPlotter:\n"
        "    \"\"\"ONLY creates plots.\"\"\"\n"
        "    def plot(self, data, results):\n"
        "        print(\"Created plots\")\n"
        "\n"
        "class DataReporter:\n"
        "    \"\"\"ONLY exports reports.\"\"\"\n"
        "    def export(self, results):\n"
        "        print(\"Exported report\")\n"
        "\n"
        "\n"
        "# Compose them\n"
        "loader = DataLoader()\n"
        "cleaner = DataCleaner()\n"
        "analyzer = DataAnalyzer()\n"
        "\n"
        "raw = loader.load(\"data.csv\")\n"
        "clean = cleaner.clean(raw)\n"
        "results = analyzer.analyze(clean)\n"
        "\n"
        "print(\"Each class has exactly ONE job:\")\n"
        "print(\"  DataLoader -> loads\")\n"
        "print(\"  DataCleaner -> cleans\")\n"
        "print(\"  DataAnalyzer -> analyzes\")\n"
        "print(\"  DataPlotter -> plots\")\n"
        "print(\"  DataReporter -> exports\")\n"
        "print(\"Results:\", results)"
    ))
    cells.append(expected_output(
        "Each class has exactly ONE job:\n"
        "  DataLoader -> loads\n"
        "  DataCleaner -> cleans\n"
        "  DataAnalyzer -> analyzes\n"
        "  DataPlotter -> plots\n"
        "  DataReporter -> exports\n"
        "Results: {'mean': 27.5}"
    ))

    # OCP
    cells.append(md(
        "---\n## Section 2: Open/Closed Principle (OCP)\n\n"
        "**\"Software entities should be open for extension, but closed for "
        "modification.\"**\n\n"
        "In plain English: **add new behavior by writing NEW code, not by "
        "changing EXISTING code**.\n\n"
        "### The Plugin Analogy\n\n"
        "Your phone is 'closed' -- you do not modify the operating system. "
        "But it is 'open' -- you install new apps (plugins) that add "
        "functionality. The phone's core code never changes."
    ))

    cells.append(md("### OCP Violation: Changing Existing Code to Add Features"))
    cells.append(code(
        "# BAD: Must modify this function every time we add an analysis type\n"
        "def analyze_bad(values, analysis_type):\n"
        "    if analysis_type == \"mean\":\n"
        "        return sum(values) / len(values)\n"
        "    elif analysis_type == \"std\":\n"
        "        m = sum(values) / len(values)\n"
        "        return (sum((x-m)**2 for x in values) / len(values)) ** 0.5\n"
        "    # To add 'median', we must MODIFY this function!\n"
        "    # elif analysis_type == \"median\":\n"
        "    #     ...\n"
        "    else:\n"
        "        raise ValueError(\"Unknown: \" + analysis_type)\n"
        "\n"
        "print(\"mean:\", analyze_bad([10, 20, 30], \"mean\"))\n"
        "print(\"Problem: adding 'median' requires changing existing code!\")"
    ))
    cells.append(expected_output(
        "mean: 20.0\n"
        "Problem: adding 'median' requires changing existing code!"
    ))

    cells.append(md("### OCP Applied: Extend Without Modifying"))
    cells.append(code(
        "class AnalyzerBase:\n"
        "    \"\"\"Base analyzer -- extend by creating subclasses.\"\"\"\n"
        "    def analyze(self, values):\n"
        "        raise NotImplementedError\n"
        "\n"
        "class MeanAnalyzer(AnalyzerBase):\n"
        "    def analyze(self, values):\n"
        "        return {\"mean\": sum(values) / len(values)} if values else {}\n"
        "\n"
        "class StdAnalyzer(AnalyzerBase):\n"
        "    def analyze(self, values):\n"
        "        if not values:\n"
        "            return {}\n"
        "        m = sum(values) / len(values)\n"
        "        return {\"std\": (sum((x-m)**2 for x in values) / len(values)) ** 0.5}\n"
        "\n"
        "# NEW: Add median WITHOUT changing existing code!\n"
        "class MedianAnalyzer(AnalyzerBase):\n"
        "    def analyze(self, values):\n"
        "        if not values:\n"
        "            return {}\n"
        "        s = sorted(values)\n"
        "        n = len(s)\n"
        "        if n % 2 == 0:\n"
        "            return {\"median\": (s[n//2 - 1] + s[n//2]) / 2}\n"
        "        return {\"median\": s[n//2]}\n"
        "\n"
        "# NEW: Event detector WITHOUT changing existing code!\n"
        "class EventAnalyzer(AnalyzerBase):\n"
        "    def __init__(self, threshold):\n"
        "        self.threshold = threshold\n"
        "    def analyze(self, values):\n"
        "        events = sum(1 for v in values if v > self.threshold)\n"
        "        return {\"events_above\": events, \"threshold\": self.threshold}\n"
        "\n"
        "\n"
        "# Use them all\n"
        "values = [10, 25, 30, 55, 20, 45, 60]\n"
        "analyzers = [MeanAnalyzer(), StdAnalyzer(), MedianAnalyzer(), EventAnalyzer(40)]\n"
        "\n"
        "all_results = {}\n"
        "for a in analyzers:\n"
        "    result = a.analyze(values)\n"
        "    all_results.update(result)\n"
        "    print(type(a).__name__ + \":\", result)\n"
        "\n"
        "print()\n"
        "print(\"Added 2 new analyzers WITHOUT changing any existing code!\")"
    ))
    cells.append(expected_output(
        "MeanAnalyzer: {'mean': 35.0}\n"
        "StdAnalyzer: {'std': 16.583}\n"
        "MedianAnalyzer: {'median': 30}\n"
        "EventAnalyzer: {'events_above': 3, 'threshold': 40}\n\n"
        "Added 2 new analyzers WITHOUT changing any existing code!"
    ))

    cells.extend(try_it(
        "Create a `MinMaxAnalyzer(AnalyzerBase)` that returns "
        "`{\"min\": ..., \"max\": ..., \"range\": ...}`. Add it to the "
        "list and run again. Notice: you did NOT modify any existing class."
    ))

    cells.append(design_decision(
        "SRP + OCP = Composable Architecture",
        "These two principles work together:\n\n"
        "- **SRP** keeps each class small and focused\n"
        "- **OCP** lets you add features by creating new classes\n\n"
        "The result: a system made of small, independent parts that can "
        "be combined in new ways. This is exactly what our v3 pipeline "
        "architecture does."
    ))

    cells.append(md("---\n## Mini-Quiz"))
    cells.append(code(
        "# Q1: State SRP in one sentence.\n"
        "# Answer: \n"
        "\n"
        "# Q2: State OCP in one sentence.\n"
        "# Answer: \n"
        "\n"
        "# Q3: How does our pipeline satisfy SRP?\n"
        "# Answer: \n"
        "\n"
        "# Q4: How does our AnalyzerBase satisfy OCP?\n"
        "# Answer: "
    ))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# WEEK 8: Strategy Pattern
# ============================================================
def week08_core():
    cells = []
    cells.append(md(
        "# OOP Week 8 -- Strategy Pattern\n\n"
        "**Course:** Object-Oriented Programming (Year 2)\n"
        "**Session:** 3 hours\n"
        "**Prerequisites:** Weeks 1-7\n"
        "**Focus:** interchangeable algorithms, config-driven selection\n\n"
        "---\n\n"
        "## Learning Objectives\n\n"
        "1. Explain the Strategy Pattern and when to use it\n"
        "2. Implement strategies as interchangeable classes\n"
        "3. Select strategies at runtime based on configuration\n"
        "4. Compose multiple strategies\n"
        "5. Recognize Strategy in real-world software"
    ))
    cells.append(setup_cell())

    cells.append(md(
        "---\n## Section 1: What is the Strategy Pattern?\n\n"
        "The Strategy Pattern defines a **family of algorithms**, puts each "
        "one in a **separate class**, and makes them **interchangeable**.\n\n"
        "### The GPS Analogy\n\n"
        "Your GPS app has multiple routing strategies:\n"
        "- **Fastest Route** -- minimize time\n"
        "- **Shortest Route** -- minimize distance\n"
        "- **Scenic Route** -- prefer highways with nice views\n"
        "- **Avoid Tolls** -- find free roads\n\n"
        "All strategies have the same interface: they take a start and "
        "end point and return a route. You can swap them without changing "
        "the rest of the app.\n\n"
        "### In Our Pipeline\n\n"
        "We have already been using this pattern! Our cleaning strategies "
        "(RangeCleaner, MissingCleaner) and analyzer types (MeanAnalyzer, "
        "StdAnalyzer) are all strategies. Now we formalize the pattern."
    ))

    cells.append(md("---\n## Section 2: Cleaning Strategies"))
    cells.append(code(
        "class CleaningStrategy:\n"
        "    \"\"\"Base strategy for cleaning decisions.\"\"\"\n"
        "    def should_keep(self, row):\n"
        "        \"\"\"Return True to keep the row, False to drop it.\"\"\"\n"
        "        return True\n"
        "\n"
        "\n"
        "class DropMissing(CleaningStrategy):\n"
        "    \"\"\"Drop rows with missing values.\"\"\"\n"
        "    def __init__(self, columns):\n"
        "        self.columns = columns\n"
        "\n"
        "    def should_keep(self, row):\n"
        "        for col in self.columns:\n"
        "            val = row.get(col)\n"
        "            if val is None or (isinstance(val, str) and val.strip() == \"\"):\n"
        "                return False\n"
        "        return True\n"
        "\n"
        "\n"
        "class DropOutOfRange(CleaningStrategy):\n"
        "    \"\"\"Drop rows where a value is outside a range.\"\"\"\n"
        "    def __init__(self, column, low, high):\n"
        "        self.column = column\n"
        "        self.low = low\n"
        "        self.high = high\n"
        "\n"
        "    def should_keep(self, row):\n"
        "        val = row.get(self.column)\n"
        "        if isinstance(val, (int, float)):\n"
        "            return self.low <= val <= self.high\n"
        "        return True  # non-numeric: keep\n"
        "\n"
        "\n"
        "class DropDuplicates(CleaningStrategy):\n"
        "    \"\"\"Drop rows with duplicate values in a column.\"\"\"\n"
        "    def __init__(self, column):\n"
        "        self.column = column\n"
        "        self._seen = set()\n"
        "\n"
        "    def should_keep(self, row):\n"
        "        val = row.get(self.column)\n"
        "        if val in self._seen:\n"
        "            return False\n"
        "        self._seen.add(val)\n"
        "        return True\n"
        "\n"
        "\n"
        "print(\"Three strategies, same interface: should_keep(row) -> bool\")"
    ))
    cells.append(expected_output(
        "Three strategies, same interface: should_keep(row) -> bool"
    ))

    # ConfigurableCleaner
    cells.append(md("---\n## Section 3: The Configurable Cleaner"))
    cells.append(code(
        "class ConfigurableCleaner:\n"
        "    \"\"\"Cleaner that uses interchangeable strategies.\"\"\"\n"
        "\n"
        "    def __init__(self, strategies=None):\n"
        "        self.strategies = strategies or []\n"
        "        self.stats = {\"checked\": 0, \"kept\": 0, \"dropped\": 0}\n"
        "\n"
        "    def add_strategy(self, strategy):\n"
        "        \"\"\"Add a cleaning strategy.\"\"\"\n"
        "        self.strategies.append(strategy)\n"
        "        return self  # for chaining\n"
        "\n"
        "    def clean(self, data):\n"
        "        \"\"\"Apply all strategies. A row must pass ALL to be kept.\"\"\"\n"
        "        result = []\n"
        "        self.stats = {\"checked\": 0, \"kept\": 0, \"dropped\": 0}\n"
        "        for row in data:\n"
        "            self.stats[\"checked\"] += 1\n"
        "            if all(s.should_keep(row) for s in self.strategies):\n"
        "                result.append(row)\n"
        "                self.stats[\"kept\"] += 1\n"
        "            else:\n"
        "                self.stats[\"dropped\"] += 1\n"
        "        return result\n"
        "\n"
        "\n"
        "# Build from config\n"
        "data = [\n"
        "    {\"id\": 1, \"value\": 25},\n"
        "    {\"id\": 2, \"value\": None},\n"
        "    {\"id\": 3, \"value\": 200},\n"
        "    {\"id\": 4, \"value\": 50},\n"
        "    {\"id\": 5, \"value\": 50},   # duplicate value\n"
        "]\n"
        "\n"
        "cleaner = ConfigurableCleaner()\n"
        "cleaner.add_strategy(DropMissing([\"value\"]))\n"
        "cleaner.add_strategy(DropOutOfRange(\"value\", 0, 100))\n"
        "cleaner.add_strategy(DropDuplicates(\"value\"))\n"
        "\n"
        "clean = cleaner.clean(data)\n"
        "print(\"Results:\", clean)\n"
        "print(\"Stats:\", cleaner.stats)"
    ))
    cells.append(expected_output(
        "Results: [{'id': 1, 'value': 25}, {'id': 4, 'value': 50}]\n"
        "Stats: {'checked': 5, 'kept': 2, 'dropped': 3}"
    ))

    # Config-driven selection
    cells.append(md(
        "---\n## Section 4: Config-Driven Strategy Selection\n\n"
        "The real power: build the entire cleaning pipeline from a "
        "configuration dictionary. No code changes needed to add or "
        "remove strategies."
    ))
    cells.append(code(
        "STRATEGY_MAP = {\n"
        "    \"drop_missing\": lambda cfg: DropMissing(cfg[\"columns\"]),\n"
        "    \"drop_range\": lambda cfg: DropOutOfRange(cfg[\"column\"], cfg[\"low\"], cfg[\"high\"]),\n"
        "    \"drop_duplicates\": lambda cfg: DropDuplicates(cfg[\"column\"]),\n"
        "}\n"
        "\n"
        "def build_cleaner_from_config(config):\n"
        "    \"\"\"Build a ConfigurableCleaner from a config dict.\"\"\"\n"
        "    cleaner = ConfigurableCleaner()\n"
        "    for step in config.get(\"cleaning_steps\", []):\n"
        "        name = step[\"strategy\"]\n"
        "        if name not in STRATEGY_MAP:\n"
        "            raise ValueError(\"Unknown strategy: \" + name)\n"
        "        strategy = STRATEGY_MAP[name](step)\n"
        "        cleaner.add_strategy(strategy)\n"
        "        print(\"Added strategy: \" + name)\n"
        "    return cleaner\n"
        "\n"
        "\n"
        "# Config (could come from a YAML/JSON file)\n"
        "config = {\n"
        "    \"cleaning_steps\": [\n"
        "        {\"strategy\": \"drop_missing\", \"columns\": [\"value\"]},\n"
        "        {\"strategy\": \"drop_range\", \"column\": \"value\", \"low\": 0, \"high\": 100},\n"
        "    ]\n"
        "}\n"
        "\n"
        "cleaner = build_cleaner_from_config(config)\n"
        "result = cleaner.clean(data)\n"
        "print(\"Clean:\", result)"
    ))
    cells.append(expected_output(
        "Added strategy: drop_missing\n"
        "Added strategy: drop_range\n"
        "Clean: [{'id': 1, 'value': 25}, {'id': 4, 'value': 50}, "
        "{'id': 5, 'value': 50}]"
    ))

    cells.extend(try_it(
        "Create a new strategy `DropStatus(CleaningStrategy)` that drops "
        "rows where `status` equals a given value (e.g., 'error'). Add it "
        "to STRATEGY_MAP and build a cleaner that uses it."
    ))

    cells.append(md("---\n## Mini-Quiz"))
    cells.append(code(
        "# Q1: What is the Strategy Pattern?\n"
        "# Answer: \n"
        "\n"
        "# Q2: What method do all cleaning strategies share?\n"
        "# Answer: \n"
        "\n"
        "# Q3: What advantage does config-driven strategy selection give?\n"
        "# Answer: "
    ))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# WEEK 9: Factory & Registry
# ============================================================
def week09_core():
    cells = []
    cells.append(md(
        "# OOP Week 9 -- Factory & Registry Pattern\n\n"
        "**Course:** Object-Oriented Programming (Year 2)\n"
        "**Session:** 3 hours\n"
        "**Prerequisites:** Weeks 1-8\n"
        "**Focus:** creating objects from config, plugin architecture\n\n"
        "---\n\n"
        "## Learning Objectives\n\n"
        "1. Explain the Factory Pattern and when to use it\n"
        "2. Build a Registry that maps names to classes\n"
        "3. Create objects from configuration dictionaries\n"
        "4. Understand how this enables plugin architecture\n"
        "5. Register new components without modifying existing code"
    ))
    cells.append(setup_cell())

    cells.append(md(
        "---\n## Section 1: What is a Factory?\n\n"
        "A **Factory** is an object (or function) that **creates other "
        "objects**. Instead of using `ClassName(...)` directly, you ask "
        "the factory to build it for you.\n\n"
        "### The Pizza Analogy\n\n"
        "Instead of making pizza yourself, you tell the pizza shop: "
        "'I want a Margherita.' The shop (factory) knows how to make it. "
        "Tomorrow they can add a new pizza type without changing how you "
        "order.\n\n"
        "### In Our Pipeline\n\n"
        "We want to create analyzers from a config file:\n"
        "```json\n"
        "{\"analyzers\": [\"mean\", \"std\", {\"name\": \"events\", "
        "\"threshold\": 50}]}\n"
        "```\n"
        "The factory reads this config and creates the right objects."
    ))

    cells.append(md("### The AnalyzerBase (from previous weeks)"))
    cells.append(code(
        "class AnalyzerBase:\n"
        "    \"\"\"Base class for analyzers.\"\"\"\n"
        "    def analyze(self, values):\n"
        "        raise NotImplementedError\n"
        "\n"
        "class MeanAnalyzer(AnalyzerBase):\n"
        "    def analyze(self, values):\n"
        "        return {\"mean\": round(sum(values)/len(values), 4)} if values else {}\n"
        "\n"
        "class StdAnalyzer(AnalyzerBase):\n"
        "    def analyze(self, values):\n"
        "        if not values:\n"
        "            return {}\n"
        "        m = sum(values) / len(values)\n"
        "        return {\"std\": round((sum((x-m)**2 for x in values)/len(values))**0.5, 4)}\n"
        "\n"
        "class EventAnalyzer(AnalyzerBase):\n"
        "    def __init__(self, threshold=50):\n"
        "        self.threshold = threshold\n"
        "    def analyze(self, values):\n"
        "        return {\"events_above\": sum(1 for v in values if v > self.threshold)}\n"
        "\n"
        "print(\"Analyzer classes defined.\")"
    ))
    cells.append(expected_output("Analyzer classes defined."))

    # Section 2: The Registry
    cells.append(md("---\n## Section 2: The Registry Pattern"))
    cells.append(code(
        "class AnalyzerFactory:\n"
        "    \"\"\"Factory + Registry for creating analyzers from config.\"\"\"\n"
        "\n"
        "    _registry = {}\n"
        "\n"
        "    @classmethod\n"
        "    def register(cls, name, analyzer_class):\n"
        "        \"\"\"Register an analyzer class under a name.\"\"\"\n"
        "        cls._registry[name] = analyzer_class\n"
        "        print(\"Registered: \" + name + \" -> \" + analyzer_class.__name__)\n"
        "\n"
        "    @classmethod\n"
        "    def create(cls, name, **kwargs):\n"
        "        \"\"\"Create an analyzer by name.\"\"\"\n"
        "        if name not in cls._registry:\n"
        "            available = list(cls._registry.keys())\n"
        "            raise ValueError(\"Unknown analyzer: \" + name\n"
        "                           + \". Available: \" + str(available))\n"
        "        return cls._registry[name](**kwargs)\n"
        "\n"
        "    @classmethod\n"
        "    def list_available(cls):\n"
        "        \"\"\"List all registered analyzers.\"\"\"\n"
        "        return list(cls._registry.keys())\n"
        "\n"
        "\n"
        "# Register built-in analyzers\n"
        "AnalyzerFactory.register(\"mean\", MeanAnalyzer)\n"
        "AnalyzerFactory.register(\"std\", StdAnalyzer)\n"
        "AnalyzerFactory.register(\"events\", EventAnalyzer)\n"
        "\n"
        "print(\"Available:\", AnalyzerFactory.list_available())"
    ))
    cells.append(expected_output(
        "Registered: mean -> MeanAnalyzer\n"
        "Registered: std -> StdAnalyzer\n"
        "Registered: events -> EventAnalyzer\n"
        "Available: ['mean', 'std', 'events']"
    ))

    # Section 3: Creating from Config
    cells.append(md("---\n## Section 3: Creating Objects from Config"))
    cells.append(code(
        "# Config (could be loaded from JSON/YAML)\n"
        "config = {\n"
        "    \"analyzers\": [\n"
        "        {\"name\": \"mean\"},\n"
        "        {\"name\": \"std\"},\n"
        "        {\"name\": \"events\", \"params\": {\"threshold\": 40}},\n"
        "    ]\n"
        "}\n"
        "\n"
        "# Build analyzers from config\n"
        "analyzers = []\n"
        "for spec in config[\"analyzers\"]:\n"
        "    params = spec.get(\"params\", {})\n"
        "    a = AnalyzerFactory.create(spec[\"name\"], **params)\n"
        "    analyzers.append(a)\n"
        "    print(\"Created: \" + spec[\"name\"] + \" -> \" + type(a).__name__)\n"
        "\n"
        "# Run all\n"
        "values = [10, 25, 30, 55, 20, 45, 60]\n"
        "combined = {}\n"
        "for a in analyzers:\n"
        "    combined.update(a.analyze(values))\n"
        "\n"
        "print()\n"
        "print(\"Results:\", combined)"
    ))
    cells.append(expected_output(
        "Created: mean -> MeanAnalyzer\n"
        "Created: std -> StdAnalyzer\n"
        "Created: events -> EventAnalyzer\n\n"
        "Results: {'mean': 35.0, 'std': 16.5831, 'events_above': 3}"
    ))

    # Plugin architecture
    cells.append(md(
        "---\n## Section 4: Plugin Architecture\n\n"
        "The factory + registry enables a **plugin** architecture. Anyone "
        "can add new analyzers without modifying existing code -- just "
        "create a new class and register it."
    ))
    cells.append(code(
        "# A plugin: new analyzer, no changes to existing code!\n"
        "class PercentileAnalyzer(AnalyzerBase):\n"
        "    def __init__(self, percentiles=None):\n"
        "        self.percentiles = percentiles or [25, 50, 75]\n"
        "    def analyze(self, values):\n"
        "        if not values:\n"
        "            return {}\n"
        "        s = sorted(values)\n"
        "        n = len(s)\n"
        "        result = {}\n"
        "        for p in self.percentiles:\n"
        "            idx = min(int(n * p / 100), n - 1)\n"
        "            result[\"p\" + str(p)] = s[idx]\n"
        "        return result\n"
        "\n"
        "# One line to register!\n"
        "AnalyzerFactory.register(\"percentile\", PercentileAnalyzer)\n"
        "\n"
        "# Now it works with the existing pipeline\n"
        "p = AnalyzerFactory.create(\"percentile\", percentiles=[10, 50, 90])\n"
        "print(\"Percentile results:\", p.analyze(values))\n"
        "print()\n"
        "print(\"Available analyzers:\", AnalyzerFactory.list_available())"
    ))
    cells.append(expected_output(
        "Registered: percentile -> PercentileAnalyzer\n"
        "Percentile results: {'p10': 10, 'p50': 30, 'p90': 55}\n\n"
        "Available analyzers: ['mean', 'std', 'events', 'percentile']"
    ))

    cells.extend(try_it(
        "Create a `VarianceAnalyzer(AnalyzerBase)`, register it with the "
        "factory, then create it from config and run it."
    ))

    cells.append(md("---\n## Mini-Quiz"))
    cells.append(code(
        "# Q1: What is a Factory?\n"
        "# Answer: \n"
        "\n"
        "# Q2: What is a Registry?\n"
        "# Answer: \n"
        "\n"
        "# Q3: How does the factory enable plugin architecture?\n"
        "# Answer: "
    ))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# WEEK 10: Testing with pytest
# ============================================================
def week10_core():
    cells = []
    cells.append(md(
        "# OOP Week 10 -- Testing with pytest\n\n"
        "**Course:** Object-Oriented Programming (Year 2)\n"
        "**Session:** 3 hours\n"
        "**Prerequisites:** Weeks 1-9\n"
        "**Focus:** test organization, fixtures, parametrize, TDD\n\n"
        "---\n\n"
        "## Learning Objectives\n\n"
        "1. Write test functions using pytest conventions\n"
        "2. Use fixtures for shared test setup\n"
        "3. Use parametrize for testing multiple cases\n"
        "4. Organize tests by component\n"
        "5. Practice Test-Driven Development (TDD)"
    ))
    cells.append(setup_cell())

    # Setup classes
    cells.append(md("---\n## Setup: Classes to Test"))
    cells.append(code(
        "class CleaningStrategy:\n"
        "    def should_keep(self, row):\n"
        "        return True\n"
        "\n"
        "class DropMissing(CleaningStrategy):\n"
        "    def __init__(self, columns):\n"
        "        self.columns = columns\n"
        "    def should_keep(self, row):\n"
        "        for col in self.columns:\n"
        "            val = row.get(col)\n"
        "            if val is None or (isinstance(val, str) and val.strip() == \"\"):\n"
        "                return False\n"
        "        return True\n"
        "\n"
        "class DropOutOfRange(CleaningStrategy):\n"
        "    def __init__(self, column, low, high):\n"
        "        self.column = column\n"
        "        self.low = low\n"
        "        self.high = high\n"
        "    def should_keep(self, row):\n"
        "        val = row.get(self.column)\n"
        "        if isinstance(val, (int, float)):\n"
        "            return self.low <= val <= self.high\n"
        "        return True\n"
        "\n"
        "class ConfigurableCleaner:\n"
        "    def __init__(self, strategies=None):\n"
        "        self.strategies = strategies or []\n"
        "    def add_strategy(self, strategy):\n"
        "        self.strategies.append(strategy)\n"
        "    def clean(self, data):\n"
        "        return [row for row in data if all(s.should_keep(row) for s in self.strategies)]\n"
        "\n"
        "print(\"Classes ready for testing.\")"
    ))
    cells.append(expected_output("Classes ready for testing."))

    # Section 1: pytest basics
    cells.append(md(
        "---\n## Section 1: pytest Basics\n\n"
        "pytest is the standard Python testing framework. Key rules:\n\n"
        "1. Test files start with `test_` (e.g., `test_cleaner.py`)\n"
        "2. Test functions start with `test_` (e.g., `test_empty_input`)\n"
        "3. Use plain `assert` statements (no special methods)\n"
        "4. Run with `pytest tests/ -v`\n\n"
        "We will write tests in this notebook, then show how they would "
        "look in actual test files."
    ))
    cells.append(code(
        "# Test 1: Cleaner handles empty input\n"
        "def test_cleaner_empty_input():\n"
        "    cleaner = ConfigurableCleaner()\n"
        "    result = cleaner.clean([])\n"
        "    assert result == []\n"
        "    assert isinstance(result, list)\n"
        "\n"
        "# Test 2: DropMissing drops None values\n"
        "def test_drop_missing_none():\n"
        "    s = DropMissing([\"value\"])\n"
        "    assert s.should_keep({\"value\": 10}) == True\n"
        "    assert s.should_keep({\"value\": None}) == False\n"
        "\n"
        "# Test 3: DropOutOfRange works\n"
        "def test_drop_out_of_range():\n"
        "    s = DropOutOfRange(\"value\", 0, 100)\n"
        "    assert s.should_keep({\"value\": 50}) == True\n"
        "    assert s.should_keep({\"value\": -10}) == False\n"
        "    assert s.should_keep({\"value\": 200}) == False\n"
        "    assert s.should_keep({\"value\": 0}) == True    # edge: exactly at min\n"
        "    assert s.should_keep({\"value\": 100}) == True   # edge: exactly at max\n"
        "\n"
        "# Test 4: Full pipeline\n"
        "def test_full_cleaning():\n"
        "    cleaner = ConfigurableCleaner([\n"
        "        DropMissing([\"value\"]),\n"
        "        DropOutOfRange(\"value\", 0, 100)\n"
        "    ])\n"
        "    data = [\n"
        "        {\"value\": 50},\n"
        "        {\"value\": None},\n"
        "        {\"value\": 200},\n"
        "        {\"value\": 25},\n"
        "    ]\n"
        "    result = cleaner.clean(data)\n"
        "    assert len(result) == 2\n"
        "    assert result[0][\"value\"] == 50\n"
        "    assert result[1][\"value\"] == 25\n"
        "\n"
        "\n"
        "# Run tests\n"
        "test_cleaner_empty_input()\n"
        "print(\"[PASS] test_cleaner_empty_input\")\n"
        "test_drop_missing_none()\n"
        "print(\"[PASS] test_drop_missing_none\")\n"
        "test_drop_out_of_range()\n"
        "print(\"[PASS] test_drop_out_of_range\")\n"
        "test_full_cleaning()\n"
        "print(\"[PASS] test_full_cleaning\")\n"
        "print()\n"
        "print(\"All 4 tests passed!\")"
    ))
    cells.append(expected_output(
        "[PASS] test_cleaner_empty_input\n"
        "[PASS] test_drop_missing_none\n"
        "[PASS] test_drop_out_of_range\n"
        "[PASS] test_full_cleaning\n\n"
        "All 4 tests passed!"
    ))

    # Section 2: Fixtures
    cells.append(md(
        "---\n## Section 2: Fixtures (Shared Test Setup)\n\n"
        "A **fixture** is reusable setup code. In pytest, you use the "
        "`@pytest.fixture` decorator. In notebooks, we use plain functions."
    ))
    cells.append(code(
        "def make_sample_data():\n"
        "    \"\"\"Fixture: standard test dataset.\"\"\"\n"
        "    return [\n"
        "        {\"id\": 1, \"value\": 25.0, \"status\": \"ok\"},\n"
        "        {\"id\": 2, \"value\": 50.0, \"status\": \"ok\"},\n"
        "        {\"id\": 3, \"value\": None, \"status\": \"error\"},\n"
        "        {\"id\": 4, \"value\": 200.0, \"status\": \"warning\"},\n"
        "        {\"id\": 5, \"value\": 75.0, \"status\": \"ok\"},\n"
        "    ]\n"
        "\n"
        "def make_cleaner():\n"
        "    \"\"\"Fixture: standard cleaner.\"\"\"\n"
        "    return ConfigurableCleaner([\n"
        "        DropMissing([\"value\"]),\n"
        "        DropOutOfRange(\"value\", 0, 100),\n"
        "    ])\n"
        "\n"
        "\n"
        "def test_with_fixtures():\n"
        "    data = make_sample_data()\n"
        "    cleaner = make_cleaner()\n"
        "    result = cleaner.clean(data)\n"
        "    assert len(result) == 3  # ids 1, 2, 5\n"
        "    values = [r[\"value\"] for r in result]\n"
        "    assert all(0 <= v <= 100 for v in values)\n"
        "\n"
        "test_with_fixtures()\n"
        "print(\"[PASS] test_with_fixtures\")"
    ))
    cells.append(expected_output("[PASS] test_with_fixtures"))

    # Section 3: Parametrize
    cells.append(md(
        "---\n## Section 3: Parametrize (Testing Many Cases)\n\n"
        "Instead of writing one test per case, you can test many inputs "
        "with one function. In pytest, use `@pytest.mark.parametrize`. "
        "In notebooks, we use a loop."
    ))
    cells.append(code(
        "# In a real pytest file, you would write:\n"
        "# @pytest.mark.parametrize(\"value,expected\", [\n"
        "#     (50, True), (-10, False), (200, False), (0, True), (100, True)\n"
        "# ])\n"
        "# def test_range_check(value, expected):\n"
        "#     s = DropOutOfRange(\"value\", 0, 100)\n"
        "#     assert s.should_keep({\"value\": value}) == expected\n"
        "\n"
        "# In a notebook, we do it like this:\n"
        "test_cases = [\n"
        "    (50, True, \"middle of range\"),\n"
        "    (-10, False, \"below range\"),\n"
        "    (200, False, \"above range\"),\n"
        "    (0, True, \"at minimum\"),\n"
        "    (100, True, \"at maximum\"),\n"
        "    (0.001, True, \"just above min\"),\n"
        "    (99.999, True, \"just below max\"),\n"
        "]\n"
        "\n"
        "s = DropOutOfRange(\"value\", 0, 100)\n"
        "for value, expected, label in test_cases:\n"
        "    result = s.should_keep({\"value\": value})\n"
        "    status = \"PASS\" if result == expected else \"FAIL\"\n"
        "    print(\"[\" + status + \"] value=\" + str(value) + \" -> \" + str(result) + \" (\" + label + \")\")\n"
        "    assert result == expected, \"Failed for \" + label\n"
        "\n"
        "print()\n"
        "print(\"All\", len(test_cases), \"parametrized cases passed!\")"
    ))
    cells.append(expected_output(
        "[PASS] value=50 -> True (middle of range)\n"
        "[PASS] value=-10 -> False (below range)\n"
        "[PASS] value=200 -> False (above range)\n"
        "[PASS] value=0 -> True (at minimum)\n"
        "[PASS] value=100 -> True (at maximum)\n"
        "[PASS] value=0.001 -> True (just above min)\n"
        "[PASS] value=99.999 -> True (just below max)\n\n"
        "All 7 parametrized cases passed!"
    ))

    # Section 4: Test file organization
    cells.append(md(
        "---\n## Section 4: Test File Organization\n\n"
        "In your project, tests should be organized like this:\n"
        "```\n"
        "tests/\n"
        "    __init__.py\n"
        "    test_data_source.py    # tests for DataSource\n"
        "    test_cleaner.py        # tests for Cleaner\n"
        "    test_analyzer.py       # tests for Analyzer\n"
        "    test_plotter.py        # tests for Plotter\n"
        "    test_reporter.py       # tests for Reporter\n"
        "    test_exceptions.py     # tests for custom exceptions\n"
        "    conftest.py            # shared fixtures\n"
        "```\n\n"
        "Run all tests: `pytest tests/ -v`\n"
        "Run one file: `pytest tests/test_cleaner.py -v`\n"
        "Run one test: `pytest tests/test_cleaner.py::test_empty_input -v`"
    ))

    cells.extend(try_it(
        "Write 3 tests for a `MeanAnalyzer`:\n"
        "1. Normal case: `[10, 20, 30]` -> mean is 20\n"
        "2. Empty case: `[]` -> returns empty dict\n"
        "3. Single value: `[42]` -> mean is 42"
    ))

    cells.append(md("---\n## Mini-Quiz"))
    cells.append(code(
        "# Q1: What naming convention does pytest use for test functions?\n"
        "# Answer: \n"
        "\n"
        "# Q2: What is a fixture?\n"
        "# Answer: \n"
        "\n"
        "# Q3: What is parametrize useful for?\n"
        "# Answer: "
    ))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# WEEK 11: Package Hygiene
# ============================================================
def week11_core():
    cells = []
    cells.append(md(
        "# OOP Week 11 -- Package Hygiene\n\n"
        "**Course:** Object-Oriented Programming (Year 2)\n"
        "**Session:** 3 hours\n"
        "**Prerequisites:** Weeks 1-10\n"
        "**Focus:** module boundaries, __init__.py, clean imports\n\n"
        "---\n\n"
        "## Learning Objectives\n\n"
        "1. Organize code into proper Python packages\n"
        "2. Write `__init__.py` files that control public API\n"
        "3. Use relative imports within a package\n"
        "4. Understand module boundaries and why they matter\n"
        "5. Create a clean import experience for users"
    ))
    cells.append(setup_cell())

    cells.append(md(
        "---\n## Section 1: Module vs Package\n\n"
        "| Term | What it is | Example |\n"
        "|------|-----------|--------|\n"
        "| **Module** | A single `.py` file | `cleaner.py` |\n"
        "| **Package** | A directory with `__init__.py` | `core/` |\n"
        "| **Sub-package** | A package inside a package | `core/strategies/` |\n\n"
        "A package is just a directory that Python treats as a namespace."
    ))

    cells.append(md("---\n## Section 2: Project Structure"))
    cells.append(code(
        "structure = \"\"\"\n"
        "src/\n"
        "  project_name/\n"
        "    __init__.py            # Top-level public API\n"
        "    config.py              # Configuration handling\n"
        "    core/\n"
        "      __init__.py          # Export components\n"
        "      data_source.py       # DataSource class\n"
        "      dataset.py           # Dataset class\n"
        "      cleaner.py           # BaseCleaner, RangeCleaner, etc.\n"
        "      analyzer.py          # AnalyzerBase, MeanAnalyzer, etc.\n"
        "      plotter.py           # Plotter class\n"
        "      reporter.py          # Reporter class\n"
        "      exceptions.py        # PipelineError hierarchy\n"
        "      factory.py           # AnalyzerFactory\n"
        "    strategies/\n"
        "      __init__.py          # Export strategies\n"
        "      cleaning.py          # Cleaning strategies\n"
        "      analysis.py          # Analysis strategies\n"
        "tests/\n"
        "  __init__.py\n"
        "  conftest.py              # Shared fixtures\n"
        "  test_data_source.py\n"
        "  test_cleaner.py\n"
        "  test_analyzer.py\n"
        "\"\"\"\n"
        "print(structure)"
    ))
    cells.append(expected_output(structure.strip() if False else "(project structure printed)"))

    cells.append(md(
        "---\n## Section 3: The `__init__.py` File\n\n"
        "`__init__.py` controls what gets exported when someone writes "
        "`from project_name.core import ...`. It is the **public API** "
        "of your package."
    ))
    cells.append(code(
        "# Example: core/__init__.py\n"
        "init_content = '''\n"
        "\"\"\"Core pipeline components.\"\"\"\n"
        "\n"
        "from .data_source import DataSource\n"
        "from .dataset import Dataset\n"
        "from .cleaner import BaseCleaner, RangeCleaner, MissingCleaner\n"
        "from .analyzer import AnalyzerBase, MeanAnalyzer, StdAnalyzer\n"
        "from .plotter import Plotter\n"
        "from .reporter import Reporter\n"
        "from .exceptions import PipelineError, SchemaError, CleaningError, EmptyDataError\n"
        "from .factory import AnalyzerFactory\n"
        "\n"
        "__all__ = [\n"
        "    \"DataSource\", \"Dataset\",\n"
        "    \"BaseCleaner\", \"RangeCleaner\", \"MissingCleaner\",\n"
        "    \"AnalyzerBase\", \"MeanAnalyzer\", \"StdAnalyzer\",\n"
        "    \"Plotter\", \"Reporter\",\n"
        "    \"PipelineError\", \"SchemaError\", \"CleaningError\", \"EmptyDataError\",\n"
        "    \"AnalyzerFactory\",\n"
        "]\n"
        "'''\n"
        "print(init_content)\n"
        "print(\"__all__ tells Python what to export with 'from core import *'\")"
    ))

    cells.append(md(
        "---\n## Section 4: Clean Import Patterns\n\n"
        "**Good imports:**\n"
        "```python\n"
        "from project_name.core import DataSource, Cleaner, Analyzer\n"
        "from project_name.core.exceptions import SchemaError\n"
        "```\n\n"
        "**Bad imports:**\n"
        "```python\n"
        "from project_name.core.data_source import DataSource  # too specific\n"
        "import project_name.core.cleaner  # exposes internals\n"
        "from project_name.core import *  # grabs everything\n"
        "```\n\n"
        "The `__init__.py` lets users write clean imports without knowing "
        "which file each class lives in."
    ))

    cells.extend(try_it(
        "Write an `__init__.py` for a `strategies/` package that exports "
        "`DropMissing`, `DropOutOfRange`, and `DropDuplicates`."
    ))

    cells.append(design_decision(
        "What goes in __init__.py?",
        "Only export what **users of the package** need. Internal helpers, "
        "utility functions, and base classes that are only used within the "
        "package should NOT be in `__init__.py`.\n\n"
        "Think of `__init__.py` as the **front door** of your package. "
        "Visitors see a clean lobby, not the messy back office."
    ))

    cells.append(md("---\n## Mini-Quiz"))
    cells.append(code(
        "# Q1: What is __init__.py for?\n"
        "# Answer: \n"
        "\n"
        "# Q2: What is the difference between a module and a package?\n"
        "# Answer: \n"
        "\n"
        "# Q3: What does __all__ control?\n"
        "# Answer: "
    ))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# WEEK 12: Plugin Exercise
# ============================================================
def week12_core():
    cells = []
    cells.append(md(
        "# OOP Week 12 -- Plugin Exercise\n\n"
        "**Course:** Object-Oriented Programming (Year 2)\n"
        "**Session:** 3 hours\n"
        "**Prerequisites:** Weeks 1-11\n"
        "**Focus:** add a new analyzer WITHOUT touching core code\n\n"
        "---\n\n"
        "## Learning Objectives\n\n"
        "1. Add a new component to an existing system without modification\n"
        "2. Demonstrate OCP in practice\n"
        "3. Write tests for the new component\n"
        "4. Register the component with the factory\n"
        "5. Verify the pipeline still works"
    ))
    cells.append(setup_cell())

    cells.append(md(
        "---\n## The Challenge\n\n"
        "You will add a **PercentileAnalyzer** to the pipeline. Rules:\n\n"
        "1. Do NOT modify any existing class (AnalyzerBase, MeanAnalyzer, etc.)\n"
        "2. Do NOT modify the AnalyzerFactory class\n"
        "3. Do NOT modify any existing test\n"
        "4. Write the new analyzer in a new class\n"
        "5. Register it with the factory (ONE line)\n"
        "6. Write at least 3 tests for it\n\n"
        "This proves that the architecture is truly open for extension."
    ))

    # Existing code
    cells.append(md("---\n## Existing Code (DO NOT MODIFY)"))
    cells.append(code(
        "# ===== EXISTING CODE -- DO NOT MODIFY =====\n"
        "\n"
        "class AnalyzerBase:\n"
        "    def analyze(self, values):\n"
        "        raise NotImplementedError\n"
        "\n"
        "class MeanAnalyzer(AnalyzerBase):\n"
        "    def analyze(self, values):\n"
        "        return {\"mean\": round(sum(values)/len(values), 4)} if values else {}\n"
        "\n"
        "class StdAnalyzer(AnalyzerBase):\n"
        "    def analyze(self, values):\n"
        "        if not values:\n"
        "            return {}\n"
        "        m = sum(values)/len(values)\n"
        "        return {\"std\": round((sum((x-m)**2 for x in values)/len(values))**0.5, 4)}\n"
        "\n"
        "class EventAnalyzer(AnalyzerBase):\n"
        "    def __init__(self, threshold=50):\n"
        "        self.threshold = threshold\n"
        "    def analyze(self, values):\n"
        "        return {\"events_above\": sum(1 for v in values if v > self.threshold)}\n"
        "\n"
        "class AnalyzerFactory:\n"
        "    _registry = {}\n"
        "    @classmethod\n"
        "    def register(cls, name, klass):\n"
        "        cls._registry[name] = klass\n"
        "    @classmethod\n"
        "    def create(cls, name, **kw):\n"
        "        if name not in cls._registry:\n"
        "            raise ValueError(\"Unknown: \" + name)\n"
        "        return cls._registry[name](**kw)\n"
        "    @classmethod\n"
        "    def list_available(cls):\n"
        "        return list(cls._registry.keys())\n"
        "\n"
        "# Register existing\n"
        "AnalyzerFactory.register(\"mean\", MeanAnalyzer)\n"
        "AnalyzerFactory.register(\"std\", StdAnalyzer)\n"
        "AnalyzerFactory.register(\"events\", EventAnalyzer)\n"
        "\n"
        "print(\"Existing analyzers:\", AnalyzerFactory.list_available())\n"
        "# ===== END EXISTING CODE ====="
    ))
    cells.append(expected_output(
        "Existing analyzers: ['mean', 'std', 'events']"
    ))

    # Student's task
    cells.append(md(
        "---\n## Your Task: Add PercentileAnalyzer\n\n"
        "Create a `PercentileAnalyzer` class that:\n"
        "- Inherits from `AnalyzerBase`\n"
        "- Takes a list of percentiles (default: [25, 50, 75])\n"
        "- Returns dict with keys like `p25`, `p50`, `p75`\n"
        "- Handles empty input gracefully"
    ))
    cells.append(code(
        "# Step 1: Create the class (inherits from AnalyzerBase)\n"
        "# YOUR CODE HERE\n"
        "\n"
        "# Step 2: Register with factory (ONE line)\n"
        "# YOUR CODE HERE\n"
        "\n"
        "# Step 3: Test it\n"
        "# YOUR CODE HERE"
    ))

    cells.append(md("---\n## Solution (try yourself first!)"))
    cells.append(code(
        "class PercentileAnalyzer(AnalyzerBase):\n"
        "    \"\"\"Computes percentiles of numeric values.\"\"\"\n"
        "    def __init__(self, percentiles=None):\n"
        "        self.percentiles = percentiles or [25, 50, 75]\n"
        "\n"
        "    def analyze(self, values):\n"
        "        if not values:\n"
        "            return {}\n"
        "        s = sorted(values)\n"
        "        n = len(s)\n"
        "        result = {}\n"
        "        for p in self.percentiles:\n"
        "            idx = min(int(n * p / 100), n - 1)\n"
        "            result[\"p\" + str(p)] = s[idx]\n"
        "        return result\n"
        "\n"
        "# Register (ONE line!)\n"
        "AnalyzerFactory.register(\"percentile\", PercentileAnalyzer)\n"
        "\n"
        "print(\"Available:\", AnalyzerFactory.list_available())\n"
        "\n"
        "# Create from factory\n"
        "pa = AnalyzerFactory.create(\"percentile\", percentiles=[10, 50, 90])\n"
        "values = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]\n"
        "print(\"Results:\", pa.analyze(values))"
    ))
    cells.append(expected_output(
        "Available: ['mean', 'std', 'events', 'percentile']\n"
        "Results: {'p10': 20, 'p50': 60, 'p90': 100}"
    ))

    # Tests
    cells.append(md("---\n## Tests for PercentileAnalyzer"))
    cells.append(code(
        "def test_percentile_normal():\n"
        "    pa = PercentileAnalyzer()\n"
        "    result = pa.analyze([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])\n"
        "    assert \"p25\" in result\n"
        "    assert \"p50\" in result\n"
        "    assert \"p75\" in result\n"
        "\n"
        "def test_percentile_empty():\n"
        "    pa = PercentileAnalyzer()\n"
        "    assert pa.analyze([]) == {}\n"
        "\n"
        "def test_percentile_custom():\n"
        "    pa = PercentileAnalyzer(percentiles=[50])\n"
        "    result = pa.analyze([1, 2, 3, 4, 5])\n"
        "    assert \"p50\" in result\n"
        "    assert \"p25\" not in result  # only asked for 50\n"
        "\n"
        "def test_percentile_factory():\n"
        "    pa = AnalyzerFactory.create(\"percentile\")\n"
        "    assert isinstance(pa, PercentileAnalyzer)\n"
        "\n"
        "test_percentile_normal()\n"
        "print(\"[PASS] test_percentile_normal\")\n"
        "test_percentile_empty()\n"
        "print(\"[PASS] test_percentile_empty\")\n"
        "test_percentile_custom()\n"
        "print(\"[PASS] test_percentile_custom\")\n"
        "test_percentile_factory()\n"
        "print(\"[PASS] test_percentile_factory\")\n"
        "print()\n"
        "print(\"All plugin tests passed!\")\n"
        "print(\"And we did NOT modify any existing code!\")"
    ))
    cells.append(expected_output(
        "[PASS] test_percentile_normal\n"
        "[PASS] test_percentile_empty\n"
        "[PASS] test_percentile_custom\n"
        "[PASS] test_percentile_factory\n\n"
        "All plugin tests passed!\n"
        "And we did NOT modify any existing code!"
    ))

    cells.append(md("---\n## Mini-Quiz"))
    cells.append(code(
        "# Q1: Which principle did we demonstrate? (SRP, OCP, or both?)\n"
        "# Answer: \n"
        "\n"
        "# Q2: How many existing files did we modify?\n"
        "# Answer: \n"
        "\n"
        "# Q3: What made this possible? (what patterns?)\n"
        "# Answer: "
    ))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# WEEK 13: Architecture Freeze
# ============================================================
def week13_core():
    cells = []
    cells.append(md(
        "# OOP Week 13 -- Architecture Freeze\n\n"
        "**Course:** Object-Oriented Programming (Year 2)\n"
        "**Session:** 3 hours\n"
        "**Prerequisites:** Weeks 1-12\n"
        "**Focus:** API stability, documentation, interface contracts\n\n"
        "---\n\n"
        "## Learning Objectives\n\n"
        "1. Define what 'architecture freeze' means\n"
        "2. Create a checklist for production readiness\n"
        "3. Document public interfaces\n"
        "4. Verify all components meet contracts\n"
        "5. Identify and fix remaining issues"
    ))
    cells.append(setup_cell())

    cells.append(md(
        "---\n## Section 1: What is an Architecture Freeze?\n\n"
        "An **architecture freeze** means:\n\n"
        "- The **public API** is locked -- no more changes to method "
        "signatures or return types\n"
        "- The **component boundaries** are fixed -- no more moving "
        "classes between modules\n"
        "- The **data contracts** are stable -- input/output schemas "
        "do not change\n\n"
        "You CAN still:\n"
        "- Fix bugs\n"
        "- Improve performance\n"
        "- Add new plugins (OCP!)\n"
        "- Improve documentation"
    ))

    cells.append(md("---\n## Section 2: Architecture Checklist"))
    cells.append(code(
        "checklist = [\n"
        "    (\"All 5 components implemented\",\n"
        "     \"DataSource, Cleaner, Analyzer, Plotter, Reporter\"),\n"
        "    (\"Custom exceptions defined\",\n"
        "     \"PipelineError, SchemaError, CleaningError, EmptyDataError\"),\n"
        "    (\"Strategy pattern working\",\n"
        "     \"Swappable cleaning/analysis strategies via config\"),\n"
        "    (\"Factory/registry working\",\n"
        "     \"Components instantiated from config dict\"),\n"
        "    (\"pytest suite passes\",\n"
        "     \"At least 10 tests covering core components\"),\n"
        "    (\"Module boundaries clean\",\n"
        "     \"core/ has __init__.py with clear exports\"),\n"
        "    (\"No logic in notebooks\",\n"
        "     \"Notebooks only import and call -- no class definitions\"),\n"
        "    (\"Plugin exercise done\",\n"
        "     \"Added new analyzer without touching core\"),\n"
        "    (\"Documentation complete\",\n"
        "     \"All public classes have docstrings\"),\n"
        "    (\"Config-driven\",\n"
        "     \"Pipeline can be configured entirely from a dict/JSON\"),\n"
        "]\n"
        "\n"
        "print(\"=== v3 Architecture Freeze Checklist ===\")\n"
        "print()\n"
        "for i, (item, detail) in enumerate(checklist, 1):\n"
        "    print(\"  [ ] \" + str(i) + \". \" + item)\n"
        "    print(\"       -> \" + detail)\n"
        "print()\n"
        "print(\"Mark each [x] when verified!\")"
    ))
    cells.append(expected_output(
        "=== v3 Architecture Freeze Checklist ===\n\n"
        "  [ ] 1. All 5 components implemented\n"
        "       -> DataSource, Cleaner, Analyzer, Plotter, Reporter\n"
        "  [ ] 2. Custom exceptions defined\n"
        "       -> PipelineError, SchemaError, CleaningError, EmptyDataError\n"
        "  (... 8 more items ...)\n\n"
        "Mark each [x] when verified!"
    ))

    cells.append(md(
        "---\n## Section 3: Interface Contracts\n\n"
        "Each component has a **contract** -- a promise about what it "
        "accepts and what it returns."
    ))
    cells.append(code(
        "contracts = {\n"
        "    \"DataSource\": {\n"
        "        \"method\": \"load()\",\n"
        "        \"input\": \"path (set in __init__)\",\n"
        "        \"output\": \"Dataset object\",\n"
        "        \"errors\": \"SchemaError if columns missing\",\n"
        "    },\n"
        "    \"Cleaner\": {\n"
        "        \"method\": \"clean(dataset)\",\n"
        "        \"input\": \"Dataset object\",\n"
        "        \"output\": \"NEW Dataset object (original unchanged)\",\n"
        "        \"errors\": \"CleaningError if too much dropped\",\n"
        "    },\n"
        "    \"Analyzer\": {\n"
        "        \"method\": \"analyze(dataset) or analyze(values)\",\n"
        "        \"input\": \"Dataset or list of values\",\n"
        "        \"output\": \"dict with analysis_summary key\",\n"
        "        \"errors\": \"EmptyDataError if no data\",\n"
        "    },\n"
        "    \"Plotter\": {\n"
        "        \"method\": \"plot(dataset, results)\",\n"
        "        \"input\": \"Dataset + results dict\",\n"
        "        \"output\": \"list of figure objects, saved to disk\",\n"
        "        \"errors\": \"graceful degradation if matplotlib missing\",\n"
        "    },\n"
        "    \"Reporter\": {\n"
        "        \"method\": \"export(dataset, results, figures)\",\n"
        "        \"input\": \"Dataset + results + figure paths\",\n"
        "        \"output\": \"dict of exported file paths\",\n"
        "        \"errors\": \"IOError if disk full/permissions\",\n"
        "    },\n"
        "}\n"
        "\n"
        "print(\"=== Component Contracts ===\")\n"
        "for name, contract in contracts.items():\n"
        "    print()\n"
        "    print(name + \":\")\n"
        "    for key, val in contract.items():\n"
        "        print(\"  \" + key + \": \" + val)"
    ))

    cells.append(md("---\n## Section 4: Automated Verification"))
    cells.append(code(
        "import os\n"
        "\n"
        "def verify_architecture():\n"
        "    \"\"\"Automated architecture checks.\"\"\"\n"
        "    print(\"=== Automated Architecture Verification ===\")\n"
        "    passed = 0\n"
        "    failed = 0\n"
        "\n"
        "    # Check required output files\n"
        "    files = [\n"
        "        \"data/cleaned/cleaned.csv\",\n"
        "        \"reports/report.json\",\n"
        "    ]\n"
        "    for f in files:\n"
        "        exists = os.path.exists(f) and os.path.getsize(f) > 0\n"
        "        status = \"PASS\" if exists else \"FAIL\"\n"
        "        print(\"  [\" + status + \"] \" + f)\n"
        "        if exists:\n"
        "            passed += 1\n"
        "        else:\n"
        "            failed += 1\n"
        "\n"
        "    # Check core module\n"
        "    core = \"src/project_template/core/__init__.py\"\n"
        "    exists = os.path.exists(core)\n"
        "    status = \"PASS\" if exists else \"FAIL\"\n"
        "    print(\"  [\" + status + \"] \" + core)\n"
        "    if exists:\n"
        "        passed += 1\n"
        "    else:\n"
        "        failed += 1\n"
        "\n"
        "    # Check tests\n"
        "    if os.path.exists(\"tests\"):\n"
        "        test_files = [f for f in os.listdir(\"tests\") if f.startswith(\"test_\")]\n"
        "        has_tests = len(test_files) >= 3\n"
        "        status = \"PASS\" if has_tests else \"FAIL\"\n"
        "        print(\"  [\" + status + \"] \" + str(len(test_files)) + \" test files\")\n"
        "        if has_tests:\n"
        "            passed += 1\n"
        "        else:\n"
        "            failed += 1\n"
        "    else:\n"
        "        print(\"  [FAIL] tests/ directory missing\")\n"
        "        failed += 1\n"
        "\n"
        "    print()\n"
        "    print(str(passed) + \" passed, \" + str(failed) + \" failed\")\n"
        "    return failed == 0\n"
        "\n"
        "verify_architecture()"
    ))

    cells.extend(try_it(
        "Run the architecture verification on YOUR project. For each "
        "FAIL, write down what you need to fix."
    ))

    cells.append(md("---\n## Mini-Quiz"))
    cells.append(code(
        "# Q1: What does 'architecture freeze' mean?\n"
        "# Answer: \n"
        "\n"
        "# Q2: What CAN you still change after a freeze?\n"
        "# Answer: \n"
        "\n"
        "# Q3: What is an interface contract?\n"
        "# Answer: "
    ))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# WEEK 14: v3 Architecture Demo
# ============================================================
def week14_core():
    cells = []
    cells.append(md(
        "# OOP Week 14 -- v3 Architecture Demo\n\n"
        "**Course:** Object-Oriented Programming (Year 2)\n"
        "**Session:** 3 hours\n"
        "**Prerequisites:** Weeks 1-13 (all complete!)\n"
        "**Focus:** final tests, architecture review, release\n\n"
        "---\n\n"
        "## Learning Objectives\n\n"
        "1. Demonstrate the complete v3 pipeline\n"
        "2. Run all tests and verify everything passes\n"
        "3. Review the architecture against SOLID principles\n"
        "4. Present your project to the class\n"
        "5. Reflect on the journey from procedural to OOP"
    ))
    cells.append(setup_cell())

    cells.append(md(
        "---\n## Section 1: The Complete Pipeline\n\n"
        "Run your entire v3 pipeline end-to-end. This should work "
        "with a single config dict."
    ))
    cells.append(code(
        "import os, json\n"
        "\n"
        "def run_v3_demo():\n"
        "    \"\"\"Run the complete v3 pipeline.\"\"\"\n"
        "    print(\"=== v3 Architecture Demo ===\")\n"
        "    print()\n"
        "\n"
        "    # This would import from your package:\n"
        "    # from project_name.core import (\n"
        "    #     DataSource, ConfigurableCleaner, DropMissing, DropOutOfRange,\n"
        "    #     Analyzer, Plotter, Reporter, AnalyzerFactory\n"
        "    # )\n"
        "\n"
        "    print(\"Step 1: Load data\")\n"
        "    print(\"  DataSource.load() -> Dataset\")\n"
        "    print()\n"
        "\n"
        "    print(\"Step 2: Clean data\")\n"
        "    print(\"  ConfigurableCleaner.clean(dataset) -> Dataset\")\n"
        "    print(\"  Strategies: DropMissing, DropOutOfRange\")\n"
        "    print()\n"
        "\n"
        "    print(\"Step 3: Analyze data\")\n"
        "    print(\"  AnalyzerFactory creates analyzers from config\")\n"
        "    print(\"  Each analyzer.analyze(values) -> dict\")\n"
        "    print()\n"
        "\n"
        "    print(\"Step 4: Plot results\")\n"
        "    print(\"  Plotter.plot(dataset, results) -> figures\")\n"
        "    print()\n"
        "\n"
        "    print(\"Step 5: Export report\")\n"
        "    print(\"  Reporter.export(dataset, results, figures) -> files\")\n"
        "    print()\n"
        "\n"
        "    print(\"=== Pipeline Complete ===\")\n"
        "\n"
        "run_v3_demo()"
    ))
    cells.append(expected_output(
        "=== v3 Architecture Demo ===\n\n"
        "Step 1: Load data\n"
        "  DataSource.load() -> Dataset\n\n"
        "Step 2: Clean data\n"
        "  ConfigurableCleaner.clean(dataset) -> Dataset\n"
        "  Strategies: DropMissing, DropOutOfRange\n\n"
        "Step 3: Analyze data\n"
        "  AnalyzerFactory creates analyzers from config\n"
        "  Each analyzer.analyze(values) -> dict\n\n"
        "Step 4: Plot results\n"
        "  Plotter.plot(dataset, results) -> figures\n\n"
        "Step 5: Export report\n"
        "  Reporter.export(dataset, results, figures) -> files\n\n"
        "=== Pipeline Complete ==="
    ))

    cells.append(md(
        "---\n## Section 2: Architecture Review\n\n"
        "Let us review our architecture against the principles we learned."
    ))
    cells.append(code(
        "principles = [\n"
        "    (\"SRP\", \"Single Responsibility\",\n"
        "     \"Each component (DataSource, Cleaner, Analyzer, Plotter, Reporter) has ONE job\"),\n"
        "    (\"OCP\", \"Open/Closed\",\n"
        "     \"New analyzers added via AnalyzerFactory without changing existing code\"),\n"
        "    (\"Composition\", \"Has-A relationships\",\n"
        "     \"Pipeline HAS components; components do not inherit from Pipeline\"),\n"
        "    (\"Strategy\", \"Interchangeable algorithms\",\n"
        "     \"Cleaning and analysis strategies are swappable via config\"),\n"
        "    (\"Factory\", \"Object creation from config\",\n"
        "     \"AnalyzerFactory creates objects from string names\"),\n"
        "    (\"Exceptions\", \"Domain-specific errors\",\n"
        "     \"PipelineError hierarchy with context-rich messages\"),\n"
        "]\n"
        "\n"
        "print(\"=== Architecture Principles Review ===\")\n"
        "for abbr, name, description in principles:\n"
        "    print()\n"
        "    print(abbr + \" -- \" + name)\n"
        "    print(\"  \" + description)"
    ))

    cells.append(md(
        "---\n## Section 3: The Journey\n\n"
        "Let us reflect on how far we have come."
    ))
    cells.append(code(
        "journey = [\n"
        "    (\"Week 1\", \"Classes & Objects\", \"Learned what a class IS\"),\n"
        "    (\"Week 2\", \"Composition\", \"Objects containing objects\"),\n"
        "    (\"Week 3\", \"Cleaner\", \"Template method, subclasses\"),\n"
        "    (\"Week 4\", \"Analyzer\", \"Stable schemas, composable analyzers\"),\n"
        "    (\"Week 5\", \"Plotter & Reporter\", \"Complete pipeline\"),\n"
        "    (\"Week 6\", \"Exceptions\", \"Domain-specific error handling\"),\n"
        "    (\"Week 7\", \"SOLID\", \"SRP + OCP principles\"),\n"
        "    (\"Week 8\", \"Strategy\", \"Swappable algorithms\"),\n"
        "    (\"Week 9\", \"Factory\", \"Config-driven creation\"),\n"
        "    (\"Week 10\", \"pytest\", \"Automated testing\"),\n"
        "    (\"Week 11\", \"Packages\", \"Clean module boundaries\"),\n"
        "    (\"Week 12\", \"Plugin\", \"OCP in practice\"),\n"
        "    (\"Week 13\", \"Freeze\", \"API stability\"),\n"
        "    (\"Week 14\", \"Demo\", \"YOU ARE HERE!\"),\n"
        "]\n"
        "\n"
        "print(\"=== Your OOP Journey ===\")\n"
        "for week, topic, achievement in journey:\n"
        "    print(\"  \" + week + \": \" + topic + \" -- \" + achievement)"
    ))
    cells.append(expected_output(
        "=== Your OOP Journey ===\n"
        "  Week 1: Classes & Objects -- Learned what a class IS\n"
        "  Week 2: Composition -- Objects containing objects\n"
        "  (... 12 more weeks ...)\n"
        "  Week 14: Demo -- YOU ARE HERE!"
    ))

    cells.append(md(
        "---\n## Section 4: Presentation Prep\n\n"
        "For your demo, be ready to show:\n\n"
        "1. **Run the pipeline** end-to-end with your track's data\n"
        "2. **Show the config** -- how the pipeline is configured\n"
        "3. **Add a plugin** live -- create a new analyzer and register it\n"
        "4. **Run the tests** -- `pytest tests/ -v`\n"
        "5. **Explain one design decision** -- why you chose a particular pattern"
    ))

    cells.append(md(
        "---\n## Final Quiz"
    ))
    cells.append(code(
        "# Q1: Name the 5 components of the v3 pipeline.\n"
        "# Answer: \n"
        "\n"
        "# Q2: What is the difference between composition and inheritance?\n"
        "# Answer: \n"
        "\n"
        "# Q3: What does SRP stand for and what does it mean?\n"
        "# Answer: \n"
        "\n"
        "# Q4: What does OCP stand for and what does it mean?\n"
        "# Answer: \n"
        "\n"
        "# Q5: How does the Factory pattern enable plugins?\n"
        "# Answer: \n"
        "\n"
        "# Q6: What is the benefit of custom exceptions over generic ones?\n"
        "# Answer: \n"
        "\n"
        "# Q7: What is a 'stable schema' and why does it matter?\n"
        "# Answer: \n"
        "\n"
        "# Q8: Name 3 things pytest can do.\n"
        "# Answer: \n"
        "\n"
        "# Q9: What is __init__.py for?\n"
        "# Answer: \n"
        "\n"
        "# Q10: What was the hardest concept this semester and why?\n"
        "# Answer: "
    ))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# MAP WEEKS TO FUNCTIONS
# ============================================================
WEEK_CORE_FUNCTIONS = {
    1: week01_core,
    2: week02_core,
    3: week03_core,
    4: week04_core,
    5: week05_core,
    6: week06_core,
    7: week07_core,
    8: week08_core,
    9: week09_core,
    10: week10_core,
    11: week11_core,
    12: week12_core,
    13: week13_core,
    14: week14_core,
}


# ============================================================
# CORE NOTEBOOK ENRICHMENT -- adds ~30 cells per week
# ============================================================
def enrich_core(week_num, title, cells):
    """Add additional worked examples, exercises, debugging tips, etc.

    Inserts extra cells before the Mini-Quiz / reflection section
    to bring every core notebook to 60+ cells.
    """
    extra = []

    # ---- Week-specific additional worked examples ----
    if week_num == 2:
        extra.append(md(
            "---\n## Section 5: More Worked Examples\n\n"
            "### Example 3: Dataset with Type Coercion\n\n"
            "Real data often has string values that need to be converted. "
            "Let us add a method that handles this."
        ))
        extra.append(code(
            "class SmartDataset(Dataset):\n"
            "    \"\"\"Dataset that can coerce column types.\"\"\"\n"
            "\n"
            "    def get_numeric_column(self, name):\n"
            "        \"\"\"Get a column, converting strings to floats where possible.\"\"\"\n"
            "        result = []\n"
            "        for row in self.rows:\n"
            "            val = row.get(name)\n"
            "            if isinstance(val, (int, float)):\n"
            "                result.append(float(val))\n"
            "            elif isinstance(val, str):\n"
            "                try:\n"
            "                    result.append(float(val))\n"
            "                except ValueError:\n"
            "                    result.append(None)  # mark as missing\n"
            "            else:\n"
            "                result.append(None)\n"
            "        return result\n"
            "\n"
            "\n"
            "messy = SmartDataset([\n"
            "    {\"id\": 1, \"value\": \"25.5\"},\n"
            "    {\"id\": 2, \"value\": 30},\n"
            "    {\"id\": 3, \"value\": \"abc\"},\n"
            "    {\"id\": 4, \"value\": None},\n"
            "], \"messy.csv\")\n"
            "\n"
            "print(\"Raw:\", messy.get_column(\"value\"))\n"
            "print(\"Numeric:\", messy.get_numeric_column(\"value\"))"
        ))
        extra.append(expected_output(
            "Raw: ['25.5', 30, 'abc', None]\n"
            "Numeric: [25.5, 30.0, None, None]"
        ))

        extra.append(md(
            "### Example 4: Chaining Operations\n\n"
            "Because each method returns a new Dataset, we can chain "
            "operations together."
        ))
        extra.append(code(
            "# Chaining: load -> filter -> filter -> get_column\n"
            "raw = Dataset([\n"
            "    {\"id\": 1, \"value\": 25.0, \"category\": \"A\"},\n"
            "    {\"id\": 2, \"value\": -5.0, \"category\": \"B\"},\n"
            "    {\"id\": 3, \"value\": 88.0, \"category\": \"A\"},\n"
            "    {\"id\": 4, \"value\": 42.0, \"category\": \"B\"},\n"
            "    {\"id\": 5, \"value\": 200.0, \"category\": \"A\"},\n"
            "], \"raw.csv\")\n"
            "\n"
            "# Chain: keep positive -> keep < 100 -> get values\n"
            "result = (raw\n"
            "    .filter_rows(\"value\", lambda v: isinstance(v, (int, float)) and v > 0)\n"
            "    .filter_rows(\"value\", lambda v: v < 100))\n"
            "\n"
            "print(\"Original:\", len(raw), \"rows\")\n"
            "print(\"After chain:\", len(result), \"rows\")\n"
            "print(\"Values:\", result.get_column(\"value\"))"
        ))
        extra.append(expected_output(
            "Original: 5 rows\n"
            "After chain: 3 rows\n"
            "Values: [25.0, 88.0, 42.0]"
        ))

        extra.append(debugging_tip(
            "TypeError: 'NoneType' object is not iterable",
            "This happens when a method returns None instead of a Dataset. "
            "Check that every method that should return a Dataset actually "
            "has a `return` statement. Common mistake:\n\n"
            "```python\n"
            "def filter_rows(self, column, condition):\n"
            "    kept = [r for r in self.rows if condition(r.get(column))]\n"
            "    Dataset(kept)  # BUG: missing 'return'!\n"
            "```\n\n"
            "Fix: `return Dataset(kept, self.source_path)`"
        ))

        extra.extend(try_it(
            "Create a `merge_datasets(ds1, ds2)` function that combines "
            "two Datasets into one new Dataset. The datasets must have "
            "the same columns. Raise ValueError if they do not.\n\n"
            "Test with:\n"
            "```python\n"
            "ds1 = Dataset([{\"x\": 1}, {\"x\": 2}])\n"
            "ds2 = Dataset([{\"x\": 3}, {\"x\": 4}])\n"
            "merged = merge_datasets(ds1, ds2)\n"
            "print(len(merged))  # should be 4\n"
            "```"
        ))

        extra.extend(common_mistake(
            "Shallow copy trap with nested data",
            (
                "# BUG: rows share references to the same dicts!\n"
                "original = Dataset([{\"value\": [1, 2, 3]}])\n"
                "copy_rows = original.rows[:]  # shallow copy of list\n"
                "copy_rows[0][\"value\"].append(999)  # modifies original too!\n"
                "\n"
                "print(\"Original:\", original.rows[0][\"value\"])\n"
                "print(\"Oops! 999 leaked into the original.\")"
            ),
            (
                "import copy\n"
                "\n"
                "original = Dataset([{\"value\": [1, 2, 3]}])\n"
                "copy_rows = copy.deepcopy(original.rows)  # deep copy!\n"
                "copy_rows[0][\"value\"].append(999)\n"
                "\n"
                "print(\"Original:\", original.rows[0][\"value\"])  # [1, 2, 3]\n"
                "print(\"Copy:\", copy_rows[0][\"value\"])  # [1, 2, 3, 999]\n"
                "print(\"Original is safe!\")"
            ),
            "When your data contains nested mutable objects (lists, dicts), "
            "a shallow copy (slicing, list()) still shares the inner objects. "
            "Use `copy.deepcopy()` for truly independent copies."
        ))

        extra.append(design_decision(
            "When to use Dataset vs plain list",
            "**Use Dataset** when:\n"
            "- You need metadata (source path, column names, row count)\n"
            "- You want helper methods (get_column, filter, describe)\n"
            "- Data will pass through multiple components\n"
            "- You want type safety (only Datasets enter the pipeline)\n\n"
            "**Use plain list** when:\n"
            "- Quick throwaway computation\n"
            "- Simple scripts with no pipeline\n"
            "- Performance-critical inner loops"
        ))

        extra.extend(try_it(
            "Add a `sample(n)` method to Dataset that returns a NEW "
            "Dataset with `n` random rows. Use `import random` and "
            "`random.sample(self.rows, n)`. Handle the case where "
            "`n > len(self.rows)`."
        ))

    elif week_num == 3:
        extra.append(md(
            "---\n## Section 4: More Cleaner Types"
        ))
        extra.append(md("### TypeCleaner -- drops rows with wrong types"))
        extra.append(code(
            "class TypeCleaner(BaseCleaner):\n"
            "    \"\"\"Drop rows where a column is not the expected type.\"\"\"\n"
            "\n"
            "    def __init__(self, column, expected_type):\n"
            "        super().__init__(\"type_\" + column)\n"
            "        self.column = column\n"
            "        self.expected_type = expected_type\n"
            "\n"
            "    def check(self, row):\n"
            "        val = row.get(self.column)\n"
            "        if not isinstance(val, self.expected_type):\n"
            "            return \"wrong_type_\" + self.column\n"
            "        return None\n"
            "\n"
            "\n"
            "tc = TypeCleaner(\"value\", (int, float))\n"
            "result = tc.clean(sample_data)\n"
            "tc.report()\n"
            "print(\"Kept values:\", result.get_column(\"value\"))"
        ))
        extra.append(expected_output(
            "Cleaner: type_value\n"
            "  Checked: 7\n"
            "  Dropped: 1\n"
            "    - wrong_type_value: 1\n"
            "Kept values: [25.0, 30.0, 88.0, -5.0, 200.0, 42.0]"
        ))

        extra.append(md("### OutlierCleaner -- drops statistical outliers"))
        extra.append(code(
            "class OutlierCleaner(BaseCleaner):\n"
            "    \"\"\"Drop rows where a value is more than N std devs from mean.\"\"\"\n"
            "\n"
            "    def __init__(self, column, n_std=2):\n"
            "        super().__init__(\"outlier_\" + column)\n"
            "        self.column = column\n"
            "        self.n_std = n_std\n"
            "        self._mean = 0\n"
            "        self._std = 0\n"
            "\n"
            "    def clean(self, dataset):\n"
            "        # Pre-compute stats before checking rows\n"
            "        vals = [r.get(self.column) for r in dataset.rows\n"
            "                if isinstance(r.get(self.column), (int, float))]\n"
            "        if vals:\n"
            "            self._mean = sum(vals) / len(vals)\n"
            "            self._std = (sum((x - self._mean)**2 for x in vals) / len(vals)) ** 0.5\n"
            "        return super().clean(dataset)\n"
            "\n"
            "    def check(self, row):\n"
            "        val = row.get(self.column)\n"
            "        if isinstance(val, (int, float)) and self._std > 0:\n"
            "            z_score = abs(val - self._mean) / self._std\n"
            "            if z_score > self.n_std:\n"
            "                return \"outlier_\" + self.column\n"
            "        return None\n"
            "\n"
            "\n"
            "data_with_outlier = Dataset([\n"
            "    {\"id\": 1, \"value\": 10.0},\n"
            "    {\"id\": 2, \"value\": 12.0},\n"
            "    {\"id\": 3, \"value\": 11.0},\n"
            "    {\"id\": 4, \"value\": 13.0},\n"
            "    {\"id\": 5, \"value\": 100.0},  # outlier!\n"
            "], \"test.csv\")\n"
            "\n"
            "oc = OutlierCleaner(\"value\", n_std=2)\n"
            "result = oc.clean(data_with_outlier)\n"
            "oc.report()\n"
            "print(\"Kept:\", result.get_column(\"value\"))"
        ))
        extra.append(expected_output(
            "Cleaner: outlier_value\n"
            "  Checked: 5\n"
            "  Dropped: 1\n"
            "    - outlier_value: 1\n"
            "Kept: [10.0, 12.0, 11.0, 13.0]"
        ))

        extra.append(md(
            "---\n## Section 5: Cleaning Pipeline with Full Report"
        ))
        extra.append(code(
            "# Build a comprehensive pipeline\n"
            "full_pipeline = CleaningPipeline()\n"
            "full_pipeline.add(TypeCleaner(\"value\", (int, float)))\n"
            "full_pipeline.add(MissingCleaner([\"status\"]))\n"
            "full_pipeline.add(RangeCleaner(\"value\", 0, 100))\n"
            "\n"
            "print(\"Input:\", sample_data, \"-- values:\", sample_data.get_column(\"value\"))\n"
            "print()\n"
            "\n"
            "clean = full_pipeline.clean(sample_data)\n"
            "print()\n"
            "print(\"Output:\", clean, \"-- values:\", clean.get_column(\"value\"))\n"
            "print()\n"
            "full_pipeline.report()"
        ))
        extra.append(expected_output(
            "Input: Dataset(7 rows) -- values: [25.0, 30.0, 88.0, -5.0, None, 200.0, 42.0]\n\n"
            "Output: Dataset(3 rows) -- values: [25.0, 30.0, 88.0]\n\n"
            "Cleaner: type_value\n  Checked: 7\n  Dropped: 1\n"
            "Cleaner: missing\n  Checked: 6\n  Dropped: 1\n"
            "Cleaner: range_value\n  Checked: 5\n  Dropped: 2\n"
            "Total dropped: 4"
        ))

        extra.extend(procedural_vs_oop(
            "Data Cleaning",
            (
                "# PROCEDURAL: one big function with many if-statements\n"
                "def clean_all(data, min_v, max_v, required_cols):\n"
                "    result = []\n"
                "    for row in data:\n"
                "        # Check type\n"
                "        if not isinstance(row.get('value'), (int, float)):\n"
                "            continue\n"
                "        # Check missing\n"
                "        skip = False\n"
                "        for col in required_cols:\n"
                "            if row.get(col) is None or row.get(col) == '':\n"
                "                skip = True\n"
                "                break\n"
                "        if skip:\n"
                "            continue\n"
                "        # Check range\n"
                "        if row['value'] < min_v or row['value'] > max_v:\n"
                "            continue\n"
                "        result.append(row)\n"
                "    return result\n"
                "\n"
                "# Hard to add new rules without modifying this function!"
            ),
            (
                "# OOP: composable, each rule is independent\n"
                "pipeline = CleaningPipeline()\n"
                "pipeline.add(TypeCleaner('value', (int, float)))\n"
                "pipeline.add(MissingCleaner(['status']))\n"
                "pipeline.add(RangeCleaner('value', 0, 100))\n"
                "# Easy to add new rules: pipeline.add(OutlierCleaner('value'))\n"
                "\n"
                "clean = pipeline.clean(dataset)\n"
                "pipeline.report()  # detailed per-step reporting!"
            ),
            "The procedural version packs all rules into one function. "
            "Adding a new rule means modifying that function (violating OCP). "
            "The OOP version lets you add/remove/reorder rules without "
            "touching any existing code."
        ))

        extra.append(debugging_tip(
            "Cleaners running in wrong order",
            "The order of cleaners matters! If you put RangeCleaner before "
            "TypeCleaner, the RangeCleaner might crash on non-numeric values.\n\n"
            "**Best practice:** Always put type/missing cleaners FIRST, "
            "then range/logic cleaners SECOND.\n\n"
            "```\n"
            "Recommended order:\n"
            "1. TypeCleaner (remove wrong types)\n"
            "2. MissingCleaner (remove nulls/empties)\n"
            "3. RangeCleaner (remove out-of-range)\n"
            "4. OutlierCleaner (remove statistical outliers)\n"
            "```"
        ))

        extra.extend(try_it(
            "Create a `StatusCleaner(BaseCleaner)` that drops rows where "
            "the `status` column contains `\"error\"`. Test it with the "
            "sample data, then add it to the full pipeline."
        ))

        extra.extend(try_it(
            "Create a `WhitespaceCleaner(BaseCleaner)` that drops rows "
            "where a specified column is all whitespace. Test with:\n"
            "```python\n"
            "data = Dataset([\n"
            "    {\"name\": \"Alice\", \"note\": \"good\"},\n"
            "    {\"name\": \"Bob\", \"note\": \"   \"},  # whitespace only\n"
            "    {\"name\": \"Charlie\", \"note\": \"\"},  # empty\n"
            "])\n"
            "```"
        ))

    elif week_num == 4:
        extra.append(md(
            "---\n## Section 4: More Analyzer Types"
        ))
        extra.append(md("### Example: CountAnalyzer"))
        extra.append(code(
            "class CountAnalyzer(AnalyzerBase):\n"
            "    \"\"\"Counts values meeting various criteria.\"\"\"\n"
            "    def analyze(self, values):\n"
            "        if not values:\n"
            "            return {\"count\": 0}\n"
            "        positives = sum(1 for v in values if v > 0)\n"
            "        negatives = sum(1 for v in values if v < 0)\n"
            "        zeros = sum(1 for v in values if v == 0)\n"
            "        return {\n"
            "            \"count\": len(values),\n"
            "            \"positives\": positives,\n"
            "            \"negatives\": negatives,\n"
            "            \"zeros\": zeros,\n"
            "        }\n"
            "\n"
            "ca = CountAnalyzer()\n"
            "test_vals = [10, -5, 0, 30, -2, 0, 15]\n"
            "print(\"Count analysis:\", ca.analyze(test_vals))"
        ))
        extra.append(expected_output(
            "Count analysis: {'count': 7, 'positives': 3, 'negatives': 2, 'zeros': 2}"
        ))

        extra.append(md("### Example: TrendAnalyzer"))
        extra.append(code(
            "class TrendAnalyzer(AnalyzerBase):\n"
            "    \"\"\"Detects if values are trending up, down, or flat.\"\"\"\n"
            "    def analyze(self, values):\n"
            "        if len(values) < 2:\n"
            "            return {\"trend\": \"insufficient_data\"}\n"
            "        mid = len(values) // 2\n"
            "        first_half = sum(values[:mid]) / mid\n"
            "        second_half = sum(values[mid:]) / (len(values) - mid)\n"
            "        diff = second_half - first_half\n"
            "        if abs(diff) < 1.0:\n"
            "            trend = \"flat\"\n"
            "        elif diff > 0:\n"
            "            trend = \"increasing\"\n"
            "        else:\n"
            "            trend = \"decreasing\"\n"
            "        return {\n"
            "            \"trend\": trend,\n"
            "            \"first_half_mean\": round(first_half, 2),\n"
            "            \"second_half_mean\": round(second_half, 2),\n"
            "        }\n"
            "\n"
            "ta = TrendAnalyzer()\n"
            "print(\"Increasing:\", ta.analyze([10, 12, 15, 20, 25, 30]))\n"
            "print(\"Decreasing:\", ta.analyze([30, 25, 20, 15, 12, 10]))\n"
            "print(\"Flat:      \", ta.analyze([20, 20, 20, 20, 20, 20]))"
        ))
        extra.append(expected_output(
            "Increasing: {'trend': 'increasing', 'first_half_mean': 12.33, 'second_half_mean': 25.0}\n"
            "Decreasing: {'trend': 'decreasing', 'first_half_mean': 25.0, 'second_half_mean': 12.33}\n"
            "Flat:       {'trend': 'flat', 'first_half_mean': 20.0, 'second_half_mean': 20.0}"
        ))

        extra.append(md(
            "---\n## Section 5: Running All Analyzers Together"
        ))
        extra.append(code(
            "def run_all_analyzers(analyzers, values):\n"
            "    \"\"\"Run all analyzers and merge results.\"\"\"\n"
            "    combined = {}\n"
            "    for a in analyzers:\n"
            "        name = type(a).__name__\n"
            "        result = a.analyze(values)\n"
            "        combined[name] = result\n"
            "        print(name + \":\", result)\n"
            "    return combined\n"
            "\n"
            "all_analyzers = [\n"
            "    MeanAnalyzer(),\n"
            "    StdAnalyzer(),\n"
            "    EventAnalyzer(50),\n"
            "    RangeAnalyzer(),\n"
            "    CountAnalyzer(),\n"
            "    TrendAnalyzer(),\n"
            "]\n"
            "\n"
            "values = [15, 25, 30, 42, 67, 88]\n"
            "print(\"=== Running 6 analyzers ===\")\n"
            "results = run_all_analyzers(all_analyzers, values)"
        ))
        extra.append(expected_output(
            "=== Running 6 analyzers ===\n"
            "MeanAnalyzer: {'mean': 44.5}\n"
            "StdAnalyzer: {'std': 25.133}\n"
            "EventAnalyzer: {'events_above': 2, 'threshold': 50}\n"
            "RangeAnalyzer: {'min': 15, 'max': 88, 'range': 73}\n"
            "CountAnalyzer: {'count': 6, 'positives': 6, 'negatives': 0, 'zeros': 0}\n"
            "TrendAnalyzer: {'trend': 'increasing', ...}"
        ))

        extra.append(debugging_tip(
            "KeyError when accessing results",
            "If your analyzer returns `{\"mean\": 20}` but your reporter "
            "tries `results[\"avg\"]`, you get a KeyError. This is why a "
            "**stable schema** matters -- everyone agrees on the key names.\n\n"
            "**Fix:** Document the exact keys each analyzer returns. "
            "Write tests that assert the expected keys exist."
        ))

        extra.extend(try_it(
            "Create a `PercentileAnalyzer(AnalyzerBase)` that takes a list "
            "of percentiles (e.g., [25, 50, 75]) and returns them as "
            "`{\"p25\": ..., \"p50\": ..., \"p75\": ...}`. Test with the "
            "sample data."
        ))

        extra.extend(try_it(
            "Create a `HistogramAnalyzer(AnalyzerBase)` that bins values "
            "into ranges and counts them. For example, with bins of width 20:\n"
            "`{\"0-20\": 1, \"20-40\": 2, \"40-60\": 1, \"60-80\": 1, \"80-100\": 1}`"
        ))

    elif week_num == 5:
        extra.append(md(
            "---\n## Section 4: More Plot Types"
        ))
        extra.append(code(
            "class EnhancedPlotter(Plotter):\n"
            "    \"\"\"Plotter with additional chart types.\"\"\"\n"
            "\n"
            "    def plot_boxplot(self, dataset, col):\n"
            "        \"\"\"Create a box plot.\"\"\"\n"
            "        try:\n"
            "            import matplotlib\n"
            "            matplotlib.use('Agg')\n"
            "            import matplotlib.pyplot as plt\n"
            "        except ImportError:\n"
            "            print('matplotlib not available')\n"
            "            return None\n"
            "\n"
            "        values = [v for v in dataset.get_column(col)\n"
            "                  if isinstance(v, (int, float))]\n"
            "        if not values:\n"
            "            return None\n"
            "\n"
            "        fig, ax = plt.subplots(figsize=(6, 4))\n"
            "        ax.boxplot(values, vert=True)\n"
            "        ax.set_title('Box Plot of ' + col)\n"
            "        ax.set_ylabel(col)\n"
            "        ax.grid(True, alpha=0.3)\n"
            "        plt.close(fig)\n"
            "        print('Created box plot for ' + col)\n"
            "        return fig\n"
            "\n"
            "    def plot_bar(self, labels, values, title='Bar Chart'):\n"
            "        \"\"\"Create a bar chart.\"\"\"\n"
            "        try:\n"
            "            import matplotlib\n"
            "            matplotlib.use('Agg')\n"
            "            import matplotlib.pyplot as plt\n"
            "        except ImportError:\n"
            "            print('matplotlib not available')\n"
            "            return None\n"
            "\n"
            "        fig, ax = plt.subplots(figsize=(8, 4))\n"
            "        ax.bar(labels, values, color='#2196F3')\n"
            "        ax.set_title(title)\n"
            "        ax.grid(True, alpha=0.3, axis='y')\n"
            "        plt.close(fig)\n"
            "        print('Created bar chart: ' + title)\n"
            "        return fig\n"
            "\n"
            "\n"
            "ep = EnhancedPlotter({\n"
            "    'project_name': 'Demo',\n"
            "    'value_column': 'value',\n"
            "    'figures_dir': '/tmp/oop_demo/figures',\n"
            "})\n"
            "\n"
            "# Box plot\n"
            "box_fig = ep.plot_boxplot(clean_data, 'value')\n"
            "\n"
            "# Bar chart from analysis results\n"
            "bar_fig = ep.plot_bar(\n"
            "    ['Mean', 'Std', 'Min', 'Max'],\n"
            "    [52.4, 25.5, 15.0, 91.0],\n"
            "    'Analysis Summary'\n"
            ")"
        ))
        extra.append(expected_output(
            "Created box plot for value\n"
            "Created bar chart: Analysis Summary"
        ))

        extra.append(md(
            "---\n## Section 5: Reporter Formats"
        ))
        extra.append(code(
            "class EnhancedReporter(Reporter):\n"
            "    \"\"\"Reporter with multiple output formats.\"\"\"\n"
            "\n"
            "    def export_text_summary(self, results, path):\n"
            "        \"\"\"Export a human-readable text summary.\"\"\"\n"
            "        os.makedirs(os.path.dirname(path), exist_ok=True)\n"
            "        lines = []\n"
            "        lines.append('=== Analysis Report ===')\n"
            "        lines.append('')\n"
            "        summary = results.get('analysis_summary', {})\n"
            "        for key, val in summary.items():\n"
            "            if isinstance(val, float):\n"
            "                lines.append(key + ': ' + str(round(val, 4)))\n"
            "            else:\n"
            "                lines.append(key + ': ' + str(val))\n"
            "        text = chr(10).join(lines)\n"
            "        with open(path, 'w') as f:\n"
            "            f.write(text)\n"
            "        print('Exported text summary: ' + path)\n"
            "        return path\n"
            "\n"
            "\n"
            "er = EnhancedReporter({\n"
            "    'project_name': 'Demo',\n"
            "    'track': 'data',\n"
            "    'cleaned_data_path': '/tmp/oop_demo/data/cleaned.csv',\n"
            "    'report_path': '/tmp/oop_demo/reports/report.json',\n"
            "})\n"
            "er.export_text_summary(sample_results, '/tmp/oop_demo/reports/summary.txt')"
        ))
        extra.append(expected_output(
            "Exported text summary: /tmp/oop_demo/reports/summary.txt"
        ))

        extra.extend(procedural_vs_oop(
            "Report Generation",
            (
                "# PROCEDURAL\n"
                "def export_report(data, results, csv_path, json_path):\n"
                "    # Save CSV\n"
                "    import csv\n"
                "    with open(csv_path, 'w') as f:\n"
                "        w = csv.DictWriter(f, fieldnames=data[0].keys())\n"
                "        w.writeheader()\n"
                "        w.writerows(data)\n"
                "    # Save JSON\n"
                "    import json\n"
                "    with open(json_path, 'w') as f:\n"
                "        json.dump(results, f)\n"
                "    # Add a new format? Modify this function!\n"
                "    return {'csv': csv_path, 'json': json_path}"
            ),
            (
                "# OOP\n"
                "reporter = Reporter(config)\n"
                "exports = reporter.export(dataset, results, figures)\n"
                "# reporter.exported tracks what was created\n"
                "# Adding new format = add new method or subclass\n"
                "# No existing code changes needed"
            ),
            "The Reporter class tracks its own state (what was exported), "
            "can be configured once and used repeatedly, and can be extended "
            "with new formats via subclassing (OCP)."
        ))

        extra.append(design_decision(
            "Graceful degradation for optional dependencies",
            "Notice how Plotter wraps matplotlib in try/except. This is "
            "**graceful degradation** -- the program still works without "
            "matplotlib, it just skips the plots.\n\n"
            "This is important because:\n"
            "- Not every environment has matplotlib installed\n"
            "- Tests should run without GUI dependencies\n"
            "- Server environments often lack display capabilities\n\n"
            "**Pattern:** Wrap optional imports in try/except at the point "
            "of use, not at the top of the file."
        ))

        extra.extend(try_it(
            "Add a `export_markdown(self, results, path)` method to "
            "EnhancedReporter that outputs the analysis as a Markdown table. "
            "Example output:\n"
            "```\n"
            "| Metric | Value |\n"
            "|--------|-------|\n"
            "| mean   | 52.4  |\n"
            "| std    | 25.5  |\n"
            "```"
        ))

        extra.extend(try_it(
            "Modify the full pipeline to take a single config dict and "
            "run all 5 components automatically. The config should specify "
            "data path, cleaning rules, analysis types, and output paths."
        ))

    elif week_num == 6:
        extra.append(md(
            "---\n## Section 4: Exception-Aware Components"
        ))
        extra.append(code(
            "class ValidatingDataSource:\n"
            "    \"\"\"DataSource that raises domain exceptions.\"\"\"\n"
            "\n"
            "    def __init__(self, path, required_columns=None):\n"
            "        self.path = path\n"
            "        self.required_columns = required_columns or []\n"
            "\n"
            "    def load(self):\n"
            "        # Simulate loading\n"
            "        raw = [\n"
            "            {\"id\": 1, \"value\": 25.0},\n"
            "            {\"id\": 2, \"value\": 30.0},\n"
            "        ]\n"
            "\n"
            "        if not raw:\n"
            "            raise EmptyDataError(\"load\")\n"
            "\n"
            "        if self.required_columns:\n"
            "            actual = list(raw[0].keys())\n"
            "            missing = set(self.required_columns) - set(actual)\n"
            "            if missing:\n"
            "                raise SchemaError(list(missing), actual)\n"
            "\n"
            "        print(\"Loaded \" + str(len(raw)) + \" rows\")\n"
            "        return raw\n"
            "\n"
            "\n"
            "# Happy path\n"
            "vds = ValidatingDataSource(\"data.csv\", required_columns=[\"id\", \"value\"])\n"
            "data = vds.load()\n"
            "print(\"Success:\", data)\n"
            "\n"
            "# Error path\n"
            "try:\n"
            "    bad = ValidatingDataSource(\"data.csv\", required_columns=[\"temperature\"])\n"
            "    bad.load()\n"
            "except SchemaError as e:\n"
            "    print(\"Caught: \" + str(e))\n"
            "    print(\"Missing columns:\", e.missing)"
        ))
        extra.append(expected_output(
            "Loaded 2 rows\n"
            "Success: [{'id': 1, 'value': 25.0}, {'id': 2, 'value': 30.0}]\n"
            "Caught: Schema mismatch: missing ['temperature']. Available: ['id', 'value']\n"
            "Missing columns: ['temperature']"
        ))

        extra.append(md(
            "---\n## Section 5: Exception-Safe Pipeline"
        ))
        extra.append(code(
            "class SafePipeline:\n"
            "    \"\"\"Pipeline that handles exceptions gracefully.\"\"\"\n"
            "\n"
            "    def __init__(self, source, cleaner):\n"
            "        self.source = source\n"
            "        self.cleaner = cleaner\n"
            "        self.errors = []\n"
            "\n"
            "    def run(self):\n"
            "        \"\"\"Run pipeline, collecting errors instead of crashing.\"\"\"\n"
            "        self.errors = []\n"
            "\n"
            "        # Step 1: Load\n"
            "        try:\n"
            "            data = self.source.load()\n"
            "        except PipelineError as e:\n"
            "            self.errors.append((\"load\", e))\n"
            "            print(\"LOAD FAILED: \" + str(e))\n"
            "            return None\n"
            "\n"
            "        # Step 2: Clean\n"
            "        try:\n"
            "            clean = self.cleaner(data)\n"
            "        except PipelineError as e:\n"
            "            self.errors.append((\"clean\", e))\n"
            "            print(\"CLEAN FAILED: \" + str(e))\n"
            "            return None\n"
            "\n"
            "        print(\"Pipeline completed successfully\")\n"
            "        return clean\n"
            "\n"
            "    def report_errors(self):\n"
            "        if not self.errors:\n"
            "            print(\"No errors\")\n"
            "            return\n"
            "        for stage, error in self.errors:\n"
            "            print(\"Error at \" + stage + \": \" + type(error).__name__\n"
            "                  + \" -- \" + str(error))\n"
            "\n"
            "\n"
            "# Test: successful run\n"
            "source = ValidatingDataSource(\"data.csv\", [\"id\", \"value\"])\n"
            "pipeline = SafePipeline(source, lambda d: [r for r in d if r.get('value', 0) > 0])\n"
            "result = pipeline.run()\n"
            "print(\"Result:\", result)\n"
            "print()\n"
            "\n"
            "# Test: error run\n"
            "bad_source = ValidatingDataSource(\"data.csv\", [\"temperature\"])\n"
            "bad_pipeline = SafePipeline(bad_source, lambda d: d)\n"
            "result = bad_pipeline.run()\n"
            "bad_pipeline.report_errors()"
        ))
        extra.append(expected_output(
            "Loaded 2 rows\n"
            "Pipeline completed successfully\n"
            "Result: [{'id': 1, 'value': 25.0}, {'id': 2, 'value': 30.0}]\n\n"
            "Loaded 2 rows\n"
            "LOAD FAILED: Schema mismatch: missing ['temperature']. ...\n"
            "Error at load: SchemaError -- ..."
        ))

        extra.extend(common_mistake(
            "Swallowing exceptions silently",
            (
                "# BAD: exception is caught but nothing is done about it!\n"
                "try:\n"
                "    data = validate_and_clean([], {})\n"
                "except:\n"
                "    pass  # silent failure -- data is undefined!\n"
                "\n"
                "try:\n"
                "    print(\"Data:\", data)  # NameError!\n"
                "except NameError as e:\n"
                "    print(\"ERROR: data was never defined because exception was swallowed\")"
            ),
            (
                "# GOOD: handle the exception properly\n"
                "try:\n"
                "    data = validate_and_clean([], {})\n"
                "except EmptyDataError as e:\n"
                "    print(\"Cannot proceed: \" + str(e))\n"
                "    data = []  # provide a fallback\n"
                "\n"
                "print(\"Data:\", data)  # safe: data is always defined"
            ),
            "Catching an exception with `except: pass` is the worst pattern. "
            "It hides bugs, makes debugging impossible, and can leave variables "
            "undefined. Always either handle the exception (log, fallback) or "
            "let it propagate."
        ))

        extra.append(debugging_tip(
            "Reading exception tracebacks",
            "When you see an error traceback, read it **bottom to top**:\n\n"
            "1. The LAST line tells you what went wrong (the exception type and message)\n"
            "2. The lines ABOVE show where it happened (file, line number, function)\n"
            "3. Follow the chain upward to find the ROOT cause\n\n"
            "Custom exceptions make step 1 much more informative:\n"
            "- `ValueError: bad data` -- useless\n"
            "- `SchemaError: missing ['temperature']. Available: ['id', 'value']` -- actionable!"
        ))

        extra.extend(try_it(
            "Add a `ConfigError` to the hierarchy. It should store "
            "the config key that is problematic and a description. "
            "Use it in a `validate_config(config)` function."
        ))

        extra.extend(try_it(
            "Create a `RetryablePipeline` that, when a load fails, "
            "waits and retries up to 3 times before giving up. "
            "Hint: use a for loop with try/except inside."
        ))

    elif week_num == 7:
        extra.append(md(
            "---\n## Section 3: SRP Case Study -- Refactoring"
        ))
        extra.append(md(
            "Here is a real refactoring example. We start with a class "
            "that violates SRP and split it into proper components."
        ))
        extra.append(code(
            "# BEFORE: One class does loading AND cleaning AND reporting\n"
            "class MessyProcessor:\n"
            "    def __init__(self, path):\n"
            "        self.path = path\n"
            "        self.data = None\n"
            "        self.clean_data = None\n"
            "        self.report = None\n"
            "\n"
            "    def process(self):\n"
            "        # Loading (responsibility 1)\n"
            "        self.data = [{\"v\": 10}, {\"v\": -5}, {\"v\": 30}, {\"v\": None}]\n"
            "        print(\"Loaded\")\n"
            "\n"
            "        # Cleaning (responsibility 2)\n"
            "        self.clean_data = [r for r in self.data\n"
            "                           if isinstance(r.get(\"v\"), (int, float)) and r[\"v\"] >= 0]\n"
            "        print(\"Cleaned\")\n"
            "\n"
            "        # Reporting (responsibility 3)\n"
            "        vals = [r[\"v\"] for r in self.clean_data]\n"
            "        self.report = {\"count\": len(vals), \"mean\": sum(vals)/len(vals)}\n"
            "        print(\"Report:\", self.report)\n"
            "\n"
            "m = MessyProcessor(\"data.csv\")\n"
            "m.process()\n"
            "print(\"\\n3 responsibilities in 1 class = SRP violation!\")"
        ))
        extra.append(expected_output(
            "Loaded\n"
            "Cleaned\n"
            "Report: {'count': 2, 'mean': 20.0}\n\n"
            "3 responsibilities in 1 class = SRP violation!"
        ))

        extra.append(md("### AFTER: Refactored into 3 classes"))
        extra.append(code(
            "# AFTER: Each class has ONE responsibility\n"
            "class Loader:\n"
            "    def load(self, path):\n"
            "        data = [{\"v\": 10}, {\"v\": -5}, {\"v\": 30}, {\"v\": None}]\n"
            "        print(\"Loaded \" + str(len(data)) + \" rows\")\n"
            "        return data\n"
            "\n"
            "class Cleaner:\n"
            "    def clean(self, data):\n"
            "        result = [r for r in data\n"
            "                  if isinstance(r.get(\"v\"), (int, float)) and r[\"v\"] >= 0]\n"
            "        print(\"Cleaned: \" + str(len(data)) + \" -> \" + str(len(result)))\n"
            "        return result\n"
            "\n"
            "class Reporter:\n"
            "    def report(self, data):\n"
            "        vals = [r[\"v\"] for r in data]\n"
            "        result = {\"count\": len(vals), \"mean\": sum(vals)/len(vals)} if vals else {}\n"
            "        print(\"Report: \" + str(result))\n"
            "        return result\n"
            "\n"
            "# Compose\n"
            "raw = Loader().load(\"data.csv\")\n"
            "clean = Cleaner().clean(raw)\n"
            "report = Reporter().report(clean)\n"
            "print(\"\\n3 classes, 3 responsibilities = SRP satisfied!\")"
        ))
        extra.append(expected_output(
            "Loaded 4 rows\n"
            "Cleaned: 4 -> 2\n"
            "Report: {'count': 2, 'mean': 20.0}\n\n"
            "3 classes, 3 responsibilities = SRP satisfied!"
        ))

        extra.append(md(
            "---\n## Section 4: OCP Case Study -- Adding Features"
        ))
        extra.append(code(
            "# OCP in action: add new analysis types without changing existing code\n"
            "\n"
            "class AnalyzerBase:\n"
            "    def analyze(self, values):\n"
            "        raise NotImplementedError\n"
            "\n"
            "class SumAnalyzer(AnalyzerBase):\n"
            "    def analyze(self, values):\n"
            "        return {\"sum\": sum(values)} if values else {}\n"
            "\n"
            "class ProductAnalyzer(AnalyzerBase):\n"
            "    def analyze(self, values):\n"
            "        if not values:\n"
            "            return {}\n"
            "        result = 1\n"
            "        for v in values:\n"
            "            result *= v\n"
            "        return {\"product\": result}\n"
            "\n"
            "# Each new analyzer = new class, zero changes to existing code\n"
            "values = [2, 3, 5]\n"
            "for a in [SumAnalyzer(), ProductAnalyzer()]:\n"
            "    print(type(a).__name__ + \":\", a.analyze(values))\n"
            "\n"
            "print(\"\\nAdded 2 analyzers. Existing code: untouched.\")"
        ))
        extra.append(expected_output(
            "SumAnalyzer: {'sum': 10}\n"
            "ProductAnalyzer: {'product': 30}\n\n"
            "Added 2 analyzers. Existing code: untouched."
        ))

        extra.extend(procedural_vs_oop(
            "Adding New Analysis Types",
            (
                "# PROCEDURAL: must modify existing function\n"
                "def analyze(values, analysis_type):\n"
                "    if analysis_type == 'mean':\n"
                "        return sum(values) / len(values)\n"
                "    elif analysis_type == 'sum':\n"
                "        return sum(values)\n"
                "    # Adding 'product' means adding ANOTHER elif here!\n"
                "    # elif analysis_type == 'product':\n"
                "    #     ...\n"
                "    else:\n"
                "        raise ValueError('Unknown: ' + analysis_type)\n"
                "\n"
                "print(analyze([2, 3, 5], 'mean'))"
            ),
            (
                "# OOP (OCP): new class, no changes to existing code\n"
                "class ProductAnalyzer(AnalyzerBase):\n"
                "    def analyze(self, values):\n"
                "        result = 1\n"
                "        for v in values:\n"
                "            result *= v\n"
                "        return {'product': result}\n"
                "\n"
                "# Just add to the list!\n"
                "analyzers.append(ProductAnalyzer())"
            ),
            "In the procedural version, every new analysis type requires "
            "modifying the existing `analyze()` function. With OCP, you "
            "create a new class and the existing code never changes."
        ))

        extra.extend(try_it(
            "Identify which SOLID principle is violated in this code and fix it:\n\n"
            "```python\n"
            "class UserManager:\n"
            "    def create_user(self, name, email): ...\n"
            "    def delete_user(self, user_id): ...\n"
            "    def send_welcome_email(self, email): ...  # ???\n"
            "    def generate_report(self): ...  # ???\n"
            "```"
        ))

        extra.extend(try_it(
            "Refactor this code to satisfy SRP:\n"
            "```python\n"
            "class FileProcessor:\n"
            "    def read_file(self, path): ...\n"
            "    def parse_csv(self, text): ...\n"
            "    def validate_data(self, data): ...\n"
            "    def save_to_database(self, data): ...\n"
            "    def send_notification(self, message): ...\n"
            "```\n"
            "How many classes should this be? What should each one do?"
        ))

        extra.append(debugging_tip(
            "How to spot SRP violations",
            "Ask yourself: **'If I need to change X, do I also need to change Y?'**\n\n"
            "If changing the email format requires touching the same class "
            "that does data analysis, that class has multiple responsibilities.\n\n"
            "**Red flags:**\n"
            "- Class has more than ~5 public methods\n"
            "- Class name includes 'And' (e.g., LoaderAndCleaner)\n"
            "- Class has methods that do not use the same attributes\n"
            "- You cannot describe the class's job in one sentence"
        ))

    elif week_num == 8:
        extra.append(md(
            "---\n## Section 5: Advanced Strategy Composition"
        ))
        extra.append(code(
            "# Strategies can be combined in different ways\n"
            "\n"
            "# OR logic: keep if ANY strategy says keep\n"
            "class OrCleaner:\n"
            "    \"\"\"Keep rows that pass ANY strategy (instead of ALL).\"\"\"\n"
            "    def __init__(self, strategies=None):\n"
            "        self.strategies = strategies or []\n"
            "\n"
            "    def clean(self, data):\n"
            "        return [row for row in data\n"
            "                if any(s.should_keep(row) for s in self.strategies)]\n"
            "\n"
            "\n"
            "# Example: keep rows that are EITHER in range OR have status 'ok'\n"
            "class KeepStatus(CleaningStrategy):\n"
            "    def __init__(self, column, value):\n"
            "        self.column = column\n"
            "        self.value = value\n"
            "    def should_keep(self, row):\n"
            "        return row.get(self.column) == self.value\n"
            "\n"
            "\n"
            "data = [\n"
            "    {\"id\": 1, \"value\": 50, \"status\": \"ok\"},\n"
            "    {\"id\": 2, \"value\": 200, \"status\": \"ok\"},     # out of range but ok status\n"
            "    {\"id\": 3, \"value\": 30, \"status\": \"error\"},    # in range but error status\n"
            "    {\"id\": 4, \"value\": 200, \"status\": \"error\"},   # both bad\n"
            "]\n"
            "\n"
            "# AND logic (default): must pass BOTH\n"
            "and_cleaner = ConfigurableCleaner([\n"
            "    DropOutOfRange(\"value\", 0, 100),\n"
            "    KeepStatus(\"status\", \"ok\"),\n"
            "])\n"
            "print(\"AND (must pass both):\")\n"
            "and_result = and_cleaner.clean(data)\n"
            "for r in and_result:\n"
            "    print(\"  \", r)\n"
            "\n"
            "# OR logic: must pass at least one\n"
            "or_cleaner = OrCleaner([\n"
            "    DropOutOfRange(\"value\", 0, 100),\n"
            "    KeepStatus(\"status\", \"ok\"),\n"
            "])\n"
            "print(\"\\nOR (must pass at least one):\")\n"
            "or_result = or_cleaner.clean(data)\n"
            "for r in or_result:\n"
            "    print(\"  \", r)"
        ))
        extra.append(expected_output(
            "AND (must pass both):\n"
            "   {'id': 1, 'value': 50, 'status': 'ok'}\n\n"
            "OR (must pass at least one):\n"
            "   {'id': 1, 'value': 50, 'status': 'ok'}\n"
            "   {'id': 2, 'value': 200, 'status': 'ok'}\n"
            "   {'id': 3, 'value': 30, 'status': 'error'}"
        ))

        extra.append(ascii_diagram(
            "Strategy Pattern Structure",
            "    +---------------------+\n"
            "    | ConfigurableCleaner |\n"
            "    +---------------------+\n"
            "    | - strategies: list  |\n"
            "    +---------------------+\n"
            "    | + add_strategy(s)   |\n"
            "    | + clean(data)       |\n"
            "    +---------------------+\n"
            "              |\n"
            "              | has-many\n"
            "              v\n"
            "    +---------------------+\n"
            "    | CleaningStrategy    |  <--- interface\n"
            "    +---------------------+\n"
            "    | + should_keep(row)  |\n"
            "    +---------------------+\n"
            "        /    |    \\\\\n"
            "       /     |     \\\\\n"
            "  +--------+ +-------+ +-----------+\n"
            "  |DropMiss| |DropOOR| |DropDupes  |\n"
            "  +--------+ +-------+ +-----------+"
        ))

        extra.extend(try_it(
            "Create a `NegatingStrategy` that wraps any other strategy "
            "and reverses its decision:\n"
            "```python\n"
            "keep_low = DropOutOfRange('value', 0, 50)  # keeps 0-50\n"
            "keep_high = NegatingStrategy(keep_low)      # keeps everything EXCEPT 0-50\n"
            "```"
        ))

        extra.extend(common_mistake(
            "Strategy with mutable state between runs",
            (
                "class BuggyDedup(CleaningStrategy):\n"
                "    def __init__(self, column):\n"
                "        self.column = column\n"
                "        self._seen = set()  # shared across all runs!\n"
                "\n"
                "    def should_keep(self, row):\n"
                "        val = row.get(self.column)\n"
                "        if val in self._seen:\n"
                "            return False\n"
                "        self._seen.add(val)\n"
                "        return True\n"
                "\n"
                "dedup = BuggyDedup('id')\n"
                "data = [{\"id\": 1}, {\"id\": 2}]\n"
                "\n"
                "# First run\n"
                "cleaner = ConfigurableCleaner([dedup])\n"
                "print(\"Run 1:\", len(cleaner.clean(data)), \"rows\")\n"
                "\n"
                "# Second run -- BUG: _seen still has {1, 2} from first run!\n"
                "print(\"Run 2:\", len(cleaner.clean(data)), \"rows\")  # 0!"
            ),
            (
                "class FixedDedup(CleaningStrategy):\n"
                "    def __init__(self, column):\n"
                "        self.column = column\n"
                "        self._seen = set()\n"
                "\n"
                "    def reset(self):\n"
                "        self._seen = set()\n"
                "\n"
                "    def should_keep(self, row):\n"
                "        val = row.get(self.column)\n"
                "        if val in self._seen:\n"
                "            return False\n"
                "        self._seen.add(val)\n"
                "        return True\n"
                "\n"
                "# Or better: reset in the cleaner before each run\n"
                "print(\"Fix: add reset() method and call it before each clean run\")"
            ),
            "Strategies with mutable state (sets, counters) must be reset "
            "between runs. Otherwise, the second run 'remembers' the first "
            "run's state. Either add a `reset()` method or create a new "
            "strategy instance for each run."
        ))

    elif week_num == 9:
        extra.append(md(
            "---\n## Section 5: Registry with Metadata"
        ))
        extra.append(code(
            "class EnhancedFactory:\n"
            "    \"\"\"Factory that stores metadata about registered classes.\"\"\"\n"
            "\n"
            "    _registry = {}\n"
            "\n"
            "    @classmethod\n"
            "    def register(cls, name, klass, description=\"\", author=\"\"):\n"
            "        cls._registry[name] = {\n"
            "            \"class\": klass,\n"
            "            \"description\": description,\n"
            "            \"author\": author,\n"
            "        }\n"
            "\n"
            "    @classmethod\n"
            "    def create(cls, name, **kwargs):\n"
            "        if name not in cls._registry:\n"
            "            raise ValueError(\"Unknown: \" + name)\n"
            "        return cls._registry[name][\"class\"](**kwargs)\n"
            "\n"
            "    @classmethod\n"
            "    def describe(cls):\n"
            "        for name, info in cls._registry.items():\n"
            "            print(name + \" (\" + info[\"class\"].__name__ + \")\")\n"
            "            if info[\"description\"]:\n"
            "                print(\"  \" + info[\"description\"])\n"
            "\n"
            "\n"
            "EnhancedFactory.register(\"mean\", MeanAnalyzer,\n"
            "    description=\"Computes arithmetic mean\", author=\"core\")\n"
            "EnhancedFactory.register(\"std\", StdAnalyzer,\n"
            "    description=\"Computes standard deviation\", author=\"core\")\n"
            "EnhancedFactory.register(\"events\", EventAnalyzer,\n"
            "    description=\"Counts events above threshold\", author=\"core\")\n"
            "\n"
            "print(\"=== Registered Analyzers ===\")\n"
            "EnhancedFactory.describe()"
        ))
        extra.append(expected_output(
            "=== Registered Analyzers ===\n"
            "mean (MeanAnalyzer)\n"
            "  Computes arithmetic mean\n"
            "std (StdAnalyzer)\n"
            "  Computes standard deviation\n"
            "events (EventAnalyzer)\n"
            "  Counts events above threshold"
        ))

        extra.append(md(
            "---\n## Section 6: Decorator-Based Registration"
        ))
        extra.append(code(
            "# Advanced: register using a decorator\n"
            "class DecoratorFactory:\n"
            "    _registry = {}\n"
            "\n"
            "    @classmethod\n"
            "    def register(cls, name):\n"
            "        \"\"\"Decorator that registers a class.\"\"\"\n"
            "        def decorator(klass):\n"
            "            cls._registry[name] = klass\n"
            "            return klass\n"
            "        return decorator\n"
            "\n"
            "    @classmethod\n"
            "    def create(cls, name, **kw):\n"
            "        return cls._registry[name](**kw)\n"
            "\n"
            "\n"
            "# Usage: just add the decorator!\n"
            "@DecoratorFactory.register(\"quick_mean\")\n"
            "class QuickMeanAnalyzer:\n"
            "    def analyze(self, values):\n"
            "        return {\"mean\": sum(values)/len(values)} if values else {}\n"
            "\n"
            "\n"
            "@DecoratorFactory.register(\"quick_count\")\n"
            "class QuickCountAnalyzer:\n"
            "    def analyze(self, values):\n"
            "        return {\"count\": len(values)}\n"
            "\n"
            "\n"
            "# No explicit register call needed!\n"
            "print(\"Registered:\", list(DecoratorFactory._registry.keys()))\n"
            "a = DecoratorFactory.create(\"quick_mean\")\n"
            "print(\"Result:\", a.analyze([10, 20, 30]))"
        ))
        extra.append(expected_output(
            "Registered: ['quick_mean', 'quick_count']\n"
            "Result: {'mean': 20.0}"
        ))

        extra.extend(try_it(
            "Create a `CleanerFactory` that works the same way as "
            "AnalyzerFactory but for cleaning strategies. Register "
            "`DropMissing`, `DropOutOfRange`, and `DropDuplicates`."
        ))

        extra.extend(common_mistake(
            "Factory returning class instead of instance",
            (
                "class BadFactory:\n"
                "    _registry = {\"mean\": MeanAnalyzer}\n"
                "\n"
                "    @classmethod\n"
                "    def create(cls, name):\n"
                "        return cls._registry[name]  # BUG: returns the CLASS, not an instance!\n"
                "\n"
                "result = BadFactory.create(\"mean\")\n"
                "print(type(result))  # <class 'type'> -- it's the class itself!\n"
                "# result.analyze([1,2,3])  # TypeError: missing self!"
            ),
            (
                "class GoodFactory:\n"
                "    _registry = {\"mean\": MeanAnalyzer}\n"
                "\n"
                "    @classmethod\n"
                "    def create(cls, name, **kw):\n"
                "        return cls._registry[name](**kw)  # FIXED: call the class!\n"
                "\n"
                "result = GoodFactory.create(\"mean\")\n"
                "print(type(result))  # MeanAnalyzer instance\n"
                "print(result.analyze([1, 2, 3]))"
            ),
            "The registry stores CLASSES, not instances. You must CALL the "
            "class (with parentheses and arguments) to create an instance. "
            "`cls._registry[name]` gives you the class; "
            "`cls._registry[name](**kw)` gives you an instance."
        ))

    elif week_num == 10:
        extra.append(md(
            "---\n## Section 5: Test-Driven Development (TDD)\n\n"
            "TDD means writing the TEST first, THEN writing the code to "
            "make it pass. The cycle is:\n\n"
            "1. **Red:** Write a test that fails\n"
            "2. **Green:** Write the minimum code to pass\n"
            "3. **Refactor:** Clean up the code\n\n"
            "Let us practice with a new feature."
        ))
        extra.append(md("### TDD Example: Building a RangeChecker"))
        extra.append(code(
            "# Step 1 (RED): Write the test FIRST\n"
            "def test_range_checker_in_range():\n"
            "    checker = RangeChecker(0, 100)\n"
            "    assert checker.check(50) == True\n"
            "\n"
            "def test_range_checker_below():\n"
            "    checker = RangeChecker(0, 100)\n"
            "    assert checker.check(-10) == False\n"
            "\n"
            "def test_range_checker_above():\n"
            "    checker = RangeChecker(0, 100)\n"
            "    assert checker.check(200) == False\n"
            "\n"
            "def test_range_checker_boundary():\n"
            "    checker = RangeChecker(0, 100)\n"
            "    assert checker.check(0) == True    # inclusive\n"
            "    assert checker.check(100) == True   # inclusive\n"
            "\n"
            "# These tests FAIL because RangeChecker doesn't exist yet!\n"
            "try:\n"
            "    test_range_checker_in_range()\n"
            "except NameError:\n"
            "    print(\"RED: RangeChecker not defined yet (expected!)\")"
        ))
        extra.append(expected_output("RED: RangeChecker not defined yet (expected!)"))

        extra.append(code(
            "# Step 2 (GREEN): Write minimum code to pass\n"
            "class RangeChecker:\n"
            "    def __init__(self, low, high):\n"
            "        self.low = low\n"
            "        self.high = high\n"
            "\n"
            "    def check(self, value):\n"
            "        return self.low <= value <= self.high\n"
            "\n"
            "\n"
            "# Run tests\n"
            "test_range_checker_in_range()\n"
            "print(\"[PASS] test_range_checker_in_range\")\n"
            "test_range_checker_below()\n"
            "print(\"[PASS] test_range_checker_below\")\n"
            "test_range_checker_above()\n"
            "print(\"[PASS] test_range_checker_above\")\n"
            "test_range_checker_boundary()\n"
            "print(\"[PASS] test_range_checker_boundary\")\n"
            "print(\"\\nGREEN: All tests pass!\")"
        ))
        extra.append(expected_output(
            "[PASS] test_range_checker_in_range\n"
            "[PASS] test_range_checker_below\n"
            "[PASS] test_range_checker_above\n"
            "[PASS] test_range_checker_boundary\n\n"
            "GREEN: All tests pass!"
        ))

        extra.append(md(
            "---\n## Section 6: Testing Edge Cases\n\n"
            "Good tests cover edge cases. Think about:\n"
            "- Empty input\n"
            "- None/null values\n"
            "- Boundary values (exactly at min/max)\n"
            "- Very large/small numbers\n"
            "- Wrong types"
        ))
        extra.append(code(
            "def test_edge_empty():\n"
            "    cleaner = ConfigurableCleaner()\n"
            "    assert cleaner.clean([]) == []\n"
            "\n"
            "def test_edge_all_filtered():\n"
            "    cleaner = ConfigurableCleaner([DropOutOfRange(\"value\", 0, 10)])\n"
            "    data = [{\"value\": 100}, {\"value\": 200}]\n"
            "    assert cleaner.clean(data) == []\n"
            "\n"
            "def test_edge_none_filtered():\n"
            "    cleaner = ConfigurableCleaner([DropOutOfRange(\"value\", 0, 1000)])\n"
            "    data = [{\"value\": 50}, {\"value\": 100}]\n"
            "    result = cleaner.clean(data)\n"
            "    assert len(result) == 2\n"
            "\n"
            "def test_edge_missing_column():\n"
            "    s = DropOutOfRange(\"value\", 0, 100)\n"
            "    # Row without 'value' column -- should it be kept or dropped?\n"
            "    result = s.should_keep({\"other\": 50})\n"
            "    print(\"Missing column result:\", result)\n"
            "\n"
            "test_edge_empty()\n"
            "print(\"[PASS] test_edge_empty\")\n"
            "test_edge_all_filtered()\n"
            "print(\"[PASS] test_edge_all_filtered\")\n"
            "test_edge_none_filtered()\n"
            "print(\"[PASS] test_edge_none_filtered\")\n"
            "test_edge_missing_column()\n"
            "print(\"[PASS] test_edge_missing_column\")"
        ))
        extra.append(expected_output(
            "[PASS] test_edge_empty\n"
            "[PASS] test_edge_all_filtered\n"
            "[PASS] test_edge_none_filtered\n"
            "Missing column result: True\n"
            "[PASS] test_edge_missing_column"
        ))

        extra.extend(try_it(
            "Use TDD to build a `Validator` class:\n"
            "1. Write 3 tests first (for valid input, empty input, invalid input)\n"
            "2. Then implement the Validator to make them pass\n"
            "3. Add 2 more edge case tests"
        ))

        extra.append(design_decision(
            "What to test and what not to test",
            "**Test:**\n"
            "- Public methods (the API your other code calls)\n"
            "- Edge cases (empty, None, boundaries)\n"
            "- Error conditions (exceptions should be raised)\n"
            "- Integration (components working together)\n\n"
            "**Do not test:**\n"
            "- Private methods (starting with _) directly\n"
            "- Third-party libraries (matplotlib, json)\n"
            "- Trivial getters/setters\n"
            "- Implementation details that might change"
        ))

    elif week_num == 11:
        extra.append(md(
            "---\n## Section 5: Relative Imports"
        ))
        extra.append(code(
            "# Inside a package, use RELATIVE imports\n"
            "\n"
            "# In core/cleaner.py:\n"
            "# from .dataset import Dataset        # from same package\n"
            "# from .exceptions import PipelineError  # from same package\n"
            "\n"
            "# In core/__init__.py:\n"
            "# from .cleaner import BaseCleaner    # from same package\n"
            "\n"
            "# NEVER use absolute paths to import siblings:\n"
            "# BAD: from project_name.core.dataset import Dataset\n"
            "# GOOD: from .dataset import Dataset\n"
            "\n"
            "print(\"Relative import rules:\")\n"
            "print(\"  . = current package\")\n"
            "print(\"  .. = parent package\")\n"
            "print(\"  .module = sibling module\")\n"
            "print(\"  ..other = uncle module\")"
        ))
        extra.append(expected_output(
            "Relative import rules:\n"
            "  . = current package\n"
            "  .. = parent package\n"
            "  .module = sibling module\n"
            "  ..other = uncle module"
        ))

        extra.append(md(
            "---\n## Section 6: Common Import Mistakes"
        ))
        extra.extend(common_mistake(
            "Circular imports",
            (
                "# BAD: circular dependency\n"
                "# In cleaner.py: from .analyzer import Analyzer\n"
                "# In analyzer.py: from .cleaner import Cleaner\n"
                "# -> ImportError: cannot import name 'Analyzer'\n"
                "\n"
                "print(\"Circular import: A imports B, B imports A\")\n"
                "print(\"Python cannot resolve this!\")"
            ),
            (
                "# FIXES for circular imports:\n"
                "\n"
                "# Fix 1: Import inside the function that needs it\n"
                "# def my_method(self):\n"
                "#     from .analyzer import Analyzer\n"
                "#     ...\n"
                "\n"
                "# Fix 2: Restructure so the shared type is in a separate module\n"
                "# Put Dataset in dataset.py, import it from both cleaner.py and analyzer.py\n"
                "\n"
                "# Fix 3: Use __init__.py to control import order\n"
                "\n"
                "print(\"Best fix: restructure to eliminate circular dependency\")"
            ),
            "Circular imports happen when two modules import each other. "
            "The best fix is to restructure: extract shared classes into "
            "a separate module that both can import."
        ))

        extra.extend(try_it(
            "Design the `__init__.py` for a `strategies/` sub-package that "
            "contains `cleaning.py` and `analysis.py`. What should be "
            "exported? What should stay internal?"
        ))

        extra.extend(try_it(
            "Sketch (as comments) the ideal file structure for your track's "
            "project. Include `src/`, `tests/`, and `notebooks/`. Mark "
            "which files have `__init__.py`."
        ))

        extra.append(design_decision(
            "Flat vs nested package structure",
            "**Flat** (few modules, simple project):\n"
            "```\n"
            "src/project/\n"
            "    __init__.py\n"
            "    loader.py\n"
            "    cleaner.py\n"
            "    analyzer.py\n"
            "```\n\n"
            "**Nested** (many modules, complex project):\n"
            "```\n"
            "src/project/\n"
            "    __init__.py\n"
            "    core/\n"
            "        __init__.py\n"
            "        ...\n"
            "    strategies/\n"
            "        __init__.py\n"
            "        ...\n"
            "```\n\n"
            "**Rule of thumb:** Start flat. Only nest when a directory has "
            "more than ~8 files or when you have clear sub-domains."
        ))

    elif week_num == 12:
        extra.append(md(
            "---\n## Section 3: Your Turn -- Second Plugin\n\n"
            "Now add a SECOND plugin: a `VarianceAnalyzer`."
        ))
        extra.append(code(
            "# YOUR TASK: Create VarianceAnalyzer\n"
            "# 1. Inherit from AnalyzerBase\n"
            "# 2. Implement analyze(values) -> {\"variance\": ...}\n"
            "# 3. Register with factory\n"
            "# 4. Write 3 tests\n"
            "\n"
            "# YOUR CODE HERE\n"
        ))

        extra.append(md("### Solution"))
        extra.append(code(
            "class VarianceAnalyzer(AnalyzerBase):\n"
            "    def analyze(self, values):\n"
            "        if not values:\n"
            "            return {}\n"
            "        m = sum(values) / len(values)\n"
            "        var = sum((x - m) ** 2 for x in values) / len(values)\n"
            "        return {\"variance\": round(var, 4)}\n"
            "\n"
            "AnalyzerFactory.register(\"variance\", VarianceAnalyzer)\n"
            "\n"
            "# Tests\n"
            "def test_variance_normal():\n"
            "    va = VarianceAnalyzer()\n"
            "    r = va.analyze([10, 20, 30])\n"
            "    assert \"variance\" in r\n"
            "    assert r[\"variance\"] > 0\n"
            "\n"
            "def test_variance_empty():\n"
            "    assert VarianceAnalyzer().analyze([]) == {}\n"
            "\n"
            "def test_variance_uniform():\n"
            "    r = VarianceAnalyzer().analyze([5, 5, 5])\n"
            "    assert r[\"variance\"] == 0\n"
            "\n"
            "test_variance_normal()\n"
            "print(\"[PASS] test_variance_normal\")\n"
            "test_variance_empty()\n"
            "print(\"[PASS] test_variance_empty\")\n"
            "test_variance_uniform()\n"
            "print(\"[PASS] test_variance_uniform\")\n"
            "print()\n"
            "print(\"Available:\", AnalyzerFactory.list_available())"
        ))
        extra.append(expected_output(
            "[PASS] test_variance_normal\n"
            "[PASS] test_variance_empty\n"
            "[PASS] test_variance_uniform\n\n"
            "Available: ['mean', 'std', 'events', 'percentile', 'variance']"
        ))

        extra.append(md(
            "---\n## Section 4: Full Pipeline with Plugins"
        ))
        extra.append(code(
            "# Run ALL registered analyzers on sample data\n"
            "values = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]\n"
            "\n"
            "print(\"=== Running all registered analyzers ===\")\n"
            "all_results = {}\n"
            "for name in AnalyzerFactory.list_available():\n"
            "    try:\n"
            "        a = AnalyzerFactory.create(name)\n"
            "        result = a.analyze(values)\n"
            "        all_results[name] = result\n"
            "        print(name + \": \" + str(result))\n"
            "    except TypeError:\n"
            "        # Some analyzers need params (like EventAnalyzer)\n"
            "        print(name + \": (needs parameters, skipping)\")\n"
            "\n"
            "print()\n"
            "print(\"Total analyzers:\", len(AnalyzerFactory.list_available()))\n"
            "print(\"All added without modifying core!\")"
        ))
        extra.append(expected_output(
            "=== Running all registered analyzers ===\n"
            "mean: {'mean': 55.0}\n"
            "std: {'std': 28.7228}\n"
            "events: {'events_above': 5}\n"
            "percentile: {'p25': 30, 'p50': 60, 'p75': 80}\n"
            "variance: {'variance': 825.0}\n\n"
            "Total analyzers: 5\n"
            "All added without modifying core!"
        ))

        extra.extend(try_it(
            "Create a third plugin: `MedianAnalyzer`. Register it, test it, "
            "and verify the total count increases."
        ))

    elif week_num == 13:
        extra.append(md(
            "---\n## Section 5: Docstring Standards\n\n"
            "Every public class and method should have a docstring. "
            "Follow this format:"
        ))
        extra.append(code(
            "class ExampleComponent:\n"
            "    \"\"\"One-line summary of the class.\n"
            "\n"
            "    Longer description if needed. Explains the purpose,\n"
            "    when to use it, and any important behavior.\n"
            "\n"
            "    Attributes:\n"
            "        config (dict): Configuration dictionary.\n"
            "        results (dict): Analysis results after run.\n"
            "    \"\"\"\n"
            "\n"
            "    def __init__(self, config):\n"
            "        \"\"\"Initialize the component.\n"
            "\n"
            "        Args:\n"
            "            config (dict): Configuration with keys:\n"
            "                - 'value_column' (str): Column to analyze.\n"
            "                - 'threshold' (float, optional): Event threshold.\n"
            "        \"\"\"\n"
            "        self.config = config\n"
            "        self.results = {}\n"
            "\n"
            "    def run(self, dataset):\n"
            "        \"\"\"Run analysis on the dataset.\n"
            "\n"
            "        Args:\n"
            "            dataset (Dataset): Clean dataset to analyze.\n"
            "\n"
            "        Returns:\n"
            "            dict: Analysis results with guaranteed keys:\n"
            "                - 'count' (int): Number of values analyzed.\n"
            "                - 'mean' (float): Arithmetic mean.\n"
            "\n"
            "        Raises:\n"
            "            EmptyDataError: If dataset has no rows.\n"
            "        \"\"\"\n"
            "        pass\n"
            "\n"
            "\n"
            "# Check docstrings\n"
            "print(ExampleComponent.__doc__)\n"
            "print()\n"
            "print(ExampleComponent.__init__.__doc__)"
        ))

        extra.append(md(
            "---\n## Section 6: API Stability Rules"
        ))
        extra.append(code(
            "rules = [\n"
            "    \"1. Do NOT rename public methods\",\n"
            "    \"2. Do NOT change method signatures (parameter names/order)\",\n"
            "    \"3. Do NOT change return types\",\n"
            "    \"4. Do NOT remove dictionary keys from results\",\n"
            "    \"5. You CAN add new optional parameters (with defaults)\",\n"
            "    \"6. You CAN add new keys to result dictionaries\",\n"
            "    \"7. You CAN add new methods\",\n"
            "    \"8. You CAN fix bugs in existing methods\",\n"
            "    \"9. You CAN improve performance\",\n"
            "    \"10. You CAN add new classes/plugins\",\n"
            "]\n"
            "\n"
            "print(\"=== API Stability Rules (Post-Freeze) ===\")\n"
            "for rule in rules:\n"
            "    print(\"  \" + rule)"
        ))
        extra.append(expected_output(
            "=== API Stability Rules (Post-Freeze) ===\n"
            "  1. Do NOT rename public methods\n"
            "  2. Do NOT change method signatures ...\n"
            "  ... (10 rules)"
        ))

        extra.extend(try_it(
            "Review your project's public API. For each component, write:\n"
            "1. The method signature\n"
            "2. The expected input type\n"
            "3. The expected output type\n"
            "4. Any exceptions it can raise"
        ))

    elif week_num == 14:
        extra.append(md(
            "---\n## Section 5: Live Coding Demo Script\n\n"
            "Follow this script during your demo presentation."
        ))
        extra.append(code(
            "demo_script = \"\"\"\n"
            "=== v3 Demo Script ===\n"
            "\n"
            "1. SHOW: Project structure (ls -R src/)\n"
            "2. SHOW: Config file (cat config.yaml or config.json)\n"
            "3. RUN: Full pipeline (python -m project_name)\n"
            "4. SHOW: Output files (data/cleaned/, reports/)\n"
            "5. LIVE CODE: Add a new analyzer plugin\n"
            "   a. Create the class\n"
            "   b. Register with factory\n"
            "   c. Update config\n"
            "   d. Run pipeline again\n"
            "   e. Show new results in report\n"
            "6. RUN: Test suite (pytest tests/ -v)\n"
            "7. EXPLAIN: One design decision\n"
            "8. Q&A\n"
            "\n"
            "Time: ~10 minutes per student\n"
            "\"\"\"\n"
            "print(demo_script)"
        ))

        extra.append(md(
            "---\n## Section 6: Architecture Comparison: v2 vs v3"
        ))
        extra.append(code(
            "comparison = {\n"
            "    \"Code organization\": {\n"
            "        \"v2\": \"Functions in one file\",\n"
            "        \"v3\": \"Classes in separate modules\",\n"
            "    },\n"
            "    \"Adding features\": {\n"
            "        \"v2\": \"Modify existing functions\",\n"
            "        \"v3\": \"Add new classes (OCP)\",\n"
            "    },\n"
            "    \"Error handling\": {\n"
            "        \"v2\": \"Generic ValueError/print\",\n"
            "        \"v3\": \"Domain exceptions with context\",\n"
            "    },\n"
            "    \"Testing\": {\n"
            "        \"v2\": \"Manual print checking\",\n"
            "        \"v3\": \"pytest with fixtures and parametrize\",\n"
            "    },\n"
            "    \"Configuration\": {\n"
            "        \"v2\": \"Hardcoded values\",\n"
            "        \"v3\": \"Config-driven, factory pattern\",\n"
            "    },\n"
            "    \"Reusability\": {\n"
            "        \"v2\": \"Copy-paste between projects\",\n"
            "        \"v3\": \"Import and configure\",\n"
            "    },\n"
            "}\n"
            "\n"
            "print(\"=== v2 vs v3 Comparison ===\")\n"
            "for aspect, versions in comparison.items():\n"
            "    print()\n"
            "    print(aspect + \":\")\n"
            "    print(\"  v2: \" + versions[\"v2\"])\n"
            "    print(\"  v3: \" + versions[\"v3\"])"
        ))
        extra.append(expected_output(
            "=== v2 vs v3 Comparison ===\n\n"
            "Code organization:\n"
            "  v2: Functions in one file\n"
            "  v3: Classes in separate modules\n"
            "(... more aspects ...)"
        ))

        extra.append(md(
            "---\n## Section 7: What Comes Next?\n\n"
            "Congratulations! You have built a professional-grade "
            "architecture. Next semester's topics will build on this:\n\n"
            "- **Data Structures & Algorithms** -- efficient implementations\n"
            "- **Advanced Patterns** -- Observer, Decorator, Command\n"
            "- **Concurrency** -- async, threading\n"
            "- **Deployment** -- packaging, CI/CD, Docker\n\n"
            "Everything you learned this semester -- classes, composition, "
            "SOLID, patterns, testing, packaging -- is the foundation for "
            "ALL of these topics."
        ))

        extra.extend(try_it(
            "Write a short 'retrospective' covering:\n"
            "1. Your biggest technical achievement this semester\n"
            "2. The concept that was hardest to learn\n"
            "3. How your code has changed since Week 1\n"
            "4. One thing you would do differently if starting over"
        ))

    # ---- Additional exercises for ALL weeks (brings count up) ----

    # Add a "Build from Scratch" exercise for every week
    extra.append(md(
        "---\n## Build from Scratch Exercise\n\n"
        "This exercise tests whether you truly understand this week's "
        "concepts. Complete it without looking at the examples above."
    ))

    build_prompts = {
        1: "Build a `TodoList` class with: items (list), add_item(text), "
           "remove_item(index), show(), count(). Test with 3 items.",
        2: "Build a `ShoppingCart` (has-a list of `CartItem` objects). "
           "CartItem has name, price, quantity. Cart has add_item(), total(), "
           "remove_item(). Demonstrate composition.",
        3: "Build a cleaning pipeline with 3 custom cleaners for student "
           "grade data: RemoveFailing (< 0), RemoveOutliers (> 100), "
           "RemoveIncomplete (None grades). Use BaseCleaner pattern.",
        4: "Build an AnalyzerSuite that runs GPA analysis: MeanGPA, "
           "MedianGPA, HighestGPA, LowestGPA. Each inherits from "
           "AnalyzerBase. Combine results into one dict.",
        5: "Build a SimpleReporter that takes analysis results and "
           "exports them as both CSV and JSON. Include a text summary method.",
        6: "Build an exception hierarchy for a web API: ApiError (base), "
           "AuthenticationError, NotFoundError, ValidationError. Each "
           "carries relevant context (status code, endpoint, etc).",
        7: "Take a 'God class' (one that loads, cleans, analyzes, and "
           "exports data) and refactor it into 4 separate classes. "
           "Show before and after.",
        8: "Build a sorting system with 3 interchangeable strategies: "
           "BubbleSort, InsertionSort, QuickSort. Each has a sort(data) "
           "method. Use a Sorter class that accepts a strategy.",
        9: "Build a ShapeFactory that creates Circle, Rectangle, and "
           "Triangle from a config dict. Register each shape. Create "
           "shapes from: [{\"type\": \"circle\", \"radius\": 5}, ...]",
        10: "Write a complete test suite (8+ tests) for a Stack class "
            "with push(), pop(), peek(), is_empty(), size(). Use TDD: "
            "write all tests first, then implement Stack.",
        11: "Design the package structure for a weather app: data loading, "
            "cleaning, analysis, visualization. Write all __init__.py files. "
            "Show the import statements users would use.",
        12: "Starting with the AnalyzerFactory from today, add TWO new "
            "plugins: MovingAverageAnalyzer and ZScoreAnalyzer. Write "
            "tests for both. Do NOT modify existing code.",
        13: "Create a complete interface contract document for a Calculator "
            "class. Include method signatures, input types, output types, "
            "exceptions, and examples for add, subtract, multiply, divide.",
        14: "Write a 2-minute demo script for your v3 pipeline. Include "
            "what to show, what to say, and anticipated questions.",
    }
    prompt = build_prompts.get(week_num, "Build a class that demonstrates this week's concept.")
    extra.append(code("# BUILD FROM SCRATCH:\n# " + prompt + "\n\n# YOUR CODE HERE\n"))
    extra.append(code("# TEST your build-from-scratch code:\n\n# YOUR TESTS HERE\n"))

    # Add a "Connect the Dots" exercise for weeks 2+
    if week_num >= 2:
        extra.append(md(
            "---\n## Connect the Dots\n\n"
            "How does this week's concept connect to previous weeks?"
        ))
        connections = {
            2: "How does composition (has-a) relate to the classes you built in Week 1?",
            3: "How does the Cleaner use composition (Week 2) and classes (Week 1)?",
            4: "How is the Analyzer similar to the Cleaner (Week 3)? How is it different?",
            5: "Draw the full pipeline showing how DataSource, Cleaner, Analyzer, "
               "Plotter, and Reporter connect.",
            6: "Where in the pipeline (Week 5) should each exception type be raised?",
            7: "Review your pipeline components -- do any violate SRP? Fix them.",
            8: "How is Strategy Pattern different from what we did in Week 3 with cleaners?",
            9: "How does the Factory Pattern build on the Strategy Pattern (Week 8)?",
            10: "Write tests for components from Weeks 2-5. Which are easiest to test? Why?",
            11: "Organize your Weeks 1-10 code into a proper package structure.",
            12: "How does the Plugin Exercise prove that our architecture follows OCP (Week 7)?",
            13: "Which of your components have the strongest interface contracts? The weakest?",
            14: "Map each week's concept to a specific file/class in your final project.",
        }
        extra.append(code(
            "# " + connections.get(week_num, "Explain the connection.") + "\n"
            "\n"
            "# YOUR ANSWER (as comments or code):\n"
        ))

    # Add "Real-World Spotting" exercise
    extra.append(md(
        "---\n## Real-World Spotting\n\n"
        "OOP patterns are everywhere in real software. Can you spot them?"
    ))

    spotting = {
        1: "Open Python and type `help(str)`. How many methods does the `str` class have? "
           "Pick 3 and explain what state and behavior they represent.",
        2: "Think about a smartphone. List 5 'has-a' composition relationships "
           "(e.g., Phone has-a Camera, Camera has-a Sensor).",
        3: "Think about a mail sorting system. What 'cleaning' rules would you apply? "
           "How would you compose them?",
        4: "Think about a fitness tracker. What analyses would it run on step data? "
           "Design 3 analyzer classes.",
        5: "Think about a social media app. What would its Reporter export? "
           "(profile data, activity stats, media files?)",
        6: "Visit any Python library's GitHub and find their custom exceptions. "
           "How are they organized? (e.g., requests library has ConnectionError, Timeout, etc.)",
        7: "Open any popular Python package (requests, flask, django) and look at "
           "their module structure. How do they apply SRP?",
        8: "Think about a music player. What strategies could it use for shuffle? "
           "(random, weighted by preference, alphabetical, etc.)",
        9: "Think about a restaurant ordering system. How would a Factory pattern "
           "help create different meal objects from a menu?",
        10: "Look at any open-source Python project's test suite. How are the tests organized?",
        11: "Run `import this` in Python. How do the 'Zen of Python' principles relate "
            "to package hygiene?",
        12: "Think about browser extensions. How are they 'plugins'? What interface "
            "do they implement?",
        13: "Think about USB. Why is it an 'interface contract'? What guarantees does "
            "it make? What happens when a device violates the contract?",
        14: "Think about your favorite app. What would its v1, v2, v3 look like? "
            "What patterns would improve each version?",
    }
    extra.append(code(
        "# " + spotting.get(week_num, "Find this pattern in real software.") + "\n"
        "\n"
        "# YOUR ANSWER:\n"
    ))

    # Add a "Diagram It" exercise
    extra.append(md(
        "---\n## Diagram It\n\n"
        "Draw an ASCII class diagram for the main classes from this week. "
        "Include:\n"
        "- Class names\n"
        "- Key attributes\n"
        "- Key methods\n"
        "- Relationships (has-a, is-a)"
    ))
    extra.append(code(
        "# Draw your ASCII diagram here:\n"
        "# +------------------+\n"
        "# |   ClassName      |\n"
        "# +------------------+\n"
        "# | - attribute      |\n"
        "# +------------------+\n"
        "# | + method()       |\n"
        "# +------------------+\n"
        "\n"
        "# YOUR DIAGRAM:\n"
    ))

    # ---- Universal enrichment for ALL weeks ----

    # Add a "Key Vocabulary" section for all weeks
    vocab = _get_week_vocabulary(week_num)
    if vocab:
        extra.append(md(
            "---\n## Key Vocabulary\n\n"
            "| Term | Definition |\n"
            "|------|------------|\n" + vocab
        ))

    # Add a recap exercise
    extra.append(md(
        "---\n## Recap Exercise\n\n"
        "Without looking at the code above, try to:"
    ))
    extra.append(code(
        "# 1. Write one class from this week FROM MEMORY\n"
        "#    (it does not need to be perfect)\n"
        "\n"
        "# YOUR CODE HERE\n"
        "\n"
        "\n"
        "# 2. Create an instance and call at least one method\n"
        "\n"
        "# YOUR CODE HERE\n"
        "\n"
        "\n"
        "# 3. Write one test for your class\n"
        "\n"
        "# YOUR CODE HERE\n"
    ))

    # Add "What to Review" section
    extra.append(md(
        "---\n## What to Review Before Next Week\n\n"
        "Before the next session, make sure you can:\n\n"
        "1. Explain this week's main concept in your own words\n"
        "2. Write a simple example from memory\n"
        "3. Identify this pattern in existing code\n"
        "4. Explain WHY this pattern is useful (not just HOW)"
    ))

    # Insert extra cells before Mini-Quiz / reflection
    # Find the Mini-Quiz cell and insert before it
    quiz_index = None
    for i, cell in enumerate(cells):
        if cell.get("cell_type") == "markdown":
            source = "".join(cell.get("source", []))
            if "Mini-Quiz" in source or "Final Quiz" in source:
                quiz_index = i
                break

    if quiz_index is not None:
        for i, cell in enumerate(extra):
            cells.insert(quiz_index + i, cell)
    else:
        # No quiz found, insert before reflection
        refl_index = None
        for i, cell in enumerate(cells):
            if cell.get("cell_type") == "markdown":
                source = "".join(cell.get("source", []))
                if "Reflection" in source:
                    refl_index = i
                    break
        if refl_index is not None:
            for i, cell in enumerate(extra):
                cells.insert(refl_index + i, cell)
        else:
            cells.extend(extra)

    return cells


def _get_week_vocabulary(week_num):
    """Return vocabulary table rows for a given week."""
    vocab_map = {
        1: (
            "| **Class** | A blueprint/template for creating objects |\n"
            "| **Object** | An instance created from a class |\n"
            "| **Instance** | Same as object -- one specific thing built from a class |\n"
            "| **Attribute** | A variable that belongs to an object (state) |\n"
            "| **Method** | A function that belongs to a class (behavior) |\n"
            "| **`__init__`** | The constructor -- runs when an object is created |\n"
            "| **`self`** | Reference to the current object inside a method |\n"
            "| **State** | The data an object holds (its attributes) |\n"
            "| **Behavior** | What an object can do (its methods) |"
        ),
        2: (
            "| **Composition** | One object contains another ('has-a') |\n"
            "| **Has-a** | A relationship where one object owns another |\n"
            "| **Is-a** | An inheritance relationship (subclass IS-A parent) |\n"
            "| **Dataset** | An object that wraps raw data with metadata |\n"
            "| **DataSource** | An object that loads data and creates Datasets |\n"
            "| **Immutable** | Cannot be changed after creation |\n"
            "| **Non-destructive** | Returns new objects instead of modifying originals |"
        ),
        3: (
            "| **Template Method** | Base class defines algorithm skeleton, subclasses fill in details |\n"
            "| **Override** | Subclass provides its own version of a parent method |\n"
            "| **`super()`** | Call the parent class version of a method |\n"
            "| **Pipeline** | A sequence of processing steps |\n"
            "| **Drop reason** | Why a row was removed during cleaning |"
        ),
        4: (
            "| **Schema** | The expected structure of data (column names, types) |\n"
            "| **Stable schema** | A schema that does not change between versions |\n"
            "| **Guard clause** | An early return that handles edge cases |\n"
            "| **NotImplementedError** | Raised when a base class method must be overridden |"
        ),
        5: (
            "| **Component** | A self-contained object with a clear interface |\n"
            "| **Graceful degradation** | Continuing to work when optional features are missing |\n"
            "| **Export** | Writing data to external files (CSV, JSON, PNG) |"
        ),
        6: (
            "| **Exception hierarchy** | A tree of exception classes (base -> specific) |\n"
            "| **Raise** | Create and throw an exception |\n"
            "| **Catch** | Handle an exception with try/except |\n"
            "| **Propagate** | Let an exception pass up to the caller |\n"
            "| **Context** | Extra information attached to an exception |"
        ),
        7: (
            "| **SRP** | Single Responsibility Principle -- one class, one job |\n"
            "| **OCP** | Open/Closed Principle -- open for extension, closed for modification |\n"
            "| **SOLID** | Five design principles (SRP, OCP, LSP, ISP, DIP) |\n"
            "| **God class** | A class that does too many things (SRP violation) |\n"
            "| **Refactor** | Restructure code without changing behavior |"
        ),
        8: (
            "| **Strategy Pattern** | Define a family of interchangeable algorithms |\n"
            "| **Interface** | A shared set of methods that all strategies implement |\n"
            "| **Config-driven** | Behavior determined by configuration, not code changes |\n"
            "| **Composable** | Can be combined with other strategies |"
        ),
        9: (
            "| **Factory** | An object that creates other objects |\n"
            "| **Registry** | A mapping from names to classes |\n"
            "| **Plugin** | A new component added without modifying core code |\n"
            "| **`@classmethod`** | A method that belongs to the class, not instances |\n"
            "| **Decorator** | A function/class that wraps another to add behavior |"
        ),
        10: (
            "| **pytest** | Python's standard testing framework |\n"
            "| **Fixture** | Reusable test setup code |\n"
            "| **Parametrize** | Run one test function with multiple inputs |\n"
            "| **TDD** | Test-Driven Development -- write tests before code |\n"
            "| **Assert** | A statement that verifies a condition is True |\n"
            "| **Edge case** | An unusual input that might break the code |"
        ),
        11: (
            "| **Module** | A single .py file |\n"
            "| **Package** | A directory with __init__.py |\n"
            "| **`__init__.py`** | File that makes a directory a package and controls exports |\n"
            "| **`__all__`** | List of names exported by `from package import *` |\n"
            "| **Relative import** | Import using `.` notation within a package |\n"
            "| **Circular import** | Two modules importing each other (causes errors) |"
        ),
        12: (
            "| **Plugin architecture** | A system where new features are added without modifying core |\n"
            "| **Extension point** | A place in the code where plugins can hook in |\n"
            "| **Registration** | Adding a new class to the factory/registry |"
        ),
        13: (
            "| **Architecture freeze** | Locking the public API from further changes |\n"
            "| **Interface contract** | A promise about what a method accepts and returns |\n"
            "| **Public API** | The set of classes and methods intended for external use |\n"
            "| **Backward compatible** | New version works with old code without changes |"
        ),
        14: (
            "| **Demo** | A live presentation of working software |\n"
            "| **Release** | A stable version ready for use |\n"
            "| **Architecture review** | Evaluating code structure against design principles |"
        ),
    }
    return vocab_map.get(week_num, "")


# ============================================================
# STUDIO NOTEBOOK GENERATOR
# ============================================================
def make_studio(week_num, title, track_key):
    """Generate a rich studio notebook (30-40+ cells) for a track."""
    track = TRACKS[track_key]
    product = track["product"]
    domain = track["domain_data"]
    cells = []

    cells.append(md(
        "# OOP Week " + str(week_num) + " Studio -- " + product + "\n\n"
        "**Track:** " + track["name"] + "\n"
        "**Topic:** " + title + "\n"
        "**Goal:** Apply this week's OOP concepts to " + product + "\n"
        "**Time:** ~2 hours\n\n"
        "---\n\n"
        "## How This Studio Works\n\n"
        "1. **Read** the core notebook first (if you have not already)\n"
        "2. **Follow** the step-by-step instructions below\n"
        "3. **Complete** the Must-Pass Core first\n"
        "4. **Then** tackle Standard and Stretch goals\n"
        "5. **Test** your code at each step"
    ))
    cells.append(setup_cell())

    # Context
    cells.append(md(
        "---\n## Your Domain: " + product + "\n\n"
        "Your project works with " + domain + ". "
        "This week you will apply **" + title.lower() + "** to your "
        + product + " codebase.\n\n"
        "Think about:\n"
        "- What classes does your domain need?\n"
        "- What data does each class hold?\n"
        "- What operations does each class perform?"
    ))

    # Week-specific studio content
    studio_content = _get_studio_content(week_num, track)

    # Must-Pass Core (always present)
    cells.append(md(
        "---\n## Must-Pass Core\n\n"
        "Complete ALL of these before moving on. This is your minimum "
        "requirement for the week.\n\n" + studio_content["must_pass_desc"]
    ))
    cells.append(md("### Step 1: " + studio_content["step1_title"]))
    cells.append(code(studio_content["step1_code"]))
    cells.append(md("**Expected:** " + studio_content["step1_expected"]))

    cells.append(md("### Step 2: " + studio_content["step2_title"]))
    cells.append(code(studio_content["step2_code"]))
    cells.append(md("**Expected:** " + studio_content["step2_expected"]))

    cells.append(md("### Step 3: Test Your Code"))
    cells.append(code(studio_content["test_code"]))
    cells.append(md("**All tests should pass before moving on.**"))

    # Standard Target
    cells.append(md(
        "---\n## Standard Target\n\n"
        "Extend your Must-Pass work with these additions.\n\n"
        + studio_content["standard_desc"]
    ))
    cells.append(code(studio_content["standard_code"]))

    cells.append(md("### Standard Test"))
    cells.append(code(studio_content["standard_test"]))

    # Stretch
    cells.append(md(
        "---\n## Stretch Goal\n\n"
        + studio_content["stretch_desc"]
    ))
    cells.append(code(studio_content["stretch_code"]))

    # Additional studio exercises to bring count to 30+
    cells.append(md(
        "---\n## Additional Practice\n\n"
        "Complete these exercises to deepen your understanding."
    ))

    # Exercise: Refactoring practice
    cells.append(md(
        "### Exercise: Refactoring Check\n\n"
        "Review the code you wrote above. Ask yourself:\n"
        "1. Does each class have exactly ONE responsibility?\n"
        "2. Are all attributes initialized in `__init__`?\n"
        "3. Do methods that transform data return NEW objects?\n"
        "4. Are there any 'magic numbers' that should be parameters?"
    ))
    cells.append(code(
        "# Refactoring notes:\n"
        "# - Things I would change:\n"
        "# - Why:\n"
        "# - Improved version (if needed):\n"
    ))

    # Exercise: Edge cases
    cells.append(md(
        "### Exercise: Edge Case Testing\n\n"
        "Write tests for edge cases specific to " + product + "."
    ))
    cells.append(code(
        "# Edge case tests for " + product + "\n"
        "\n"
        "def test_empty_input():\n"
        "    # What happens with no data?\n"
        "    # YOUR CODE HERE\n"
        "    print(\"[PASS] test_empty_input\")\n"
        "\n"
        "def test_invalid_input():\n"
        "    # What happens with wrong type/format?\n"
        "    # YOUR CODE HERE\n"
        "    print(\"[PASS] test_invalid_input\")\n"
        "\n"
        "def test_boundary_values():\n"
        "    # What happens at the limits?\n"
        "    # YOUR CODE HERE\n"
        "    print(\"[PASS] test_boundary_values\")\n"
        "\n"
        "# Run tests\n"
        "test_empty_input()\n"
        "test_invalid_input()\n"
        "test_boundary_values()"
    ))

    # Exercise: Documentation
    cells.append(md(
        "### Exercise: Write Documentation\n\n"
        "Add proper docstrings to all your classes and methods. "
        "Include:\n"
        "- One-line summary\n"
        "- Parameters (with types)\n"
        "- Return values\n"
        "- Example usage"
    ))
    cells.append(code(
        "# Copy your main class here with FULL docstrings:\n"
        "\n"
        "# YOUR CODE HERE\n"
    ))

    # Exercise: Design diagram
    cells.append(md(
        "### Exercise: Design Diagram\n\n"
        "Draw an ASCII class diagram showing ALL the classes you "
        "created today and their relationships."
    ))
    cells.append(code(
        "# ASCII Class Diagram for " + product + "\n"
        "# \n"
        "# +------------------+     +------------------+\n"
        "# |   ClassName1     |---->|   ClassName2     |\n"
        "# +------------------+     +------------------+\n"
        "# | - attributes     |     | - attributes     |\n"
        "# +------------------+     +------------------+\n"
        "# | + methods        |     | + methods        |\n"
        "# +------------------+     +------------------+\n"
        "# \n"
        "# YOUR DIAGRAM:\n"
    ))

    # Exercise: Integration plan
    cells.append(md(
        "### Exercise: Integration Plan\n\n"
        "How will today's code integrate with the rest of your "
        + product + " pipeline? Write a brief plan."
    ))
    cells.append(code(
        "# Integration plan:\n"
        "# 1. Which existing components will use today's code?\n"
        "#    Answer: \n"
        "# \n"
        "# 2. What interface (method signatures) will they need?\n"
        "#    Answer: \n"
        "# \n"
        "# 3. What tests should I add to verify integration?\n"
        "#    Answer: \n"
        "# \n"
        "# 4. Any potential conflicts or breaking changes?\n"
        "#    Answer: \n"
    ))

    # Self-assessment
    cells.append(md(
        "---\n## Self-Assessment\n\n"
        "Rate your understanding of this week's concepts:"
    ))
    cells.append(code(
        "# Rate 1-5 (1=confused, 5=confident)\n"
        "understanding = {\n"
        "    \"Main concept\": 0,        # Rate yourself\n"
        "    \"Implementation\": 0,       # Could you build it from scratch?\n"
        "    \"Testing\": 0,              # Can you write good tests?\n"
        "    \"Connection to pipeline\": 0, # See how it fits?\n"
        "}\n"
        "\n"
        "for topic, rating in understanding.items():\n"
        "    print(topic + \": \" + str(rating) + \"/5\")\n"
        "\n"
        "# What would help you improve?\n"
        "# Answer: "
    ))

    # Checklist
    cells.append(md(
        "---\n## Completion Checklist\n\n"
        "Before submitting, verify:\n\n"
        "- [ ] Must-Pass: " + studio_content["check1"] + "\n"
        "- [ ] Must-Pass: All tests pass\n"
        "- [ ] Standard: " + studio_content["check2"] + "\n"
        "- [ ] Stretch: " + studio_content["check3"] + " (optional)\n"
        "- [ ] Code has docstrings on all classes and methods\n"
        "- [ ] No logic copied from core notebook (you adapted it)\n"
        "- [ ] Edge case tests written\n"
        "- [ ] Design diagram drawn\n"
        "- [ ] Self-assessment completed"
    ))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


def _get_studio_content(week_num, track):
    """Return week-specific studio content for a track."""
    product = track["product"]
    domain_obj = track["domain_object"]
    ex_class = track["example_class"]
    ex_method = track["example_method"]
    ex_attr = track["example_attr"]

    # Default content (for weeks without specific content)
    default = {
        "must_pass_desc": (
            "Apply this week's pattern to " + product + ".\n\n"
            "1. Create the class described below\n"
            "2. Add at least 2 methods\n"
            "3. Write at least 2 tests"
        ),
        "step1_title": "Create Your Class",
        "step1_code": (
            "# Create a class for your domain\n"
            "# It should apply this week's concept to " + product + "\n"
            "\n"
            "class " + ex_class + ":\n"
            "    \"\"\"" + ex_class + " for " + product + ".\"\"\"\n"
            "\n"
            "    def __init__(self):\n"
            "        # TODO: add attributes\n"
            "        pass\n"
            "\n"
            "    def " + ex_method + "(self):\n"
            "        # TODO: implement\n"
            "        pass\n"
            "\n"
            "    def __str__(self):\n"
            "        return \"" + ex_class + "(...)\"\n"
            "\n"
            "\n"
            "# Test it\n"
            "obj = " + ex_class + "()\n"
            "print(obj)"
        ),
        "step1_expected": "Your class should create without errors and print a description.",
        "step2_title": "Add Domain-Specific Methods",
        "step2_code": (
            "# Add methods specific to " + product + "\n"
            "# Think: what operations does your domain need?\n"
            "\n"
            "# YOUR CODE HERE\n"
        ),
        "step2_expected": "Methods should handle normal input and edge cases.",
        "test_code": (
            "# Write at least 2 tests\n"
            "def test_" + ex_class.lower() + "_creation():\n"
            "    obj = " + ex_class + "()\n"
            "    assert obj is not None\n"
            "    print(\"[PASS] test_" + ex_class.lower() + "_creation\")\n"
            "\n"
            "def test_" + ex_class.lower() + "_method():\n"
            "    obj = " + ex_class + "()\n"
            "    # TODO: test " + ex_method + "()\n"
            "    print(\"[PASS] test_" + ex_class.lower() + "_method\")\n"
            "\n"
            "test_" + ex_class.lower() + "_creation()\n"
            "test_" + ex_class.lower() + "_method()"
        ),
        "standard_desc": (
            "1. Add at least 2 more methods to your class\n"
            "2. Add error handling (raise exceptions on bad input)\n"
            "3. Write 2 more tests"
        ),
        "standard_code": "# YOUR STANDARD IMPLEMENTATION\n",
        "standard_test": (
            "# Write 2 more tests for your standard features\n"
            "\n"
            "# YOUR TESTS HERE\n"
        ),
        "stretch_desc": (
            "Go beyond the requirements:\n"
            "- Add a visualization method\n"
            "- Add a `to_dict()` method for JSON export\n"
            "- Compose with another class from a previous week"
        ),
        "stretch_code": "# YOUR STRETCH IMPLEMENTATION\n",
        "check1": "Class created with __init__ and at least 2 methods",
        "check2": "Extended with error handling and additional methods",
        "check3": "Extra features implemented",
    }

    # Week-specific overrides
    if week_num == 1:
        default["must_pass_desc"] = (
            "Create a class for your domain's primary data object.\n\n"
            "1. Define a `" + domain_obj + "` class with `__init__`, at least 2 attributes, and 2 methods\n"
            "2. Create at least 2 instances with different data\n"
            "3. Verify each instance has independent state"
        )
        default["step1_title"] = "Define Your " + domain_obj + " Class"
        default["step1_code"] = (
            "class " + domain_obj + ":\n"
            "    \"\"\"Represents a " + domain_obj.lower() + " in " + product + ".\"\"\"\n"
            "\n"
            "    def __init__(self, " + ex_attr + ", name):\n"
            "        self." + ex_attr + " = " + ex_attr + "\n"
            "        self.name = name\n"
            "        self.data = []  # TODO: add appropriate attributes\n"
            "\n"
            "    def add_data(self, value):\n"
            "        \"\"\"Add a data point.\"\"\"\n"
            "        self.data.append(value)\n"
            "\n"
            "    def summary(self):\n"
            "        \"\"\"Return a summary of this " + domain_obj.lower() + ".\"\"\"\n"
            "        count = len(self.data)\n"
            "        if count == 0:\n"
            "            return \"No data yet\"\n"
            "        mean = sum(self.data) / count\n"
            "        return str(count) + \" readings, mean=\" + str(round(mean, 2))\n"
            "\n"
            "    def __str__(self):\n"
            "        return \"" + domain_obj + "(\" + self." + ex_attr + " + \")\"\n"
            "\n"
            "\n"
            "# Create instances\n"
            "obj1 = " + domain_obj + "(\"A001\", \"Primary\")\n"
            "obj2 = " + domain_obj + "(\"B002\", \"Secondary\")\n"
            "\n"
            "obj1.add_data(42.0)\n"
            "obj1.add_data(43.5)\n"
            "obj2.add_data(100.0)\n"
            "\n"
            "print(obj1, \"->\", obj1.summary())\n"
            "print(obj2, \"->\", obj2.summary())"
        )
        default["check1"] = domain_obj + " class with __init__, add_data, summary, __str__"

    elif week_num == 2:
        default["must_pass_desc"] = (
            "Create a Dataset class that wraps " + product + " data.\n\n"
            "1. Build a `" + domain_obj + "Dataset` class\n"
            "2. Build a `" + domain_obj + "Source` class that creates datasets\n"
            "3. Demonstrate composition (source creates dataset)"
        )
        default["step1_title"] = "Build " + domain_obj + "Dataset and " + domain_obj + "Source"
        default["check1"] = "Dataset and Source classes with has-a relationship"

    elif week_num >= 3 and week_num <= 5:
        component = {3: "Cleaner", 4: "Analyzer", 5: "Plotter/Reporter"}[week_num]
        default["must_pass_desc"] = (
            "Build a " + component + " for " + product + ".\n\n"
            "1. Create the " + component + " class following the pattern from core\n"
            "2. Adapt it for your domain's data (" + track["domain_data"] + ")\n"
            "3. Test with sample data"
        )
        default["check1"] = component + " class working with domain data"

    elif week_num == 6:
        default["must_pass_desc"] = (
            "Add custom exceptions to " + product + ".\n\n"
            "1. Define at least 3 domain-specific exceptions\n"
            "2. Add validation that raises them\n"
            "3. Write try/except blocks that handle them gracefully"
        )
        default["check1"] = "3+ custom exceptions with validation"

    elif week_num == 10:
        default["must_pass_desc"] = (
            "Write a test suite for " + product + ".\n\n"
            "1. Write at least 5 test functions\n"
            "2. Use at least 1 fixture\n"
            "3. Use parametrize for at least 1 test"
        )
        default["check1"] = "5+ tests with fixtures and parametrize"

    elif week_num == 12:
        default["must_pass_desc"] = (
            "Add a new analyzer to " + product + " WITHOUT touching core code.\n\n"
            "1. Create a new analyzer class\n"
            "2. Register with the factory\n"
            "3. Write tests\n"
            "4. Verify no existing code was modified"
        )
        default["check1"] = "New analyzer added without modifying existing code"

    return default


# ============================================================
# HOMEWORK NOTEBOOK GENERATOR
# ============================================================
def make_homework(week_num, title):
    """Generate a rich homework notebook (10-15 exercises)."""
    cells = []
    cells.append(md(
        "# OOP Week " + str(week_num) + " Homework -- " + title + "\n\n"
        "**Due:** Before next week's session\n"
        "**Estimated time:** 2-3 hours\n"
        "**Grading:** Must-pass (exercises 1-5), Standard (6-8), "
        "Stretch (9-12)\n\n"
        "---\n\n"
        "## Instructions\n\n"
        "1. Complete exercises **in order** -- they build on each other\n"
        "2. **Run each cell** and verify it works before moving on\n"
        "3. **Write comments** explaining your thinking\n"
        "4. **Test** your code (at minimum: does it run without errors?)\n"
        "5. Submit this notebook with all cells executed"
    ))

    hw_content = _get_homework_content(week_num, title)

    for i, (ex_title, ex_desc, ex_code) in enumerate(hw_content, 1):
        tier = "Must-Pass" if i <= 5 else ("Standard" if i <= 8 else "Stretch")
        cells.append(md(
            "---\n## Exercise " + str(i) + " [" + tier + "]: " + ex_title
            + "\n\n" + ex_desc
        ))
        cells.append(code(ex_code))

    cells.append(md(
        "---\n## Submission Checklist\n\n"
        "- [ ] Exercises 1-5 complete and running (Must-Pass)\n"
        "- [ ] Exercises 6-8 complete (Standard)\n"
        "- [ ] Exercises 9-12 attempted (Stretch)\n"
        "- [ ] All cells executed (no errors)\n"
        "- [ ] Comments explain your thinking"
    ))

    return cells


def _get_homework_content(week_num, title):
    """Return list of (title, description, starter_code) tuples."""
    exercises = []

    if week_num == 1:
        exercises = [
            ("Create a Dog class",
             "Create a `Dog` class with attributes `name`, `breed`, and `age`. "
             "Add a method `bark()` that prints a message.",
             "# YOUR CODE HERE\n\nclass Dog:\n    pass\n"),
            ("Add methods to Dog",
             "Add `birthday()` (increments age) and `describe()` (prints all info).",
             "# YOUR CODE HERE\n"),
            ("Create a BankAccount class",
             "Attributes: `owner`, `balance` (default 0). "
             "Methods: `deposit(amount)`, `withdraw(amount)`, `get_balance()`.\n"
             "`withdraw` should print a warning if insufficient funds.",
             "# YOUR CODE HERE\n"),
            ("Multiple instances",
             "Create 3 Dog objects and 2 BankAccount objects. "
             "Verify they have independent state.",
             "# YOUR CODE HERE\n"),
            ("Add __str__ to both classes",
             "Add `__str__` methods that return readable strings. "
             "Example: `Dog(Rex, Labrador, 5 years)`",
             "# YOUR CODE HERE\n"),
            ("Procedural vs OOP comparison",
             "Write a procedural version of BankAccount using functions and "
             "dicts. Then compare: which is easier to use? Write your answer "
             "as a comment.",
             "# Procedural version\n\n# YOUR CODE HERE\n\n# Comparison (write as comments):\n# "),
            ("Counter class",
             "Create a `Counter` class with `increment()`, `decrement()`, "
             "`reset()`, and `value` attribute. Add a `history` list that "
             "records every change.",
             "# YOUR CODE HERE\n"),
            ("Student class with grades",
             "Create a `Student` class that stores a name and list of grades. "
             "Methods: `add_grade(grade)`, `average()`, `highest()`, `lowest()`, "
             "`is_passing()` (average >= 60).",
             "# YOUR CODE HERE\n"),
            ("Inventory Item",
             "Create an `InventoryItem` class with `name`, `quantity`, `price`. "
             "Methods: `restock(amount)`, `sell(amount)` (with stock check), "
             "`total_value()`. Add `__str__`.",
             "# YOUR CODE HERE\n"),
            ("Design before code",
             "BEFORE writing any code, draw an ASCII class diagram for a "
             "`Library` system with `Book` and `Member` classes. Include "
             "attributes and methods. Then implement it.",
             "# ASCII diagram (in comments):\n# +--------+\n# | Book   |\n# +--------+\n# | ...    |\n# +--------+\n\n# Implementation:\n"),
            ("Error handling",
             "Add error handling to your BankAccount: raise `ValueError` if "
             "deposit/withdraw amount is negative. Write tests that verify "
             "the errors are raised.",
             "# YOUR CODE HERE\n"),
            ("Reflection: Procedural vs OOP",
             "Write a 5-sentence paragraph (as a string) explaining when you "
             "would choose OOP over procedural programming and vice versa. "
             "Give a concrete example of each.",
             "reflection = \"\"\"\n# YOUR REFLECTION HERE\n\"\"\"\nprint(reflection)\n"),
        ]
    elif week_num == 2:
        exercises = [
            ("Basic composition",
             "Create `Engine` and `Car` classes where Car HAS-A Engine.",
             "# YOUR CODE HERE\n"),
            ("Dataset wrapper",
             "Create a `Dataset` class that wraps a list of dicts. Add "
             "`get_column()`, `__len__()`, `__str__()`.",
             "# YOUR CODE HERE\n"),
            ("DataSource class",
             "Create a `DataSource` that loads sample data and returns "
             "a `Dataset`.",
             "# YOUR CODE HERE\n"),
            ("Filter method",
             "Add a `filter_rows(column, condition)` method to Dataset "
             "that returns a NEW Dataset.",
             "# YOUR CODE HERE\n"),
            ("Verify immutability",
             "Prove that filtering does NOT change the original dataset.",
             "# YOUR CODE HERE\n"),
            ("Column statistics",
             "Add a `column_stats(name)` method that returns min, max, mean "
             "for numeric columns.",
             "# YOUR CODE HERE\n"),
            ("Multi-source",
             "Create two DataSources with different data. Load both and "
             "compare their Datasets.",
             "# YOUR CODE HERE\n"),
            ("Validation",
             "Add column validation to DataSource: raise ValueError if "
             "required columns are missing.",
             "# YOUR CODE HERE\n"),
            ("Composition diagram",
             "Draw an ASCII composition diagram showing the has-a "
             "relationships in your pipeline.",
             "# YOUR DIAGRAM HERE\n"),
            ("Pipeline class",
             "Create a `MiniPipeline` class that HAS-A DataSource and "
             "SimpleCleaner. Add a `run()` method.",
             "# YOUR CODE HERE\n"),
            ("Design question",
             "Why is composition preferred over inheritance in modern "
             "Python? Write 3 reasons with examples.",
             "# YOUR ANSWER HERE\n"),
            ("Extend Dataset",
             "Add `to_csv_string()` and `from_csv_string(text)` methods "
             "to Dataset.",
             "# YOUR CODE HERE\n"),
        ]
    else:
        # Generic homework for other weeks
        topic_lower = title.lower()
        exercises = [
            ("Concept review",
             "In your own words, explain the main concept from this week "
             "(" + topic_lower + "). Give a real-world analogy.",
             "# YOUR ANSWER (as comments or string)\n"),
            ("Basic implementation",
             "Implement the basic pattern from this week's core notebook "
             "with your own example (not copied).",
             "# YOUR CODE HERE\n"),
            ("Second example",
             "Create a different example that uses the same pattern "
             "but in a different domain.",
             "# YOUR CODE HERE\n"),
            ("Edge cases",
             "Identify 3 edge cases for this week's pattern and write "
             "code that handles them.",
             "# YOUR CODE HERE\n"),
            ("Tests",
             "Write at least 3 test functions for your implementations.",
             "# YOUR TESTS HERE\ndef test_1():\n    pass\n\ndef test_2():\n    pass\n\ndef test_3():\n    pass\n"),
            ("Compare approaches",
             "Show 2 different ways to solve the same problem: one using "
             "this week's pattern and one without. Compare the trade-offs.",
             "# Approach 1:\n\n# Approach 2:\n\n# Comparison:\n"),
            ("Integration",
             "Integrate this week's concept with a component from "
             "a previous week.",
             "# YOUR CODE HERE\n"),
            ("Error handling",
             "Add proper error handling to your implementation. Use "
             "custom exceptions where appropriate.",
             "# YOUR CODE HERE\n"),
            ("Design question",
             "Design (on paper/ASCII first, then code) a system that "
             "uses this week's pattern for a domain you are interested in.",
             "# DESIGN:\n\n# IMPLEMENTATION:\n"),
            ("Debugging challenge",
             "The code below has 3 bugs related to this week's topic. "
             "Find and fix them.",
             "# BUGGY CODE (find and fix 3 bugs):\n"
             "# Bug 1: \n# Bug 2: \n# Bug 3: \n"),
            ("Teaching exercise",
             "Write a short tutorial (as comments) explaining this week's "
             "concept to someone who has never seen it. Include an example.",
             "# YOUR TUTORIAL HERE\n"),
            ("Reflection",
             "How does this week's concept improve the architecture of "
             "your project? Be specific.",
             "reflection = \"\"\"\n# YOUR REFLECTION HERE\n\"\"\"\nprint(reflection)\n"),
        ]

    return exercises


# ============================================================
# CHECK NOTEBOOK GENERATOR
# ============================================================
def make_check(week_num):
    """Generate a universal check notebook."""
    cells = [
        md("# OOP Week " + str(week_num) + " -- Universal Check\n\n"
           "Run this notebook to verify your project meets this week's "
           "requirements."),
        setup_cell(),
        code(
            "import os, json\n"
            "\n"
            "print(\"=== OOP Week " + str(week_num) + " Universal Check ===\")\n"
            "print()\n"
            "passed = 0\n"
            "failed = 0\n"
            "\n"
            "# Check 1: Core module exists\n"
            "core_path = \"src/project_template/core\"\n"
            "if os.path.exists(core_path):\n"
            "    print(\"[PASS] \" + core_path + \"/ exists\")\n"
            "    passed += 1\n"
            "else:\n"
            "    print(\"[FAIL] \" + core_path + \"/ missing\")\n"
            "    failed += 1\n"
            "\n"
            "# Check 2: Required exports\n"
            "for f in [\"data/cleaned/cleaned.csv\", \"reports/report.json\"]:\n"
            "    if os.path.exists(f) and os.path.getsize(f) > 0:\n"
            "        print(\"[PASS] \" + f)\n"
            "        passed += 1\n"
            "    else:\n"
            "        print(\"[FAIL] \" + f)\n"
            "        failed += 1\n"
            "\n"
            "# Check 3: Tests exist\n"
            "if os.path.exists(\"tests\"):\n"
            "    test_files = [f for f in os.listdir(\"tests\") if f.startswith(\"test_\")]\n"
            "    if test_files:\n"
            "        print(\"[PASS] \" + str(len(test_files)) + \" test file(s) found\")\n"
            "        passed += 1\n"
            "    else:\n"
            "        print(\"[FAIL] No test files in /tests\")\n"
            "        failed += 1\n"
            "else:\n"
            "    print(\"[FAIL] /tests directory missing\")\n"
            "    failed += 1\n"
            "\n"
            "print()\n"
            "print(str(passed) + \" passed, \" + str(failed) + \" failed\")"
        ),
    ]
    return cells


# ============================================================
# GENERATE ALL NOTEBOOKS
# ============================================================
print("Generating OOP notebooks...")

for week_num, title, focus in WEEKS:
    wk = "W" + str(week_num).zfill(2)

    # Core notebook
    if week_num in WEEK_CORE_FUNCTIONS:
        core_cells = WEEK_CORE_FUNCTIONS[week_num]()
    else:
        core_cells = WEEK_CORE_FUNCTIONS[1]()  # fallback

    # Enrich with additional examples, exercises, debugging tips
    core_cells = enrich_core(week_num, title, core_cells)

    save_notebook(
        notebook(core_cells, "OOP " + wk + " Core -- " + title),
        os.path.join(BASE, wk + "_core.ipynb"),
    )

    # Studio notebooks (one per track)
    for tk in TRACKS:
        studio_cells = make_studio(week_num, title, tk)
        save_notebook(
            notebook(studio_cells, "OOP " + wk + " Studio " + TRACKS[tk]["name"]),
            os.path.join(BASE, wk + "_studio_" + tk + ".ipynb"),
        )

    # Check notebook
    check_cells = make_check(week_num)
    save_notebook(
        notebook(check_cells, "OOP " + wk + " Check"),
        os.path.join(BASE, wk + "_check.ipynb"),
    )

    # Homework notebook
    hw_cells = make_homework(week_num, title)
    save_notebook(
        notebook(hw_cells, "OOP " + wk + " Homework -- " + title),
        os.path.join(BASE, wk + "_homework.ipynb"),
    )

    print("  " + wk + ": core + 5 studios + check + homework")

total = 14 * 8
print()
print("OOP complete: " + str(total) + " notebooks generated!")
