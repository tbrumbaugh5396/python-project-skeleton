"""
Utility functions for the skeleton project.
"""

import logging
import sys
from typing import Optional
from pathlib import Path

# Handle both relative and absolute imports for version
try:
    from . import __version__
except ImportError:
    try:
        from skeleton import __version__
    except ImportError:
        # Fallback if package not installed
        __version__ = "0.1.0"


def get_version() -> str:
    """
    Get the current version of the application.
    
    Returns:
        Version string
    """
    return __version__


def setup_logging(
    level: str = "INFO",
    log_file: Optional[Path] = None,
    format_string: Optional[str] = None
) -> None:
    """
    Set up logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for logging output
        format_string: Optional custom format string
    """
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Convert string level to logging constant
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {level}")
    
    # Configure logging
    handlers = []
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(logging.Formatter(format_string))
    handlers.append(console_handler)
    
    # File handler (if specified)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(logging.Formatter(format_string))
        handlers.append(file_handler)
    
    # Configure root logger
    logging.basicConfig(
        level=numeric_level,
        format=format_string,
        handlers=handlers,
        force=True
    )


def get_app_data_dir() -> Path:
    """
    Get the application data directory.
    
    Returns:
        Path to the application data directory
    """
    if sys.platform == "win32":
        app_data = Path.home() / "AppData" / "Local" / "SkeletonProject"
    elif sys.platform == "darwin":
        app_data = Path.home() / "Library" / "Application Support" / "SkeletonProject"
    else:
        app_data = Path.home() / ".local" / "share" / "skeleton-project"
    
    app_data.mkdir(parents=True, exist_ok=True)
    return app_data


def get_config_dir() -> Path:
    """
    Get the application configuration directory.
    
    Returns:
        Path to the configuration directory
    """
    if sys.platform == "win32":
        config_dir = Path.home() / "AppData" / "Local" / "SkeletonProject" / "config"
    elif sys.platform == "darwin":
        config_dir = Path.home() / "Library" / "Preferences" / "SkeletonProject"
    else:
        config_dir = Path.home() / ".config" / "skeleton-project"
    
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir 