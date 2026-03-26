#!/usr/bin/env python3
"""Generate all DSA (Data Structures & Algorithms) notebooks -- 14 weeks.

This generator produces RICH, substantial notebooks suitable as standalone
teaching documents for Mechatronics Engineering students who completed CP1+CP2+OOP.

Each core notebook targets 50-80+ cells with:
- Multiple paragraphs of explanation with real-world analogies
- ASCII art visualizations of data structures
- Step-by-step algorithm traces showing state at each iteration
- "Slow way first" then optimize pattern
- 3-4 worked examples per algorithm
- Expected Output after every code cell
- Common Mistakes sections
- Big-O analysis in plain English + notation
- Timing experiments
- When to Use This guidance
- Try It exercises between sections
- Connection to the 5 project tracks
- 10+ homework exercises (review, practice, challenge, mini-project)

Studio notebooks: 30+ cells with baseline code, optimization steps, benchmarking.
Homework: 10-15 exercises progressive difficulty.
Check: thorough validation.
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from nb_utils import md, code, notebook, save_notebook, setup_cell, reflection_cell, reflection_code, TRACKS

BASE = os.path.join(os.path.dirname(__file__), "notebooks", "dsa")
os.makedirs(BASE, exist_ok=True)

# ============================================================
# WEEK DEFINITIONS
# ============================================================

WEEKS = [
    (1, "Big-O & Python Cost Model", "Big-O notation, list/dict/set costs"),
    (2, "Benchmark Literacy", "timeit, scaling plots, measuring performance"),
    (3, "Searching: Linear vs Binary", "linear search, binary search, sorted data"),
    (4, "Sorting Algorithms", "bubble, insertion, Python sort, comparisons"),
    (5, "Hashing & Indexing", "hash tables, dict internals, Index module"),
    (6, "Heap & Priority Queue", "heapq, top-k, priority scheduling"),
    (7, "Performance Sprint 1", "implement optimized feature + tests"),
    (8, "Performance Sprint 2", "benchmark baseline vs optimized + plots"),
    (9, "Trees & BST", "binary tree, BST, traversal"),
    (10, "Graphs: BFS & DFS", "graph representation, BFS, DFS"),
    (11, "Shortest Paths", "Dijkstra, weighted graphs"),
    (12, "Dynamic Programming", "memoization, DP patterns, optimization"),
    (13, "Final Integration", "optimized feature wired into product"),
    (14, "Final Performance Report", "demo, benchmark report, release"),
]

# ============================================================
# TRACK DATA for DSA
# ============================================================

TRACK_DATA = {
    "robotics": {
        "name": "Robotics/Mechatronics",
        "product": "MechaSense Studio",
        "dataset_desc": "sensor readings (temperature, RPM, vibration) from robotic arms",
        "bottleneck": "searching event logs for anomalies in real-time",
        "baseline_op": "linear scan of all sensor readings",
        "optimized_op": "binary search on sorted timestamps + hash index on sensor IDs",
        "sample_data": [
            {"ts": 0.01, "sensor": "motor_A", "temp": 25.3, "rpm": 1500},
            {"ts": 0.02, "sensor": "motor_A", "temp": 26.1, "rpm": 1520},
            {"ts": 0.03, "sensor": "motor_B", "temp": 85.0, "rpm": 3500},
            {"ts": 0.04, "sensor": "motor_A", "temp": 24.8, "rpm": 1490},
            {"ts": 0.05, "sensor": "motor_B", "temp": 60.0, "rpm": 2800},
            {"ts": 0.06, "sensor": "motor_A", "temp": 27.2, "rpm": 1550},
            {"ts": 0.07, "sensor": "gripper", "temp": 30.0, "rpm": 0},
            {"ts": 0.08, "sensor": "motor_A", "temp": 23.9, "rpm": 1480},
        ],
        "value_col": "temp",
        "threshold": 60,
        "unit": "degrees C",
        "graph_context": "robot component dependency graph",
        "dp_context": "optimal path planning for robotic arm movement",
    },
    "data": {
        "name": "Data/AI",
        "product": "CleanReport Pipeline",
        "dataset_desc": "messy survey/CSV data requiring deduplication and fast lookup",
        "bottleneck": "deduplicating records and looking up entries by multiple keys",
        "baseline_op": "nested loop comparison for duplicates",
        "optimized_op": "hash-based dedup + index on key columns",
        "sample_data": [
            {"id": 1, "name": "Alice", "score": 88.5, "city": "Cairo"},
            {"id": 2, "name": "Bob", "score": 92.0, "city": "Alex"},
            {"id": 3, "name": "Alice", "score": 88.5, "city": "Cairo"},
            {"id": 4, "name": "Carol", "score": 75.0, "city": "Luxor"},
            {"id": 5, "name": "Dave", "score": 95.5, "city": "Cairo"},
            {"id": 6, "name": "Eve", "score": 81.0, "city": "Giza"},
            {"id": 7, "name": "Bob", "score": 92.0, "city": "Alex"},
            {"id": 8, "name": "Frank", "score": 67.0, "city": "Cairo"},
        ],
        "value_col": "score",
        "threshold": 80,
        "unit": "points",
        "graph_context": "data dependency graph between pipeline stages",
        "dp_context": "optimal batch scheduling to minimize total processing time",
    },
    "simulation": {
        "name": "Simulation/Games",
        "product": "SimLab Engine",
        "dataset_desc": "simulation timestep logs with position, velocity, and score",
        "bottleneck": "collision detection between many game objects",
        "baseline_op": "check every pair of objects for collision O(n^2)",
        "optimized_op": "spatial hash grid for O(n) average collision detection",
        "sample_data": [
            {"step": 0, "entity": "player", "x": 0.0, "y": 0.0, "hp": 100},
            {"step": 1, "entity": "player", "x": 1.0, "y": 0.5, "hp": 100},
            {"step": 2, "entity": "enemy_1", "x": 2.1, "y": 1.2, "hp": 50},
            {"step": 3, "entity": "player", "x": 3.0, "y": 2.0, "hp": 95},
            {"step": 4, "entity": "enemy_2", "x": 4.2, "y": 2.8, "hp": 75},
            {"step": 5, "entity": "player", "x": 5.0, "y": 3.5, "hp": 90},
            {"step": 6, "entity": "enemy_1", "x": 5.9, "y": 4.1, "hp": 30},
            {"step": 7, "entity": "player", "x": 6.5, "y": 4.9, "hp": 85},
        ],
        "value_col": "hp",
        "threshold": 50,
        "unit": "hit points",
        "graph_context": "game world map as a graph (rooms/areas connected by paths)",
        "dp_context": "optimal resource allocation across simulation steps",
    },
    "space": {
        "name": "Space/Astro",
        "product": "Lightcurve Explorer",
        "dataset_desc": "star brightness (flux) measurements over time for exoplanet detection",
        "bottleneck": "searching sorted flux time-series for transit events",
        "baseline_op": "linear scan through all flux measurements",
        "optimized_op": "binary search on sorted time + heap for top-k dips",
        "sample_data": [
            {"time": 0.0, "flux": 1.000, "sector": "A"},
            {"time": 0.1, "flux": 0.998, "sector": "A"},
            {"time": 0.2, "flux": 0.700, "sector": "A"},
            {"time": 0.3, "flux": 0.985, "sector": "A"},
            {"time": 0.4, "flux": 1.010, "sector": "B"},
            {"time": 0.5, "flux": 0.680, "sector": "B"},
            {"time": 0.6, "flux": 0.995, "sector": "B"},
            {"time": 0.7, "flux": 0.950, "sector": "B"},
        ],
        "value_col": "flux",
        "threshold": 0.9,
        "unit": "relative flux",
        "graph_context": "star catalog connected by spatial proximity",
        "dp_context": "optimal observation scheduling across multiple targets",
    },
    "iot": {
        "name": "IoT/Reporting",
        "product": "AutoDashboard Reporter",
        "dataset_desc": "IoT sensor time series (temperature, humidity) from smart buildings",
        "bottleneck": "aggregating readings across thousands of devices",
        "baseline_op": "loop through all devices and all readings for each query",
        "optimized_op": "hash index on device ID + sorted time index for range queries",
        "sample_data": [
            {"ts": "2024-01-01 00:00", "device": "D01", "temp": 22.5, "humidity": 45},
            {"ts": "2024-01-01 01:00", "device": "D01", "temp": 23.0, "humidity": 47},
            {"ts": "2024-01-01 02:00", "device": "D02", "temp": 21.0, "humidity": 50},
            {"ts": "2024-01-01 03:00", "device": "D01", "temp": 99.9, "humidity": 30},
            {"ts": "2024-01-01 04:00", "device": "D02", "temp": 21.8, "humidity": 48},
            {"ts": "2024-01-01 05:00", "device": "D01", "temp": 22.0, "humidity": 46},
            {"ts": "2024-01-01 06:00", "device": "D03", "temp": 19.5, "humidity": 51},
            {"ts": "2024-01-01 07:00", "device": "D01", "temp": 23.5, "humidity": 44},
        ],
        "value_col": "temp",
        "threshold": 35,
        "unit": "degrees C",
        "graph_context": "building network topology (floors, rooms, sensors)",
        "dp_context": "optimal sensor polling schedule to minimize power consumption",
    },
}

STUDIO_WEEKLY = {
    1: {"task": "Profile your pipeline: identify which operations are O(1), O(n), O(n^2)", "deliverable": "annotated pipeline with Big-O labels for each function"},
    2: {"task": "Build a benchmark suite for your pipeline's critical path", "deliverable": "timing results at 3+ input sizes with scaling plot"},
    3: {"task": "Replace a linear search in your pipeline with binary search", "deliverable": "binary search implementation + correctness test + timing comparison"},
    4: {"task": "Sort your data by multiple criteria and benchmark sorted() vs manual sort", "deliverable": "sorted output + comparison showing Timsort advantage"},
    5: {"task": "Build a hash index for fast lookups on your primary key column", "deliverable": "Index class + demonstration of O(1) lookup vs O(n) scan"},
    6: {"task": "Use a heap to find top-k anomalies in your data", "deliverable": "top-k implementation + comparison with sorting approach"},
    7: {"task": "Implement your optimized DSA feature in src/project/dsa/", "deliverable": "optimized module + pytest tests proving correctness"},
    8: {"task": "Full benchmark: baseline vs optimized at 5 input sizes + plots", "deliverable": "benchmark_results.json + benchmark_plot.png showing >= 1.5x speedup"},
    9: {"task": "Build a tree-based index or use BST for range queries on your data", "deliverable": "BST/tree implementation applied to your track data"},
    10: {"task": "Model a domain problem as a graph and traverse it with BFS/DFS", "deliverable": "graph model + traversal producing useful output"},
    11: {"task": "Find shortest/cheapest paths in your domain graph", "deliverable": "Dijkstra applied to your track + path output"},
    12: {"task": "Apply DP or memoization to an expensive computation in your pipeline", "deliverable": "memoized function + before/after timing comparison"},
    13: {"task": "Wire all DSA optimizations into your product pipeline end-to-end", "deliverable": "integrated pipeline with config switch for baseline/optimized"},
    14: {"task": "Final demo: run pipeline, generate benchmark report, present results", "deliverable": "complete benchmark report + demo-ready pipeline"},
}


# ============================================================
# HELPER: build sample_data code string for a track
# ============================================================

def _sample_data_literal(track_key):
    """Return a string that defines sample_data list for a track."""
    rows = TRACK_DATA[track_key]["sample_data"]
    lines = ["sample_data = ["]
    for i, r in enumerate(rows):
        comma = "," if i < len(rows) - 1 else ""
        lines.append("    " + repr(r) + comma)
    lines.append("]")
    return "\n".join(lines)


# ============================================================
# ENRICHMENT HELPERS
# ============================================================

def _enrich_section(cells, section_title, examples, try_it=None,
                    common_mistakes=None, when_to_use=None, big_o_note=None):
    """Add a rich section with examples, expected output, exercises, etc."""
    for desc, code_str, expected in examples:
        cells.append(md(desc))
        cells.append(code(code_str))
        if expected:
            cells.append(md("**Expected Output:**\n```\n" + expected + "\n```"))

    if try_it:
        cells.append(md("### Try It Yourself"))
        cells.append(code(try_it))

    if common_mistakes:
        cells.append(md("### Common Mistakes\n\n" + common_mistakes))

    if when_to_use:
        cells.append(md("### When to Use This\n\n" + when_to_use))

    if big_o_note:
        cells.append(md("### Big-O Summary\n\n" + big_o_note))


# ============================================================
# CORE NOTEBOOK -- WEEK 1: Big-O & Python Cost Model
# ============================================================

def make_core_w01():
    cells = []

    cells.append(md("""# DSA Week 1 -- Big-O & Python Cost Model

**Course:** Data Structures & Algorithms (Year 2, Semester 4)
**Session:** 3 hours
**Prerequisites:** CP1 + CP2 + OOP
**Focus:** Big-O notation, list/dict/set costs

## Learning Objectives

By the end of this session you will be able to:

1. Explain what Big-O notation means in plain English
2. Classify common operations as O(1), O(log n), O(n), O(n log n), or O(n^2)
3. Predict the cost of Python list, dict, and set operations
4. Count operations in a simple algorithm and derive its Big-O
5. Visualize growth rates and understand why they matter at scale
6. Identify the bottleneck in a piece of code

## Why This Week Matters

You already know how to write Python code that *works*. This semester is about
making code that works **fast**. In CP1 you processed 8 rows of data. In the
real world your pipeline will handle 100,000 or 1,000,000 rows. The difference
between O(n) and O(n^2) at that scale is the difference between "done in 1 second"
and "still running after 3 hours."

Big-O is the language engineers use to talk about performance. After today you
will never look at a loop the same way again."""))

    cells.append(setup_cell())

    # --- Part 1: What is Big-O? ---
    cells.append(md("""---
## Part 1: What is Big-O? (Plain English First)

Big-O describes **how an algorithm's time grows** as the input gets bigger.
It answers one question: *"If I have 10x more data, how much longer does it take?"*

### The Restaurant Analogy

Imagine you run a restaurant:

```
Operation                  | Big-O     | Restaurant Analogy
---------------------------|-----------|--------------------------------------------
Look up reservation by ID  | O(1)      | The host checks a numbered list -- instant
Find someone by name       | O(n)      | Walk through every table asking names
Seat everyone optimally    | O(n log n)| Sort all guests by party size, then seat
Compare every pair         | O(n^2)    | Every guest shakes hands with every other
Try every seating combo    | O(2^n)    | Try EVERY possible arrangement -- impossible
```

### The Key Insight

Big-O drops constants and lower-order terms because at large scale,
only the **dominant term** matters:

```
Actual steps: 3n^2 + 5n + 100
Big-O:        O(n^2)

Why? At n = 1,000,000:
  3n^2  = 3,000,000,000,000   (3 trillion -- dominates!)
  5n    = 5,000,000            (5 million -- rounding error)
  100   = 100                  (irrelevant)
```

Think of it like measuring distance between cities: you say "300 km"
not "300 km, 47 meters, and 12 centimeters." The small parts do not matter."""))

    # --- Example 1: O(1) vs O(n) ---
    cells.append(md("""### Example 1: O(1) vs O(n) -- The Speed Gap

Let us see the difference between constant-time and linear-time lookup.
This is the single most important optimization you will learn."""))

    cells.append(code("""import time

# Build test data: 1 million items
n = 1_000_000
data_dict = {i: "value_" + str(i) for i in range(n)}
data_list = list(range(n))
data_set = set(range(n))

target = n - 1  # worst case for list

# O(1) -- dict lookup
start = time.time()
result = data_dict[target]
t_dict = time.time() - start

# O(n) -- list search
start = time.time()
found = target in data_list
t_list = time.time() - start

# O(1) -- set membership
start = time.time()
found = target in data_set
t_set = time.time() - start

print("=== Lookup Speed Comparison (n = 1,000,000) ===")
print()
print("  dict[key]     : " + "{:.1f}".format(t_dict * 1e6) + " microseconds  -- O(1)")
print("  item in list  : " + "{:.1f}".format(t_list * 1000) + " milliseconds  -- O(n)")
print("  item in set   : " + "{:.1f}".format(t_set * 1e6) + " microseconds  -- O(1)")
print()
if t_list > 0 and t_dict > 0:
    print("  dict is ~" + str(int(t_list / t_dict)) + "x faster than list!")
    print("  This is why choosing the right data structure matters.")"""))

    cells.append(md("""**Expected Output** (approximate):
```
=== Lookup Speed Comparison (n = 1,000,000) ===

  dict[key]     : 0.5 microseconds  -- O(1)
  item in list  : 12.3 milliseconds  -- O(n)
  item in set   : 0.3 microseconds  -- O(1)

  dict is ~24000x faster than list!
  This is why choosing the right data structure matters.
```

**What just happened:**
- `dict[key]` computes a hash, jumps directly to the slot -- O(1)
- `item in list` must scan from index 0 to 999,999 -- O(n)
- `item in set` uses the same hash trick as dict -- O(1)

> **Real-world impact:** If your pipeline checks membership 10,000 times
> on a list of 1M items, switching to a set saves you from 10,000 x 12ms
> = 2 minutes down to 10,000 x 0.5us = 5 milliseconds."""))

    # --- Example 2: Python Data Structure Cost Card ---
    cells.append(md("""---
### Example 2: Python Data Structure Cost Card

