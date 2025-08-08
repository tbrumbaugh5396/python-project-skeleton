# Python Skeleton Project

A comprehensive Python project template ready for PyPI distribution and executable packaging.

**Note: This is a template project. To create new projects from this template, use the [Python Project Generator](../Python%20Project%20Generator/) tool.**

## Features

- ✅ Modern Python packaging with `pyproject.toml` and `setup.py`
- ✅ Command-line interface (CLI) with argument parsing
- ✅ Graphical user interface (GUI) using wxPython
- ✅ Ready for PyPI deployment
- ✅ Executable packaging with PyInstaller
- ✅ Comprehensive testing setup with pytest
- ✅ Code quality tools (Black, Flake8, MyPy)
- ✅ CI/CD ready structure
- ✅ Cross-platform compatibility

## Project Structure

```
├── src/
│   └── skeleton/
│       ├── __init__.py          # Package initialization
│       ├── core.py              # Core application logic
│       ├── cli.py               # Command-line interface
│       ├── gui.py               # Graphical user interface
│       └── utils.py             # Utility functions
├── tests/                       # Test files
├── scripts/                     # Build and deployment scripts
│   ├── build.py                 # Package building
│   ├── build_executable.py     # Executable building
│   └── deploy.py                # PyPI deployment
├── pyproject.toml              # Modern Python project configuration
├── setup.py                    # Legacy setup script
├── requirements.txt            # Runtime dependencies
├── requirements-dev.txt        # Development dependencies
└── README.md                   # This file
```

## Installation

### From PyPI (when published)

```bash
pip install python-skeleton-project
```

### From Source

```bash
git clone <repository-url>
cd python-skeleton-project
pip install -e .
```

### Development Installation

```bash
git clone <repository-url>
cd python-skeleton-project
pip install -e .[dev]
```

### Running Without Installation

You can run the applications directly from source without installing:

```bash
# First, install wxPython for GUI applications
pip install wxpython

# Then run from the project root directory:
python3 run_generator.py    # Project generator GUI
python3 run_gui.py          # Example GUI application  
python3 run_cli.py --help   # CLI application
```

## Usage

### Command Line Interface

```bash
# Basic usage
skeleton-cli

# With debug mode
skeleton-cli --debug

# With custom log level
skeleton-cli --log-level DEBUG

# Save logs to file
skeleton-cli --log-file app.log

# Show version
skeleton-cli --version

# Or run directly from source (from project root)
python3 run_cli.py --version
```

### Creating New Projects

To create new projects based on this template, use the **Python Project Generator** tool located in the sibling directory:

```bash
cd "../Python Project Generator"
python3 generator_gui.py
```

The generator provides an intuitive GUI to create customized Python projects with your choice of features:

**Features you can select:**
- ✅ Command Line Interface (CLI)
- ✅ Graphical User Interface (GUI) with wxPython
- ✅ Unit testing with pytest
- ✅ Executable building with PyInstaller
- ✅ PyPI packaging (setup.py, pyproject.toml)
- ✅ Development requirements
- ✅ License files (MIT, Apache, GPL, etc.)
- ✅ README.md documentation
- ✅ Makefile for common tasks
- ✅ .gitignore file
- ✅ GitHub Actions CI/CD workflow

### Graphical User Interface

```bash
# Start GUI application
skeleton-gui

# Or run directly from source (from project root)
python3 run_gui.py
```

Or install GUI dependencies separately:
```bash
pip install python-skeleton-project[gui]
skeleton-gui
```

### Python API

```python
from skeleton import SkeletonApp

# Create and run application
app = SkeletonApp({"debug": True})
result = app.run()

# Get application status
status = app.get_status()
print(status)
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone <repository-url>
cd python-skeleton-project

# Install development dependencies
pip install -r requirements-dev.txt

# Install in development mode
pip install -e .
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=skeleton --cov-report=html

# Run specific test file
pytest tests/test_core.py
```

### Code Quality

```bash
# Format code with Black
black src tests

# Check with Flake8
flake8 src tests

# Type checking with MyPy
mypy src

# Sort imports with isort
isort src tests
```

### Building

#### Build Python Package

```bash
python scripts/build.py
```

This creates distribution files in the `dist/` directory:
- `*.whl` - Wheel distribution
- `*.tar.gz` - Source distribution

#### Build Executables

```bash
python scripts/build_executable.py
```

This creates standalone executables in the `dist/` directory:
- `skeleton-cli` - Command-line executable
- `skeleton-gui` - GUI executable

### Deployment

#### Deploy to PyPI

```bash
python scripts/deploy.py
```

This script will:
1. Check package integrity
2. Ask whether to deploy to Test PyPI or production PyPI
3. Upload the package

#### Manual Deployment

```bash
# Check package
twine check dist/*

# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Upload to production PyPI
twine upload dist/*
```

## Configuration

### Package Metadata

Edit the following files to customize your project:

- `pyproject.toml` - Modern configuration
- `setup.py` - Legacy configuration for compatibility
- `src/skeleton/__init__.py` - Package version and metadata

### Dependencies

- `requirements.txt` - Runtime dependencies
- `requirements-dev.txt` - Development dependencies
- `pyproject.toml` - Dependencies in modern format

## Customization

### Changing Package Name

1. Rename `src/skeleton/` directory
2. Update package name in `pyproject.toml` and `setup.py`
3. Update imports throughout the codebase
4. Update entry points in configuration files

### Adding Dependencies

Add to `requirements.txt` for runtime dependencies:
```
requests>=2.28.0
click>=8.0.0
```

Add to `requirements-dev.txt` for development dependencies:
```
pytest-mock>=3.10.0
sphinx>=5.0
```

### Customizing GUI

The GUI uses wxPython. To customize:

1. Edit `src/skeleton/gui.py`
2. Modify the `SkeletonFrame` class
3. Add new panels, menus, or dialogs as needed

### Customizing CLI

The CLI uses argparse. To customize:

1. Edit `src/skeleton/cli.py`
2. Modify the `create_parser()` function
3. Add new arguments and commands

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and quality checks
5. Submit a pull request

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Make sure you've installed the package with `pip install -e .`
2. **wxPython installation fails**: Try `pip install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-20.04/ wxpython`
3. **PyInstaller build fails**: Ensure all dependencies are properly installed

### Platform-Specific Notes

- **Windows**: May need Visual C++ Build Tools for some dependencies
- **macOS**: May need Xcode Command Line Tools
- **Linux**: May need additional system packages for wxPython

## Support

- Create an issue on GitHub for bugs or feature requests
- Check the documentation for detailed usage instructions
- Review the examples in the `examples/` directory (if available) 