"""
Python Skeleton Project

A template Python project ready for PyPI distribution and executable packaging.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .core import SkeletonApp
from .utils import get_version, setup_logging

__all__ = ["SkeletonApp", "get_version", "setup_logging"] 