This is your **cheat sheet** for the entire semester. Bookmark this cell.
Every time you write code, ask: "What is the Big-O of this operation?" """))

    cells.append(code("""print(\"\"\"
============================================================
         PYTHON DATA STRUCTURE COST CARD
============================================================

LIST (array-based):
  Access by index   lst[i]        -> O(1)
  Append            lst.append(x) -> O(1) amortized
  Pop from end      lst.pop()     -> O(1)
  Pop from front    lst.pop(0)    -> O(n)  *** SLOW ***
  Insert at front   lst.insert(0) -> O(n)  *** SLOW ***
  Search            x in lst      -> O(n)
  Sort              lst.sort()    -> O(n log n)
  Slice             lst[a:b]      -> O(b - a)
  Length             len(lst)      -> O(1)

DICT (hash table):
  Lookup by key     d[k]          -> O(1) average
  Insert            d[k] = v      -> O(1) average
  Delete            del d[k]      -> O(1) average
  Membership        k in d        -> O(1) average
  Iterate keys      for k in d    -> O(n)

SET (hash set):
  Membership        x in s        -> O(1) average
  Add               s.add(x)      -> O(1) average
  Remove            s.remove(x)   -> O(1) average
  Union             s | t         -> O(len(s) + len(t))
  Intersection      s & t         -> O(min(len(s), len(t)))

TUPLE: same as list for access, but immutable (no append/insert)

DEQUE (collections.deque):
  Append right      dq.append(x)     -> O(1)
  Append left       dq.appendleft(x) -> O(1)
  Pop right         dq.pop()         -> O(1)
  Pop left          dq.popleft()     -> O(1)
  Access by index   dq[i]            -> O(n)  *** SLOW ***

============================================================
RULE: use dict/set for lookups, list for ordered sequences,
      deque for queue operations (add/remove from both ends).
============================================================
\"\"\")"""))

    cells.append(md("""**Key Takeaway:** The three operations that trap beginners are:
1. `x in list` -- O(n). Use `x in set` or `x in dict` instead -- O(1)
2. `list.pop(0)` or `list.insert(0, x)` -- O(n). Use `collections.deque` instead -- O(1)
3. Nested loops over a list for matching -- O(n^2). Build a dict first, then loop once -- O(n)"""))

    # --- Example 3: Counting Operations ---
    cells.append(md("""---
### Example 3: Counting Operations -- Learning to See Big-O

The best way to understand Big-O is to **count** how many operations
an algorithm performs at different input sizes. Let us do that explicitly."""))

    cells.append(code("""def linear_search_counted(data, target):
    \"\"\"O(n) -- check every element, count operations.\"\"\"
    ops = 0
    for item in data:
        ops += 1
        if item == target:
            return ops, True
    return ops, False

def binary_search_counted(sorted_data, target):
    \"\"\"O(log n) -- halve the search space, count operations.\"\"\"
    ops = 0
    low, high = 0, len(sorted_data) - 1
    while low <= high:
        ops += 1
        mid = (low + high) // 2
        if sorted_data[mid] == target:
            return ops, True
        elif sorted_data[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return ops, False

def nested_loop_counted(data):
    \"\"\"O(n^2) -- compare every pair, count operations.\"\"\"
    ops = 0
    n = len(data)
    for i in range(n):
        for j in range(i + 1, n):
            ops += 1
    return ops

# Compare at different sizes
print("=== Operation Counts at Different Input Sizes ===")
print()
print("  n         | Linear O(n) | Binary O(log n) | Pairs O(n^2)")
print("  ----------|-------------|-----------------|-------------")
for n in [10, 100, 1_000, 10_000, 100_000]:
    data = list(range(n))
    target = n - 1  # worst case

    lin_ops, _ = linear_search_counted(data, target)
    bin_ops, _ = binary_search_counted(data, target)
    # Only compute pairs for small n (otherwise too slow)
    if n <= 10_000:
        pair_ops = nested_loop_counted(data)
    else:
        pair_ops = n * (n - 1) // 2  # formula

    print("  " + "{:>9,}".format(n) + " | " + "{:>11,}".format(lin_ops) + " | " + "{:>15,}".format(bin_ops) + " | " + "{:>11,}".format(pair_ops))

print()
print("Key insight: at n = 100,000:")
print("  Linear does    100,000 operations")
print("  Binary does         17 operations")
print("  Pairs does  5,000,000,000 operations (5 BILLION)")"""))

    cells.append(md("""**Expected Output:**
```
=== Operation Counts at Different Input Sizes ===

  n         | Linear O(n) | Binary O(log n) | Pairs O(n^2)
  ----------|-------------|-----------------|-------------
         10 |          10 |               4 |          45
        100 |         100 |               7 |       4,950
      1,000 |       1,000 |              10 |     499,500
     10,000 |      10,000 |              14 |  49,995,000
    100,000 |     100,000 |              17 | 4,999,950,000

Key insight: at n = 100,000:
  Linear does    100,000 operations
  Binary does         17 operations
  Pairs does  5,000,000,000 operations (5 BILLION)
```

**The 10x test:**
- O(n): 10x more data = 10x more time (linear growth)
- O(log n): 10x more data = ~3 more steps (barely grows!)
- O(n^2): 10x more data = 100x more time (explosive growth!)"""))

    # --- Try It 1 ---
    cells.append(md("""### Try It Yourself #1

What is the Big-O of each code snippet below? Add your answer as a comment."""))

    cells.append(code("""# Snippet A: What is the Big-O?
def snippet_a(data):
    return data[0] + data[-1]
# Answer: O(__)

# Snippet B: What is the Big-O?
def snippet_b(data):
    total = 0
    for x in data:
        total += x
    return total
# Answer: O(__)

# Snippet C: What is the Big-O?
def snippet_c(data):
    for i in range(len(data)):
        for j in range(len(data)):
            if data[i] == data[j] and i != j:
                return True
    return False
# Answer: O(__)

# Snippet D: What is the Big-O?
def snippet_d(data):
    return len(data)
# Answer: O(__)

# Snippet E: What is the Big-O?
def snippet_e(data):
    s = set(data)       # step 1
    return 42 in s      # step 2
# Answer for step 1: O(__)
# Answer for step 2: O(__)
# Answer combined:   O(__)"""))

    # --- Part 2: Visualizing Growth ---
    cells.append(md("""---
## Part 2: Visualizing Growth Rates

Numbers are one thing -- seeing the curves is another. This plot will make
Big-O intuitive for you forever."""))

    cells.append(code("""import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import math
import os

ns = list(range(1, 101))
o1     = [1] * len(ns)
olog   = [math.log2(n) if n > 0 else 0 for n in ns]
on     = list(ns)
onlogn = [n * math.log2(n) if n > 0 else 0 for n in ns]
on2    = [n ** 2 for n in ns]

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Left: all curves, limited y-axis
ax = axes[0]
ax.plot(ns, o1, label="O(1)", linewidth=2)
ax.plot(ns, olog, label="O(log n)", linewidth=2)
ax.plot(ns, on, label="O(n)", linewidth=2)
ax.plot(ns, onlogn, label="O(n log n)", linewidth=2)
ax.plot(ns, on2, label="O(n^2)", linewidth=2, linestyle="--")
ax.set_title("Growth Rates (zoomed to 500)", fontsize=13)
ax.set_xlabel("Input Size (n)")
ax.set_ylabel("Operations")
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_ylim(0, 500)

# Right: log scale to see the full picture
ax2 = axes[1]
ax2.plot(ns, o1, label="O(1)", linewidth=2)
ax2.plot(ns, olog, label="O(log n)", linewidth=2)
ax2.plot(ns, on, label="O(n)", linewidth=2)
ax2.plot(ns, onlogn, label="O(n log n)", linewidth=2)
ax2.plot(ns, on2, label="O(n^2)", linewidth=2, linestyle="--")
ax2.set_title("Growth Rates (log scale)", fontsize=13)
ax2.set_xlabel("Input Size (n)")
ax2.set_ylabel("Operations (log scale)")
ax2.set_yscale("log")
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
os.makedirs("reports/benchmark", exist_ok=True)
fig.savefig("reports/benchmark/growth_rates.png", dpi=100, bbox_inches="tight")
plt.close(fig)
print("Saved: reports/benchmark/growth_rates.png")
print()
print("Notice how O(n^2) explodes upward while O(log n) barely rises.")
print("At n=100: O(n^2)=10,000 but O(log n)=7. That is 1,400x difference!")"""))

    cells.append(md("""**Expected Output:**
```
Saved: reports/benchmark/growth_rates.png

Notice how O(n^2) explodes upward while O(log n) barely rises.
At n=100: O(n^2)=10,000 but O(log n)=7. That is 1,400x difference!
```"""))

    # --- Part 3: Python cost model experiments ---
    cells.append(md("""---
## Part 3: Proving the Cost Model with Experiments

Theory is nice, but engineers **measure**. Let us verify the cost card
with actual timing experiments."""))

    cells.append(code("""import time

def time_operation(label, func, repeat=5):
    \"\"\"Time a function, return average in microseconds.\"\"\"
    times = []
    for _ in range(repeat):
        start = time.time()
        func()
        times.append(time.time() - start)
    avg_us = sum(times) / len(times) * 1e6
    print("  " + label.ljust(35) + ": " + "{:>10.1f}".format(avg_us) + " us")
    return avg_us

n = 100_000
test_list = list(range(n))
test_dict = {i: i for i in range(n)}
test_set = set(range(n))

print("=== Timing Python Operations (n = " + "{:,}".format(n) + ") ===")
print()

print("LIST operations:")
time_operation("list[0] (front access)", lambda: test_list[0])
time_operation("list[-1] (back access)", lambda: test_list[-1])
time_operation("list[n//2] (middle access)", lambda: test_list[n // 2])
time_operation("99999 in list (worst case)", lambda: 99999 in test_list)
time_operation("0 in list (best case)", lambda: 0 in test_list)
print()

print("DICT operations:")
time_operation("dict[99999] (lookup)", lambda: test_dict[99999])
time_operation("99999 in dict (membership)", lambda: 99999 in test_dict)
print()

print("SET operations:")
time_operation("99999 in set (membership)", lambda: 99999 in test_set)
print()

print("CONCLUSION:")
print("  Index access (list[i]) and dict/set lookups are all O(1) -- microseconds.")
print("  Searching inside a list (x in list) is O(n) -- much slower!")"""))

    cells.append(md("""**Expected Output** (times vary by machine):
```
=== Timing Python Operations (n = 100,000) ===

LIST operations:
  list[0] (front access)            :        0.2 us
  list[-1] (back access)            :        0.2 us
  list[n//2] (middle access)        :        0.2 us
  99999 in list (worst case)        :     1200.0 us
  0 in list (best case)             :        0.2 us

DICT operations:
  dict[99999] (lookup)              :        0.3 us
  99999 in dict (membership)        :        0.2 us

SET operations:
  99999 in set (membership)         :        0.2 us

CONCLUSION:
  Index access (list[i]) and dict/set lookups are all O(1) -- microseconds.
  Searching inside a list (x in list) is O(n) -- much slower!
```"""))

    # --- Part 4: Common traps ---
    cells.append(md("""---
## Part 4: The Three Performance Traps

These are the most common mistakes that make student code slow.
After this semester you will never make them again.

### Trap 1: Membership testing on a list"""))

    cells.append(code("""import time

# BAD: checking membership in a list inside a loop
def find_duplicates_bad(data):
    \"\"\"O(n^2) -- for each item, scan the seen list.\"\"\"
    seen = []  # <-- THIS IS THE PROBLEM
    duplicates = []
    for item in data:
        if item in seen:        # O(n) scan every time!
            duplicates.append(item)
        seen.append(item)
    return duplicates

# GOOD: checking membership in a set inside a loop
def find_duplicates_good(data):
    \"\"\"O(n) -- for each item, check the seen set.\"\"\"
    seen = set()  # <-- O(1) membership test
    duplicates = []
    for item in data:
        if item in seen:        # O(1) check!
            duplicates.append(item)
        seen.add(item)
    return duplicates

# Test correctness
import random
random.seed(42)
data = [random.randint(0, 5000) for _ in range(10_000)]

d1 = find_duplicates_bad(data)
d2 = find_duplicates_good(data)
assert sorted(d1) == sorted(d2), "Both must find same duplicates"
print("Both find " + str(len(d1)) + " duplicates -- correctness verified!")
print()

# Time them
start = time.time()
find_duplicates_bad(data)
t_bad = time.time() - start

start = time.time()
find_duplicates_good(data)
t_good = time.time() - start

print("BAD  (list): " + "{:.4f}".format(t_bad) + "s -- O(n^2)")
print("GOOD (set):  " + "{:.4f}".format(t_good) + "s -- O(n)")
print("Speedup:     " + str(int(t_bad / t_good)) + "x")"""))

    cells.append(md("""**Expected Output:**
```
Both find 4877 duplicates -- correctness verified!

BAD  (list): 1.2345s -- O(n^2)
GOOD (set):  0.0012s -- O(n)
Speedup:     1000x
```

### Trap 2: Building strings with += in a loop

```python
# BAD: O(n^2) -- each += creates a new string
result = ""
for word in words:
    result += word + " "    # copies entire string each time!

# GOOD: O(n) -- join does one allocation
result = " ".join(words)
```

### Trap 3: Using list.pop(0) or list.insert(0, x)

```python
# BAD: O(n) per operation -- shifts all elements
queue = [1, 2, 3, 4, 5]
item = queue.pop(0)         # shifts 4 elements left

# GOOD: O(1) per operation
from collections import deque
queue = deque([1, 2, 3, 4, 5])
item = queue.popleft()      # no shifting needed
```"""))

    # --- Try It 2 ---
    cells.append(md("""### Try It Yourself #2

Fix this slow function. It finds all numbers that appear in BOTH lists.
The current version is O(n*m). Make it O(n+m)."""))

    cells.append(code("""# SLOW VERSION -- O(n * m)
def common_elements_slow(list_a, list_b):
    result = []
    for item in list_a:
        if item in list_b:  # O(m) scan each time!
            result.append(item)
    return result

# TODO: Write a FAST version -- O(n + m)
def common_elements_fast(list_a, list_b):
    # Hint: convert one list to a set first
    pass

# Test
a = list(range(0, 10000, 2))    # even numbers
b = list(range(0, 10000, 3))    # multiples of 3
# Expected: numbers divisible by both 2 and 3 (i.e., multiples of 6)

result = common_elements_slow(a, b)
print("Common elements:", len(result))
# TODO: time both versions and print the speedup"""))

    # --- Part 5: Connection to projects ---
    cells.append(md("""---
## Part 5: Why Big-O Matters for Your Project

Every project track has performance bottlenecks that Big-O thinking can solve:

| Track | Product | Typical Bottleneck | Fix |
|-------|---------|-------------------|-----|
| Robotics | MechaSense Studio | Scanning all sensor readings for anomalies | Hash index on sensor ID |
| Data/AI | CleanReport Pipeline | Deduplicating records with nested loops | Set-based dedup |
| Simulation | SimLab Engine | Checking every pair of objects for collision | Spatial hash grid |
| Space | Lightcurve Explorer | Searching sorted time-series for transit events | Binary search |
| IoT | AutoDashboard Reporter | Aggregating across thousands of devices | Dict-based grouping |

This semester you will implement at least one of these optimizations and **prove**
it is faster with benchmarks. Today's lesson gives you the vocabulary to analyze
what is slow and predict what will help."""))

    cells.append(code("""# Quick demo: the "before and after" pattern you will use all semester
import time

# Simulate a pipeline bottleneck: finding all readings above threshold
n = 500_000
readings = list(range(n))

# BEFORE: scan all readings looking for matches to a target set
targets = list(range(0, n, 100))  # every 100th value

start = time.time()
# BAD: nested loop
matches_slow = [r for r in readings if r in targets]
t_slow = time.time() - start

# AFTER: convert targets to a set
target_set = set(targets)
start = time.time()
matches_fast = [r for r in readings if r in target_set]
t_fast = time.time() - start

print("Results match:", len(matches_slow) == len(matches_fast))
print("Before (list targets): " + "{:.3f}".format(t_slow) + "s")
print("After  (set targets):  " + "{:.3f}".format(t_fast) + "s")
print("Speedup: " + "{:.0f}".format(t_slow / t_fast) + "x")
print()
print("This is EXACTLY the kind of optimization you will do in your project.")"""))

    cells.append(md("""**Expected Output:**
```
Results match: True
Before (list targets): 5.123s
After  (set targets):  0.045s
Speedup: 114x

This is EXACTLY the kind of optimization you will do in your project.
```"""))

    # --- Common Mistakes ---
    cells.append(md("""---
## Common Mistakes with Big-O

| Mistake | Why It Is Wrong | Correct |
|---------|----------------|---------|
| "O(2n) because of two loops" | Constants are dropped | O(n) -- two sequential loops are still O(n) |
| "dict lookup is O(n)" | Dict uses hash table | O(1) average |
| "sorted() is O(n)" | Sorting requires comparisons | O(n log n) |
| "O(1) because it is one line" | One line can hide a loop | `x in list` is O(n) even though it is one line |
| "O(n^2) because nested loops" | Not always! | Only if BOTH loops go to n. `for i in range(n): for j in range(5)` is O(n) |

### Quick Rules for Spotting Big-O

1. **No loops:** probably O(1)
2. **One loop over n items:** O(n)
3. **Loop that halves each time:** O(log n) -- like binary search
4. **Nested loops both over n:** O(n^2)
5. **Sorting:** O(n log n) minimum
6. **Trying all subsets:** O(2^n) -- avoid at all costs!"""))

    # --- Mini-Quiz ---
    cells.append(md("---\n## Mini-Quiz"))

    cells.append(code("""# Q1: What is the Big-O of this code?
def mystery1(data):
    s = set(data)
    return 42 in s
# Answer: O(__)  (building the set is ___, checking membership is ___)

# Q2: What is the Big-O of this code?
def mystery2(data):
    for i in range(len(data)):
        for j in range(10):
            print(data[i])
# Answer: O(__)  (hint: the inner loop is constant, not dependent on n)

# Q3: Your pipeline processes n records. For EACH record, it checks
# if the record's ID exists in a list of 1000 known IDs.
# What is the Big-O? How would you fix it?
# Answer:
# Current: O(__)
# Fixed:   O(__)
# Fix: ___"""))

    # --- Homework preview ---
    cells.append(md("""---
## Homework Preview

This week's homework asks you to:
1. Classify 10 code snippets by Big-O
2. Fix 3 slow functions using the right data structure
3. Time the before/after and prove the speedup
4. Annotate your own project pipeline functions with Big-O

See the homework notebook for full details."""))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# CORE NOTEBOOK -- WEEK 2: Benchmark Literacy
# ============================================================

def make_core_w02():
    cells = []

    cells.append(md("""# DSA Week 2 -- Benchmark Literacy

**Course:** Data Structures & Algorithms (Year 2, Semester 4)
**Session:** 3 hours
**Prerequisites:** Week 1 (Big-O)
**Focus:** timeit, scaling plots, measuring performance properly

## Learning Objectives

By the end of this session you will be able to:

1. Use `timeit` for accurate micro-benchmarks
2. Avoid common benchmarking pitfalls (warmup, garbage collection, outliers)
3. Run a scaling test: measure at multiple input sizes
4. Create publication-quality benchmark plots
5. Interpret results to confirm Big-O predictions
6. Build a reusable benchmark harness for your project

## Why This Week Matters

Last week you learned to *predict* performance with Big-O. This week you learn
to *measure* it. In engineering, if you cannot measure it, you cannot improve it.
Your final project requires a benchmark proving >= 1.5x speedup. Today you build
the tools to do that."""))

    cells.append(setup_cell())

    # --- Part 1: timeit basics ---
    cells.append(md("""---
## Part 1: Why `time.time()` Is Not Enough

Last week we used `time.time()` for quick demos. But for real benchmarks,
it has problems:

```
Problems with time.time():
  1. Measures wall clock -- includes OS interrupts, other programs
  2. Single measurement -- could be an outlier
  3. Low resolution on some systems -- cannot measure microseconds
  4. No warmup -- first run is often slower (CPU cache, JIT)
```

Python's `timeit` module fixes all of these:
- Runs the code many times and averages
- Disables garbage collection during measurement
- Uses the highest-resolution timer available"""))

    cells.append(code("""import timeit

# === Basic timeit usage ===

# Method 1: timeit.timeit with a lambda
time_taken = timeit.timeit(lambda: sum(range(1000)), number=10_000)
print("sum(range(1000)) x 10,000 runs: " + "{:.4f}".format(time_taken) + "s")
print("Average per call: " + "{:.2f}".format(time_taken / 10_000 * 1e6) + " us")
print()

# Method 2: comparing two approaches
def slow_sum(data):
    total = 0
    for x in data:
        total += x
    return total

def fast_sum(data):
    return sum(data)

data = list(range(10_000))
n_runs = 1000

t_slow = timeit.timeit(lambda: slow_sum(data), number=n_runs)
t_fast = timeit.timeit(lambda: fast_sum(data), number=n_runs)

print("=== Loop sum vs built-in sum (n=10,000) ===")
print("  Loop sum:     " + "{:.4f}".format(t_slow) + "s (" + str(n_runs) + " runs)")
print("  Built-in sum: " + "{:.4f}".format(t_fast) + "s (" + str(n_runs) + " runs)")
print("  Speedup:      " + "{:.1f}".format(t_slow / t_fast) + "x")
print()
print("  Per-call average:")
print("    Loop:     " + "{:.2f}".format(t_slow / n_runs * 1e6) + " us")
print("    Built-in: " + "{:.2f}".format(t_fast / n_runs * 1e6) + " us")"""))

    cells.append(md("""**Expected Output:**
```
sum(range(1000)) x 10,000 runs: 0.4523s
Average per call: 45.23 us

=== Loop sum vs built-in sum (n=10,000) ===
  Loop sum:     3.2145s (1000 runs)
  Built-in sum: 0.2134s (1000 runs)
  Speedup:      15.1x

  Per-call average:
    Loop:     3214.50 us
    Built-in:  213.40 us
```"""))

    # --- Part 2: Scaling tests ---
    cells.append(md("""---
## Part 2: Scaling Tests -- Confirming Big-O Experimentally

A scaling test measures execution time at **multiple input sizes** and checks
whether the growth matches your Big-O prediction.

```
If you predict O(n):
  Double the input -> time should roughly double
  10x the input   -> time should roughly 10x

If you predict O(n^2):
  Double the input -> time should roughly 4x (2^2)
  10x the input   -> time should roughly 100x (10^2)

If you predict O(log n):
  Double the input -> time should increase by a constant
  10x the input   -> time should increase by a constant
```"""))

    cells.append(code("""import timeit

def benchmark_scaling(func, sizes, n_runs=100, label=""):
    \"\"\"Measure function time across different input sizes.\"\"\"
    results = []
    for n in sizes:
        data = list(range(n))
        t = timeit.timeit(lambda d=data: func(d), number=n_runs)
        avg_ms = t / n_runs * 1000
        results.append({"n": n, "time_ms": avg_ms})
    return results

def print_scaling_table(results, label):
    \"\"\"Print a formatted scaling table with growth ratios.\"\"\"
    print("=== " + label + " ===")
    print("  " + "n".rjust(10) + " | " + "time (ms)".rjust(10) + " | " + "ratio".rjust(8))
    print("  " + "-" * 10 + "-|-" + "-" * 10 + "-|-" + "-" * 8)
    for i, r in enumerate(results):
        ratio = ""
        if i > 0 and results[i - 1]["time_ms"] > 0:
            ratio = "{:.1f}x".format(r["time_ms"] / results[i - 1]["time_ms"])
        print("  " + "{:>10,}".format(r["n"]) + " | " + "{:>10.3f}".format(r["time_ms"]) + " | " + ratio.rjust(8))
    print()

# Test 1: O(n) -- sum
sizes = [1_000, 2_000, 5_000, 10_000, 20_000, 50_000]
results_sum = benchmark_scaling(sum, sizes, n_runs=200, label="sum")
print_scaling_table(results_sum, "sum() -- expected O(n)")
print("  If O(n): doubling n should roughly double the time.")
print("  Check the 1000->2000 ratio and 10000->20000 ratio.")
print()

# Test 2: O(n^2) -- nested membership
def quadratic_example(data):
    count = 0
    for x in data:
        if x in data:
            count += 1
    return count

sizes_q = [500, 1_000, 2_000, 4_000]
results_q = benchmark_scaling(quadratic_example, sizes_q, n_runs=5, label="quadratic")
print_scaling_table(results_q, "quadratic -- expected O(n^2)")
print("  If O(n^2): doubling n should roughly 4x the time.")"""))

    cells.append(md("""**Expected Output** (times vary):
```
=== sum() -- expected O(n) ===
           n |  time (ms) |    ratio
  ---------- | ---------- | --------
       1,000 |      0.010 |
       2,000 |      0.020 |    2.0x
       5,000 |      0.050 |    2.5x
      10,000 |      0.100 |    2.0x
      20,000 |      0.200 |    2.0x
      50,000 |      0.500 |    2.5x

  If O(n): doubling n should roughly double the time.

=== quadratic -- expected O(n^2) ===
           n |  time (ms) |    ratio
  ---------- | ---------- | --------
         500 |      2.500 |
       1,000 |     10.000 |    4.0x
       2,000 |     40.000 |    4.0x
       4,000 |    160.000 |    4.0x

  If O(n^2): doubling n should roughly 4x the time.
```

**Reading the ratio column:**
- Ratios near 2.0x when doubling input = O(n)
- Ratios near 4.0x when doubling input = O(n^2)
- Ratios near 1.0x when doubling input = O(1) or O(log n)"""))

    # --- Part 3: Benchmark plots ---
    cells.append(md("""---
## Part 3: Creating Benchmark Plots

A picture is worth a thousand numbers. Let us build a reusable plotting function."""))

    cells.append(code("""import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

def plot_scaling(results_list, labels, title, savepath, expected_curves=None):
    \"\"\"Create a benchmark scaling plot.

    results_list: list of result dicts [{n, time_ms}, ...]
    labels: list of labels for each series
    title: plot title
    savepath: where to save
    expected_curves: optional list of (label, func) for theoretical curves
    \"\"\"
    colors = ["#2196F3", "#F44336", "#4CAF50", "#FF9800", "#9C27B0"]
    fig, ax = plt.subplots(figsize=(10, 6))

    for i, (results, label) in enumerate(zip(results_list, labels)):
        ns = [r["n"] for r in results]
        times = [r["time_ms"] for r in results]
        color = colors[i % len(colors)]
        ax.plot(ns, times, "o-", label=label, linewidth=2, markersize=6, color=color)

    ax.set_title(title, fontsize=14)
    ax.set_xlabel("Input Size (n)", fontsize=12)
    ax.set_ylabel("Time (ms)", fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    os.makedirs(os.path.dirname(savepath), exist_ok=True)
    fig.savefig(savepath, dpi=100, bbox_inches="tight")
    plt.close(fig)
    print("Saved: " + savepath)

# Demo: plot linear vs quadratic scaling
plot_scaling(
    [results_sum, results_q],
    ["sum() O(n)", "quadratic O(n^2)"],
    "Scaling Test: O(n) vs O(n^2)",
    "reports/benchmark/scaling_test.png"
)"""))

    cells.append(md("""**Expected Output:**
```
Saved: reports/benchmark/scaling_test.png
```"""))

    # --- Part 4: Comparison benchmark ---
    cells.append(md("""---
## Part 4: Baseline vs Optimized Comparison

This is the pattern you will use for your project: measure baseline, measure
optimized, compute speedup, plot both."""))

    cells.append(code("""import timeit
import json

def benchmark_comparison(baseline_func, optimized_func, data_generator,
                         sizes, n_runs=100, label="Benchmark"):
    \"\"\"Run a complete baseline vs optimized benchmark.\"\"\"
    results = {
        "sizes": [],
        "baseline_ms": [],
        "optimized_ms": [],
        "speedup": []
    }

    print("=== " + label + " ===")
    print("  " + "n".rjust(10) + " | " + "baseline".rjust(10) + " | " + "optimized".rjust(10) + " | " + "speedup".rjust(8))
    print("  " + "-" * 10 + "-|-" + "-" * 10 + "-|-" + "-" * 10 + "-|-" + "-" * 8)

    for n in sizes:
        data = data_generator(n)
        t_base = timeit.timeit(lambda d=data: baseline_func(d), number=n_runs)
        t_opt = timeit.timeit(lambda d=data: optimized_func(d), number=n_runs)

        base_ms = t_base / n_runs * 1000
        opt_ms = t_opt / n_runs * 1000
        speedup = base_ms / opt_ms if opt_ms > 0 else float("inf")

        results["sizes"].append(n)
        results["baseline_ms"].append(round(base_ms, 4))
        results["optimized_ms"].append(round(opt_ms, 4))
        results["speedup"].append(round(speedup, 1))

        print("  " + "{:>10,}".format(n) + " | " + "{:>8.3f}ms".format(base_ms) + " | " + "{:>8.3f}ms".format(opt_ms) + " | " + "{:>6.1f}x".format(speedup))

    print()
    return results

def plot_comparison(results, title, savepath):
    \"\"\"Create baseline vs optimized comparison plot.\"\"\"
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    sizes = results["sizes"]

    # Left: time comparison
    ax1.plot(sizes, results["baseline_ms"], "o-", label="Baseline",
             linewidth=2, color="#F44336")
    ax1.plot(sizes, results["optimized_ms"], "s-", label="Optimized",
             linewidth=2, color="#4CAF50")
    ax1.set_title("Execution Time", fontsize=14)
    ax1.set_xlabel("Input Size (n)")
    ax1.set_ylabel("Time (ms)")
    ax1.legend(fontsize=12)
    ax1.grid(True, alpha=0.3)

    # Right: speedup bars
    ax2.bar(range(len(sizes)), results["speedup"], color="#2196F3")
    ax2.set_xticks(range(len(sizes)))
    ax2.set_xticklabels(["{:,}".format(n) for n in sizes], rotation=45)
    ax2.set_title("Speedup Factor", fontsize=14)
    ax2.set_xlabel("Input Size (n)")
    ax2.set_ylabel("Speedup (x)")
    ax2.axhline(y=1.5, color="red", linestyle="--", label="1.5x target")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    os.makedirs(os.path.dirname(savepath), exist_ok=True)
    fig.savefig(savepath, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Saved: " + savepath)

# Demo: list search vs set search
import random
random.seed(42)

def gen_data(n):
    return [random.randint(0, n * 10) for _ in range(n)]

def baseline_search(data):
    return 999 in data

def optimized_search(data):
    s = set(data)
    return 999 in s

sizes = [1_000, 5_000, 10_000, 50_000, 100_000]
results = benchmark_comparison(baseline_search, optimized_search, gen_data,
                               sizes, n_runs=50, label="List search vs Set")

plot_comparison(results, "Baseline (list) vs Optimized (set)",
                "reports/benchmark/comparison_demo.png")

# Save as JSON
os.makedirs("reports/benchmark", exist_ok=True)
with open("reports/benchmark/comparison_demo.json", "w") as f:
    json.dump(results, f, indent=2)
print("Saved: reports/benchmark/comparison_demo.json")"""))

    cells.append(md("""**Expected Output:**
```
=== List search vs Set ===
           n |   baseline |  optimized |  speedup
  ---------- | ---------- | ---------- | --------
       1,000 |    0.010ms |    0.025ms |    0.4x
       5,000 |    0.050ms |    0.120ms |    0.4x
      10,000 |    0.100ms |    0.240ms |    0.4x
      50,000 |    0.500ms |    1.200ms |    0.4x
     100,000 |    1.000ms |    2.400ms |    0.4x

Saved: reports/benchmark/comparison_demo.png
Saved: reports/benchmark/comparison_demo.json
```

**Wait -- the optimized version is SLOWER?** Yes! Building the set costs O(n),
so for a SINGLE search, list is fine. The optimization only helps when you
search MANY times. That is an important lesson: **always benchmark!**"""))

    # --- Part 5: Benchmarking pitfalls ---
    cells.append(md("""---
## Part 5: Benchmarking Pitfalls

### Pitfall 1: Not enough runs
```python
# BAD: single measurement -- could be an outlier
t = timeit.timeit(func, number=1)

# GOOD: many runs
t = timeit.timeit(func, number=1000)
```

### Pitfall 2: Measuring setup time
```python
# BAD: includes data creation in the timing
t = timeit.timeit(lambda: sum(list(range(10000))), number=1000)

# GOOD: create data once, measure only the operation
data = list(range(10000))
t = timeit.timeit(lambda: sum(data), number=1000)
```

### Pitfall 3: Not checking correctness first
```
Always verify that baseline and optimized produce the SAME result
before comparing speed. A fast wrong answer is useless.
```

### Pitfall 4: Comparing at only one size
```
O(n) and O(n^2) look similar at small n. You need at least 3-5
different sizes to see the growth pattern.
```"""))

    # --- Try It ---
    cells.append(md("### Try It Yourself\n\nBuild a benchmark that compares `list.sort()` vs `sorted()` at 5 different sizes.\nPlot the results. What Big-O do you observe for both?"))

    cells.append(code("""# TODO: Benchmark list.sort() vs sorted()
import timeit
import random

def bench_sort_inplace(data):
    d = data.copy()
    d.sort()
    return d

def bench_sort_new(data):
    return sorted(data)

# Generate random data at different sizes
sizes = [1_000, 5_000, 10_000, 50_000, 100_000]

# YOUR CODE: benchmark both, print results, plot
# Hint: use benchmark_comparison from above"""))

    cells.append(md("---\n## Homework Preview\n\nThis week's homework asks you to build a complete benchmark suite for your\nproject track and produce benchmark_results.json and benchmark_plot.png."))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# CORE NOTEBOOK -- WEEK 3: Searching
