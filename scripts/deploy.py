#!/usr/bin/env python3
"""
Deployment script for uploading to PyPI.
"""

import os
import sys
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


def check_twine():
    """Check if twine is available."""
    try:
        subprocess.run(
            [sys.executable, "-m", "twine", "--version"],
            check=True,
            capture_output=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Twine not found. Install it with: pip install twine")
        return False


def check_dist_files():
    """Check if distribution files exist."""
    dist_path = Path("dist")
    if not dist_path.exists():
        print("No 'dist' directory found. Run the build script first.")
        return False
    
    wheel_files = list(dist_path.glob("*.whl"))
    tar_files = list(dist_path.glob("*.tar.gz"))
    
    if not wheel_files and not tar_files:
        print("No distribution files found in 'dist' directory.")
        return False
    
    print(f"Found {len(wheel_files)} wheel files and {len(tar_files)} source distributions.")
    return True


def upload_to_test_pypi():
    """Upload to Test PyPI."""
    print("Uploading to Test PyPI...")
    
    cmd = [
        sys.executable, "-m", "twine",
        "upload",
        "--repository", "testpypi",
        "dist/*"
    ]
    
    return run_command(cmd)


def upload_to_pypi():
    """Upload to PyPI."""
    print("Uploading to PyPI...")
    
    cmd = [
        sys.executable, "-m", "twine",
        "upload",
        "dist/*"
    ]
    
    return run_command(cmd)


def check_package():
    """Check the package before upload."""
    print("Checking package...")
    
    cmd = [
        sys.executable, "-m", "twine",
        "check",
        "dist/*"
    ]
    
    return run_command(cmd)


def main():
    """Main deployment function."""
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print("Starting deployment process...")
    
    # Check dependencies
    if not check_twine():
        return 1
    
    # Check if distribution files exist
    if not check_dist_files():
        return 1
    
    # Check package
    if not check_package():
        print("Package check failed!")
        return 1
    
    # Ask user where to deploy
    while True:
        choice = input("Deploy to (t)est PyPI, (p)roduction PyPI, or (c)ancel? [t/p/c]: ").lower()
        
        if choice == 'c':
            print("Deployment cancelled.")
            return 0
        elif choice == 't':
            if upload_to_test_pypi():
                print("Successfully uploaded to Test PyPI!")
                print("You can install with: pip install -i https://test.pypi.org/simple/ python-skeleton-project")
                return 0
            else:
                print("Upload to Test PyPI failed!")
                return 1
        elif choice == 'p':
            # Confirm production deployment
            confirm = input("Are you sure you want to upload to production PyPI? [y/N]: ").lower()
            if confirm == 'y':
                if upload_to_pypi():
                    print("Successfully uploaded to PyPI!")
                    print("You can install with: pip install python-skeleton-project")
                    return 0
                else:
                    print("Upload to PyPI failed!")
                    return 1
            else:
                print("Production deployment cancelled.")
                continue
        else:
            print("Invalid choice. Please enter 't', 'p', or 'c'.")


if __name__ == "__main__":
    sys.exit(main()) 