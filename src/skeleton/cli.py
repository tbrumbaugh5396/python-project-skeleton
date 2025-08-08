"""
Command-line interface for the skeleton project.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

# Handle both relative and absolute imports
try:
    from .core import SkeletonApp
    from .utils import setup_logging, get_version, get_app_data_dir
except ImportError:
    # If running as __main__, try absolute imports
    try:
        from skeleton.core import SkeletonApp
        from skeleton.utils import setup_logging, get_version, get_app_data_dir
    except ImportError:
        # Last resort - add parent directory to path
        import os
        parent_dir = Path(__file__).parent.parent.parent / "src"
        sys.path.insert(0, str(parent_dir))
        
        from skeleton.core import SkeletonApp
        from skeleton.utils import setup_logging, get_version, get_app_data_dir


def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser.
    
    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        prog="skeleton-cli",
        description="A skeleton Python project CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  skeleton-cli --version
  skeleton-cli --debug
  skeleton-cli --log-file /path/to/logfile.log
        """
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {get_version()}"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set the logging level (default: INFO)"
    )
    
    parser.add_argument(
        "--log-file",
        type=Path,
        help="Log to specified file instead of console"
    )
    
    parser.add_argument(
        "--config-file",
        type=Path,
        help="Path to configuration file"
    )
    
    return parser


def load_config(config_file: Optional[Path] = None) -> dict:
    """
    Load configuration from file.
    
    Args:
        config_file: Path to configuration file
        
    Returns:
        Configuration dictionary
    """
    config = {}
    
    if config_file and config_file.exists():
        # In a real application, you might use JSON, YAML, or TOML
        # For this skeleton, we'll just return an empty dict
        pass
    
    return config


def main(argv: Optional[List[str]] = None) -> int:
    """
    Main entry point for the CLI application.
    
    Args:
        argv: Optional list of command-line arguments
        
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    parser = create_parser()
    args = parser.parse_args(argv)
    
    # Set up logging
    log_file = args.log_file
    if log_file is None and args.debug:
        # Use default log file in debug mode
        log_file = get_app_data_dir() / "debug.log"
    
    setup_logging(
        level=args.log_level,
        log_file=log_file
    )
    
    # Load configuration
    config = load_config(args.config_file)
    
    # Add CLI arguments to config
    config.update({
        "debug": args.debug,
        "log_level": args.log_level,
        "log_file": str(log_file) if log_file else None,
    })
    
    # Create and run the application
    app = SkeletonApp(config)
    return app.run()


if __name__ == "__main__":
    sys.exit(main()) 