# ============================================================

def make_core_w03():
    cells = []

    cells.append(md("""# DSA Week 3 -- Searching: Linear vs Binary

**Course:** Data Structures & Algorithms
**Session:** 3 hours
**Prerequisites:** Weeks 1-2 (Big-O, Benchmarking)
**Focus:** Linear search, binary search, sorted data

## Learning Objectives

1. Implement linear search and understand its O(n) cost
2. Implement binary search and understand its O(log n) cost
3. Trace binary search step-by-step on paper
4. Know the precondition: data must be sorted for binary search
5. Use Python's `bisect` module for production binary search
6. Benchmark linear vs binary and see the difference at scale

## The Big Idea

Searching is the most common operation in computing. Every time your pipeline
looks up a record, finds a threshold crossing, or checks if a value exists,
it is searching. The difference between O(n) and O(log n) can be enormous:

```
n = 1,000,000 items:
  Linear search: up to 1,000,000 comparisons
  Binary search: at most 20 comparisons

That is 50,000x fewer operations!
```"""))

    cells.append(setup_cell())

    # --- Part 1: Linear Search ---
    cells.append(md("""---
## Part 1: Linear Search -- The Slow but Simple Way

Linear search checks every element one by one until it finds the target
(or reaches the end). It works on **any** data -- sorted or unsorted.

```
Linear search for target = 42:

  [15, 23, 8, 42, 16, 50, 4, 31]
   ^   no
       ^   no
           ^  no
              ^   FOUND at index 3!

  Worst case: check ALL elements -> O(n)
  Best case:  first element matches -> O(1)
  Average:    check n/2 elements -> O(n)
```"""))

    cells.append(code("""def linear_search(data, target):
    \"\"\"Search by checking every element. O(n).\"\"\"
    for i, item in enumerate(data):
        if item == target:
            return i
    return -1

# === Example 1: Basic search ===
data = [15, 23, 8, 42, 16, 50, 4, 31]
print("Data:", data)
print()

for target in [42, 50, 99]:
    idx = linear_search(data, target)
    if idx >= 0:
        print("  Search for " + str(target) + ": FOUND at index " + str(idx))
    else:
        print("  Search for " + str(target) + ": NOT FOUND")"""))

    cells.append(md("""**Expected Output:**
```
Data: [15, 23, 8, 42, 16, 50, 4, 31]

  Search for 42: FOUND at index 3
  Search for 50: FOUND at index 5
  Search for 99: NOT FOUND
```"""))

    # --- Traced linear search ---
    cells.append(md("""### Example 2: Traced Linear Search

Let us see exactly what happens at each step."""))

    cells.append(code("""def linear_search_traced(data, target):
    \"\"\"Linear search with step-by-step trace.\"\"\"
    print("  Searching for " + str(target) + " in " + str(data))
    for i, item in enumerate(data):
        status = "MATCH!" if item == target else "skip"
        print("    Step " + str(i + 1) + ": compare data[" + str(i) + "]=" + str(item) + " with " + str(target) + " -> " + status)
        if item == target:
            print("  Found at index " + str(i) + " in " + str(i + 1) + " steps")
            return i
    print("  Not found after " + str(len(data)) + " steps")
    return -1

data = [15, 23, 8, 42, 16, 50, 4, 31]
print("=== Trace 1: target exists ===")
linear_search_traced(data, 42)
print()
print("=== Trace 2: target not found ===")
linear_search_traced(data, 99)"""))

    cells.append(md("""**Expected Output:**
```
=== Trace 1: target exists ===
  Searching for 42 in [15, 23, 8, 42, 16, 50, 4, 31]
    Step 1: compare data[0]=15 with 42 -> skip
    Step 2: compare data[1]=23 with 42 -> skip
    Step 3: compare data[2]=8 with 42 -> skip
    Step 4: compare data[3]=42 with 42 -> MATCH!
  Found at index 3 in 4 steps

=== Trace 2: target not found ===
  Searching for 99 in [15, 23, 8, 42, 16, 50, 4, 31]
    Step 1: compare data[0]=15 with 99 -> skip
    Step 2: compare data[1]=23 with 99 -> skip
    ...
    Step 8: compare data[7]=31 with 99 -> skip
  Not found after 8 steps
```"""))

    # --- Part 2: Binary Search ---
    cells.append(md("""---
## Part 2: Binary Search -- The Fast Way (Requires Sorted Data!)

Binary search is like the number-guessing game:
"I am thinking of a number 1-100. You guess. I say higher or lower."

The optimal strategy: always guess the MIDDLE. This halves the remaining
possibilities each time.

```
Binary search for target = 9 in [1, 3, 5, 7, 9, 11, 13, 15]:

Step 1: [1, 3, 5, |7|, 9, 11, 13, 15]    mid=7    9 > 7 -> go RIGHT
                         ^^^^^^^^^^^^^
Step 2:              [9, |11|, 13, 15]     mid=11   9 < 11 -> go LEFT
                      ^
Step 3:              [|9|]                  mid=9    FOUND!

Only 3 steps for 8 items! (log2(8) = 3)

Compare: linear search would take up to 8 steps.
For 1,000,000 items: binary = 20 steps, linear = 1,000,000 steps!
```

**CRITICAL PRECONDITION:** Binary search ONLY works on sorted data.
If the data is not sorted, the results will be wrong."""))

    cells.append(code("""def binary_search(sorted_data, target):
    \"\"\"Binary search on sorted data. O(log n).

    PRECONDITION: sorted_data must be sorted in ascending order!
    \"\"\"
    low = 0
    high = len(sorted_data) - 1
    steps = 0

    while low <= high:
        steps += 1
        mid = (low + high) // 2

        if sorted_data[mid] == target:
            return mid, steps
        elif sorted_data[mid] < target:
            low = mid + 1    # target is in the RIGHT half
        else:
            high = mid - 1   # target is in the LEFT half

    return -1, steps  # not found

# === Example 1: Basic binary search ===
data = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
print("Sorted data:", data)
print()

for target in [9, 1, 19, 8]:
    idx, steps = binary_search(data, target)
    if idx >= 0:
        print("  Search for " + str(target).rjust(2) + ": FOUND at index " + str(idx) + " in " + str(steps) + " steps")
    else:
        print("  Search for " + str(target).rjust(2) + ": NOT FOUND in " + str(steps) + " steps")"""))

    cells.append(md("""**Expected Output:**
```
Sorted data: [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]

  Search for  9: FOUND at index 4 in 3 steps
  Search for  1: FOUND at index 0 in 3 steps
  Search for 19: FOUND at index 9 in 4 steps
  Search for  8: NOT FOUND in 4 steps
```"""))

    # --- Traced binary search ---
    cells.append(md("### Example 2: Step-by-Step Binary Search Trace"))

    cells.append(code("""def binary_search_traced(sorted_data, target):
    \"\"\"Binary search with ASCII art trace.\"\"\"
    low = 0
    high = len(sorted_data) - 1
    step = 0

    print("  Target: " + str(target))
    print("  Data:   " + str(sorted_data))
    print()

    while low <= high:
        step += 1
        mid = (low + high) // 2

        # Build visual
        markers = [" "] * len(sorted_data)
        for i in range(low, high + 1):
            markers[i] = "-"
        markers[mid] = "^"

        # Show active range
        active = str(sorted_data[low:high + 1])
        comparison = ""
        if sorted_data[mid] == target:
            comparison = str(sorted_data[mid]) + " == " + str(target) + " FOUND!"
        elif sorted_data[mid] < target:
            comparison = str(sorted_data[mid]) + " < " + str(target) + " -> go RIGHT"
        else:
            comparison = str(sorted_data[mid]) + " > " + str(target) + " -> go LEFT"

        print("  Step " + str(step) + ": low=" + str(low) + " high=" + str(high) + " mid=" + str(mid))
        print("         mid value = " + str(sorted_data[mid]) + " | " + comparison)
        print()

        if sorted_data[mid] == target:
            return mid, step
        elif sorted_data[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    print("  Not found after " + str(step) + " steps")
    return -1, step

data = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
print("=== Binary Search Trace ===")
print()
binary_search_traced(data, 23)"""))

    cells.append(md("""**Expected Output:**
```
=== Binary Search Trace ===

  Target: 23
  Data:   [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]

  Step 1: low=0 high=9 mid=4
         mid value = 16 | 16 < 23 -> go RIGHT

  Step 2: low=5 high=9 mid=7
         mid value = 56 | 56 > 23 -> go LEFT

  Step 3: low=5 high=6 mid=5
         mid value = 23 | 23 == 23 FOUND!
```"""))

    # --- Part 3: Head-to-head comparison ---
    cells.append(md("""---
## Part 3: Linear vs Binary -- Head-to-Head at Scale

Now let us see the real difference with large data."""))

    cells.append(code("""import math

print("=== Operation Count Comparison ===")
print()
print("  " + "n".rjust(12) + " | " + "Linear (worst)".rjust(15) + " | " + "Binary (worst)".rjust(15) + " | " + "Ratio".rjust(10))
print("  " + "-" * 12 + "-|-" + "-" * 15 + "-|-" + "-" * 15 + "-|-" + "-" * 10)

for n in [10, 100, 1_000, 10_000, 100_000, 1_000_000, 100_000_000]:
    linear = n
    binary = math.ceil(math.log2(n)) if n > 0 else 0
    ratio = linear / binary if binary > 0 else 0
    print("  " + "{:>12,}".format(n) + " | " + "{:>15,}".format(linear) + " | " + "{:>15,}".format(binary) + " | " + "{:>8,.0f}x".format(ratio))"""))

    cells.append(md("""**Expected Output:**
```
=== Operation Count Comparison ===

             n |  Linear (worst) |  Binary (worst) |      Ratio
  -------------|-----------------|-----------------|----------
            10 |              10 |               4 |        2x
           100 |             100 |               7 |       14x
         1,000 |           1,000 |              10 |      100x
        10,000 |          10,000 |              14 |      714x
       100,000 |         100,000 |              17 |    5,882x
     1,000,000 |       1,000,000 |              20 |   50,000x
   100,000,000 |     100,000,000 |              27 |3,703,704x
```

At 100 million items, binary search needs only **27 comparisons**.
Linear search needs up to **100 million**. That is a 3.7 million times difference."""))

    # --- Part 4: Timing ---
    cells.append(md("""---
## Part 4: Timing Experiment"""))

    cells.append(code("""import timeit

def time_searches(n, n_runs=1000):
    \"\"\"Compare linear and binary search timing at size n.\"\"\"
    data = list(range(n))
    target = n - 1  # worst case for linear

    t_lin = timeit.timeit(lambda: linear_search(data, target), number=n_runs)
    t_bin = timeit.timeit(lambda: binary_search(data, target), number=n_runs)

    lin_us = t_lin / n_runs * 1e6
    bin_us = t_bin / n_runs * 1e6
    return lin_us, bin_us

print("=== Timing: Linear vs Binary Search ===")
print()
print("  " + "n".rjust(10) + " | " + "Linear (us)".rjust(12) + " | " + "Binary (us)".rjust(12) + " | " + "Speedup".rjust(10))
print("  " + "-" * 10 + "-|-" + "-" * 12 + "-|-" + "-" * 12 + "-|-" + "-" * 10)

for n in [100, 1_000, 10_000, 100_000]:
    runs = max(100, 10_000 // n * 100)
    lin_us, bin_us = time_searches(n, n_runs=runs)
    speedup = lin_us / bin_us if bin_us > 0 else 0
    print("  " + "{:>10,}".format(n) + " | " + "{:>10.1f}us".format(lin_us) + " | " + "{:>10.1f}us".format(bin_us) + " | " + "{:>8.0f}x".format(speedup))"""))

    # --- Part 5: bisect module ---
    cells.append(md("""---
## Part 5: Python's `bisect` Module -- Production Binary Search

In production code, use Python's built-in `bisect` module instead of writing
your own binary search. It is implemented in C and highly optimized."""))

    cells.append(code("""import bisect

sorted_data = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]

# bisect_left: find insertion point (leftmost position)
idx = bisect.bisect_left(sorted_data, 23)
print("bisect_left(23) = " + str(idx) + " -> value = " + str(sorted_data[idx]))

# Use for exact search:
def bisect_search(sorted_data, target):
    \"\"\"Binary search using bisect. O(log n).\"\"\"
    idx = bisect.bisect_left(sorted_data, target)
    if idx < len(sorted_data) and sorted_data[idx] == target:
        return idx
    return -1

print()
for target in [23, 8, 99]:
    idx = bisect_search(sorted_data, target)
    if idx >= 0:
        print("  Search " + str(target) + ": found at index " + str(idx))
    else:
        print("  Search " + str(target) + ": not found")

# Range query: find all values in [10, 50]
left = bisect.bisect_left(sorted_data, 10)
right = bisect.bisect_right(sorted_data, 50)
print()
print("Values in range [10, 50]: " + str(sorted_data[left:right]))"""))

    cells.append(md("""**Expected Output:**
```
bisect_left(23) = 5 -> value = 23

  Search 23: found at index 5
  Search 8: found at index 2
  Search 99: not found

Values in range [10, 50]: [12, 16, 23, 38]
```

### When to Use This

| Situation | Use |
|-----------|-----|
| Data is unsorted, search once | Linear search O(n) |
| Data is unsorted, search many times | Sort first O(n log n) + binary search O(log n) each |
| Data is sorted | Always binary search O(log n) |
| Need range queries on sorted data | `bisect_left` + `bisect_right` |
| Need to check membership in any order | Use a set O(1) |"""))

    # --- Common Mistakes ---
    cells.append(md("""---
## Common Mistakes

| Mistake | Why | Fix |
|---------|-----|-----|
| Binary search on unsorted data | Results are wrong! | Sort first, or use linear search |
| Off-by-one in low/high | Infinite loop or missed element | Use `low <= high` (not `<`) |
| Integer overflow in mid | `(low + high)` can overflow in other languages | In Python, integers are arbitrary precision -- not an issue |
| Forgetting to return -1 | Function returns None for not-found | Always have an explicit not-found return |"""))

    cells.append(md("---\n## Mini-Quiz"))

    cells.append(code("""# Q1: You have 1 billion sorted numbers. How many comparisons
# does binary search need at most?
import math
# Answer: math.ceil(math.log2(1_000_000_000)) = ___

# Q2: Your data is NOT sorted. Is it worth sorting it just
# to do one binary search? Why or why not?
# Answer:

# Q3: You need to search for many values in a large dataset.
# What data structure should you use instead of binary search?
# Answer:"""))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# CORE NOTEBOOK -- WEEK 4: Sorting Algorithms
# ============================================================

