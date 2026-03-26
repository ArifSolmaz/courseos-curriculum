"""Notebook generation utility for CourseOS curriculum."""
import json
import os

def md(source):
    """Create a markdown cell."""
    if isinstance(source, str):
        source = source.split('\n')
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + '\n' for line in source[:-1]] + [source[-1]] if source else []
    }

def code(source, collapsed=False):
    """Create a code cell."""
    if isinstance(source, str):
        source = source.split('\n')
    meta = {}
    if collapsed:
        meta["collapsed"] = True
    return {
        "cell_type": "code",
        "metadata": meta,
        "source": [line + '\n' for line in source[:-1]] + [source[-1]] if source else [],
        "execution_count": None,
        "outputs": []
    }

def notebook(cells, title="Notebook"):
    """Create a complete notebook dict."""
    return {
        "nbformat": 4,
        "nbformat_minor": 0,
        "metadata": {
            "colab": {
                "provenance": [],
                "toc_visible": True,
                "name": title
            },
            "kernelspec": {
                "name": "python3",
                "display_name": "Python 3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "cells": cells
    }

def save_notebook(nb_dict, filepath):
    """Save notebook dict to .ipynb file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(nb_dict, f, indent=1, ensure_ascii=False)

def setup_cell(course="cp1"):
    """Standard Colab setup cell."""
    return code(f"""# === SETUP (run this first) ===
# If running in Google Colab, uncomment and run the lines below:
# !git clone https://github.com/YOUR-ORG/YOUR-REPO.git
# %cd YOUR-REPO

import sys, os
# Add src to path so we can import project modules
if os.path.exists('src'):
    sys.path.insert(0, 'src')
elif os.path.exists('../src'):
    sys.path.insert(0, '../src')
elif os.path.exists('../../src'):
    sys.path.insert(0, '../../src')

print("Setup complete! Ready to work.")""")

def reflection_cell():
    """Standard end-of-session reflection cell."""
    return md("""---
## Reflection (Required - Complete before submitting)

In the cell below, write 3-5 bullet points:
1. **What I learned today:**
2. **What was hardest:**
3. **What I still don't understand:**
4. **What I will review before next week:**
5. **If I used AI tools, what for:**""")

def reflection_code():
    return code("""# YOUR REFLECTION (write as comments or as a multi-line string)
reflection = \"\"\"
- What I learned:
- What was hardest:
- What I still don't understand:
- What I will review:
- AI tools used (if any):
\"\"\"
print(reflection)""")

TRACKS = {
    "robotics": {"name": "Robotics/Mechatronics", "product": "MechaSense Studio", "short": "robotics"},
    "data": {"name": "Data/AI", "product": "CleanReport Pipeline", "short": "data"},
    "simulation": {"name": "Simulation/Games", "product": "SimLab Engine", "short": "simulation"},
    "space": {"name": "Space/Astro", "product": "Lightcurve Explorer", "short": "space"},
    "iot": {"name": "IoT/Reporting", "product": "AutoDashboard Reporter", "short": "iot"},
}
