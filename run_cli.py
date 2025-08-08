#!/usr/bin/env python3
"""
Standalone script to run the skeleton CLI application.

Run this from the project root directory:
    python run_cli.py [arguments]
"""

import sys
from pathlib import Path

# Add the src directory to the path
project_root = Path(__file__).parent
src_dir = project_root / "src"
sys.path.insert(0, str(src_dir))

try:
    from skeleton.cli import main
except ImportError as e:
    print(f"Error importing the CLI module: {e}")
    print("Make sure you're running this from the project root directory.")
    sys.exit(1)

if __name__ == "__main__":
    # Pass through command line arguments (excluding script name)
    sys.exit(main(sys.argv[1:])) 