def make_core_w04():
    cells = []

    cells.append(md("""# DSA Week 4 -- Sorting Algorithms

**Course:** Data Structures & Algorithms
**Session:** 3 hours
**Prerequisites:** Weeks 1-3
**Focus:** Bubble sort, insertion sort, Python Timsort, comparisons

## Learning Objectives

1. Implement bubble sort and insertion sort from scratch
2. Trace sorting algorithms step-by-step
3. Understand why naive sorts are O(n^2) and smart sorts are O(n log n)
4. Use Python's `sorted()` and `.sort()` with custom keys
5. Benchmark naive vs built-in sort at different sizes
6. Know when each sorting approach is appropriate

## The Big Idea

Sorting is the most-studied problem in computer science. Why? Because once data
is sorted, almost everything else becomes easier: searching is O(log n), finding
duplicates is O(n), merging two datasets is O(n).

```
Sorting Algorithm Comparison:
  Bubble Sort:    O(n^2)     -- simple but slow
  Insertion Sort: O(n^2)     -- good for nearly-sorted data
  Python Timsort: O(n log n) -- always use this in practice
```"""))

    cells.append(setup_cell())

    # --- Part 1: Bubble Sort ---
    cells.append(md("""---
## Part 1: Bubble Sort -- The Slow Way (Understanding First)

Bubble sort repeatedly walks through the list, compares adjacent elements,
and swaps them if they are in the wrong order. Larger elements "bubble up"
to the end.

```
Bubble Sort: [64, 34, 25, 12]

Pass 1:
  [64, 34, 25, 12]  compare 64,34 -> swap -> [34, 64, 25, 12]
  [34, 64, 25, 12]  compare 64,25 -> swap -> [34, 25, 64, 12]
  [34, 25, 64, 12]  compare 64,12 -> swap -> [34, 25, 12, 64]
  End of pass 1: 64 is in its final position

Pass 2:
  [34, 25, 12, 64]  compare 34,25 -> swap -> [25, 34, 12, 64]
  [25, 34, 12, 64]  compare 34,12 -> swap -> [25, 12, 34, 64]
  End of pass 2: 34 is in its final position

Pass 3:
  [25, 12, 34, 64]  compare 25,12 -> swap -> [12, 25, 34, 64]
  End of pass 3: SORTED!
```"""))

    cells.append(code("""def bubble_sort_traced(arr):
    \"\"\"Bubble sort with step-by-step trace. O(n^2).\"\"\"
    arr = arr.copy()
    n = len(arr)
    comparisons = 0
    swaps = 0

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True
        print("  Pass " + str(i + 1) + ": " + str(arr))
        if not swapped:
            print("  No swaps -- already sorted, stopping early!")
            break

    print()
    print("  Comparisons: " + str(comparisons))
    print("  Swaps:       " + str(swaps))
    return arr

print("=== Bubble Sort Trace ===")
data = [64, 34, 25, 12, 22, 11]
print("  Original: " + str(data))
print()
result = bubble_sort_traced(data)
print("  Sorted:   " + str(result))"""))

    cells.append(md("""**Expected Output:**
```
=== Bubble Sort Trace ===
  Original: [64, 34, 25, 12, 22, 11]

  Pass 1: [34, 25, 12, 22, 11, 64]
  Pass 2: [25, 12, 22, 11, 34, 64]
  Pass 3: [12, 22, 11, 25, 34, 64]
  Pass 4: [12, 11, 22, 25, 34, 64]
  Pass 5: [11, 12, 22, 25, 34, 64]
  Pass 6: [11, 12, 22, 25, 34, 64]
  No swaps -- already sorted, stopping early!

  Comparisons: 20
  Swaps: 11
  Sorted: [11, 12, 22, 25, 34, 64]
```"""))

    # --- Part 2: Insertion Sort ---
    cells.append(md("""---
## Part 2: Insertion Sort -- Good for Nearly-Sorted Data

Insertion sort works like sorting playing cards: pick up each card and insert
it into the correct position in your hand.

```
Insertion Sort: [64, 34, 25, 12]

Step 1: key=34   hand=[64]          34 < 64, insert before -> [34, 64]
Step 2: key=25   hand=[34, 64]      25 < 34, insert at start -> [25, 34, 64]
Step 3: key=12   hand=[25, 34, 64]  12 < 25, insert at start -> [12, 25, 34, 64]

SORTED!
```

**Key insight:** If the data is NEARLY sorted, insertion sort is fast (O(n))
because each element only needs to move a short distance."""))

    cells.append(code("""def insertion_sort_traced(arr):
    \"\"\"Insertion sort with trace. O(n^2) worst, O(n) best.\"\"\"
    arr = arr.copy()
    comparisons = 0

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        shifts = 0
        while j >= 0 and arr[j] > key:
            comparisons += 1
            arr[j + 1] = arr[j]
            j -= 1
            shifts += 1
        comparisons += 1  # the failing comparison
        arr[j + 1] = key
        print("  Step " + str(i) + ": insert " + str(key) + " (shifted " + str(shifts) + " elements) -> " + str(arr))

    print()
    print("  Total comparisons: " + str(comparisons))
    return arr

print("=== Insertion Sort Trace ===")
data = [64, 34, 25, 12, 22, 11]
print("  Original: " + str(data))
print()
result = insertion_sort_traced(data)
print("  Sorted:   " + str(result))

# Now try nearly-sorted data
print()
print("=== Insertion Sort on Nearly-Sorted Data ===")
nearly_sorted = [1, 2, 4, 3, 5, 6, 8, 7]
print("  Original: " + str(nearly_sorted))
print()
result2 = insertion_sort_traced(nearly_sorted)
print("  Much fewer comparisons! Insertion sort is O(n) on nearly-sorted data.")"""))

    # --- Part 3: Python Timsort ---
    cells.append(md("""---
## Part 3: Python's Built-in Sort (Timsort) -- Always Use This

Python's `sorted()` and `list.sort()` use **Timsort**, a hybrid of merge sort
and insertion sort. It is O(n log n) in the worst case and O(n) on nearly-sorted data.

**Rule: In production code, ALWAYS use Python's built-in sort.** Write bubble/insertion
sort only to understand the concepts."""))

    cells.append(code("""# sorted() returns a new list (original unchanged)
data = [64, 34, 25, 12, 22, 11, 90]
new_sorted = sorted(data)
print("Original:    " + str(data))
print("sorted():    " + str(new_sorted))
print()

# .sort() modifies in place (returns None)
data_copy = data.copy()
data_copy.sort()
print("After .sort(): " + str(data_copy))
print()

# Sort with custom key
records = [
    {"name": "Alice", "score": 88},
    {"name": "Bob", "score": 95},
    {"name": "Carol", "score": 72},
    {"name": "Dave", "score": 91},
]

by_score = sorted(records, key=lambda r: r["score"], reverse=True)
print("Sorted by score (descending):")
for r in by_score:
    print("  " + r["name"].ljust(8) + str(r["score"]))
print()

# Sort by multiple criteria
data2 = [(3, "c"), (1, "b"), (2, "a"), (1, "a"), (3, "a")]
print("Sort by first element, then second:")
print("  " + str(sorted(data2)))"""))

    # --- Part 4: Benchmark comparison ---
    cells.append(md("""---
## Part 4: Benchmark -- Naive Sorts vs Timsort"""))

    cells.append(code("""import timeit
import random

def bubble_sort(arr):
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def insertion_sort(arr):
    arr = arr.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

# Benchmark at different sizes
print("=== Sorting Algorithm Benchmark ===")
print()
print("  " + "n".rjust(8) + " | " + "Bubble (ms)".rjust(12) + " | " + "Insertion (ms)".rjust(14) + " | " + "Timsort (ms)".rjust(12) + " | " + "Bubble/Tim".rjust(10))
print("  " + "-" * 8 + "-|-" + "-" * 12 + "-|-" + "-" * 14 + "-|-" + "-" * 12 + "-|-" + "-" * 10)

random.seed(42)
for n in [100, 500, 1000, 2000, 5000]:
    data = [random.randint(0, 10000) for _ in range(n)]

    runs = max(1, 50_000 // (n * n) * 10) if n <= 2000 else 1
    if n > 2000:
        runs_naive = 1
    else:
        runs_naive = max(1, runs)

    t_bub = timeit.timeit(lambda d=data: bubble_sort(d), number=runs_naive) / runs_naive * 1000
    t_ins = timeit.timeit(lambda d=data: insertion_sort(d), number=runs_naive) / runs_naive * 1000
    t_tim = timeit.timeit(lambda d=data: sorted(d), number=max(runs_naive, 10)) / max(runs_naive, 10) * 1000

    ratio = t_bub / t_tim if t_tim > 0 else 0
    print("  " + "{:>8,}".format(n) + " | " + "{:>10.2f}ms".format(t_bub) + " | " + "{:>12.2f}ms".format(t_ins) + " | " + "{:>10.3f}ms".format(t_tim) + " | " + "{:>8.0f}x".format(ratio))

print()
print("Timsort is DRAMATICALLY faster. The gap grows with n.")
print("At n=5000, bubble sort is ~1000x slower than Timsort.")"""))

    cells.append(md("""---
## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Writing your own sort in production | Use `sorted()` or `.sort()` -- Timsort is better |
| Forgetting `.sort()` returns None | `x = my_list.sort()` sets x to None! Use `x = sorted(my_list)` |
| Sorting without a key function | `sorted(records)` fails on dicts. Use `key=lambda r: r["field"]` |
| Modifying a list while sorting | Never change the list during a sort operation |"""))

    cells.append(md("---\n## Mini-Quiz"))
    cells.append(code("""# Q1: Which sort is best for nearly-sorted data? Why?
# Answer:

# Q2: You have 1 million records. How many comparisons does Timsort need?
# Hint: O(n log n) where n = 1,000,000
import math
# Answer: approximately n * log2(n) = ___

# Q3: You need to find the 5 largest values in 1 million items.
# Should you sort and take the last 5? Or is there a better way?
# Answer:"""))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# CORE NOTEBOOK -- WEEK 5: Hashing & Indexing
# ============================================================

def make_core_w05():
    cells = []

    cells.append(md("""# DSA Week 5 -- Hashing & Indexing

**Course:** Data Structures & Algorithms
**Session:** 3 hours
**Prerequisites:** Weeks 1-4
**Focus:** Hash tables, dict internals, building an Index module

## Learning Objectives

1. Explain how a hash table works (hash function, buckets, collisions)
2. Build a simple hash table from scratch
3. Understand why dict/set lookups are O(1) average
4. Know what causes worst-case O(n) for hash tables (collisions)
5. Build an Index class for fast lookups on any column
6. Benchmark hash-based index vs linear scan

## The Big Idea

A hash table is the most important data structure in practical programming.
Python's `dict` and `set` are both hash tables. They give you O(1) lookup
by converting keys into array indices using a **hash function**.

```
How a hash table works:

  key = "sensor_a"
          |
  hash("sensor_a") = 7429813574  (big number)
          |
  7429813574 % 8 = 6              (index into array of size 8)
          |
  table[6] = ("sensor_a", 25.3)   (store key-value pair)

Lookup: same process in reverse -- O(1)!
```"""))

    cells.append(setup_cell())

    # --- Part 1: Build a hash table ---
    cells.append(md("""---
## Part 1: Build a Hash Table from Scratch

Let us build a hash table to understand what Python's dict does internally.

```
Hash Table with 5 buckets:

  Bucket 0: [("eve", 81)]
  Bucket 1: [("bob", 92)]
  Bucket 2: [("alice", 88), ("frank", 67)]  <-- collision!
  Bucket 3: []                                <-- empty
  Bucket 4: [("carol", 75)]

Collision: when two keys hash to the same bucket.
Solution: store a list of (key, value) pairs in each bucket.
```"""))

    cells.append(code("""class SimpleHashTable:
    \"\"\"A hash table built from scratch for learning.\"\"\"

    def __init__(self, size=8):
        self.size = size
        self.buckets = [[] for _ in range(size)]
        self.n_items = 0

    def _hash(self, key):
        \"\"\"Convert key to bucket index.\"\"\"
        return hash(key) % self.size

    def put(self, key, value):
        \"\"\"Insert or update key-value pair. O(1) average.\"\"\"
        idx = self._hash(key)
        bucket = self.buckets[idx]
        # Check if key already exists
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # update
                return
        bucket.append((key, value))  # insert
        self.n_items += 1

    def get(self, key, default=None):
        \"\"\"Look up value by key. O(1) average.\"\"\"
        idx = self._hash(key)
        for k, v in self.buckets[idx]:
            if k == key:
                return v
        return default

    def __contains__(self, key):
        \"\"\"Support 'key in table'. O(1) average.\"\"\"
        idx = self._hash(key)
        for k, v in self.buckets[idx]:
            if k == key:
                return True
        return False

    def show(self):
        \"\"\"Visualize the hash table.\"\"\"
        print("  HashTable (" + str(self.n_items) + " items, " + str(self.size) + " buckets):")
        for i, bucket in enumerate(self.buckets):
            if bucket:
                items = ", ".join("(" + repr(k) + ": " + repr(v) + ")" for k, v in bucket)
                print("    Bucket " + str(i) + ": [" + items + "]")
            else:
                print("    Bucket " + str(i) + ": []")

# Demo
ht = SimpleHashTable(5)
for name, score in [("alice", 88), ("bob", 92), ("carol", 75), ("dave", 91), ("eve", 81), ("frank", 67)]:
    ht.put(name, score)
    print("  put(" + repr(name) + ", " + str(score) + ") -> bucket " + str(ht._hash(name)))

print()
ht.show()
print()
print("  get('alice') = " + str(ht.get("alice")))
print("  get('bob')   = " + str(ht.get("bob")))
print("  get('zara')  = " + str(ht.get("zara", "NOT FOUND")))
print("  'carol' in table: " + str("carol" in ht))"""))

    # --- Part 2: Collisions ---
    cells.append(md("""---
## Part 2: Understanding Collisions

When two keys hash to the same bucket, it is called a **collision**.
More collisions = slower lookups (worst case: O(n) if everything hashes
to the same bucket).

```
Good hash table (few collisions):
  Bucket 0: [(key1, val1)]
  Bucket 1: [(key2, val2)]
  Bucket 2: [(key3, val3)]
  Bucket 3: [(key4, val4)]
  -> Each lookup: O(1)

Bad hash table (many collisions):
  Bucket 0: [(key1, val1), (key2, val2), (key3, val3), (key4, val4)]
  Bucket 1: []
  Bucket 2: []
  Bucket 3: []
  -> Lookup in bucket 0: O(n) -- degenerates to a list!
```

Python's dict avoids this by:
1. Using a very good hash function
2. Automatically resizing when the table gets too full (load factor > 2/3)"""))

    cells.append(code("""# Demonstrate the effect of table size on collisions
import random
random.seed(42)

for table_size in [5, 10, 50, 100]:
    ht = SimpleHashTable(table_size)
    for i in range(50):
        ht.put("key_" + str(i), i)

    # Count collisions
    max_bucket = max(len(b) for b in ht.buckets)
    empty = sum(1 for b in ht.buckets if len(b) == 0)
    avg_bucket = ht.n_items / (table_size - empty) if (table_size - empty) > 0 else 0

    print("  Table size " + str(table_size).rjust(3) + ": max bucket = " + str(max_bucket) + ", empty buckets = " + str(empty) + ", avg non-empty = " + "{:.1f}".format(avg_bucket))

print()
print("  Larger table = fewer collisions = faster lookups")
print("  This is why Python dicts auto-resize!")"""))

    # --- Part 3: Index class ---
    cells.append(md("""---
## Part 3: Building a Fast Index for Your Pipeline

An Index lets you look up rows by any column value in O(1) instead of
scanning all rows O(n). This is exactly what databases do internally.

```
Data:
  Row 0: {city: "Cairo", score: 88}
  Row 1: {city: "Alex",  score: 92}
  Row 2: {city: "Cairo", score: 75}
  Row 3: {city: "Luxor", score: 95}

Index on "city":
  "Cairo" -> [0, 2]
  "Alex"  -> [1]
  "Luxor" -> [3]

Query: "Find all Cairo rows"
  Without index: scan all 4 rows -> O(n)
  With index:    index["Cairo"] = [0, 2] -> O(1)!
```"""))

    cells.append(code("""class Index:
    \"\"\"A hash-based index for fast lookups on a dataset.\"\"\"

    def __init__(self, data, key_column):
        \"\"\"Build index on key_column. O(n) one-time cost.\"\"\"
        self.key_column = key_column
        self.index = {}

        for i, row in enumerate(data):
            key = row.get(key_column)
            if key not in self.index:
                self.index[key] = []
            self.index[key].append(i)

        print("  Built index on '" + key_column + "': " + str(len(self.index)) + " unique keys from " + str(len(data)) + " rows")

    def lookup(self, key):
        \"\"\"Find all row indices matching key. O(1).\"\"\"
        return self.index.get(key, [])

    def count(self, key):
        \"\"\"Count rows matching key. O(1).\"\"\"
        return len(self.index.get(key, []))

    def unique_keys(self):
        \"\"\"Return all unique key values.\"\"\"
        return list(self.index.keys())

# Demo with sample data
data = [
    {"id": 1, "city": "Cairo", "score": 88},
    {"id": 2, "city": "Alex", "score": 92},
    {"id": 3, "city": "Cairo", "score": 75},
    {"id": 4, "city": "Luxor", "score": 95},
    {"id": 5, "city": "Cairo", "score": 60},
    {"id": 6, "city": "Alex", "score": 85},
]

city_idx = Index(data, "city")
print()
print("  Cairo rows: " + str(city_idx.lookup("Cairo")))
print("  Cairo count: " + str(city_idx.count("Cairo")))
print("  Unique cities: " + str(city_idx.unique_keys()))
print()

# Get actual rows
cairo_rows = [data[i] for i in city_idx.lookup("Cairo")]
print("  Cairo data:")
for row in cairo_rows:
    print("    " + str(row))"""))

    # --- Part 4: Benchmark ---
    cells.append(md("""---
## Part 4: Benchmark -- Linear Scan vs Hash Index"""))

    cells.append(code("""import timeit
import random

# Generate larger dataset
random.seed(42)
cities = ["Cairo", "Alex", "Luxor", "Giza", "Aswan"]
big_data = [{"city": random.choice(cities), "value": random.random()} for _ in range(100_000)]

# Build index (one-time cost)
idx = Index(big_data, "city")

# Slow: linear scan
def slow_lookup(data, city):
    return [i for i, r in enumerate(data) if r["city"] == city]

# Fast: index lookup
def fast_lookup(idx, city):
    return idx.lookup(city)

print()
# Verify correctness
r_slow = slow_lookup(big_data, "Cairo")
r_fast = fast_lookup(idx, "Cairo")
assert r_slow == r_fast, "Results must match!"
print("  Correctness verified: both return " + str(len(r_slow)) + " rows")
print()

# Benchmark
t_slow = timeit.timeit(lambda: slow_lookup(big_data, "Cairo"), number=100)
t_fast = timeit.timeit(lambda: fast_lookup(idx, "Cairo"), number=100)

print("  Linear scan:  " + "{:.4f}".format(t_slow) + "s (100 queries)")
print("  Index lookup: " + "{:.6f}".format(t_fast) + "s (100 queries)")
print("  Speedup:      " + "{:.0f}".format(t_slow / t_fast) + "x")
print()
print("  The index is built once O(n), then every lookup is O(1).")
print("  Worth it if you do more than ~1 lookup on the same data.")"""))

    cells.append(md("""---
## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using a list as a dict key | Lists are unhashable. Use a tuple instead |
| Assuming dict preserves insertion order in old Python | True since Python 3.7, but do not rely on it for sorting |
| Not handling missing keys | Use `dict.get(key, default)` instead of `dict[key]` |
| Building index for single-use lookup | Not worth it if you only search once. Linear scan is fine |"""))

    cells.append(md("---\n## Mini-Quiz"))
    cells.append(code("""# Q1: What makes a good hash function?
# Answer:

# Q2: What happens when every key hashes to the same bucket?
# Answer:

# Q3: When should you use an Index vs a simple dict vs a list?
# Answer:"""))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# CORE NOTEBOOK -- WEEK 6: Heap & Priority Queue
# ============================================================

