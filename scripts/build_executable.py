#!/usr/bin/env python3
"""
Build script for creating executable packages.
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


def clean_executable_dirs():
    """Clean up executable build directories."""
    print("Cleaning executable build directories...")
    dirs_to_clean = ["build", "dist"]
    
    for dir_name in dirs_to_clean:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"Removing {dir_path}")
            shutil.rmtree(dir_path)


def create_pyinstaller_spec():
    """Create PyInstaller spec files."""
    cli_spec = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/skeleton/cli.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='skeleton-cli',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
"""

    gui_spec = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/skeleton/gui.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['wx', 'wx.lib.agw.aui'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='skeleton-gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
"""

    # Write spec files
    with open("skeleton-cli.spec", "w") as f:
        f.write(cli_spec.strip())
    
    with open("skeleton-gui.spec", "w") as f:
        f.write(gui_spec.strip())
    
    print("PyInstaller spec files created.")


def build_cli_executable():
    """Build CLI executable."""
    print("Building CLI executable...")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name", "skeleton-cli",
        "--console",
        "src/skeleton/cli.py"
    ]
    
    return run_command(cmd)


def build_gui_executable():
    """Build GUI executable."""
    print("Building GUI executable...")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name", "skeleton-gui",
        "--windowed",
        "--hidden-import", "wx",
        "--hidden-import", "wx.lib.agw.aui",
        "src/skeleton/gui.py"
    ]
    
    return run_command(cmd)


def check_pyinstaller():
    """Check if PyInstaller is available."""
    try:
        subprocess.run(
            [sys.executable, "-m", "PyInstaller", "--version"],
            check=True,
            capture_output=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("PyInstaller not found. Install it with: pip install pyinstaller")
        return False


def main():
    """Main build function."""
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print("Starting executable build process...")
    
    # Check dependencies
    if not check_pyinstaller():
        return 1
    
    # Clean previous builds
    clean_executable_dirs()
    
    # Create spec files
    create_pyinstaller_spec()
    
    # Build executables
    success = True
    
    if not build_cli_executable():
        print("CLI executable build failed!")
        success = False
    
    if not build_gui_executable():
        print("GUI executable build failed!")
        success = False
    
    if success:
        print("Executable build completed successfully!")
        print("Executables are in the 'dist' directory.")
        return 0
    else:
        print("Executable build failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 