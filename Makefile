.PHONY: help install install-dev test lint format clean build build-exe deploy

# Default target
help:
	@echo "Available targets:"
	@echo "  install     - Install the package"
	@echo "  install-dev - Install development dependencies"
	@echo "  test        - Run tests"
	@echo "  lint        - Run linting (flake8, mypy)"
	@echo "  format      - Format code (black, isort)"
	@echo "  clean       - Clean build artifacts"
	@echo "  build       - Build package"
	@echo "  build-exe   - Build executables"
	@echo "  deploy      - Deploy to PyPI"

# Installation
install:
	pip install -e .

install-dev:
	pip install -r requirements-dev.txt
	pip install -e .

# Testing
test:
	pytest

test-cov:
	pytest --cov=skeleton --cov-report=html --cov-report=term

# Code quality
lint:
	flake8 src tests
	mypy src

format:
	black src tests scripts
	isort src tests scripts

format-check:
	black --check src tests scripts
	isort --check-only src tests scripts

# Building
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: clean
	python scripts/build.py

build-exe: clean
	python scripts/build_executable.py

# Deployment
deploy:
	python scripts/deploy.py

# Development shortcuts
dev-setup: install-dev
	@echo "Development environment ready!"

dev-test: format lint test
	@echo "All checks passed!" 