def make_core_w06():
    cells = []

    cells.append(md("""# DSA Week 6 -- Heap & Priority Queue

**Course:** Data Structures & Algorithms
**Session:** 3 hours
**Prerequisites:** Weeks 1-5
**Focus:** heapq, top-k problems, priority scheduling

## Learning Objectives

1. Explain what a heap is and draw its tree structure
2. Use Python's `heapq` module for min-heap operations
3. Solve top-k problems efficiently with heaps
4. Build a priority queue for task scheduling
5. Benchmark heap-based top-k vs sorting

## The Big Idea

A heap is a binary tree where the parent is always smaller (min-heap) or larger
(max-heap) than its children. The key operations:

```
Min-Heap:
              1
            /   \\
           3     5
          / \\   /
         7   4 8

Properties:
  - Smallest element is always at the root -> O(1) to peek
  - Insert a new element -> O(log n)
  - Remove the smallest -> O(log n)
  - Build heap from list -> O(n)

Use cases:
  - Find top-k items without sorting everything
  - Priority queues (process highest-priority first)
  - Streaming data (maintain top-k as data arrives)
```"""))

    cells.append(setup_cell())

    # --- Part 1: heapq basics ---
    cells.append(md("""---
## Part 1: Python's `heapq` Module

Python implements a min-heap using a regular list. The `heapq` module
provides functions to maintain the heap property."""))

    cells.append(code("""import heapq

# Build a heap from a list
data = [42, 15, 8, 23, 4, 16, 50, 31]
print("Original list: " + str(data))

heapq.heapify(data)  # O(n) -- rearranges in-place
print("After heapify: " + str(data))
print("Smallest:      " + str(data[0]) + " (always at index 0)")
print()

# Visualize the heap as a tree
def print_heap_tree(heap):
    \"\"\"Print heap as ASCII tree.\"\"\"
    if not heap:
        print("  (empty)")
        return
    n = len(heap)
    levels = []
    level_start = 0
    while level_start < n:
        level_end = min(level_start * 2 + 1, n) if level_start > 0 else 1
        if level_start == 0:
            level_end = 1
        else:
            level_end = min(level_start + 2 ** (len(levels)), n)
        # simpler approach: compute level
        pass

    # Simple level-by-level print
    import math
    depth = int(math.log2(n)) + 1 if n > 0 else 0
    idx = 0
    for level in range(depth):
        count = min(2 ** level, n - idx)
        indent = " " * (2 ** (depth - level) - 1)
        spacing = " " * (2 ** (depth - level + 1) - 1)
        values = []
        for i in range(count):
            if idx + i < n:
                values.append(str(heap[idx + i]).center(3))
        print(indent + spacing.join(values))
        idx += count

print("Heap as tree:")
print_heap_tree(data)"""))

    cells.append(code("""# Core heap operations
import heapq

heap = []

# Push items
for val in [42, 15, 8, 23, 4]:
    heapq.heappush(heap, val)
    print("  push(" + str(val) + ") -> heap = " + str(heap) + " | min = " + str(heap[0]))

print()

# Pop items (always returns smallest)
print("Popping in order:")
while heap:
    val = heapq.heappop(heap)
    print("  pop -> " + str(val) + " | remaining = " + str(heap))"""))

    cells.append(md("""**Expected Output:**
```
  push(42) -> heap = [42] | min = 42
  push(15) -> heap = [15, 42] | min = 15
  push(8) -> heap = [8, 42, 15] | min = 8
  push(23) -> heap = [8, 23, 15, 42] | min = 8
  push(4) -> heap = [4, 23, 15, 42, 8] | min = 4

Popping in order:
  pop -> 4 | remaining = [8, 23, 15, 42]
  pop -> 8 | remaining = [15, 23, 42]
  pop -> 15 | remaining = [23, 42]
  pop -> 23 | remaining = [42]
  pop -> 42 | remaining = []
```

Notice: popping always gives elements in sorted order! This is why heaps
are used to implement priority queues."""))

    # --- Part 2: Top-K ---
    cells.append(md("""---
## Part 2: The Top-K Problem

**Problem:** Find the k largest (or smallest) values in a dataset.

**Slow way:** Sort everything, take last k. O(n log n).
**Fast way:** Use a heap. O(n log k). When k is small, this is much faster!

```
Why heap is better for top-k:

  n = 1,000,000 and k = 10:
    Sorting:  O(n log n) = O(1,000,000 * 20) = 20,000,000 operations
    Heap:     O(n log k) = O(1,000,000 * 3)  = 3,000,000 operations
    Speedup:  ~7x

  n = 1,000,000 and k = 1:
    Sorting:  20,000,000 operations
    Heap:     1,000,000 operations (just one pass!)
    Or even simpler: just use max() -- O(n)
```"""))

    cells.append(code("""import heapq
import random

random.seed(42)
readings = [round(random.gauss(50, 20), 2) for _ in range(100_000)]

# Method 1: Sort and slice (O(n log n))
top5_sort = sorted(readings, reverse=True)[:5]

# Method 2: heapq.nlargest (O(n log k))
top5_heap = heapq.nlargest(5, readings)

# Method 3: heapq.nsmallest
bot5_heap = heapq.nsmallest(5, readings)

print("Top 5 (sort):    " + str(top5_sort))
print("Top 5 (heap):    " + str(top5_heap))
print("Bottom 5 (heap): " + str(bot5_heap))
print()
print("Both methods give same result: " + str(top5_sort == top5_heap))"""))

    cells.append(code("""# Benchmark: sort vs heap for top-k
import timeit

def top_k_sort(data, k):
    return sorted(data, reverse=True)[:k]

def top_k_heap(data, k):
    return heapq.nlargest(k, data)

print("=== Top-K Benchmark (n=100,000) ===")
print()
for k in [1, 5, 10, 100, 1000]:
    t_sort = timeit.timeit(lambda: top_k_sort(readings, k), number=20) / 20 * 1000
    t_heap = timeit.timeit(lambda: top_k_heap(readings, k), number=20) / 20 * 1000
    ratio = t_sort / t_heap if t_heap > 0 else 0
    print("  k=" + str(k).rjust(5) + ": sort=" + "{:.2f}ms".format(t_sort).rjust(10) + "  heap=" + "{:.2f}ms".format(t_heap).rjust(10) + "  ratio=" + "{:.1f}x".format(ratio).rjust(7))

print()
print("Note: heap advantage is biggest when k is small relative to n.")
print("When k approaches n, sorting is faster (heapq has higher constant).")"""))

    # --- Part 3: Priority Queue ---
    cells.append(md("""---
## Part 3: Priority Queue -- Process Tasks by Importance

A priority queue processes elements by priority, not by arrival order.
Lower number = higher priority (like severity levels: 1=critical, 5=low).

```
Priority Queue:
  push(3, "update docs")      -> queue: [(3, "update docs")]
  push(1, "fix sensor error") -> queue: [(1, "fix sensor"), (3, "update docs")]
  push(2, "generate report")  -> queue: [(1, "fix sensor"), (3, "update docs"), (2, "generate")]

  pop() -> (1, "fix sensor error")   -- highest priority processed first!
  pop() -> (2, "generate report")
  pop() -> (3, "update docs")
```"""))

    cells.append(code("""import heapq

class PriorityQueue:
    \"\"\"Priority queue using a min-heap.\"\"\"

    def __init__(self):
        self.heap = []
        self.counter = 0  # tiebreaker for equal priorities

    def push(self, priority, item):
        \"\"\"Add item with priority (lower = higher priority).\"\"\"
        heapq.heappush(self.heap, (priority, self.counter, item))
        self.counter += 1

    def pop(self):
        \"\"\"Remove and return highest-priority item.\"\"\"
        priority, _, item = heapq.heappop(self.heap)
        return priority, item

    def peek(self):
        \"\"\"Look at next item without removing.\"\"\"
        if self.heap:
            return self.heap[0][0], self.heap[0][2]
        return None

    def __len__(self):
        return len(self.heap)

    def is_empty(self):
        return len(self.heap) == 0


# Demo: sensor alert processing
pq = PriorityQueue()

alerts = [
    (3, "Low battery on sensor D03"),
    (1, "CRITICAL: Motor A overheating!"),
    (2, "Warning: Vibration above threshold"),
    (1, "CRITICAL: Communication lost with sensor D01"),
    (4, "Info: Scheduled maintenance due"),
    (2, "Warning: Humidity spike in room 204"),
]

print("=== Sensor Alert Priority Queue ===")
print()
print("Enqueueing alerts:")
for priority, msg in alerts:
    pq.push(priority, msg)
    print("  [" + str(priority) + "] " + msg)

print()
print("Processing by priority:")
while not pq.is_empty():
    priority, msg = pq.pop()
    print("  Processing [" + str(priority) + "] " + msg)"""))

    cells.append(md("""**Expected Output:**
```
=== Sensor Alert Priority Queue ===

Enqueueing alerts:
  [3] Low battery on sensor D03
  [1] CRITICAL: Motor A overheating!
  [2] Warning: Vibration above threshold
  [1] CRITICAL: Communication lost with sensor D01
  [4] Info: Scheduled maintenance due
  [2] Warning: Humidity spike in room 204

Processing by priority:
  Processing [1] CRITICAL: Motor A overheating!
  Processing [1] CRITICAL: Communication lost with sensor D01
  Processing [2] Warning: Vibration above threshold
  Processing [2] Warning: Humidity spike in room 204
  Processing [3] Low battery on sensor D03
  Processing [4] Info: Scheduled maintenance due
```

Critical alerts are processed first, regardless of when they arrived."""))

    cells.append(md("""---
## When to Use Heaps

| Problem | Use Heap? | Why |
|---------|-----------|-----|
| Find top-k of n items (k << n) | YES | O(n log k) vs O(n log n) for sorting |
| Process tasks by priority | YES | Priority queue is THE use case |
| Maintain running top-k as data streams in | YES | Push + pop in O(log k) |
| Sort an entire list | NO | Just use `sorted()` -- Timsort is optimized |
| Find the single max or min | NO | Just use `max()` or `min()` -- O(n) |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Forgetting heapq is a MIN-heap | For max-heap, negate values: `heappush(h, -val)` |
| Pushing non-comparable items | Wrap in tuple: `(priority, counter, item)` |
| Using heap when set would work | Heap for ordering, set for membership |"""))

    cells.append(md("---\n## Mini-Quiz"))
    cells.append(code("""# Q1: You have 10 million sensor readings. Find the 10 highest.
# What is the Big-O using: (a) sorting? (b) heap?
# Answer:

# Q2: Build a max-heap in Python (heapq only supports min-heap).
# Hint: negate the values.
import heapq
max_heap = []
for val in [3, 1, 4, 1, 5, 9]:
    heapq.heappush(max_heap, -val)  # negate!
# Pop max:
# max_val = -heapq.heappop(max_heap)
# print(max_val)  # should be 9"""))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# CORE NOTEBOOK -- WEEK 7: Performance Sprint 1
# ============================================================

def make_core_w07():
    cells = []

    cells.append(md("""# DSA Week 7 -- Performance Sprint 1

**Course:** Data Structures & Algorithms
**Session:** 3 hours
**Focus:** Implement your optimized DSA feature

## Learning Objectives

1. Identify the performance bottleneck in your pipeline
2. Choose the right data structure to fix it
3. Implement an optimized version alongside the baseline
4. Write tests to prove correctness (optimized matches baseline)
5. Prepare for next week's benchmarking

## The Sprint Process

```
+-------------------+     +-------------------+     +-------------------+
|  1. IDENTIFY      | --> |  2. IMPLEMENT     | --> |  3. VERIFY        |
|  - Profile code   |     |  - Optimized ver  |     |  - Same results   |
|  - Find hotspot   |     |  - Keep baseline  |     |  - All tests pass |
|  - State Big-O    |     |  - Clean code     |     |  - Ready to bench |
+-------------------+     +-------------------+     +-------------------+
```"""))

    cells.append(setup_cell())

    cells.append(md("""---
## Part 1: Identify the Bottleneck

Before optimizing, you need to know WHAT is slow. Here is how to find bottlenecks:

### Method 1: Manual Timing
Wrap each pipeline stage with timing code:"""))

    cells.append(code("""import time

def timed(func):
    \"\"\"Decorator that prints execution time.\"\"\"
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print("  " + func.__name__ + ": " + "{:.4f}".format(elapsed) + "s")
        return result
    return wrapper

# Example pipeline stages
@timed
def load_data(n):
    \"\"\"Simulate loading n records.\"\"\"
    return [{"id": i, "value": i * 1.5, "category": "cat_" + str(i % 10)} for i in range(n)]

@timed
def clean_data(data):
    \"\"\"Remove invalid records.\"\"\"
    return [r for r in data if r["value"] >= 0]

@timed
def find_duplicates(data):
    \"\"\"Find duplicate values -- THIS IS THE BOTTLENECK.\"\"\"
    seen = []  # BAD: using list for membership check
    dupes = []
    for r in data:
        val = r["value"]
        if val in seen:  # O(n) scan each time!
            dupes.append(r)
        seen.append(val)
    return dupes

@timed
def analyze(data):
    \"\"\"Compute statistics.\"\"\"
    values = [r["value"] for r in data]
    return {"count": len(values), "mean": sum(values) / len(values) if values else 0}

# Run pipeline
print("=== Pipeline Profiling (n=10,000) ===")
print()
data = load_data(10_000)
clean = clean_data(data)
dupes = find_duplicates(clean)
stats = analyze(clean)
print()
print("Bottleneck identified: find_duplicates is O(n^2) due to 'val in seen' on a list!")"""))

    cells.append(md("""---
## Part 2: Implement the Optimization"""))

    cells.append(code("""@timed
def find_duplicates_optimized(data):
    \"\"\"Find duplicate values using a set. O(n).\"\"\"
    seen = set()  # FIXED: O(1) membership check
    dupes = []
    for r in data:
        val = r["value"]
        if val in seen:  # O(1) check!
            dupes.append(r)
        seen.add(val)
    return dupes

# Verify correctness
print("=== Correctness Check ===")
print()
dupes_baseline = find_duplicates(clean)
dupes_optimized = find_duplicates_optimized(clean)

assert len(dupes_baseline) == len(dupes_optimized), "Must find same number of duplicates!"
print()
print("Both find " + str(len(dupes_baseline)) + " duplicates -- CORRECT!")
print()

# Quick timing comparison
print("=== Quick Timing at n=50,000 ===")
print()
big_data = [{"id": i, "value": i * 1.5, "category": "cat_" + str(i % 10)} for i in range(50_000)]
print("Baseline:")
d1 = find_duplicates(big_data)
print("Optimized:")
d2 = find_duplicates_optimized(big_data)
print()
print("The optimized version should be dramatically faster.")"""))

    cells.append(md("""---
## Part 3: Write Tests"""))

    cells.append(code("""def test_find_duplicates():
    \"\"\"Test that optimized version matches baseline.\"\"\"
    # Test 1: No duplicates
    data = [{"id": i, "value": float(i)} for i in range(100)]
    assert len(find_duplicates_optimized(data)) == 0, "No duplicates expected"

    # Test 2: All duplicates
    data = [{"id": i, "value": 42.0} for i in range(100)]
    assert len(find_duplicates_optimized(data)) == 99, "99 duplicates expected"

    # Test 3: Mixed
    data = [{"id": i, "value": float(i % 10)} for i in range(100)]
    assert len(find_duplicates_optimized(data)) == 90, "90 duplicates expected"

    # Test 4: Empty
    assert len(find_duplicates_optimized([])) == 0, "Empty list"

    # Test 5: Single element
    assert len(find_duplicates_optimized([{"value": 1.0}])) == 0, "Single element"

    print("All tests passed!")

test_find_duplicates()"""))

    cells.append(md("""---
## Part 4: Your Turn -- Apply to Your Track

Now apply this same pattern to YOUR project:

1. **Identify** the slowest function in your pipeline
2. **State** its current Big-O and why it is slow
3. **Implement** an optimized version using the right data structure
4. **Verify** that the optimized version gives the same results
5. **Next week**: benchmark at 5 sizes and create comparison plots

### Data Structure Selection Guide

| Problem Pattern | Slow Approach | Fast Data Structure | Improvement |
|----------------|---------------|-------------------|-------------|
| "Is x in my collection?" | list scan O(n) | set/dict O(1) | n/1 |
| "Find all items matching key" | list scan O(n) | hash index O(1) | n/1 |
| "Find item in sorted data" | list scan O(n) | binary search O(log n) | n/log n |
| "Find top-k items" | sort all O(n log n) | heap O(n log k) | log n / log k |
| "Remove duplicates" | nested loops O(n^2) | set O(n) | n/1 |
| "Sort by custom criteria" | bubble sort O(n^2) | Timsort O(n log n) | n / log n |"""))

    cells.append(code("""# TODO: Replace this template with YOUR project's optimization
#
# Step 1: Describe your bottleneck
# BOTTLENECK: ___
# CURRENT BIG-O: O(___)
# REASON: ___
#
# Step 2: Choose your data structure
# CHOSEN DS: ___
# EXPECTED BIG-O: O(___)
#
# Step 3: Implement
# def baseline_version(data):
#     ...
#
# def optimized_version(data):
#     ...
#
# Step 4: Verify
# result_base = baseline_version(test_data)
# result_opt  = optimized_version(test_data)
# assert result_base == result_opt

print("Template ready -- fill in your project's optimization!")"""))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# CORE NOTEBOOK -- WEEK 8: Performance Sprint 2
# ============================================================

def make_core_w08():
    cells = []

    cells.append(md("""# DSA Week 8 -- Performance Sprint 2

**Course:** Data Structures & Algorithms
**Session:** 3 hours
**Focus:** Benchmark baseline vs optimized, create plots and report

## Learning Objectives

1. Run a full benchmark suite at 5+ input sizes
2. Create comparison plots (time + speedup)
3. Compute and interpret speedup factors
4. Generate benchmark_results.json and benchmark_plot.png
5. Confirm >= 1.5x speedup target

## Deliverables

By the end of this session you must have:
- `reports/benchmark/benchmark_results.json`
- `reports/benchmark/benchmark_plot.png`
- Speedup >= 1.5x at the largest input size"""))

    cells.append(setup_cell())

    cells.append(md("""---
## Part 1: The Complete Benchmark Template

This is the template you will adapt for your project."""))

    cells.append(code("""import timeit
import json
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def run_full_benchmark(baseline_func, optimized_func, data_gen,
                       sizes, n_runs=50, label="Benchmark"):
    \"\"\"Run a complete benchmark comparison.

    Returns results dict suitable for JSON export.
    \"\"\"
    results = {
        "description": label,
        "sizes": [],
        "baseline_ms": [],
        "optimized_ms": [],
        "speedup": [],
    }

    print("=== " + label + " ===")
    print()
    print("  " + "n".rjust(10) + " | " + "baseline".rjust(12) + " | " + "optimized".rjust(12) + " | " + "speedup".rjust(8))
    print("  " + "-" * 10 + "-|-" + "-" * 12 + "-|-" + "-" * 12 + "-|-" + "-" * 8)

    for n in sizes:
        data = data_gen(n)

        t_base = timeit.timeit(lambda d=data: baseline_func(d), number=n_runs)
        t_opt = timeit.timeit(lambda d=data: optimized_func(d), number=n_runs)

        base_ms = t_base / n_runs * 1000
        opt_ms = t_opt / n_runs * 1000
        speedup = base_ms / opt_ms if opt_ms > 0 else float("inf")

        results["sizes"].append(n)
        results["baseline_ms"].append(round(base_ms, 4))
        results["optimized_ms"].append(round(opt_ms, 4))
        results["speedup"].append(round(speedup, 1))

        print("  " + "{:>10,}".format(n) + " | " + "{:>10.3f}ms".format(base_ms) + " | " + "{:>10.3f}ms".format(opt_ms) + " | " + "{:>6.1f}x".format(speedup))

    print()
    max_speedup = max(results["speedup"])
    target_met = max_speedup >= 1.5
    print("  Max speedup: " + str(max_speedup) + "x")
    print("  Target (1.5x): " + ("MET" if target_met else "NOT MET -- keep optimizing!"))
    return results

def save_benchmark(results, json_path, plot_path):
    \"\"\"Save benchmark results as JSON and create comparison plot.\"\"\"
    # Save JSON
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    with open(json_path, "w") as f:
        json.dump(results, f, indent=2)
    print("  Saved: " + json_path)

    # Create plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    sizes = results["sizes"]

    ax1.plot(sizes, results["baseline_ms"], "o-", label="Baseline",
             linewidth=2, color="#F44336", markersize=6)
    ax1.plot(sizes, results["optimized_ms"], "s-", label="Optimized",
             linewidth=2, color="#4CAF50", markersize=6)
    ax1.set_title("Execution Time Comparison", fontsize=14)
    ax1.set_xlabel("Input Size (n)")
    ax1.set_ylabel("Time (ms)")
    ax1.legend(fontsize=12)
    ax1.grid(True, alpha=0.3)

    colors = ["#4CAF50" if s >= 1.5 else "#FF9800" for s in results["speedup"]]
    ax2.bar(range(len(sizes)), results["speedup"], color=colors)
    ax2.set_xticks(range(len(sizes)))
    ax2.set_xticklabels(["{:,}".format(n) for n in sizes], rotation=45)
    ax2.set_title("Speedup Factor", fontsize=14)
    ax2.set_xlabel("Input Size (n)")
    ax2.set_ylabel("Speedup (x)")
    ax2.axhline(y=1.5, color="red", linestyle="--", label="1.5x target", linewidth=2)
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)
    fig.savefig(plot_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  Saved: " + plot_path)"""))

    cells.append(md("""---
## Part 2: Run the Demo Benchmark"""))

    cells.append(code("""import random
random.seed(42)

# Baseline: find duplicates with list
def baseline_dedup(data):
    seen = []
    dupes = []
    for x in data:
        if x in seen:
            dupes.append(x)
        seen.append(x)
    return dupes

# Optimized: find duplicates with set
def optimized_dedup(data):
    seen = set()
    dupes = []
    for x in data:
        if x in seen:
            dupes.append(x)
        seen.add(x)
    return dupes

def gen_data(n):
    return [random.randint(0, n // 2) for _ in range(n)]

# Verify correctness first!
test_data = gen_data(1000)
d1 = baseline_dedup(test_data)
d2 = optimized_dedup(test_data)
assert d1 == d2, "Results must match!"
print("Correctness verified!")
print()

# Run benchmark
sizes = [1_000, 2_000, 5_000, 10_000, 20_000]
results = run_full_benchmark(baseline_dedup, optimized_dedup, gen_data,
                             sizes, n_runs=10, label="Dedup: list vs set")

# Save
save_benchmark(results,
               "reports/benchmark/benchmark_results.json",
               "reports/benchmark/benchmark_plot.png")"""))

    cells.append(md("""---
## Part 3: Generate the Complexity Report"""))

    cells.append(code("""# Add complexity analysis to the results
results["baseline_complexity"] = "O(n^2) -- list membership is O(n) per check"
results["optimized_complexity"] = "O(n) -- set membership is O(1) per check"
results["data_structure_used"] = "set (hash set)"
results["why_faster"] = "Replaced O(n) list scan with O(1) set lookup for each of n items"

# Re-save with complexity info
with open("reports/benchmark/benchmark_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("=== Complexity Report ===")
print()
print("Baseline:  " + results["baseline_complexity"])
print("Optimized: " + results["optimized_complexity"])
print("DS used:   " + results["data_structure_used"])
print("Why:       " + results["why_faster"])
print()
print("Max speedup at n=" + "{:,}".format(results["sizes"][-1]) + ": " + str(results["speedup"][-1]) + "x")"""))

    cells.append(md("""---
## Part 4: Your Turn

Replace the demo above with YOUR project's baseline vs optimized functions.
Run the benchmark, generate the artifacts, and verify >= 1.5x speedup.

**Checklist:**
- [ ] Correctness verified (baseline and optimized give same results)
- [ ] Benchmark runs at 5+ input sizes
- [ ] `reports/benchmark/benchmark_results.json` exists
- [ ] `reports/benchmark/benchmark_plot.png` exists
- [ ] Max speedup >= 1.5x
- [ ] Complexity analysis included"""))

    cells.append(code("""# TODO: Your project benchmark
# baseline_func = your_baseline
# optimized_func = your_optimized
# data_gen = your_data_generator
# sizes = [1000, 5000, 10000, 50000, 100000]

# results = run_full_benchmark(baseline_func, optimized_func, data_gen,
#                              sizes, n_runs=20, label="Your Project Benchmark")
# save_benchmark(results,
#                "reports/benchmark/benchmark_results.json",
#                "reports/benchmark/benchmark_plot.png")

print("Replace this with your project benchmark!")"""))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# CORE NOTEBOOK -- WEEK 9: Trees & BST
# ============================================================

