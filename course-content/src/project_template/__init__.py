"""
Project Template — CourseOS Two-Year Pipeline
=============================================
This package implements the standard project contract:
  load_data → clean_data → analyze → plot → export_results → self_check

Replace 'project_template' with your actual project name.
"""

__version__ = "1.0.0"

from .config import get_config
from .io import load_data
from .cleaning import clean_data
from .analysis import analyze
from .plotting import plot
from .reporting import export_results, self_check
