#!/usr/bin/env python3
"""
Build script for the Python skeleton project.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run a command and handle errors."""
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False


def clean_build_dirs():
    """Clean up build directories."""
    print("Cleaning build directories...")
    dirs_to_clean = ["build", "dist", "*.egg-info"]
    
    for pattern in dirs_to_clean:
        for path in Path(".").glob(pattern):
            if path.is_dir():
                print(f"Removing {path}")
                shutil.rmtree(path)
            elif path.is_file():
                print(f"Removing {path}")
                path.unlink()


def build_package():
    """Build the Python package."""
    print("Building Python package...")
    
    # Build using the modern build tool
    if not run_command([sys.executable, "-m", "build"]):
        return False
    
    print("Package built successfully!")
    return True


def main():
    """Main build function."""
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print("Starting build process...")
    
    # Clean previous builds
    clean_build_dirs()
    
    # Build the package
    if not build_package():
        print("Build failed!")
        return 1
    
    print("Build completed successfully!")
    print("Built packages are in the 'dist' directory.")
    return 0


if __name__ == "__main__":
    sys.exit(main()) 