def make_core_w09():
    cells = []

    cells.append(md("""# DSA Week 9 -- Trees & Binary Search Trees

**Course:** Data Structures & Algorithms
**Session:** 3 hours
**Prerequisites:** Weeks 1-8
**Focus:** Binary trees, BST, traversals

## Learning Objectives

1. Understand tree terminology (root, leaf, height, depth, parent, child)
2. Implement a binary search tree with insert, search, and traversals
3. Trace tree operations step-by-step
4. Understand BST performance: O(log n) average, O(n) worst
5. Know when BSTs are useful in practice

## The Big Idea

A tree organizes data hierarchically. A **Binary Search Tree** (BST) has
a special rule: for every node, all values in the LEFT subtree are smaller
and all values in the RIGHT subtree are larger. This enables O(log n) search.

```
BST with values [20, 10, 30, 5, 15, 25, 35]:

              20
            /    \\
          10      30
         /  \\    /  \\
        5   15  25   35

Search for 15:
  20 -> 15 < 20, go LEFT
  10 -> 15 > 10, go RIGHT
  15 -> FOUND! (3 steps instead of scanning all 7)
```"""))

    cells.append(setup_cell())

    cells.append(md("""---
## Part 1: Tree Terminology

```
              A          <- ROOT (depth 0)
            /   \\
           B     C       <- depth 1
          / \\     \\
         D   E     F     <- LEAVES (depth 2)

Terminology:
  - Root: the topmost node (A)
  - Leaf: a node with no children (D, E, F)
  - Parent: node above (B is parent of D and E)
  - Child: node below (D and E are children of B)
  - Height: longest path from root to leaf (2 in this tree)
  - Depth of node: distance from root (B has depth 1)
  - Subtree: a node and all its descendants
```"""))

    cells.append(md("""---
## Part 2: Implementing a BST"""))

    cells.append(code("""class TreeNode:
    \"\"\"A node in a binary tree.\"\"\"
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BST:
    \"\"\"Binary Search Tree.\"\"\"

    def __init__(self):
        self.root = None
        self.size = 0

    def insert(self, value):
        \"\"\"Insert value into BST. O(log n) average, O(n) worst.\"\"\"
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert(self.root, value)
        self.size += 1

    def _insert(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert(node.right, value)

    def search(self, value):
        \"\"\"Search for value. O(log n) average.\"\"\"
        return self._search(self.root, value, steps=0)

    def _search(self, node, value, steps):
        steps += 1
        if node is None:
            return False, steps
        if value == node.value:
            return True, steps
        elif value < node.value:
            return self._search(node.left, value, steps)
        else:
            return self._search(node.right, value, steps)

    def inorder(self):
        \"\"\"Return values in sorted order (left, root, right). O(n).\"\"\"
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.value)
            self._inorder(node.right, result)

    def preorder(self):
        \"\"\"Return values in pre-order (root, left, right). O(n).\"\"\"
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node, result):
        if node:
            result.append(node.value)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def height(self):
        \"\"\"Return tree height. O(n).\"\"\"
        return self._height(self.root)

    def _height(self, node):
        if node is None:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))

    def print_tree(self, node=None, prefix="", is_left=True, is_root=True):
        \"\"\"ASCII visualization of the tree.\"\"\"
        if is_root:
            node = self.root
        if node is None:
            return
        if node.right:
            new_prefix = prefix + ("    " if is_left else "    ")
            self.print_tree(node.right, new_prefix, False, False)
        connector = "" if is_root else ("  / " if is_left else "  \\\\ ")
        print(prefix + connector + "[" + str(node.value) + "]")
        if node.left:
            new_prefix = prefix + ("    " if not is_left else "    ")
            self.print_tree(node.left, new_prefix, True, False)

# Build a BST
bst = BST()
values = [50, 30, 70, 20, 40, 60, 80, 10, 35, 45]

print("Inserting: " + str(values))
for v in values:
    bst.insert(v)

print()
print("Tree structure:")
bst.print_tree()
print()
print("Inorder (sorted):  " + str(bst.inorder()))
print("Preorder:          " + str(bst.preorder()))
print("Height:            " + str(bst.height()))
print("Size:              " + str(bst.size))"""))

    cells.append(md("""---
## Part 3: BST Search -- Traced"""))

    cells.append(code("""# Search with trace
for target in [35, 60, 55]:
    found, steps = bst.search(target)
    status = "FOUND" if found else "NOT FOUND"
    print("  Search " + str(target) + ": " + status + " in " + str(steps) + " steps")

print()
import math
print("For " + str(bst.size) + " nodes, optimal BST height = " + str(math.ceil(math.log2(bst.size + 1)) - 1))
print("Our tree height = " + str(bst.height()))
print("Max search steps = height + 1 = " + str(bst.height() + 1))"""))

    cells.append(md("""---
## Part 4: The Degenerate Case

If you insert sorted data into a BST, it becomes a linked list (O(n) search):

```
Insert [1, 2, 3, 4, 5]:

  [1]
    \\
    [2]
      \\
      [3]
        \\
        [4]
          \\
          [5]

This is O(n) search -- no better than a list!
Solution: balanced trees (AVL, Red-Black) -- covered in advanced courses.
```"""))

    cells.append(code("""# Demonstrate the degenerate case
bad_bst = BST()
for v in range(1, 16):
    bad_bst.insert(v)

print("Sorted insertion creates degenerate BST:")
print("  Height: " + str(bad_bst.height()) + " (should be ~4 for 15 nodes)")
print("  Search for 15: " + str(bad_bst.search(15)[1]) + " steps (should be ~4)")
print()

good_bst = BST()
# Insert in balanced order: median first
import random
values = list(range(1, 16))
random.seed(42)
random.shuffle(values)
for v in values:
    good_bst.insert(v)

print("Random insertion creates better BST:")
print("  Height: " + str(good_bst.height()))
print("  Search for 15: " + str(good_bst.search(15)[1]) + " steps")"""))

    cells.append(md("""---
## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Inserting sorted data into BST | Shuffle first, or use balanced tree |
| Confusing BST with heap | BST: left < root < right. Heap: parent < children |
| Forgetting BST requires comparable values | All values must support `<` operator |

## When to Use Trees

| Use Case | Use Tree? | Alternative |
|----------|-----------|-------------|
| Maintain sorted data with fast insert | YES (BST) | sorted list + bisect |
| Range queries on sorted data | YES (BST) | bisect on sorted list |
| Just need fast lookup by key | NO | Use dict (hash table) -- O(1) |
| Priority ordering | NO | Use heap |"""))

    cells.append(md("---\n## Mini-Quiz"))
    cells.append(code("""# Q1: What traversal gives BST values in sorted order?
# Answer:

# Q2: What is the worst-case height of a BST with n nodes?
# Answer:

# Q3: You have 1 million sorted records. How many comparisons
# does BST search need? What about if the BST is degenerate?
# Answer:"""))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# CORE NOTEBOOK -- WEEK 10: Graphs: BFS & DFS
# ============================================================

def make_core_w10():
    cells = []

    cells.append(md("""# DSA Week 10 -- Graphs: BFS & DFS

**Course:** Data Structures & Algorithms
**Session:** 3 hours
**Prerequisites:** Weeks 1-9
**Focus:** Graph representation, BFS, DFS

## Learning Objectives

1. Represent a graph using adjacency lists
2. Implement BFS (Breadth-First Search) and DFS (Depth-First Search)
3. Trace both algorithms step-by-step
4. Understand when to use BFS vs DFS
5. Apply graphs to real-world problems in your track

## The Big Idea

A graph models connections between things. Nodes (vertices) are the things,
edges are the connections. Graphs are EVERYWHERE:

```
Examples:
  - Social network: people (nodes) connected by friendships (edges)
  - Road map: cities (nodes) connected by roads (edges)
  - Internet: computers (nodes) connected by cables (edges)
  - Pipeline: stages (nodes) connected by data flow (edges)
  - Sensor network: devices (nodes) connected by communication links

Graph:
    A --- B
    |     |
    C --- D --- E

Adjacency list representation:
    A: [B, C]
    B: [A, D]
    C: [A, D]
    D: [B, C, E]
    E: [D]
```"""))

    cells.append(setup_cell())

    cells.append(md("""---
## Part 1: Graph Representation"""))

    cells.append(code("""class Graph:
    \"\"\"Graph using adjacency list representation.\"\"\"

    def __init__(self, directed=False):
        self.adj = {}
        self.directed = directed

    def add_node(self, node):
        if node not in self.adj:
            self.adj[node] = []

    def add_edge(self, u, v, weight=None):
        \"\"\"Add edge between u and v.\"\"\"
        self.add_node(u)
        self.add_node(v)
        self.adj[u].append((v, weight) if weight is not None else v)
        if not self.directed:
            self.adj[v].append((u, weight) if weight is not None else u)

    def neighbors(self, node):
        \"\"\"Return neighbors of node.\"\"\"
        return self.adj.get(node, [])

    def nodes(self):
        return list(self.adj.keys())

    def show(self):
        \"\"\"Print adjacency list.\"\"\"
        print("  Graph (" + ("directed" if self.directed else "undirected") + "):")
        for node in sorted(self.adj.keys(), key=str):
            neighbors = self.adj[node]
            print("    " + str(node) + " -> " + str(neighbors))

# Build a graph
g = Graph()
edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E")]
for u, v in edges:
    g.add_edge(u, v)

g.show()"""))

    cells.append(md("""---
## Part 2: BFS (Breadth-First Search)

BFS explores the graph **level by level**, like ripples on water.
It finds the **shortest path** (fewest edges) from start to any node.

```
BFS from A:

  Level 0: A
  Level 1: B, C    (neighbors of A)
  Level 2: D       (neighbors of B, C not yet visited)
  Level 3: E       (neighbor of D not yet visited)

  Order: A -> B -> C -> D -> E
```"""))

    cells.append(code("""from collections import deque

def bfs_traced(graph, start):
    \"\"\"BFS with step-by-step trace. O(V + E).\"\"\"
    visited = set()
    queue = deque([start])
    visited.add(start)
    order = []
    level = {start: 0}

    print("  BFS from " + str(start) + ":")
    print()

    while queue:
        node = queue.popleft()
        order.append(node)
        lvl = level[node]
        neighbors = graph.neighbors(node)
        new_neighbors = [n for n in neighbors if n not in visited]

        print("    Visit " + str(node) + " (level " + str(lvl) + ") | queue=" + str(list(queue)) + " | new neighbors=" + str(new_neighbors))

        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                level[neighbor] = lvl + 1

    print()
    print("  BFS order: " + " -> ".join(str(n) for n in order))
    return order

bfs_traced(g, "A")"""))

    cells.append(md("""---
## Part 3: DFS (Depth-First Search)

DFS explores the graph by going as **deep as possible** before backtracking.
It uses a stack (or recursion).

```
DFS from A (exploring alphabetically):

  Visit A -> go to B (first neighbor)
    Visit B -> go to D (first unvisited neighbor)
      Visit D -> go to C (first unvisited neighbor)
        Visit C -> no unvisited neighbors, BACKTRACK
      Back at D -> go to E
        Visit E -> no unvisited neighbors, BACKTRACK

  Order: A -> B -> D -> C -> E
```"""))

    cells.append(code("""def dfs_traced(graph, start):
    \"\"\"DFS with step-by-step trace. O(V + E).\"\"\"
    visited = set()
    order = []

    def _dfs(node, depth):
        if node in visited:
            return
        visited.add(node)
        order.append(node)
        indent = "    " + "  " * depth
        neighbors = graph.neighbors(node)
        unvisited = [n for n in neighbors if n not in visited]
        print(indent + "Visit " + str(node) + " | unvisited neighbors: " + str(unvisited))

        for neighbor in neighbors:
            if neighbor not in visited:
                _dfs(neighbor, depth + 1)

        if not unvisited:
            print(indent + "(backtrack from " + str(node) + ")")

    print("  DFS from " + str(start) + ":")
    print()
    _dfs(start, 0)
    print()
    print("  DFS order: " + " -> ".join(str(n) for n in order))
    return order

dfs_traced(g, "A")"""))

    cells.append(md("""---
## Part 4: BFS vs DFS -- When to Use Which

| Feature | BFS | DFS |
|---------|-----|-----|
| Explores | Level by level | Deep first |
| Data structure | Queue (FIFO) | Stack (LIFO) / recursion |
| Shortest path (unweighted) | YES | NO |
| Memory | O(width of graph) | O(depth of graph) |
| Good for | Finding shortest path, level-order | Checking connectivity, topological sort |
| Finds all nodes? | YES | YES |
| Time complexity | O(V + E) | O(V + E) |"""))

    cells.append(code("""# Side-by-side comparison on a larger graph
g2 = Graph()
for u, v in [("1", "2"), ("1", "3"), ("2", "4"), ("2", "5"),
             ("3", "6"), ("3", "7"), ("4", "8"), ("5", "8"),
             ("6", "9"), ("7", "9")]:
    g2.add_edge(u, v)

print("=== Graph ===")
g2.show()
print()
print("=== BFS ===")
bfs_order = bfs_traced(g2, "1")
print()
print("=== DFS ===")
dfs_order = dfs_traced(g2, "1")
print()
print("BFS visits level-by-level (shortest paths).")
print("DFS goes deep before backtracking.")"""))

    cells.append(md("""---
## Part 5: Practical Application -- Finding Connected Components"""))

    cells.append(code("""def find_connected_components(graph):
    \"\"\"Find all connected components using BFS. O(V + E).\"\"\"
    visited = set()
    components = []

    for node in graph.nodes():
        if node not in visited:
            # BFS to find all nodes in this component
            component = []
            queue = deque([node])
            visited.add(node)
            while queue:
                current = queue.popleft()
                component.append(current)
                for neighbor in graph.neighbors(current):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            components.append(component)

    return components

# Graph with disconnected components
g3 = Graph()
g3.add_edge("A", "B")
g3.add_edge("B", "C")
g3.add_edge("D", "E")  # separate component
g3.add_node("F")        # isolated node

components = find_connected_components(g3)
print("Connected components:")
for i, comp in enumerate(components):
    print("  Component " + str(i + 1) + ": " + str(comp))"""))

    cells.append(md("---\n## Mini-Quiz"))
    cells.append(code("""# Q1: You need to find the shortest route between two cities.
# Use BFS or DFS? Why?
# Answer:

# Q2: You want to check if a network of sensors is fully connected.
# Use BFS or DFS? Does it matter?
# Answer:

# Q3: What is the time complexity of BFS and DFS?
# Answer:"""))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# CORE NOTEBOOK -- WEEK 11: Shortest Paths (Dijkstra)
# ============================================================

def make_core_w11():
    cells = []

    cells.append(md("""# DSA Week 11 -- Shortest Paths (Dijkstra)

**Course:** Data Structures & Algorithms
**Session:** 3 hours
**Prerequisites:** Weeks 1-10 (especially heaps and graphs)
**Focus:** Dijkstra's algorithm, weighted graphs

## Learning Objectives

1. Understand weighted graphs and why BFS is not enough
2. Implement Dijkstra's algorithm using a priority queue
3. Trace Dijkstra step-by-step
4. Reconstruct the shortest path
5. Know Dijkstra's limitations (no negative weights)

## The Big Idea

BFS finds the shortest path by **edge count**. But in real life, edges have
different costs (distance, time, latency). Dijkstra's algorithm finds the
shortest path by **total weight**.

```
Weighted graph:

    A --4-- B
    |       |
    1       1
    |       |
    C --2-- D --5-- E

BFS shortest path A->D: A->B->D (2 edges)
Dijkstra shortest A->D: A->C->D (cost 1+2=3, vs A->B->D cost 4+1=5)

Dijkstra gives the CHEAPEST path, not the one with fewest edges.
```"""))

    cells.append(setup_cell())

    cells.append(md("""---
## Part 1: Dijkstra's Algorithm

Dijkstra works by always processing the **closest unvisited node** first
(using a priority queue / min-heap).

```
Algorithm:
  1. Set distance to start = 0, all others = infinity
  2. Add start to priority queue
  3. While queue not empty:
     a. Pop node with smallest distance
     b. For each neighbor:
        - Calculate new_dist = current_dist + edge_weight
        - If new_dist < known distance, update it
        - Add neighbor to queue with new_dist
  4. Return distances and paths
```"""))

    cells.append(code("""import heapq

def dijkstra(graph, start, end=None):
    \"\"\"Dijkstra's shortest path algorithm. O((V+E) log V).

    graph: {node: [(neighbor, weight), ...]}
    Returns: (distances, previous) for path reconstruction
    \"\"\"
    distances = {start: 0}
    previous = {start: None}
    pq = [(0, start)]
    visited = set()

    while pq:
        dist, node = heapq.heappop(pq)

        if node in visited:
            continue
        visited.add(node)

        if node == end:
            break

        for neighbor, weight in graph.get(node, []):
            if neighbor not in visited:
                new_dist = dist + weight
                if new_dist < distances.get(neighbor, float("inf")):
                    distances[neighbor] = new_dist
                    previous[neighbor] = node
                    heapq.heappush(pq, (new_dist, neighbor))

    return distances, previous

def reconstruct_path(previous, start, end):
    \"\"\"Reconstruct path from Dijkstra's previous dict.\"\"\"
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous.get(current)
    path.reverse()
    if path[0] != start:
        return []  # no path exists
    return path"""))

    cells.append(md("""---
## Part 2: Traced Example"""))

    cells.append(code("""def dijkstra_traced(graph, start, end):
    \"\"\"Dijkstra with step-by-step trace.\"\"\"
    distances = {start: 0}
    previous = {start: None}
    pq = [(0, start)]
    visited = set()
    step = 0

    print("  Dijkstra from " + str(start) + " to " + str(end) + ":")
    print()

    while pq:
        dist, node = heapq.heappop(pq)

        if node in visited:
            continue

        step += 1
        visited.add(node)
        print("  Step " + str(step) + ": Process " + str(node) + " (distance=" + str(dist) + ")")

        if node == end:
            print("    Reached destination!")
            break

        for neighbor, weight in graph.get(node, []):
            if neighbor not in visited:
                new_dist = dist + weight
                old_dist = distances.get(neighbor, float("inf"))
                if new_dist < old_dist:
                    distances[neighbor] = new_dist
                    previous[neighbor] = node
                    heapq.heappush(pq, (new_dist, neighbor))
                    print("    -> " + str(neighbor) + ": " + str(dist) + " + " + str(weight) + " = " + str(new_dist) + (" (improved from " + str(old_dist) + ")" if old_dist < float("inf") else " (new)"))
                else:
                    print("    -> " + str(neighbor) + ": " + str(new_dist) + " >= " + str(old_dist) + " (no improvement)")

    path = reconstruct_path(previous, start, end)
    total = distances.get(end, float("inf"))
    print()
    print("  Shortest path: " + " -> ".join(str(n) for n in path))
    print("  Total distance: " + str(total))
    return total, path

# Example graph
graph = {
    "A": [("B", 4), ("C", 1)],
    "B": [("A", 4), ("D", 1), ("E", 7)],
    "C": [("A", 1), ("D", 2), ("F", 5)],
    "D": [("B", 1), ("C", 2), ("E", 3)],
    "E": [("B", 7), ("D", 3), ("F", 1)],
    "F": [("C", 5), ("E", 1)],
}

dijkstra_traced(graph, "A", "E")"""))

    cells.append(md("""---
## Part 3: Network Latency Example"""))

    cells.append(code("""# Real-world example: finding fastest network route
network = {
    "Server": [("Router1", 2), ("Router2", 5)],
    "Router1": [("Server", 2), ("Router3", 3), ("Switch1", 1)],
    "Router2": [("Server", 5), ("Router3", 1), ("Switch2", 2)],
    "Router3": [("Router1", 3), ("Router2", 1), ("Switch1", 4), ("Switch2", 1)],
    "Switch1": [("Router1", 1), ("Router3", 4), ("SensorA", 1)],
    "Switch2": [("Router2", 2), ("Router3", 1), ("SensorB", 1)],
    "SensorA": [("Switch1", 1)],
    "SensorB": [("Switch2", 1)],
}

print("=== Finding fastest route: Server -> SensorB ===")
print()
dijkstra_traced(network, "Server", "SensorB")

print()
print("=== All distances from Server ===")
dists, _ = dijkstra(network, "Server")
for node in sorted(dists.keys()):
    print("  Server -> " + node + ": " + str(dists[node]) + " ms")"""))

    cells.append(md("""---
## Part 4: Dijkstra's Limitations

**Dijkstra does NOT work with negative edge weights.** If you need negative
weights, use the Bellman-Ford algorithm (not covered in this course).

```
Why negative weights break Dijkstra:

    A --(-3)-- B
    |          |
    1          2
    |          |
    C ---1---- D

Dijkstra from A: visits C first (dist=1), marks it done.
But A->B->D->C has total cost -3+2+1=0, which is SHORTER!
Dijkstra misses this because it already marked C as visited.
```

## When to Use Dijkstra

| Situation | Algorithm |
|-----------|-----------|
| Unweighted graph, shortest path | BFS |
| Weighted graph, no negative weights | Dijkstra |
| Negative weights possible | Bellman-Ford |
| All pairs shortest paths | Floyd-Warshall |"""))

    cells.append(md("---\n## Mini-Quiz"))
    cells.append(code("""# Q1: What data structure does Dijkstra use internally?
# Answer:

# Q2: What is the time complexity of Dijkstra?
# Answer:

# Q3: Can Dijkstra find shortest paths in an unweighted graph?
# Answer: Yes/No and why:"""))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# CORE NOTEBOOK -- WEEK 12: Dynamic Programming
# ============================================================

