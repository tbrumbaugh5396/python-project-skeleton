#!/usr/bin/env python3
"""
Setup script for the Python project skeleton.
"""

import os
from setuptools import setup, find_packages

# Read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open(os.path.join(this_directory, 'requirements.txt'),
          encoding='utf-8') as f:
    requirements = [
        line.strip() for line in f if line.strip() and not line.startswith('#')
    ]

setup(
    name="python-skeleton-project",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description=
    "A skeleton Python project ready for PyPI and executable packaging",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/python-skeleton-project",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
            "build>=0.10.0",
            "twine>=4.0.0",
        ],
        "gui": [
            "wxpython>=4.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "skeleton-cli=skeleton.cli:main",
        ],
        "gui_scripts": [
            "skeleton-gui=skeleton.gui:main",
        ],
    },
    include_package_data=True,
    package_data={
        "skeleton": ["data/*", "templates/*"],
    },
    zip_safe=False,
)
