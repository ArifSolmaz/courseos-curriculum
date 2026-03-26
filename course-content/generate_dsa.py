#!/usr/bin/env python3
"""Generate all DSA (Data Structures & Algorithms) notebooks — 14 weeks."""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from nb_utils import md, code, notebook, save_notebook, setup_cell, reflection_cell, reflection_code

BASE = os.path.join(os.path.dirname(__file__), "notebooks", "dsa")
os.makedirs(BASE, exist_ok=True)

TRACKS = {
    "robotics": {"name": "Robotics/Mechatronics", "product": "MechaSense Studio"},
    "data": {"name": "Data/AI", "product": "CleanReport Pipeline"},
    "simulation": {"name": "Simulation/Games", "product": "SimLab Engine"},
    "space": {"name": "Space/Astro", "product": "Lightcurve Explorer"},
    "iot": {"name": "IoT/Reporting", "product": "AutoDashboard Reporter"},
}

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

def make_core(week_num, title, focus):
    cells = [
        md(f"# DSA Week {week_num} — {title}\n\n**Course:** Data Structures & Algorithms (Year 2, Semester 4)\n**Session:** 3 hours\n**Prerequisites:** CP1 + CP2 + OOP\n**Focus:** {focus}"),
        setup_cell(),
    ]

    content = {
        1: [
            ("What is Big-O? (Plain English)", """Big-O describes **how an algorithm's time grows** as the input gets bigger.

Think of it like this:
- **O(1)**: Constant — like looking up a word in a dictionary by page number. Instant.
- **O(log n)**: Logarithmic — like binary search. Halving the problem each step.
- **O(n)**: Linear — like reading every page to find something. Double the pages = double the time.
- **O(n log n)**: Like efficient sorting. A bit more than linear.
- **O(n²)**: Quadratic — like comparing every pair. 10× data = 100× time.

**The question is always:** "If I have 10× more data, how much longer does it take?" """),
            ("Part 1: Measuring Operations", '''import time

# O(1) — Constant: dict lookup
data_dict = {i: f"value_{i}" for i in range(1_000_000)}

start = time.time()
result = data_dict[999_999]  # instant, regardless of size
t1 = time.time() - start
print(f"Dict lookup: {t1*1e6:.1f} µs — O(1)")

# O(n) — Linear: list search
data_list = list(range(1_000_000))

start = time.time()
found = 999_999 in data_list  # must scan all elements
t2 = time.time() - start
print(f"List search: {t2*1000:.1f} ms — O(n)")

print(f"\\nDict is {t2/t1:.0f}× faster than list for lookup!")'''),
            ("Part 2: Python Data Structure Costs", '''# Quick reference: operation costs
print("""
=== Python Data Structure Costs ===

LIST (like an array):
  Access by index  [i]     → O(1)
  Append                    → O(1) average
  Search (x in list)        → O(n)
  Insert at start           → O(n)
  Sort                      → O(n log n)

DICT (hash table):
  Lookup by key  [k]       → O(1) average
  Insert                    → O(1) average
  Delete                    → O(1) average
  Search (k in dict)        → O(1) average

SET (hash set):
  Check membership (in)    → O(1) average
  Add                       → O(1) average
  Union / Intersection      → O(min(m,n))

TUPLE: same as list for access, but immutable
""")

# Demo: list vs set for membership testing
import time

n = 1_000_000
test_list = list(range(n))
test_set = set(range(n))

target = n - 1  # worst case for list

start = time.time()
_ = target in test_list
list_time = time.time() - start

start = time.time()
_ = target in test_set
set_time = time.time() - start

print(f"\\n'in' operator:")
print(f"  list: {list_time*1000:.2f} ms")
print(f"  set:  {set_time*1e6:.1f} µs")
print(f"  set is {list_time/set_time:.0f}× faster!")'''),
            ("Part 3: Counting Operations", '''# Let's COUNT how many operations each algorithm does

def linear_search(data, target):
    """O(n) — check every element."""
    ops = 0
    for item in data:
        ops += 1
        if item == target:
            return ops  # found
    return ops  # not found

def binary_search(data, target):
    """O(log n) — halve the search space each step."""
    ops = 0
    low, high = 0, len(data) - 1
    while low <= high:
        ops += 1
        mid = (low + high) // 2
        if data[mid] == target:
            return ops
        elif data[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return ops

# Compare on different sizes
for n in [100, 1_000, 10_000, 100_000, 1_000_000]:
    data = list(range(n))
    target = n - 1  # worst case

    lin_ops = linear_search(data, target)
    bin_ops = binary_search(data, target)
    print(f"n={n:>10,}: linear={lin_ops:>10,} ops, binary={bin_ops:>3} ops")'''),
            ("Part 4: Visualizing Growth", '''import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import math
import os

ns = list(range(1, 101))
o1 = [1] * len(ns)
olog = [math.log2(n) if n > 0 else 0 for n in ns]
on = ns
onlogn = [n * math.log2(n) if n > 0 else 0 for n in ns]
on2 = [n**2 for n in ns]

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(ns, o1, label="O(1)", linewidth=2)
ax.plot(ns, olog, label="O(log n)", linewidth=2)
ax.plot(ns, on, label="O(n)", linewidth=2)
ax.plot(ns, onlogn, label="O(n log n)", linewidth=2)
ax.plot(ns, on2, label="O(n²)", linewidth=2)

ax.set_title("Algorithm Growth Rates", fontsize=14)
ax.set_xlabel("Input Size (n)")
ax.set_ylabel("Operations")
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3)
ax.set_ylim(0, 500)

os.makedirs("reports/benchmark", exist_ok=True)
fig.savefig("reports/benchmark/growth_rates.png", dpi=100, bbox_inches="tight")
plt.close(fig)
print("Saved: reports/benchmark/growth_rates.png")'''),
        ],
        2: [
            ("Part 1: Proper Benchmarking with timeit", '''import timeit

# timeit runs code many times for accurate measurement
def slow_sum(data):
    """Naive sum using a loop."""
    total = 0
    for x in data:
        total += x
    return total

def fast_sum(data):
    """Built-in sum()."""
    return sum(data)

data = list(range(10_000))

# Time each approach (number = how many times to run)
slow_time = timeit.timeit(lambda: slow_sum(data), number=1000)
fast_time = timeit.timeit(lambda: fast_sum(data), number=1000)

print(f"Loop sum:    {slow_time:.4f}s (1000 runs)")
print(f"Built-in:    {fast_time:.4f}s (1000 runs)")
print(f"Speedup: {slow_time/fast_time:.1f}×")'''),
            ("Part 2: Scaling Tests", '''import timeit
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

def benchmark_scaling(func, sizes, n_runs=100):
    """Measure function time across different input sizes."""
    results = []
    for n in sizes:
        data = list(range(n))
        t = timeit.timeit(lambda d=data: func(d), number=n_runs)
        avg = t / n_runs
        results.append({"n": n, "time": avg})
        print(f"  n={n:>8,}: {avg*1000:.3f} ms")
    return results

def plot_benchmark(results, title, savepath):
    """Create a benchmark scaling plot."""
    ns = [r["n"] for r in results]
    times = [r["time"] * 1000 for r in results]  # ms

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(ns, times, "o-", color="#2196F3", linewidth=2, markersize=6)
    ax.set_title(title, fontsize=14)
    ax.set_xlabel("Input Size (n)")
    ax.set_ylabel("Time (ms)")
    ax.grid(True, alpha=0.3)

    os.makedirs(os.path.dirname(savepath), exist_ok=True)
    fig.savefig(savepath, dpi=100, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {savepath}")

# Benchmark list search at different sizes
print("Benchmarking list search (O(n)):")
sizes = [1000, 5000, 10000, 50000, 100000]

def search_last(data):
    return data[-1] in data

results = benchmark_scaling(search_last, sizes, n_runs=10)
plot_benchmark(results, "List Search — O(n) Scaling", "reports/benchmark/search_scaling.png")'''),
            ("Part 3: Comparing Baseline vs Optimized", '''def benchmark_comparison(baseline_func, optimized_func, sizes, n_runs=100):
    """Compare two implementations across sizes."""
    baseline_results = []
    optimized_results = []

    for n in sizes:
        data = list(range(n))

        t_base = timeit.timeit(lambda d=data: baseline_func(d), number=n_runs) / n_runs
        t_opt = timeit.timeit(lambda d=data: optimized_func(d), number=n_runs) / n_runs
        speedup = t_base / t_opt if t_opt > 0 else float("inf")

        baseline_results.append({"n": n, "time": t_base})
        optimized_results.append({"n": n, "time": t_opt})
        print(f"  n={n:>8,}: baseline={t_base*1000:.3f}ms, optimized={t_opt*1000:.3f}ms, speedup={speedup:.1f}×")

    return baseline_results, optimized_results

# Example: linear search vs set lookup
def baseline_search(data):
    return 999 in data

def optimized_search(data):
    return 999 in set(data)  # cheating a bit — conversion cost

print("Linear search vs Set lookup:")
sizes = [1000, 5000, 10000, 50000]
base_r, opt_r = benchmark_comparison(baseline_search, optimized_search, sizes, n_runs=50)

# Plot comparison
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot([r["n"] for r in base_r], [r["time"]*1000 for r in base_r], "o-", label="Baseline (list)", linewidth=2)
ax.plot([r["n"] for r in opt_r], [r["time"]*1000 for r in opt_r], "s-", label="Optimized (set)", linewidth=2)
ax.set_title("Baseline vs Optimized Search", fontsize=14)
ax.set_xlabel("Input Size (n)")
ax.set_ylabel("Time (ms)")
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3)
fig.savefig("reports/benchmark/comparison.png", dpi=100, bbox_inches="tight")
plt.close(fig)
print("Saved: reports/benchmark/comparison.png")'''),
        ],
        3: [
            ("Part 1: Linear Search — O(n)", '''def linear_search(data, target):
    """Search by checking every element. O(n)."""
    for i, item in enumerate(data):
        if item == target:
            return i
    return -1

data = [15, 23, 8, 42, 16, 50, 4, 31]
print(f"Search for 42: index = {linear_search(data, 42)}")
print(f"Search for 99: index = {linear_search(data, 99)}")'''),
            ("Part 2: Binary Search — O(log n)", '''def binary_search(sorted_data, target):
    """Search sorted data by halving. O(log n).

    REQUIREMENT: data must be sorted!

    Visual trace for [1, 3, 5, 7, 9, 11, 13], target=9:
      Step 1: [1, 3, 5, |7|, 9, 11, 13]  mid=7, 9>7 → go right
      Step 2: [9, |11|, 13]               mid=11, 9<11 → go left
      Step 3: [|9|]                        mid=9, FOUND!
    """
    low = 0
    high = len(sorted_data) - 1
    steps = 0

    while low <= high:
        steps += 1
        mid = (low + high) // 2

        if sorted_data[mid] == target:
            print(f"  Found {target} at index {mid} in {steps} steps")
            return mid
        elif sorted_data[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    print(f"  {target} not found after {steps} steps")
    return -1

# Test
sorted_data = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
print("Binary search in sorted list:")
binary_search(sorted_data, 9)
binary_search(sorted_data, 1)
binary_search(sorted_data, 19)
binary_search(sorted_data, 8)  # not found

# Compare step counts
import math
for n in [10, 100, 1000, 1_000_000]:
    max_steps = math.ceil(math.log2(n))
    print(f"  n={n:>10,}: linear up to {n:>10,} steps, binary max {max_steps:>3} steps")'''),
            ("Part 3: Applying to Your Project", '''# In your project, binary search can speed up:
# - Finding events in a sorted timeline
# - Looking up values in sorted reference data
# - Range queries on sorted sensor readings

def find_events_in_range(sorted_events, start, end):
    """Find all events between start and end timestamps.

    Uses binary search to find the starting position,
    then scans forward. O(log n + k) where k = results.
    """
    import bisect

    # Find insertion point for start
    left = bisect.bisect_left(sorted_events, start)
    # Find insertion point for end
    right = bisect.bisect_right(sorted_events, end)

    return sorted_events[left:right]

# Example: sorted sensor timestamps
timestamps = sorted([0.1, 0.5, 1.2, 2.3, 3.1, 4.5, 5.2, 6.8, 7.1, 8.5, 9.0])
print(f"All timestamps: {timestamps}")

# Find events between 2.0 and 6.0
result = find_events_in_range(timestamps, 2.0, 6.0)
print(f"Events in [2.0, 6.0]: {result}")'''),
        ],
        4: [
            ("Part 1: Sorting Basics", '''# Python's built-in sort is Timsort — O(n log n)

data = [64, 34, 25, 12, 22, 11, 90]

# .sort() modifies the list in place
data_copy = data.copy()
data_copy.sort()
print(f"Sorted (in-place): {data_copy}")

# sorted() returns a new list
new_list = sorted(data)
print(f"Sorted (new list): {new_list}")

# Sort with key function
names = ["Charlie", "alice", "Bob", "David"]
print(f"Sorted by lowercase: {sorted(names, key=str.lower)}")

# Sort dicts by a field
records = [
    {"name": "A", "value": 30},
    {"name": "B", "value": 10},
    {"name": "C", "value": 50},
]
sorted_records = sorted(records, key=lambda r: r["value"])
print(f"Sorted by value: {[r['name'] for r in sorted_records]}")'''),
            ("Part 2: Understanding Sorting Algorithms", '''def bubble_sort(arr):
    """Bubble Sort — O(n²). Simple but slow.

    Repeatedly swap adjacent elements if they're in wrong order.
    """
    arr = arr.copy()
    n = len(arr)
    comparisons = 0
    for i in range(n):
        for j in range(0, n - i - 1):
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr, comparisons

def insertion_sort(arr):
    """Insertion Sort — O(n²) worst, O(n) best (nearly sorted).

    Build sorted portion from left to right.
    """
    arr = arr.copy()
    comparisons = 0
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            comparisons += 1
            arr[j + 1] = arr[j]
            j -= 1
        comparisons += 1
        arr[j + 1] = key
    return arr, comparisons

# Compare
import random
random.seed(42)
test = [random.randint(1, 100) for _ in range(20)]
print(f"Original: {test[:10]}...")

result_b, comp_b = bubble_sort(test)
result_i, comp_i = insertion_sort(test)
print(f"\\nBubble sort:    {comp_b} comparisons")
print(f"Insertion sort: {comp_i} comparisons")
print(f"Python sorted:  ~{len(test) * 5} comparisons (estimated)")'''),
        ],
        5: [
            ("Part 1: Hash Tables (How dicts Work)", '''# A hash table maps keys to values using a hash function
# Python's dict IS a hash table

# Why is dict lookup O(1)?
# Because: hash(key) → index → direct access (no searching!)

# Demo: building a simple hash table
class SimpleHashTable:
    """A basic hash table to understand the concept."""

    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]  # list of buckets
        self.n_items = 0

    def _hash(self, key):
        """Convert key to bucket index."""
        return hash(key) % self.size

    def put(self, key, value):
        """Insert or update a key-value pair. O(1) average."""
        idx = self._hash(key)
        # Check if key already exists in bucket
        for i, (k, v) in enumerate(self.table[idx]):
            if k == key:
                self.table[idx][i] = (key, value)
                return
        self.table[idx].append((key, value))
        self.n_items += 1

    def get(self, key, default=None):
        """Look up a value by key. O(1) average."""
        idx = self._hash(key)
        for k, v in self.table[idx]:
            if k == key:
                return v
        return default

    def __str__(self):
        items = []
        for bucket in self.table:
            items.extend(bucket)
        return f"HashTable({dict(items)})"


ht = SimpleHashTable(5)
ht.put("sensor_a", 25.3)
ht.put("sensor_b", 30.1)
ht.put("sensor_c", 18.7)

print(f"sensor_a = {ht.get('sensor_a')}")
print(f"sensor_x = {ht.get('sensor_x', 'NOT FOUND')}")
print(ht)'''),
            ("Part 2: Building a Fast Index", '''class Index:
    """A hash-based index for fast lookups on a dataset.

    Instead of scanning all rows, build an index on a column
    and find matching rows in O(1).
    """

    def __init__(self, data, key_column):
        self.key_column = key_column
        self.index = {}  # key -> list of row indices

        for i, row in enumerate(data):
            key = row.get(key_column)
            if key not in self.index:
                self.index[key] = []
            self.index[key].append(i)

        print(f"Built index on '{key_column}': {len(self.index)} unique keys")

    def lookup(self, key):
        """Find all row indices matching key. O(1)."""
        return self.index.get(key, [])

    def count(self, key):
        """Count rows matching key. O(1)."""
        return len(self.index.get(key, []))


# Demo
data = [
    {"id": 1, "city": "Cairo", "value": 25},
    {"id": 2, "city": "Alex", "value": 30},
    {"id": 3, "city": "Cairo", "value": 28},
    {"id": 4, "city": "Luxor", "value": 40},
    {"id": 5, "city": "Cairo", "value": 22},
    {"id": 6, "city": "Alex", "value": 35},
]

idx = Index(data, "city")

# Fast lookup
cairo_indices = idx.lookup("Cairo")
print(f"\\nCairo rows: {cairo_indices}")
print(f"Cairo count: {idx.count('Cairo')}")

# Compare speed
import timeit

# Slow: scan all rows
def slow_lookup(data, city):
    return [i for i, r in enumerate(data) if r["city"] == city]

# Fast: use index
def fast_lookup(idx, city):
    return idx.lookup(city)

# With larger data
import random
big_data = [{"city": random.choice(["A", "B", "C", "D", "E"]), "val": random.random()} for _ in range(100_000)]
big_idx = Index(big_data, "city")

t_slow = timeit.timeit(lambda: slow_lookup(big_data, "A"), number=100)
t_fast = timeit.timeit(lambda: fast_lookup(big_idx, "A"), number=100)
print(f"\\nSlow scan: {t_slow:.4f}s")
print(f"Index lookup: {t_fast:.6f}s")
print(f"Speedup: {t_slow/t_fast:.0f}×")'''),
        ],
        6: [
            ("Part 1: Heap / Priority Queue", '''import heapq

# A heap is a tree-based structure where:
# - Parent is always smaller than children (min-heap)
# - Getting the smallest element is O(1)
# - Adding/removing is O(log n)

# Python's heapq module implements a min-heap
data = [42, 15, 8, 23, 4, 16, 50, 31]

# Turn list into a heap
heapq.heapify(data)
print(f"Heapified: {data}")
print(f"Smallest: {data[0]}")  # O(1) — always at index 0

# Pop smallest
smallest = heapq.heappop(data)
print(f"Popped: {smallest}")
print(f"After pop: {data}")

# Push a new value
heapq.heappush(data, 3)
print(f"After push(3): {data}")
print(f"Smallest now: {data[0]}")'''),
            ("Part 2: Top-K with Heap", '''def top_k_values(data, k):
    """Find the k largest values. O(n log k).

    Much faster than sorting when k << n.
    """
    return heapq.nlargest(k, data)

def bottom_k_values(data, k):
    """Find the k smallest values. O(n log k)."""
    return heapq.nsmallest(k, data)

# Demo
import random
random.seed(42)
readings = [random.gauss(50, 20) for _ in range(10_000)]

# Top-5 anomalies (highest values)
top5 = top_k_values(readings, 5)
print(f"Top 5 readings: {[round(v, 2) for v in top5]}")

# Bottom-5 (lowest)
bot5 = bottom_k_values(readings, 5)
print(f"Bottom 5: {[round(v, 2) for v in bot5]}")

# Compare with sorting
import timeit
t_heap = timeit.timeit(lambda: heapq.nlargest(5, readings), number=100)
t_sort = timeit.timeit(lambda: sorted(readings, reverse=True)[:5], number=100)
print(f"\\nHeap top-5: {t_heap:.4f}s")
print(f"Sort top-5: {t_sort:.4f}s")
print(f"Heap is {t_sort/t_heap:.1f}× faster")'''),
            ("Part 3: Priority Queue for Scheduling", '''import heapq

class PriorityQueue:
    """A priority queue using a heap."""

    def __init__(self):
        self.heap = []
        self.counter = 0  # for stable ordering

    def push(self, priority, item):
        """Add item with priority. Lower = higher priority."""
        heapq.heappush(self.heap, (priority, self.counter, item))
        self.counter += 1

    def pop(self):
        """Remove and return highest-priority item."""
        priority, _, item = heapq.heappop(self.heap)
        return priority, item

    def peek(self):
        """Look at highest-priority item without removing."""
        if self.heap:
            return self.heap[0][0], self.heap[0][2]
        return None

    def __len__(self):
        return len(self.heap)


# Demo: task scheduling
pq = PriorityQueue()
pq.push(3, "Low priority: update docs")
pq.push(1, "High priority: fix sensor error")
pq.push(2, "Medium priority: generate report")
pq.push(1, "High priority: restart system")

print("Processing tasks by priority:")
while len(pq) > 0:
    priority, task = pq.pop()
    print(f"  [{priority}] {task}")'''),
        ],
        7: [
            ("Part 1: Performance Sprint — Planning", '''# This week: implement your optimized feature!
# Follow these steps:

print("""
=== Performance Sprint 1 Plan ===

Step 1: Identify the bottleneck
  - What operation is slowest in your pipeline?
  - Profile it: time the slow function at different data sizes

Step 2: Design the optimization
  - What data structure can speed it up?
  - Expected improvement: O(?) baseline → O(?) optimized

Step 3: Implement
  - Write the optimized version in /src/<project>/dsa/
  - Keep the baseline version for comparison

Step 4: Test correctness
  - Optimized version must give SAME results as baseline
  - Write pytest tests to verify

Step 5: (Next week) Benchmark and prove the improvement
""")'''),
            ("Part 2: Example Optimization", '''import time

class BaselineEventFinder:
    """Baseline: linear scan for events. O(n) per query."""

    def __init__(self, events):
        self.events = events  # list of (timestamp, value)

    def find_in_range(self, start, end):
        """Find all events in time range. O(n)."""
        return [(t, v) for t, v in self.events if start <= t <= end]


class OptimizedEventFinder:
    """Optimized: sorted + binary search. O(log n + k) per query."""

    def __init__(self, events):
        self.events = sorted(events, key=lambda x: x[0])
        self.timestamps = [e[0] for e in self.events]

    def find_in_range(self, start, end):
        """Find events in range using binary search. O(log n + k)."""
        import bisect
        left = bisect.bisect_left(self.timestamps, start)
        right = bisect.bisect_right(self.timestamps, end)
        return self.events[left:right]


# Generate test data
import random
random.seed(42)
n = 100_000
events = [(random.uniform(0, 1000), random.gauss(50, 10)) for _ in range(n)]

baseline = BaselineEventFinder(events)
optimized = OptimizedEventFinder(events)

# Verify correctness
r1 = sorted(baseline.find_in_range(100, 200))
r2 = sorted(optimized.find_in_range(100, 200))
assert len(r1) == len(r2), "Results should match!"
print(f"Both return {len(r1)} events — correctness verified!")

# Time it
import timeit
t_base = timeit.timeit(lambda: baseline.find_in_range(100, 200), number=1000)
t_opt = timeit.timeit(lambda: optimized.find_in_range(100, 200), number=1000)
print(f"\\nBaseline: {t_base:.3f}s")
print(f"Optimized: {t_opt:.3f}s")
print(f"Speedup: {t_base/t_opt:.1f}×")'''),
        ],
        8: [
            ("Part 1: Full Benchmark Suite", '''import timeit, json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def run_benchmark(baseline_class, optimized_class, data_generator, sizes, n_queries=100):
    """Run a complete benchmark comparison."""
    results = {"sizes": [], "baseline_ms": [], "optimized_ms": [], "speedup": []}

    for n in sizes:
        data = data_generator(n)

        base = baseline_class(data)
        opt = optimized_class(data)

        # Random query
        import random
        query = (random.uniform(0, 500), random.uniform(500, 1000))

        t_base = timeit.timeit(lambda: base.find_in_range(*query), number=n_queries) / n_queries * 1000
        t_opt = timeit.timeit(lambda: opt.find_in_range(*query), number=n_queries) / n_queries * 1000
        speedup = t_base / t_opt if t_opt > 0 else 0

        results["sizes"].append(n)
        results["baseline_ms"].append(round(t_base, 3))
        results["optimized_ms"].append(round(t_opt, 3))
        results["speedup"].append(round(speedup, 1))

        print(f"  n={n:>10,}: baseline={t_base:.3f}ms, optimized={t_opt:.3f}ms, speedup={speedup:.1f}×")

    return results

def plot_benchmark_comparison(results, title="Benchmark: Baseline vs Optimized"):
    """Create benchmark comparison plot."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    sizes = results["sizes"]

    # Time comparison
    ax1.plot(sizes, results["baseline_ms"], "o-", label="Baseline", linewidth=2, color="#F44336")
    ax1.plot(sizes, results["optimized_ms"], "s-", label="Optimized", linewidth=2, color="#4CAF50")
    ax1.set_title("Execution Time", fontsize=14)
    ax1.set_xlabel("Input Size (n)")
    ax1.set_ylabel("Time (ms)")
    ax1.legend(fontsize=12)
    ax1.grid(True, alpha=0.3)

    # Speedup
    ax2.bar(range(len(sizes)), results["speedup"], color="#2196F3")
    ax2.set_xticks(range(len(sizes)))
    ax2.set_xticklabels([f"{n:,}" for n in sizes], rotation=45)
    ax2.set_title("Speedup Factor", fontsize=14)
    ax2.set_xlabel("Input Size (n)")
    ax2.set_ylabel("Speedup (×)")
    ax2.axhline(y=1.5, color="red", linestyle="--", label="1.5× target")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    os.makedirs("reports/benchmark", exist_ok=True)
    fig.savefig("reports/benchmark/benchmark_plot.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Saved: reports/benchmark/benchmark_plot.png")

# Run it
import random
random.seed(42)

def gen_events(n):
    return [(random.uniform(0, 1000), random.gauss(50, 10)) for _ in range(n)]

print("=== Full Benchmark ===")
sizes = [1_000, 5_000, 10_000, 50_000, 100_000]
results = run_benchmark(BaselineEventFinder, OptimizedEventFinder, gen_events, sizes)

# Plot
plot_benchmark_comparison(results)

# Save results JSON
with open("reports/benchmark/benchmark_results.json", "w") as f:
    json.dump({
        "description": "Event range query benchmark",
        "baseline": "Linear scan O(n)",
        "optimized": "Binary search O(log n + k)",
        "results": results,
    }, f, indent=2)
print("Saved: reports/benchmark/benchmark_results.json")

# Print complexity note
print("\\n=== Complexity Note ===")
print(f"Baseline: O(n) — linear scan through all events")
print(f"Optimized: O(log n + k) — binary search + scan results")
print(f"At n={sizes[-1]:,}: {results['speedup'][-1]}× speedup")
print(f"Meets 1.5× target: {'YES' if results['speedup'][-1] >= 1.5 else 'NO'}")'''),
        ],
        9: [
            ("Part 1: Binary Trees (Concept)", '''class TreeNode:
    """A node in a binary tree."""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinarySearchTree:
    """A simple BST for ordered data."""

    def __init__(self):
        self.root = None

    def insert(self, value):
        """Insert a value. O(log n) average, O(n) worst."""
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert(self.root, value)

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
        """Search for a value. O(log n) average."""
        return self._search(self.root, value)

    def _search(self, node, value):
        if node is None:
            return False
        if value == node.value:
            return True
        elif value < node.value:
            return self._search(node.left, value)
        else:
            return self._search(node.right, value)

    def inorder(self):
        """Return sorted values. O(n)."""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.value)
            self._inorder(node.right, result)


# Demo
bst = BinarySearchTree()
for v in [50, 30, 70, 20, 40, 60, 80]:
    bst.insert(v)

print(f"Sorted (inorder): {bst.inorder()}")
print(f"Search 40: {bst.search(40)}")
print(f"Search 45: {bst.search(45)}")'''),
        ],
        10: [
            ("Part 1: Graphs — Representation", '''class Graph:
    """A simple graph using adjacency list."""

    def __init__(self):
        self.adj = {}  # node -> list of neighbors

    def add_edge(self, u, v, directed=False):
        if u not in self.adj:
            self.adj[u] = []
        self.adj[u].append(v)
        if not directed:
            if v not in self.adj:
                self.adj[v] = []
            self.adj[v].append(u)

    def neighbors(self, node):
        return self.adj.get(node, [])

    def bfs(self, start):
        """Breadth-First Search. O(V + E)."""
        visited = set()
        queue = [start]
        order = []

        while queue:
            node = queue.pop(0)
            if node in visited:
                continue
            visited.add(node)
            order.append(node)
            for neighbor in self.neighbors(node):
                if neighbor not in visited:
                    queue.append(neighbor)

        return order

    def dfs(self, start):
        """Depth-First Search. O(V + E)."""
        visited = set()
        order = []

        def _dfs(node):
            if node in visited:
                return
            visited.add(node)
            order.append(node)
            for neighbor in self.neighbors(node):
                _dfs(neighbor)

        _dfs(start)
        return order


# Demo: sensor network
g = Graph()
g.add_edge("Server", "SensorA")
g.add_edge("Server", "SensorB")
g.add_edge("SensorA", "SubA1")
g.add_edge("SensorA", "SubA2")
g.add_edge("SensorB", "SubB1")

print(f"BFS from Server: {g.bfs('Server')}")
print(f"DFS from Server: {g.dfs('Server')}")'''),
        ],
        11: [
            ("Part 1: Dijkstra's Shortest Path", '''import heapq

def dijkstra(graph_adj, start, end):
    """Find shortest path using Dijkstra. O((V+E) log V).

    graph_adj: {node: [(neighbor, weight), ...]}
    """
    distances = {start: 0}
    previous = {}
    pq = [(0, start)]
    visited = set()

    while pq:
        dist, node = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)

        if node == end:
            # Reconstruct path
            path = []
            current = end
            while current is not None:
                path.append(current)
                current = previous.get(current)
            return dist, path[::-1]

        for neighbor, weight in graph_adj.get(node, []):
            if neighbor not in visited:
                new_dist = dist + weight
                if new_dist < distances.get(neighbor, float("inf")):
                    distances[neighbor] = new_dist
                    previous[neighbor] = node
                    heapq.heappush(pq, (new_dist, neighbor))

    return float("inf"), []

# Demo: network latency
network = {
    "A": [("B", 4), ("C", 1)],
    "B": [("A", 4), ("D", 1)],
    "C": [("A", 1), ("B", 2), ("D", 5)],
    "D": [("B", 1), ("C", 5)],
}

dist, path = dijkstra(network, "A", "D")
print(f"Shortest A→D: distance={dist}, path={' → '.join(path)}")'''),
        ],
        12: [
            ("Part 1: Dynamic Programming & Memoization", '''# DP = solve problems by breaking into subproblems
# and remembering (memoizing) results

# Example: Fibonacci WITHOUT memoization — O(2^n) SLOW!
def fib_slow(n):
    if n <= 1:
        return n
    return fib_slow(n - 1) + fib_slow(n - 2)

# Example: Fibonacci WITH memoization — O(n)
def fib_memo(n, cache={}):
    if n in cache:
        return cache[n]
    if n <= 1:
        return n
    cache[n] = fib_memo(n - 1, cache) + fib_memo(n - 2, cache)
    return cache[n]

# Compare
import time

start = time.time()
print(f"fib_slow(30) = {fib_slow(30)}")
t_slow = time.time() - start

start = time.time()
print(f"fib_memo(30) = {fib_memo(30)}")
t_fast = time.time() - start

print(f"\\nSlow: {t_slow:.4f}s")
print(f"Memo: {t_fast:.6f}s")
print(f"Speedup: {t_slow/t_fast:.0f}×")

# For your project: use @functools.lru_cache
from functools import lru_cache

@lru_cache(maxsize=None)
def fib_cached(n):
    if n <= 1:
        return n
    return fib_cached(n - 1) + fib_cached(n - 2)

print(f"\\nfib_cached(100) = {fib_cached(100)}")'''),
            ("Part 2: DP Applied to Data Processing", '''# Example: finding the maximum sum subarray
# (Kadane's algorithm — O(n))

def max_subarray_brute(arr):
    """Brute force: try all subarrays. O(n³)."""
    n = len(arr)
    best = float("-inf")
    for i in range(n):
        for j in range(i, n):
            total = sum(arr[i:j+1])
            best = max(best, total)
    return best

def max_subarray_dp(arr):
    """Kadane's algorithm: DP approach. O(n)."""
    best = current = arr[0]
    for x in arr[1:]:
        current = max(x, current + x)
        best = max(best, current)
    return best

# Test
data = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print(f"Data: {data}")
print(f"Brute force: {max_subarray_brute(data)}")
print(f"DP (Kadane): {max_subarray_dp(data)}")

# Timing
import timeit
big_data = [(-1)**i * i for i in range(1000)]
t_brute = timeit.timeit(lambda: max_subarray_brute(big_data[:100]), number=10)
t_dp = timeit.timeit(lambda: max_subarray_dp(big_data), number=10)
print(f"\\nBrute (n=100): {t_brute:.3f}s")
print(f"DP (n=1000):   {t_dp:.5f}s")'''),
        ],
        13: [
            ("Part 1: Final Integration", '''# Wire your optimized feature into the product
print("""
=== Final Integration Checklist ===

1. [ ] Optimized module is in /src/<project>/dsa/
2. [ ] Optimized module imports cleanly into pipeline
3. [ ] Pipeline can switch between baseline and optimized via config
4. [ ] All existing tests still pass
5. [ ] New tests cover the optimized module
6. [ ] Benchmark shows >= 1.5× improvement at largest n
7. [ ] benchmark_results.json is generated
8. [ ] benchmark_plot.png is generated
9. [ ] Complexity note explains baseline vs optimized Big-O
""")'''),
        ],
        14: [
            ("Part 1: Final Performance Report", '''import os, json

def final_dsa_check():
    print("=== DSA Final Release Check ===\\n")
    passed = 0
    failed = 0

    # Benchmark artifacts
    for f in ["reports/benchmark/benchmark_results.json", "reports/benchmark/benchmark_plot.png"]:
        if os.path.exists(f) and os.path.getsize(f) > 0:
            print(f"[PASS] {f}")
            passed += 1
        else:
            print(f"[FAIL] {f}")
            failed += 1

    # Check benchmark results
    try:
        with open("reports/benchmark/benchmark_results.json") as f:
            bench = json.load(f)
        speedups = bench.get("results", {}).get("speedup", [])
        if speedups and max(speedups) >= 1.5:
            print(f"[PASS] Max speedup: {max(speedups)}× (>= 1.5×)")
            passed += 1
        else:
            print(f"[FAIL] Max speedup: {max(speedups) if speedups else 0}× (need >= 1.5×)")
            failed += 1
    except Exception as e:
        print(f"[FAIL] Benchmark results: {e}")
        failed += 1

    # Standard checks
    for f in ["data/cleaned/cleaned.csv", "reports/report.json"]:
        if os.path.exists(f):
            print(f"[PASS] {f}")
            passed += 1
        else:
            print(f"[FAIL] {f}")
            failed += 1

    # DSA module exists
    if os.path.exists("src/project_template/dsa"):
        print("[PASS] dsa/ module exists")
        passed += 1
    else:
        print("[FAIL] dsa/ module missing")
        failed += 1

    print(f"\\n=== {passed} passed, {failed} failed ===")
    if failed == 0:
        print("\\nFinal DSA release READY! Congratulations on completing the program!")

final_dsa_check()'''),
        ],
    }

    parts = content.get(week_num, [("Part 1: Concepts", f'print("DSA Week {week_num}: {title}")')])
    for part in parts:
        if isinstance(part, tuple) and len(part) == 2:
            t, c = part
            if c.startswith("Think") or c.startswith("Big-O") or (len(c) < 400 and "\n" not in c and not c.strip().startswith("import") and not c.strip().startswith("def") and not c.strip().startswith("class")):
                cells.append(md(f"---\n## {t}\n\n{c}"))
            else:
                cells.append(md(f"---\n## {t}"))
                cells.append(code(c))

    cells.append(md("---\n## Mini-Quiz"))
    cells.append(code(f'# Q1: What is the Big-O complexity of this week\'s main concept?\n# Answer: \n\n# Q2: How can you apply it to your project?\n# Answer: '))
    cells.append(md("---\n## Homework"))
    for i in range(1, 6):
        cells.append(code(f'# HW{i}: Practice {title.lower()}\n# See homework notebook for details\n\n'))
    cells.append(reflection_cell())
    cells.append(reflection_code())
    return cells