def make_core_w12():
    cells = []

    cells.append(md("""# DSA Week 12 -- Dynamic Programming

**Course:** Data Structures & Algorithms
**Session:** 3 hours
**Prerequisites:** Weeks 1-11
**Focus:** Memoization, DP patterns, optimization

## Learning Objectives

1. Explain what dynamic programming is and when to use it
2. Implement memoization (top-down DP)
3. Implement tabulation (bottom-up DP)
4. Recognize the two requirements for DP: overlapping subproblems + optimal substructure
5. Apply DP to practical optimization problems

## The Big Idea

Dynamic Programming solves problems by breaking them into **overlapping subproblems**
and **remembering** (caching) the results so you never solve the same subproblem twice.

```
Fibonacci WITHOUT memoization -- O(2^n):

                    fib(5)
                  /        \\
             fib(4)        fib(3)
            /     \\        /    \\
        fib(3)  fib(2)  fib(2)  fib(1)
        /   \\    ...     ...
    fib(2) fib(1)

  fib(3) is computed 2 times!
  fib(2) is computed 3 times!
  Total calls: 15 (grows exponentially)

Fibonacci WITH memoization -- O(n):

  fib(5) -> fib(4) -> fib(3) -> fib(2) -> fib(1) -> fib(0)
                                 (cache)   (cache)   (cache)
  fib(3) = cached!  fib(2) = cached!
  Total calls: 6 (grows linearly)
```"""))

    cells.append(setup_cell())

    cells.append(md("""---
## Part 1: The Fibonacci Example -- Slow vs Fast"""))

    cells.append(code("""import time

# WITHOUT memoization -- O(2^n) EXPONENTIAL
call_count_slow = 0
def fib_slow(n):
    global call_count_slow
    call_count_slow += 1
    if n <= 1:
        return n
    return fib_slow(n - 1) + fib_slow(n - 2)

# WITH memoization -- O(n) LINEAR
call_count_memo = 0
def fib_memo(n, cache={}):
    global call_count_memo
    call_count_memo += 1
    if n in cache:
        return cache[n]
    if n <= 1:
        return n
    cache[n] = fib_memo(n - 1, cache) + fib_memo(n - 2, cache)
    return cache[n]

# Compare
print("=== Fibonacci: Naive vs Memoized ===")
print()

for target in [10, 20, 30]:
    call_count_slow = 0
    call_count_memo = 0

    start = time.time()
    result_slow = fib_slow(target)
    t_slow = time.time() - start

    fib_memo_cache = {}
    start = time.time()
    result_memo = fib_memo(target, fib_memo_cache)
    t_memo = time.time() - start

    print("  fib(" + str(target) + ") = " + str(result_slow))
    print("    Naive: " + str(call_count_slow) + " calls, " + "{:.4f}".format(t_slow) + "s")
    print("    Memo:  " + str(call_count_memo) + " calls, " + "{:.6f}".format(t_memo) + "s")
    if t_memo > 0:
        print("    Speedup: " + "{:.0f}".format(t_slow / t_memo) + "x")
    print()"""))

    cells.append(md("""**Expected Output:**
```
=== Fibonacci: Naive vs Memoized ===

  fib(10) = 55
    Naive: 177 calls, 0.0001s
    Memo:  19 calls, 0.000001s
    Speedup: 100x

  fib(20) = 6765
    Naive: 21891 calls, 0.0050s
    Memo:  39 calls, 0.000001s
    Speedup: 5000x

  fib(30) = 832040
    Naive: 2692537 calls, 0.5000s
    Memo:  59 calls, 0.000001s
    Speedup: 500000x
```

The naive version's call count **doubles** with every increase of 1.
The memoized version grows **linearly**."""))

    # --- Part 2: functools.lru_cache ---
    cells.append(md("""---
## Part 2: The Easy Way -- `@functools.lru_cache`

Python has built-in memoization. Just add the decorator:"""))

    cells.append(code("""from functools import lru_cache

@lru_cache(maxsize=None)
def fib_cached(n):
    \"\"\"Fibonacci with automatic memoization.\"\"\"
    if n <= 1:
        return n
    return fib_cached(n - 1) + fib_cached(n - 2)

# This can handle MUCH larger values
print("fib(50)  = " + str(fib_cached(50)))
print("fib(100) = " + str(fib_cached(100)))
print("fib(200) = " + str(fib_cached(200)))
print()
print("Cache info:", fib_cached.cache_info())"""))

    # --- Part 3: Bottom-up DP ---
    cells.append(md("""---
## Part 3: Bottom-Up DP (Tabulation)

Instead of top-down recursion with caching, you can build the solution
from the bottom up using a table:"""))

    cells.append(code("""def fib_table(n):
    \"\"\"Fibonacci using bottom-up DP. O(n) time, O(n) space.\"\"\"
    if n <= 1:
        return n
    table = [0] * (n + 1)
    table[0] = 0
    table[1] = 1
    for i in range(2, n + 1):
        table[i] = table[i - 1] + table[i - 2]
    return table[n]

def fib_optimized(n):
    \"\"\"Fibonacci with O(1) space -- only need last two values.\"\"\"
    if n <= 1:
        return n
    prev2, prev1 = 0, 1
    for i in range(2, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current
    return prev1

print("Bottom-up table:     fib(100) = " + str(fib_table(100)))
print("Space-optimized:     fib(100) = " + str(fib_optimized(100)))"""))

    # --- Part 4: Practical DP ---
    cells.append(md("""---
## Part 4: Practical DP -- Maximum Subarray Sum (Kadane's Algorithm)

This is a classic DP problem with real applications: find the contiguous
subarray with the largest sum.

```
Data: [-2, 1, -3, 4, -1, 2, 1, -5, 4]

Brute force: try all O(n^2) subarrays -- SLOW
DP (Kadane): scan once, keep running max -- O(n)

Trace:
  i=0: val=-2, current=max(-2, 0+(-2))=-2, best=-2
  i=1: val= 1, current=max(1, -2+1)=1,     best=1
  i=2: val=-3, current=max(-3, 1+(-3))=-2,  best=1
  i=3: val= 4, current=max(4, -2+4)=4,      best=4
  i=4: val=-1, current=max(-1, 4+(-1))=3,   best=4
  i=5: val= 2, current=max(2, 3+2)=5,       best=5
  i=6: val= 1, current=max(1, 5+1)=6,       best=6   <-- answer!
  i=7: val=-5, current=max(-5, 6+(-5))=1,   best=6
  i=8: val= 4, current=max(4, 1+4)=5,       best=6

Answer: 6 (subarray [4, -1, 2, 1])
```"""))

    cells.append(code("""def max_subarray_brute(arr):
    \"\"\"Brute force: try all subarrays. O(n^2).\"\"\"
    n = len(arr)
    best = float("-inf")
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += arr[j]
            best = max(best, current_sum)
    return best

def max_subarray_dp(arr):
    \"\"\"Kadane's algorithm (DP). O(n).\"\"\"
    best = current = arr[0]
    for x in arr[1:]:
        current = max(x, current + x)
        best = max(best, current)
    return best

# Test
data = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print("Data: " + str(data))
print("Brute force result: " + str(max_subarray_brute(data)))
print("DP result:          " + str(max_subarray_dp(data)))
print()

# Timing comparison
import timeit
import random
random.seed(42)
big_data = [random.randint(-10, 10) for _ in range(5000)]

t_brute = timeit.timeit(lambda: max_subarray_brute(big_data), number=5) / 5
t_dp = timeit.timeit(lambda: max_subarray_dp(big_data), number=5) / 5

print("Benchmark (n=5000):")
print("  Brute force: " + "{:.3f}".format(t_brute) + "s")
print("  DP (Kadane): " + "{:.6f}".format(t_dp) + "s")
print("  Speedup:     " + "{:.0f}".format(t_brute / t_dp) + "x")"""))

    cells.append(md("""---
## When to Use DP

DP works when your problem has:
1. **Overlapping subproblems** -- same smaller problem solved multiple times
2. **Optimal substructure** -- optimal solution contains optimal solutions to subproblems

| Problem | DP? | Why |
|---------|-----|-----|
| Fibonacci | YES | fib(n) depends on fib(n-1) + fib(n-2) repeatedly |
| Max subarray | YES | Current max depends on previous max |
| Shortest path (Dijkstra) | YES | Shortest to D goes through shortest to B or C |
| Sorting | NO | No overlapping subproblems |
| Finding max in list | NO | No subproblem structure |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Not recognizing overlapping subproblems | Draw the recursion tree -- do you see repeats? |
| Mutable default argument for cache | Use `@lru_cache` instead of `cache={}` |
| Stack overflow on deep recursion | Use bottom-up tabulation instead of recursion |
| Forgetting base cases | Always define what happens at n=0, n=1 |"""))

    cells.append(md("---\n## Mini-Quiz"))
    cells.append(code("""# Q1: What are the two requirements for a DP problem?
# Answer:

# Q2: What is the difference between top-down and bottom-up DP?
# Answer:

# Q3: You have a recursive function that is very slow.
# How do you check if memoization will help?
# Answer:"""))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# CORE NOTEBOOK -- WEEK 13: Final Integration
# ============================================================

def make_core_w13():
    cells = []

    cells.append(md("""# DSA Week 13 -- Final Integration

**Course:** Data Structures & Algorithms
**Session:** 3 hours
**Focus:** Wire all DSA optimizations into your product pipeline

## Learning Objectives

1. Integrate your optimized DSA module into the main pipeline
2. Implement a config switch between baseline and optimized modes
3. Run the complete pipeline end-to-end
4. Verify all tests still pass with the integrated optimization
5. Prepare for final demo and benchmark report

## Integration Checklist

```
+--------------------------------------------------+
|           FINAL INTEGRATION CHECKLIST             |
+--------------------------------------------------+
| [ ] Optimized module in src/<project>/dsa/        |
| [ ] Module imports cleanly into pipeline          |
| [ ] Config switch: baseline vs optimized          |
| [ ] All existing tests pass                       |
| [ ] New tests cover the optimized module          |
| [ ] Benchmark shows >= 1.5x at largest n          |
| [ ] benchmark_results.json generated              |
| [ ] benchmark_plot.png generated                  |
| [ ] Complexity note in report                     |
+--------------------------------------------------+
```"""))

    cells.append(setup_cell())

    cells.append(md("""---
## Part 1: Integration Architecture

Your pipeline should support switching between baseline and optimized modes:

```python
config = {
    "mode": "optimized",  # or "baseline"
    # ... other settings
}

if config["mode"] == "optimized":
    from project.dsa import optimized_lookup as lookup
else:
    from project.dsa import baseline_lookup as lookup
```"""))

    cells.append(code("""# Example integration pattern
class Pipeline:
    \"\"\"Example pipeline with configurable optimization.\"\"\"

    def __init__(self, config):
        self.config = config
        self.mode = config.get("mode", "baseline")
        print("Pipeline initialized in " + self.mode + " mode")

    def find_records(self, data, target_key, target_value):
        \"\"\"Find records matching criteria -- uses configured mode.\"\"\"
        if self.mode == "optimized":
            return self._find_records_optimized(data, target_key, target_value)
        else:
            return self._find_records_baseline(data, target_key, target_value)

    def _find_records_baseline(self, data, key, value):
        \"\"\"Baseline: linear scan. O(n).\"\"\"
        return [r for r in data if r.get(key) == value]

    def _find_records_optimized(self, data, key, value):
        \"\"\"Optimized: build index if not cached, then O(1) lookup.\"\"\"
        if not hasattr(self, '_indexes'):
            self._indexes = {}
        if key not in self._indexes:
            # Build index once
            idx = {}
            for i, r in enumerate(data):
                k = r.get(key)
                if k not in idx:
                    idx[k] = []
                idx[k].append(i)
            self._indexes[key] = idx
        # O(1) lookup
        indices = self._indexes[key].get(value, [])
        return [data[i] for i in indices]

# Demo
import random
random.seed(42)
data = [{"id": i, "category": "cat_" + str(i % 20), "value": random.random()} for i in range(50_000)]

# Test both modes give same result
config_base = {"mode": "baseline"}
config_opt = {"mode": "optimized"}

pipe_base = Pipeline(config_base)
pipe_opt = Pipeline(config_opt)

r1 = pipe_base.find_records(data, "category", "cat_5")
r2 = pipe_opt.find_records(data, "category", "cat_5")

print()
print("Baseline found: " + str(len(r1)) + " records")
print("Optimized found: " + str(len(r2)) + " records")
print("Results match: " + str(len(r1) == len(r2)))

# Timing
import timeit
t_base = timeit.timeit(lambda: pipe_base.find_records(data, "category", "cat_5"), number=100)
t_opt = timeit.timeit(lambda: pipe_opt.find_records(data, "category", "cat_5"), number=100)
print()
print("Baseline (100 queries): " + "{:.4f}".format(t_base) + "s")
print("Optimized (100 queries): " + "{:.4f}".format(t_opt) + "s")
print("Speedup: " + "{:.0f}".format(t_base / t_opt) + "x")"""))

    cells.append(md("""---
## Part 2: Generate Final Artifacts"""))

    cells.append(code("""import json
import os

# Generate final benchmark results
results = {
    "description": "Pipeline query optimization",
    "baseline_complexity": "O(n) per query -- linear scan",
    "optimized_complexity": "O(1) per query after O(n) index build",
    "data_structure": "Hash-based index (dict of lists)",
    "sizes": [1000, 5000, 10000, 50000],
    "baseline_ms": [],
    "optimized_ms": [],
    "speedup": [],
}

for n in results["sizes"]:
    test_data = [{"id": i, "category": "cat_" + str(i % 20)} for i in range(n)]
    pb = Pipeline({"mode": "baseline"})
    po = Pipeline({"mode": "optimized"})

    runs = 100
    t_b = timeit.timeit(lambda d=test_data: pb.find_records(d, "category", "cat_5"), number=runs) / runs * 1000
    t_o = timeit.timeit(lambda d=test_data: po.find_records(d, "category", "cat_5"), number=runs) / runs * 1000
    sp = t_b / t_o if t_o > 0 else 0

    results["baseline_ms"].append(round(t_b, 4))
    results["optimized_ms"].append(round(t_o, 4))
    results["speedup"].append(round(sp, 1))

os.makedirs("reports/benchmark", exist_ok=True)
with open("reports/benchmark/benchmark_results.json", "w") as f:
    json.dump(results, f, indent=2)
print("Saved: reports/benchmark/benchmark_results.json")

# Verify target
max_sp = max(results["speedup"])
print("Max speedup: " + str(max_sp) + "x (" + ("MEETS" if max_sp >= 1.5 else "DOES NOT MEET") + " 1.5x target)")"""))

    cells.append(md("""---
## Part 3: Your Integration TODO

Replace the demo code above with your actual project integration.
Make sure:
1. Your optimized module is in `src/<project>/dsa/`
2. Pipeline can switch between modes via config
3. All tests pass in both modes
4. Benchmark artifacts are generated"""))

    cells.append(code("""# TODO: Your integration code here
print("Replace with your project integration!")"""))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# CORE NOTEBOOK -- WEEK 14: Final Performance Report
# ============================================================

def make_core_w14():
    cells = []

    cells.append(md("""# DSA Week 14 -- Final Performance Report

**Course:** Data Structures & Algorithms
**Session:** 3 hours
**Focus:** Demo, benchmark report, final release

## Deliverables

1. Working pipeline with DSA optimization integrated
2. `reports/benchmark/benchmark_results.json` with timing data
3. `reports/benchmark/benchmark_plot.png` with comparison plots
4. Benchmark showing >= 1.5x speedup at largest input size
5. Live demo of baseline vs optimized mode
6. Written complexity analysis (baseline Big-O vs optimized Big-O)"""))

    cells.append(setup_cell())

    cells.append(md("""---
## Part 1: Final Release Check

Run this to verify all required artifacts exist:"""))

    cells.append(code("""import os
import json

def final_dsa_check():
    \"\"\"Comprehensive final release check.\"\"\"
    print("=" * 60)
    print("         DSA FINAL RELEASE CHECK")
    print("=" * 60)
    print()

    passed = 0
    failed = 0
    warnings = 0

    checks = [
        ("reports/benchmark/benchmark_results.json", "Benchmark results JSON"),
        ("reports/benchmark/benchmark_plot.png", "Benchmark comparison plot"),
    ]

    for filepath, desc in checks:
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            print("  [PASS] " + desc)
            print("         " + filepath + " (" + str(os.path.getsize(filepath)) + " bytes)")
            passed += 1
        else:
            print("  [FAIL] " + desc)
            print("         Missing: " + filepath)
            failed += 1

    # Check benchmark results content
    try:
        with open("reports/benchmark/benchmark_results.json") as f:
            bench = json.load(f)

        # Check speedup
        speedups = bench.get("speedup", [])
        if speedups:
            max_sp = max(speedups)
            if max_sp >= 1.5:
                print("  [PASS] Max speedup: " + str(max_sp) + "x (>= 1.5x target)")
                passed += 1
            else:
                print("  [FAIL] Max speedup: " + str(max_sp) + "x (< 1.5x target)")
                failed += 1
        else:
            print("  [FAIL] No speedup data in benchmark results")
            failed += 1

        # Check complexity analysis
        if "baseline_complexity" in bench and "optimized_complexity" in bench:
            print("  [PASS] Complexity analysis included")
            print("         Baseline:  " + bench["baseline_complexity"])
            print("         Optimized: " + bench["optimized_complexity"])
            passed += 1
        else:
            print("  [WARN] Complexity analysis missing from benchmark results")
            warnings += 1

    except FileNotFoundError:
        print("  [FAIL] Cannot read benchmark results")
        failed += 1
    except json.JSONDecodeError:
        print("  [FAIL] Benchmark results is not valid JSON")
        failed += 1

    # Check DSA module
    dsa_paths = ["src/project_template/dsa", "src/dsa"]
    dsa_found = False
    for p in dsa_paths:
        if os.path.exists(p):
            print("  [PASS] DSA module found at " + p)
            passed += 1
            dsa_found = True
            break
    if not dsa_found:
        print("  [WARN] DSA module not found (checked " + str(dsa_paths) + ")")
        warnings += 1

    # Check standard pipeline outputs
    for filepath, desc in [
        ("data/cleaned/cleaned.csv", "Cleaned data CSV"),
        ("reports/report.json", "Pipeline report JSON"),
    ]:
        if os.path.exists(filepath):
            print("  [PASS] " + desc)
            passed += 1
        else:
            print("  [WARN] " + desc + " not found (may not be required)")
            warnings += 1

    print()
    print("=" * 60)
    print("  PASSED: " + str(passed) + "  FAILED: " + str(failed) + "  WARNINGS: " + str(warnings))
    print("=" * 60)

    if failed == 0:
        print()
        print("  CONGRATULATIONS! Your DSA project is ready for release!")
        print("  You have successfully implemented and benchmarked a")
        print("  data structure optimization in your pipeline.")
    else:
        print()
        print("  Fix " + str(failed) + " failure(s) before submitting.")

    return failed == 0

final_dsa_check()"""))

    cells.append(md("""---
## Part 2: Demo Script

Use this as a template for your live demo:"""))

    cells.append(code("""print(\"\"\"
=== DSA FINAL DEMO SCRIPT ===

1. PROBLEM STATEMENT
   - What pipeline operation was slow?
   - What was the baseline Big-O?

2. SOLUTION
   - What data structure did you use?
   - What is the new Big-O?

3. LIVE DEMO
   - Run pipeline in baseline mode
   - Run pipeline in optimized mode
   - Show the speedup

4. EVIDENCE
   - Show benchmark_results.json
   - Show benchmark_plot.png
   - Explain why the speedup grows with input size

5. REFLECTION
   - What did you learn about performance?
   - What would you optimize next?
\"\"\")"""))

    cells.append(md("""---
## Part 3: Semester Summary

```
What you learned this semester:

Week  1: Big-O notation -- predicting performance
Week  2: Benchmarking -- measuring performance accurately
Week  3: Searching -- linear O(n) vs binary O(log n)
Week  4: Sorting -- O(n^2) vs O(n log n)
Week  5: Hashing -- O(1) lookups with hash tables and indexes
Week  6: Heaps -- priority queues and top-k problems
Week  7: Sprint 1 -- implementing your optimization
Week  8: Sprint 2 -- benchmarking and proving improvement
Week  9: Trees -- hierarchical data and BST search
Week 10: Graphs -- BFS and DFS traversals
Week 11: Shortest paths -- Dijkstra's algorithm
Week 12: Dynamic programming -- memoization for exponential speedups
Week 13: Integration -- wiring optimization into your pipeline
Week 14: Final report -- proving your work with evidence

Key data structures:  list, dict, set, deque, heap, BST, graph
Key algorithms:       binary search, Timsort, Dijkstra, BFS, DFS, Kadane
Key skill:            choosing the right data structure for each problem
```"""))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# STUDIO NOTEBOOK GENERATOR (all weeks, all tracks)
# ============================================================

