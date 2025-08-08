#!/usr/bin/env python3
"""
Standalone script to run the skeleton GUI application.

Run this from the project root directory:
    python run_gui.py
"""

import sys
from pathlib import Path

# Add the src directory to the path
project_root = Path(__file__).parent
src_dir = project_root / "src"
sys.path.insert(0, str(src_dir))

try:
    from skeleton.gui import main
except ImportError as e:
    print(f"Error importing the GUI module: {e}")
    print("Make sure you have wxPython installed: pip install wxpython")
    print("And that you're running this from the project root directory.")
    sys.exit(1)

if __name__ == "__main__":
    print("Starting Skeleton GUI...")
    sys.exit(main()) 