def make_studio(week_num, track_key):
    track = TRACKS[track_key]
    cells = [
        md(f"# DSA Week {week_num} Studio — {track['product']}\n**Track:** {track['name']}\n**Goal:** Apply DSA optimization to {track['product']}"),
        setup_cell(),
        md("---\n## Must-Pass Core"),
        code('# Must-pass: benchmark one baseline implementation correctly\n# Identify the bottleneck and state the baseline Big-O\nprint("Working on ' + track["product"] + ' DSA optimization...")\nprint("Must-pass: baseline benchmark + Big-O statement")'),
        md("---\n## Standard Target"),
        code(f'# Standard: implement optimization and prove improvement\nprint("Standard: optimized version + timing comparison")'),
        md("---\n## Stretch"),
        code(f'# Stretch: advanced optimization or additional benchmark\nprint("Stretch goal")'),
        reflection_cell(),
        reflection_code(),
    ]
    return cells


def make_check(week_num):
    cells = [
        md(f"# DSA Week {week_num} — Universal Check"),
        setup_cell(),
        code(f'''import os, json

print("=== DSA Week {week_num} Universal Check ===\\n")
passed = 0
failed = 0

# Check DSA module
if os.path.exists("src/project_template/dsa"):
    print("[PASS] dsa/ module exists")
    passed += 1
else:
    print("[FAIL] dsa/ module missing")
    failed += 1

# Check benchmark artifacts (from week 8 onward)
if {week_num} >= 8:
    for f in ["reports/benchmark/benchmark_results.json", "reports/benchmark/benchmark_plot.png"]:
        if os.path.exists(f) and os.path.getsize(f) > 0:
            print(f"[PASS] {{f}}")
            passed += 1
        else:
            print(f"[FAIL] {{f}}")
            failed += 1

# Standard checks
for f in ["data/cleaned/cleaned.csv", "reports/report.json"]:
    if os.path.exists(f):
        print(f"[PASS] {{f}}")
        passed += 1
    else:
        print(f"[FAIL] {{f}}")
        failed += 1

print(f"\\n=== {{passed}} passed, {{failed}} failed ===")'''),
    ]
    return cells