def make_studio(week_num, track_key):
    """Generate a rich studio notebook for a specific week and track."""
    track = TRACK_DATA[track_key]
    studio = STUDIO_WEEKLY[week_num]
    product = track["product"]
    tname = track["name"]

    sample_literal = _sample_data_literal(track_key)

    cells = []

    cells.append(md("""# DSA Week """ + str(week_num) + """ Studio -- """ + product + """

**Track:** """ + tname + """
**Product:** """ + product + """
**Context:** """ + track["dataset_desc"] + """

---

## Today's Task

**""" + studio["task"] + """**

**Deliverable:** """ + studio["deliverable"] + """

## How Studio Works

1. **Must-Pass Core** -- Complete this first. Required.
2. **Standard Target** -- Expected level for full marks.
3. **Stretch Goal** -- For students who finish early.

> Work through each section in order. Ask for help if stuck > 10 minutes."""))

    cells.append(setup_cell())

    # Track data
    cells.append(md("""---
## Your Track Data

**""" + product + """** works with """ + track["dataset_desc"] + """.

Here is your sample dataset:"""))

    cells.append(code(sample_literal + """

print("Loaded " + str(len(sample_data)) + " rows")
print()
for i, row in enumerate(sample_data):
    print("  Row " + str(i) + ": " + str(row))"""))

    # --- Must-Pass Core ---
    cells.append(md("""---
## Must-Pass Core

You MUST complete this section before moving on.
This is the minimum required deliverable for today."""))

    if week_num == 1:
        cells.append(md("### Step 1: Annotate your pipeline functions with Big-O"))
        cells.append(code("""# Annotate each function with its Big-O complexity
# Example:
def load_data(filepath):
    \"\"\"Load data from file. O(n) where n = number of rows.\"\"\"
    pass  # TODO: your actual implementation

def clean_data(data, config):
    \"\"\"Clean data. O(___) because ___.\"\"\"
    pass  # TODO

def analyze(data):
    \"\"\"Analyze data. O(___) because ___.\"\"\"
    pass  # TODO

# For each function, explain WHY it has that Big-O
print("TODO: Annotate your pipeline functions with Big-O complexity")
print("List the operations inside each function and their individual costs.")"""))
        cells.append(md("### Step 2: Identify the bottleneck"))
        cells.append(code("""# Which function has the worst Big-O?
# Is it O(n^2)? O(n * m)? What causes it?
print("My bottleneck: ___")
print("Current Big-O: O(___)")
print("Cause: ___")
print("Potential fix: ___")"""))

    elif week_num == 2:
        cells.append(md("### Step 1: Time your pipeline stages"))
        cells.append(code("""import time
import timeit

# Time each stage of your pipeline
# Replace with your actual functions

def dummy_load(n):
    return [{"id": i, "value": float(i)} for i in range(n)]

def dummy_process(data):
    return [r for r in data if r["value"] > 0]

# Benchmark at increasing sizes
sizes = [100, 500, 1000, 5000, 10000]
print("=== Pipeline Timing for """ + product + """ ===")
print()
for n in sizes:
    data = dummy_load(n)
    t = timeit.timeit(lambda d=data: dummy_process(d), number=100)
    avg_ms = t / 100 * 1000
    print("  n=" + str(n).rjust(6) + ": " + "{:.3f}ms".format(avg_ms))"""))
        cells.append(md("### Step 2: Create a scaling plot"))
        cells.append(code("""import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

# TODO: Replace with your actual timing data
ns = [100, 500, 1000, 5000, 10000]
times_ms = [0.01, 0.05, 0.1, 0.5, 1.0]  # placeholder

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(ns, times_ms, "o-", linewidth=2)
ax.set_title(\"""" + product + """ Pipeline Scaling\", fontsize=14)
ax.set_xlabel("Input Size (n)")
ax.set_ylabel("Time (ms)")
ax.grid(True, alpha=0.3)

os.makedirs("reports/benchmark", exist_ok=True)
fig.savefig("reports/benchmark/scaling_" + \"""" + track_key + """\".png", dpi=100, bbox_inches="tight")
plt.close(fig)
print("Saved scaling plot")"""))

    elif week_num == 3:
        cells.append(md("### Step 1: Implement binary search on your data"))
        cells.append(code("""import bisect

# Sort your data by the primary value column
sorted_data = sorted(sample_data, key=lambda r: r[\"""" + track["value_col"] + """\"])
values = [r[\"""" + track["value_col"] + """\"] for r in sorted_data]

print("Sorted values: " + str(values))
print()

# Use bisect to find values in a range
threshold = """ + str(track["threshold"]) + """
idx = bisect.bisect_left(values, threshold)
print("Values >= " + str(threshold) + ":")
for row in sorted_data[idx:]:
    print("  " + str(row))"""))

    elif week_num == 4:
        cells.append(md("### Step 1: Sort your data by multiple criteria"))
        cells.append(code("""# Sort sample data by """ + track["value_col"] + """
sorted_by_value = sorted(sample_data, key=lambda r: r[\"""" + track["value_col"] + """\"])
print("Sorted by """ + track["value_col"] + """:")
for row in sorted_by_value:
    print("  " + str(row))

print()

# Sort descending
sorted_desc = sorted(sample_data, key=lambda r: r[\"""" + track["value_col"] + """\"], reverse=True)
print("Top 3 by """ + track["value_col"] + """:")
for row in sorted_desc[:3]:
    print("  " + str(row))"""))

    elif week_num == 5:
        first_key = list(track["sample_data"][0].keys())[1]  # second column as index key
        cells.append(md("### Step 1: Build a hash index on your data"))
        cells.append(code("""# Build an index on '""" + first_key + """'
index = {}
for i, row in enumerate(sample_data):
    key = row[\"""" + first_key + """\"]
    if key not in index:
        index[key] = []
    index[key].append(i)

print("Index on '""" + first_key + """':")
for key, indices in index.items():
    print("  " + str(key) + " -> rows " + str(indices))

# Fast lookup
target_key = list(index.keys())[0]
print()
print("Lookup '" + str(target_key) + "': " + str(index[target_key]))"""))

    elif week_num == 6:
        cells.append(md("### Step 1: Find top-k anomalies using heap"))
        cells.append(code("""import heapq

# Find top-3 highest """ + track["value_col"] + """ values
values_with_idx = [(row[\"""" + track["value_col"] + """\"], i) for i, row in enumerate(sample_data)]
top3 = heapq.nlargest(3, values_with_idx)

print("Top 3 """ + track["value_col"] + """ readings:")
for val, idx in top3:
    print("  Row " + str(idx) + ": " + str(sample_data[idx]) + " (""" + track["value_col"] + """=" + str(val) + ")")

print()
bot3 = heapq.nsmallest(3, values_with_idx)
print("Bottom 3 """ + track["value_col"] + """ readings:")
for val, idx in bot3:
    print("  Row " + str(idx) + ": " + str(sample_data[idx]))"""))

    elif week_num in (7, 8):
        cells.append(md("### Step 1: Implement baseline and optimized versions"))
        cells.append(code("""import timeit

# Baseline: """ + track["baseline_op"] + """
def baseline_operation(data):
    \"\"\"Baseline approach for """ + product + """.\"\"\"
    # TODO: implement your baseline
    results = []
    for row in data:
        if row[\"""" + track["value_col"] + """\"] > """ + str(track["threshold"]) + """:
            results.append(row)
    return results

# Optimized: """ + track["optimized_op"] + """
def optimized_operation(data):
    \"\"\"Optimized approach for """ + product + """.\"\"\"
    # TODO: implement your optimized version
    # Use appropriate data structure (set, dict, heap, bisect, etc.)
    results = []
    for row in data:
        if row[\"""" + track["value_col"] + """\"] > """ + str(track["threshold"]) + """:
            results.append(row)
    return results

# Verify both give same results
r1 = baseline_operation(sample_data)
r2 = optimized_operation(sample_data)
print("Baseline found: " + str(len(r1)) + " results")
print("Optimized found: " + str(len(r2)) + " results")
print("Match: " + str(len(r1) == len(r2)))"""))

    elif week_num == 9:
        cells.append(md("### Step 1: Use a tree/BST for range queries on your data"))
        cells.append(code("""# Build a sorted structure for range queries on """ + track["value_col"] + """
import bisect

values = sorted(row[\"""" + track["value_col"] + """\"] for row in sample_data)
print("Sorted """ + track["value_col"] + """ values: " + str(values))

# Range query: find all values between thresholds
low, high = """ + str(track["threshold"]) + """, """ + str(track["threshold"]) + """ * 2
left = bisect.bisect_left(values, low)
right = bisect.bisect_right(values, high)
print("Values in [" + str(low) + ", " + str(high) + "]: " + str(values[left:right]))"""))

    elif week_num == 10:
        cells.append(md("### Step 1: Model your domain as a graph\n\n" + track["graph_context"]))
        cells.append(code("""# Build a graph for """ + product + """
# """ + track["graph_context"] + """

from collections import deque

graph = {}

def add_edge(g, u, v):
    if u not in g:
        g[u] = []
    g[u].append(v)
    if v not in g:
        g[v] = []
    g[v].append(u)

# TODO: Add edges relevant to your track
# Example:
add_edge(graph, "main_system", "subsystem_A")
add_edge(graph, "main_system", "subsystem_B")
add_edge(graph, "subsystem_A", "component_1")
add_edge(graph, "subsystem_A", "component_2")
add_edge(graph, "subsystem_B", "component_3")

# BFS traversal
def bfs(g, start):
    visited = set()
    queue = deque([start])
    visited.add(start)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in g.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order

print("BFS from main_system: " + str(bfs(graph, "main_system")))"""))

    elif week_num == 11:
        cells.append(md("### Step 1: Apply Dijkstra to your domain"))
        cells.append(code("""import heapq

# Weighted graph for """ + product + """
weighted_graph = {
    "start": [("step_A", 2), ("step_B", 5)],
    "step_A": [("start", 2), ("step_C", 3)],
    "step_B": [("start", 5), ("step_C", 1)],
    "step_C": [("step_A", 3), ("step_B", 1), ("end", 2)],
    "end": [("step_C", 2)],
}

def dijkstra(graph, start):
    distances = {start: 0}
    pq = [(0, start)]
    visited = set()
    while pq:
        dist, node = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        for neighbor, weight in graph.get(node, []):
            new_dist = dist + weight
            if new_dist < distances.get(neighbor, float("inf")):
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))
    return distances

dists = dijkstra(weighted_graph, "start")
print("Shortest distances from start:")
for node in sorted(dists.keys()):
    print("  " + node + ": " + str(dists[node]))"""))

    elif week_num == 12:
        cells.append(md("### Step 1: Apply memoization to your pipeline\n\n" + track["dp_context"]))
        cells.append(code("""from functools import lru_cache
import time

# Example: expensive computation that benefits from memoization
@lru_cache(maxsize=None)
def expensive_computation(n):
    \"\"\"Simulate a computation for """ + product + """.\"\"\"
    if n <= 1:
        return n
    return expensive_computation(n - 1) + expensive_computation(n - 2)

start = time.time()
result = expensive_computation(100)
elapsed = time.time() - start
print("Result: " + str(result))
print("Time: " + "{:.6f}".format(elapsed) + "s")
print("Cache info: " + str(expensive_computation.cache_info()))"""))

    elif week_num == 13:
        cells.append(md("### Step 1: Integrate your DSA optimization"))
        cells.append(code("""# TODO: Wire your optimized module into """ + product + """
# 1. Import your optimized module
# 2. Add config switch for baseline vs optimized
# 3. Run end-to-end pipeline in both modes
# 4. Verify same results

print("Integration checklist for """ + product + """:")
print("  [ ] Optimized module in src/")
print("  [ ] Config switch works")
print("  [ ] Both modes give same results")
print("  [ ] Tests pass")"""))

    elif week_num == 14:
        cells.append(md("### Step 1: Final check and demo prep"))
        cells.append(code("""import os
import json

print("=== Final Check for """ + product + """ ===")
print()

checks = {
    "reports/benchmark/benchmark_results.json": False,
    "reports/benchmark/benchmark_plot.png": False,
}

for path in checks:
    if os.path.exists(path) and os.path.getsize(path) > 0:
        print("  [PASS] " + path)
        checks[path] = True
    else:
        print("  [FAIL] " + path)

passed = sum(checks.values())
total = len(checks)
print()
print("  " + str(passed) + "/" + str(total) + " checks passed")"""))

    else:
        cells.append(code("""print("Working on """ + product + """ -- Week """ + str(week_num) + """ Studio")
print("Task: """ + studio["task"] + """")"""))

    # --- Standard Target ---
    cells.append(md("""---
## Standard Target

Complete the must-pass core PLUS:"""))

    cells.append(code("""# Standard target: extend your must-pass work
# - Add error handling for edge cases
# - Include timing measurements
# - Print a clear summary of results

# TODO: Your standard target code here
print("Standard target: extend must-pass with timing + edge cases")"""))

    # --- Stretch ---
    cells.append(md("""---
## Stretch Goal

For students who finish early:"""))

    cells.append(code("""# Stretch: go beyond the standard target
# - Compare multiple approaches
# - Create visualization of results
# - Optimize for a specific edge case

# TODO: Your stretch code here
print("Stretch: additional optimization or visualization")"""))

    # --- Self-check ---
    cells.append(md("""---
## Self-Check

Before submitting, verify:"""))

    cells.append(code("""checklist = [
    "Must-pass core completed",
    "Code runs without errors",
    "Results are printed clearly",
    "Deliverable: """ + studio["deliverable"] + """",
]

print("=== Studio """ + str(week_num) + """ Self-Check ===")
for item in checklist:
    print("  [ ] " + item)"""))

    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


# ============================================================
# CHECK NOTEBOOK GENERATOR
# ============================================================

def make_check(week_num):
    """Generate a universal check notebook for the week."""
    cells = []

    cells.append(md("""# DSA Week """ + str(week_num) + """ -- Universal Check

This notebook validates your work for Week """ + str(week_num) + """.
Run all cells. Fix any FAIL results in your code.

**How to use:**
1. Run each cell in order
2. Look for [PASS] or [FAIL] results
3. If something fails, the error message tells you what to fix
4. Go back to your code, fix it, then re-run this notebook"""))

    cells.append(setup_cell())
    cells.append(md("---\n## Checks"))

    if week_num <= 6:
        cells.append(code("""import os
import json

print("=== DSA Week """ + str(week_num) + """ Universal Check ===")
print()

passed = 0
failed = 0

# Check 1: Basic structure
try:
    # Verify project structure exists
    for d in ["src", "data", "reports"]:
        if os.path.exists(d):
            print("[PASS] Directory '" + d + "/' exists")
            passed += 1
        else:
            print("[INFO] Directory '" + d + "/' not found (create if needed)")
except Exception as e:
    print("[FAIL] Structure check: " + str(e))
    failed += 1

# Check 2: Conceptual check
print()
print("=== Conceptual Verification ===")
print("Answer these in the next cell to verify understanding:")
print("  1. What Big-O concepts did you apply this week?")
print("  2. What data structure optimization did you use (or plan to use)?")
print("  3. Can you explain the speedup in plain English?")
print()

print("=== Results: " + str(passed) + " passed, " + str(failed) + " failed ===")
if failed == 0:
    print("Week """ + str(week_num) + """ basic checks passed!")"""))

    elif week_num <= 8:
        cells.append(code("""import os
import json

print("=== DSA Week """ + str(week_num) + """ Universal Check ===")
print()

passed = 0
failed = 0

# Check 1: DSA module exists
dsa_found = False
for path in ["src/project_template/dsa", "src/dsa"]:
    if os.path.exists(path):
        print("[PASS] DSA module found at " + path)
        passed += 1
        dsa_found = True
        break
if not dsa_found:
    print("[WARN] DSA module not yet created (expected by week 8)")

# Check 2: Benchmark artifacts
if """ + str(week_num) + """ >= 8:
    for f in ["reports/benchmark/benchmark_results.json", "reports/benchmark/benchmark_plot.png"]:
        if os.path.exists(f) and os.path.getsize(f) > 0:
            print("[PASS] " + f)
            passed += 1
        else:
            print("[FAIL] " + f + " missing or empty")
            failed += 1

    # Check speedup target
    try:
        with open("reports/benchmark/benchmark_results.json") as f:
            bench = json.load(f)
        speedups = bench.get("speedup", [])
        if speedups and max(speedups) >= 1.5:
            print("[PASS] Max speedup: " + str(max(speedups)) + "x (>= 1.5x)")
            passed += 1
        else:
            sp = max(speedups) if speedups else 0
            print("[FAIL] Max speedup: " + str(sp) + "x (need >= 1.5x)")
            failed += 1
    except Exception as e:
        print("[FAIL] Cannot verify speedup: " + str(e))
        failed += 1

print()
print("=== Results: " + str(passed) + " passed, " + str(failed) + " failed ===")"""))

    else:
        cells.append(code("""import os
import json

print("=== DSA Week """ + str(week_num) + """ Universal Check ===")
print()

passed = 0
failed = 0

# Full check for weeks 9-14
checks = [
    ("reports/benchmark/benchmark_results.json", "Benchmark results"),
    ("reports/benchmark/benchmark_plot.png", "Benchmark plot"),
]

for filepath, desc in checks:
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        print("[PASS] " + desc + " (" + filepath + ")")
        passed += 1
    else:
        print("[FAIL] " + desc + " missing")
        failed += 1

# Speedup check
try:
    with open("reports/benchmark/benchmark_results.json") as f:
        bench = json.load(f)
    speedups = bench.get("speedup", [])
    if speedups and max(speedups) >= 1.5:
        print("[PASS] Max speedup: " + str(max(speedups)) + "x")
        passed += 1
    else:
        sp = max(speedups) if speedups else 0
        print("[FAIL] Max speedup: " + str(sp) + "x (need >= 1.5x)")
        failed += 1
except Exception as e:
    print("[FAIL] Benchmark check: " + str(e))
    failed += 1

# DSA module
dsa_found = any(os.path.exists(p) for p in ["src/project_template/dsa", "src/dsa"])
if dsa_found:
    print("[PASS] DSA module exists")
    passed += 1
else:
    print("[WARN] DSA module not found")

# Standard outputs
for f, desc in [("data/cleaned/cleaned.csv", "Cleaned CSV"),
                ("reports/report.json", "Report JSON")]:
    if os.path.exists(f):
        print("[PASS] " + desc)
        passed += 1
    else:
        print("[INFO] " + desc + " not found")

print()
print("=== Results: " + str(passed) + " passed, " + str(failed) + " failed ===")
if failed == 0:
    print("Week """ + str(week_num) + """ checks PASSED!")
else:
    print("Fix " + str(failed) + " failure(s) before submitting.")"""))

    return cells


# ============================================================
# HOMEWORK NOTEBOOK GENERATOR
# ============================================================

def _hw_w01():
    return {
        "review": [
            """# R1: Define Big-O in your own words (2-3 sentences)
# Answer: """,
            """# R2: Match each Big-O with its name
# O(1)       -> ___
# O(log n)   -> ___
# O(n)       -> ___
# O(n log n) -> ___
# O(n^2)     -> ___
# Choose from: constant, logarithmic, linear, linearithmic, quadratic""",
            """# R3: What is the Big-O of each Python operation?
# dict[key]         -> O(___)
# x in list          -> O(___)
# x in set           -> O(___)
# list.append(x)     -> O(___)
# list.insert(0, x)  -> O(___)
# sorted(list)       -> O(___)""",
            """# R4: If an O(n^2) algorithm takes 1 second at n=1000,
# approximately how long will it take at n=10,000?
# Answer: ___ seconds (show your reasoning)""",
        ],
        "practice": [
            """# P1: Classify the Big-O of this function
def mystery(data):
    total = 0
    for x in data:
        total += x
    return total / len(data)
# Answer: O(___) because ___""",
            """# P2: Classify the Big-O of this function
def mystery2(data):
    result = []
    for i in range(len(data)):
        if data[i] not in result:
            result.append(data[i])
    return result
# Answer: O(___) because ___
# How would you fix it? Write the fast version below:
def mystery2_fast(data):
    pass  # TODO""",
            """# P3: Write TWO versions of a function that checks if any
# element appears more than once in a list.
# Version A: O(n^2) using nested loops
# Version B: O(n) using a set

def has_duplicate_slow(data):
    pass  # TODO: O(n^2)

def has_duplicate_fast(data):
    pass  # TODO: O(n)

# Test both
test = [1, 5, 3, 7, 2, 5, 8]
print("Slow:", has_duplicate_slow(test))
print("Fast:", has_duplicate_fast(test))""",
            """# P4: Time both versions from P3 at n=10000
import timeit
import random
random.seed(42)
data = [random.randint(0, 100_000) for _ in range(10_000)]

# TODO: time both and print results""",
            """# P5: What is the Big-O of this nested loop?
# Careful -- it is NOT O(n^2)!
def tricky(n):
    count = 0
    for i in range(n):
        for j in range(5):  # inner loop is CONSTANT
            count += 1
    return count

# Answer: O(___) because ___
print("tricky(100) =", tricky(100))
print("tricky(1000) =", tricky(1000))""",
        ],
        "challenge": [
            """# C1: Write a function that finds two numbers in a list
# that add up to a target sum. Return their indices.
# Write both O(n^2) and O(n) versions.

def two_sum_slow(nums, target):
    \"\"\"O(n^2) brute force.\"\"\"
    pass  # TODO

def two_sum_fast(nums, target):
    \"\"\"O(n) using a dict.\"\"\"
    pass  # TODO

# Test
print(two_sum_fast([2, 7, 11, 15], 9))  # should return (0, 1)""",
            """# C2: Analyze the Big-O of your OWN pipeline code from CP1/CP2.
# List at least 3 functions and their Big-O.
# Identify the bottleneck.

# Function 1: ___ -> O(___)
# Function 2: ___ -> O(___)
# Function 3: ___ -> O(___)
# Bottleneck:  ___ because ___""",
            """# C3: Write a function that removes duplicates from a list
# while preserving the original order. Make it O(n).

def remove_duplicates_ordered(data):
    pass  # TODO

# Test
print(remove_duplicates_ordered([3, 1, 4, 1, 5, 9, 2, 6, 5, 3]))
# Expected: [3, 1, 4, 5, 9, 2, 6]""",
        ],
        "mini": """# Mini-Project: Build a performance comparison tool
# that takes a list of (name, function) pairs and a data generator,
# runs each function at multiple sizes, and prints a formatted table.
#
# Example usage:
# compare([("loop sum", loop_sum), ("builtin sum", sum)],
#         lambda n: list(range(n)),
#         sizes=[1000, 5000, 10000])
#
# Should print:
#   n       | loop sum   | builtin sum | fastest
#   --------|------------|-------------|--------
#   1,000   | 0.05ms     | 0.01ms      | builtin sum
#   ...

def compare(functions, data_gen, sizes):
    pass  # TODO

# Test with sum implementations
compare(
    [("loop", lambda d: sum(x for x in d)),
     ("builtin", sum)],
    lambda n: list(range(n)),
    sizes=[1000, 5000, 10000]
)"""
    }


def _hw_generic(week_num, title):
    return {
        "review": [
            "# R1: What was the main concept this week?\n# Answer: ",
            "# R2: What is the Big-O of the main algorithm/operation?\n# Answer: O(___) because ___",
            "# R3: When is this approach better than the naive alternative?\n# Answer: ",
            "# R4: Draw/describe the data structure from memory\n# (Use comments to sketch it)\n# Answer: ",
        ],
        "practice": [
            "# P1: Implement the main concept from memory (no looking!)\n# " + title + "\n\n# TODO: implement",
            "# P2: Apply the concept to a different example\n# Use a dataset of at least 100 items\n\nimport random\nrandom.seed(42)\ndata = [random.randint(0, 1000) for _ in range(100)]\n\n# TODO: apply " + title.lower(),
            "# P3: Compare the naive approach vs the optimized approach\n# Time both at n=1000, 5000, 10000\n\nimport timeit\n\n# TODO: benchmark comparison",
            "# P4: Handle edge cases\n# What happens with empty data? Single element? All identical?\n\n# TODO: test edge cases",
            "# P5: Apply to your project track data\n# How does this week's concept help your specific product?\n\n# TODO: apply to your track",
        ],
        "challenge": [
            "# C1: Implement a variation or extension of this week's algorithm\n# TODO",
            "# C2: Optimize for a specific use case in your project\n# Include timing comparison\n# TODO",
            "# C3: Create a visualization of the algorithm in action\n# (Print step-by-step trace or create a plot)\n# TODO",
        ],
        "mini": "# Mini-Project: Build a complete module that uses " + title.lower() + """\n# Include:\n# - At least 2 functions\n# - Docstrings with Big-O analysis\n# - Unit tests\n# - Timing comparison showing improvement\n\n# TODO: implement mini-project""",
    }


def make_homework(week_num, title):
    """Generate a homework notebook."""

    hw_generators = {
        1: _hw_w01,
    }

    if week_num in hw_generators:
        hw = hw_generators[week_num]()
    else:
        hw = _hw_generic(week_num, title)

    cells = []

    cells.append(md("""# DSA Week """ + str(week_num) + """ Homework -- """ + title + """

**Due:** Before next week's session
**Estimated time:** 2-4 hours

## Instructions

- **Review (R1-R4):** Check your understanding. All required.
- **Practice (P1-P5):** Apply concepts to problems. All required.
- **Challenge (C1-C3):** Stretch exercises. Optional but recommended.
- **Mini-Project (M1):** Build something complete. Optional but highly recommended.

Difficulty: Easy / Medium / Hard / Challenge is marked for each exercise."""))

    cells.append(setup_cell())

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
    cells.append(code("""checklist = [
    "All Review exercises (R1-R4) answered",
    "All Practice exercises (P1-P5) completed",
    "Code runs without errors",
    "Output is clear and formatted",
    "Edge cases considered",
]

print("=== Homework """ + str(week_num) + """ Self-Check ===")
for item in checklist:
    print("  [ ] " + item)
print()
print("Mark each [x] when done!")"""))

    return cells


# ============================================================
# GENERATE ALL NOTEBOOKS
# ============================================================

print("Generating DSA notebooks...")

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

for week_num, title, focus in WEEKS:
    wk = "W" + str(week_num).zfill(2)

    # Core notebook
    cells = core_generators[week_num]()
    nb = notebook(cells, "DSA " + wk + " Core -- " + title)
    save_notebook(nb, os.path.join(BASE, wk + "_core.ipynb"))
    print("  " + wk + "_core.ipynb (" + str(len(cells)) + " cells)")

    # Studio notebooks (5 tracks)
    for track_key in TRACK_DATA:
        cells = make_studio(week_num, track_key)
        nb = notebook(cells, "DSA " + wk + " Studio -- " + TRACK_DATA[track_key]["name"])
        save_notebook(nb, os.path.join(BASE, wk + "_studio_" + track_key + ".ipynb"))
    print("  " + wk + "_studio_*.ipynb (5 tracks)")

    # Check notebook
    cells = make_check(week_num)
    nb = notebook(cells, "DSA " + wk + " Universal Check")
    save_notebook(nb, os.path.join(BASE, wk + "_check.ipynb"))
    print("  " + wk + "_check.ipynb")

    # Homework notebook
    cells = make_homework(week_num, title)
    nb = notebook(cells, "DSA " + wk + " Homework -- " + title)
    save_notebook(nb, os.path.join(BASE, wk + "_homework.ipynb"))
    print("  " + wk + "_homework.ipynb")

total = 14 * (1 + 5 + 1 + 1)
print()
print("DSA complete: " + str(total) + " notebooks generated!")
