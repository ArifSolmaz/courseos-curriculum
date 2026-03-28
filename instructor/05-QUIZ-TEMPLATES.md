# Quiz & Oral Check Templates

## How to use

- **Micro-quizzes**: 5 questions, 10 minutes, start of every session. Paper or Google Form. Individual.
- **Oral checks**: 2 minutes, random selection, 2–3 students per session. "Explain this code."
- **Code-reading quizzes** (Year 2): show code, ask what it does or what's wrong.

---

## CP1 Micro-Quiz Bank

### W1–W2: Basics
1. What does `print("hello")` do?
2. What is the difference between `=` and `==`?
3. What type is `3.14`? (int / float / str / bool)
4. What does `type(42)` return?
5. What is a variable?
6. Fix this: `print("Hello)` — what's missing?
7. What is `10 // 3`?
8. What is `10 % 3`?
9. Write an f-string that prints: "My name is Ahmed and I am 20"
10. What is a config dictionary used for?

### W3–W4: Conditionals
1. What does `elif` mean?
2. What is the output of: `if 5 > 10: print("A") else: print("B")`?
3. What operator checks "not equal"?
4. What does `and` do? Give an example.
5. What does `continue` do inside a loop?
6. Write an if/elif/else that classifies age: child (<13), teen (13-17), adult (18+)
7. What is the difference between `or` and `and`?
8. Can you put an `if` inside another `if`? What is it called?
9. What does `not True` evaluate to?
10. Why do we use conditionals in `clean_data()`?

### W5–W6: Loops
1. How many times does `for i in range(5)` run?
2. What does `range(2, 8)` produce?
3. Write a loop that sums all numbers from 1 to 100.
4. What is the "accumulator pattern"?
5. What is the danger of a `while` loop?
6. What does `break` do?
7. Count how many values in `[3, 7, 2, 9, 5]` are greater than 4.
8. What is a threshold crossing?
9. What is an edge case? Give an example.
10. Why must we handle empty lists before computing stats?

### W7–W8: Lists & Strings
1. What does `data[0]` return for `data = [10, 20, 30]`?
2. What does `data[-1]` return?
3. What does `data[1:3]` return?
4. What does `"hello world".split()` return?
5. What does `"  abc  ".strip()` return?
6. How do you add an item to the end of a list?
7. What is a list comprehension? Write one that squares numbers 1–5.
8. What does `"a,b,c".split(",")` return?
9. What is a moving average?
10. Why is parsing important for data pipelines?

### W9–W10: Functions
1. What does `def` do?
2. What does `return` do?
3. What is the difference between a parameter and an argument?
4. What is DRY?
5. What is a docstring?
6. Write a function that takes a list and returns its mean.
7. Can a function call another function?
8. What is a default parameter?
9. Why do we refactor code into functions?
10. What is the scope of a variable defined inside a function?

### W11–W14: Exceptions, I/O, Integration
1. What does `try/except` do?
2. Name 3 common Python exception types.
3. What does `with open("f.csv") as f:` do?
4. What module do we use to read CSV files?
5. How do you write a dictionary to a JSON file?
6. What is `csv.DictReader`?
7. What does `matplotlib.pyplot.savefig()` do?
8. What is `self_check()` for?
9. Why must we NOT use `input()` in graded code?
10. Name the 5 pipeline functions in order.

---

## CP2 Quiz Bank

1. What is schema validation?
2. What does `collections.Counter` do?
3. What is the IQR method for outlier detection?
4. What is a "golden output" test?
5. Why must logic live in `/src`, not in notebooks?
6. What does `import numpy as np` give us?
7. How do you time a function with `timeit`?
8. What is `config.get("key", default)`?
9. What is the difference between JSON and Markdown reports?
10. What does "modularize" mean?

---

## OOP Quiz Bank

1. What is the difference between a class and an object?
2. What does `__init__` do?
3. What does `self` refer to?
4. What is composition (has-a)?
5. What is SRP (Single Responsibility Principle)?
6. What is the Strategy pattern?
7. What is a Factory?
8. What does `@pytest.fixture` do?
9. What is encapsulation?
10. Explain OCP: how can you add a new analyzer without modifying existing code?

---

## DSA Quiz Bank

1. What does O(n) mean in plain English?
2. What is O(1) for a dict lookup?
3. How many steps does binary search take on 1,000,000 items?
4. When is insertion sort better than merge sort?
5. What is a hash collision?
6. What does `heapq.nlargest(5, data)` do?
7. What is the difference between BFS and DFS?
8. What is memoization?
9. What is the Big-O of Python's `in` operator on a list vs a set?
10. What does "1.5× speedup" mean in benchmarking?

---

## Oral Check Prompts

Use these when doing random 2-minute oral checks:

### General (any course)
- "Walk me through this function line by line."
- "What would happen if the input list is empty?"
- "Why did you use a dict here instead of a list?"
- "What does this line do?" (point to a specific line)
- "If I change this threshold from 50 to 0, what happens?"

### OOP-specific
- "Why is this a separate class instead of a function?"
- "What invariant does this class protect?"
- "How would you add a new cleaning strategy?"
- "What happens if I remove `self` from this method?"

### DSA-specific
- "What is the Big-O of your baseline? Your optimized version?"
- "Why did you choose this data structure?"
- "Show me the benchmark plot. Explain what it proves."
- "What happens at n=1,000,000?"