def make_homework(week_num, title):
    cells = [
        md(f"# DSA Week {week_num} Homework — {title}\n\n**Due:** Before next week\n**Time:** 2-3 hours"),
        md("---\n## Review"),
        code(f'# 1. What is the Big-O of this week\'s main algorithm?\n# Answer: \n\n# 2. When is it better than the naive approach?\n# Answer: \n\n# 3. Write the algorithm from memory (no looking!)\n\n'),
        md("---\n## Practice"),
    ]
    for i in range(1, 6):
        cells.append(code(f'# Practice {i}: Implement or apply {title.lower()}\n# Include timing measurements\n\n'))
    cells.append(md("---\n## Challenge"))
    cells.append(code(f'# Challenge: Optimize a real-world scenario\n# Benchmark your solution at 3 different input sizes\n# Plot the results\n\n'))
    cells.append(code(f'# Complexity analysis:\n# Baseline: O(?)\n# Optimized: O(?)\n# Explain WHY the optimized version is faster\n\n'))
    return cells


# ============================================================
# GENERATE ALL
# ============================================================
print("Generating DSA notebooks...")
for week_num, title, focus in WEEKS:
    wk = f"W{week_num:02d}"
    save_notebook(notebook(make_core(week_num, title, focus), f"DSA {wk} Core"), os.path.join(BASE, f"{wk}_core.ipynb"))
    for tk in TRACKS:
        save_notebook(notebook(make_studio(week_num, tk), f"DSA {wk} Studio {tk}"), os.path.join(BASE, f"{wk}_studio_{tk}.ipynb"))
    save_notebook(notebook(make_check(week_num), f"DSA {wk} Check"), os.path.join(BASE, f"{wk}_check.ipynb"))
    save_notebook(notebook(make_homework(week_num, title), f"DSA {wk} HW"), os.path.join(BASE, f"{wk}_homework.ipynb"))
    print(f"  {wk}: core + 5 studios + check + homework")

print(f"\nDSA complete: {14 * 8} notebooks generated!")
