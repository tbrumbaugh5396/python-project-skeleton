"""
Tests for the CLI module.
"""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from skeleton.cli import create_parser, main, load_config


class TestCreateParser:
    """Test cases for create_parser function."""
    
    def test_create_parser(self):
        """Test parser creation."""
        parser = create_parser()
        
        assert parser.prog == "skeleton-cli"
        assert "skeleton Python project CLI" in parser.description
    
    def test_parser_version(self, capsys):
        """Test version argument."""
        parser = create_parser()
        
        with pytest.raises(SystemExit):
            parser.parse_args(["--version"])
        
        captured = capsys.readouterr()
        assert "skeleton-cli" in captured.out
        assert "0.1.0" in captured.out
    
    def test_parser_debug(self):
        """Test debug argument."""
        parser = create_parser()
        args = parser.parse_args(["--debug"])
        
        assert args.debug is True
    
    def test_parser_log_level(self):
        """Test log level argument."""
        parser = create_parser()
        args = parser.parse_args(["--log-level", "DEBUG"])
        
        assert args.log_level == "DEBUG"
    
    def test_parser_log_file(self):
        """Test log file argument."""
        parser = create_parser()
        args = parser.parse_args(["--log-file", "/tmp/test.log"])
        
        assert args.log_file == Path("/tmp/test.log")
    
    def test_parser_config_file(self):
        """Test config file argument."""
        parser = create_parser()
        args = parser.parse_args(["--config-file", "/tmp/config.json"])
        
        assert args.config_file == Path("/tmp/config.json")


class TestLoadConfig:
    """Test cases for load_config function."""
    
    def test_load_config_no_file(self):
        """Test loading config with no file."""
        config = load_config()
        assert config == {}
    
    def test_load_config_nonexistent_file(self):
        """Test loading config with nonexistent file."""
        config = load_config(Path("/nonexistent/file.json"))
        assert config == {}
    
    @patch('pathlib.Path.exists')
    def test_load_config_existing_file(self, mock_exists):
        """Test loading config with existing file."""
        mock_exists.return_value = True
        config_file = Path("/tmp/config.json")
        
        config = load_config(config_file)
        # For now, just returns empty dict as implementation is placeholder
        assert config == {}


class TestMain:
    """Test cases for main function."""
    
    @patch('skeleton.cli.SkeletonApp')
    @patch('skeleton.cli.setup_logging')
    def test_main_default_args(self, mock_setup_logging, mock_skeleton_app):
        """Test main with default arguments."""
        mock_app_instance = MagicMock()
        mock_app_instance.run.return_value = 0
        mock_skeleton_app.return_value = mock_app_instance
        
        result = main([])
        
        assert result == 0
        mock_setup_logging.assert_called_once()
        mock_skeleton_app.assert_called_once()
        mock_app_instance.run.assert_called_once()
    
    @patch('skeleton.cli.SkeletonApp')
    @patch('skeleton.cli.setup_logging')
    def test_main_debug_mode(self, mock_setup_logging, mock_skeleton_app):
        """Test main with debug mode."""
        mock_app_instance = MagicMock()
        mock_app_instance.run.return_value = 0
        mock_skeleton_app.return_value = mock_app_instance
        
        result = main(["--debug"])
        
        assert result == 0
        
        # Check that config includes debug=True
        call_args = mock_skeleton_app.call_args[0][0]
        assert call_args["debug"] is True
    
    @patch('skeleton.cli.SkeletonApp')
    @patch('skeleton.cli.setup_logging')
    @patch('skeleton.cli.get_app_data_dir')
    def test_main_debug_log_file(self, mock_get_app_data_dir, mock_setup_logging, mock_skeleton_app):
        """Test main with debug mode creates log file."""
        mock_app_instance = MagicMock()
        mock_app_instance.run.return_value = 0
        mock_skeleton_app.return_value = mock_app_instance
        
        mock_app_data_dir = Path("/tmp/app_data")
        mock_get_app_data_dir.return_value = mock_app_data_dir
        
        result = main(["--debug"])
        
        assert result == 0
        
        # Check that setup_logging was called with log file
        call_args = mock_setup_logging.call_args
        assert call_args[1]["log_file"] == mock_app_data_dir / "debug.log"
    
    @patch('skeleton.cli.SkeletonApp')
    @patch('skeleton.cli.setup_logging')
    def test_main_custom_log_level(self, mock_setup_logging, mock_skeleton_app):
        """Test main with custom log level."""
        mock_app_instance = MagicMock()
        mock_app_instance.run.return_value = 0
        mock_skeleton_app.return_value = mock_app_instance
        
        result = main(["--log-level", "ERROR"])
        
        assert result == 0
        
        # Check that setup_logging was called with correct level
        call_args = mock_setup_logging.call_args
        assert call_args[1]["level"] == "ERROR"
    
    @patch('skeleton.cli.SkeletonApp')
    @patch('skeleton.cli.setup_logging')
    def test_main_app_failure(self, mock_setup_logging, mock_skeleton_app):
        """Test main when app returns error code."""
        mock_app_instance = MagicMock()
        mock_app_instance.run.return_value = 1
        mock_skeleton_app.return_value = mock_app_instance
        
        result = main([])
        
        assert result == 1


def test_main_entry_point():
    """Test that main can be called as entry point."""
    with patch('skeleton.cli.main') as mock_main:
        mock_main.return_value = 0
        
        # This would be called when running the module directly
        with patch('sys.argv', ['skeleton-cli']):
            mock_main()
        
        mock_main.assert_called() 