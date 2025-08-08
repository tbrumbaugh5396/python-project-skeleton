"""
Tests for the utils module.
"""

import logging
import sys
from pathlib import Path
from unittest.mock import patch, mock_open

import pytest

from skeleton.utils import (
    get_version,
    setup_logging,
    get_app_data_dir,
    get_config_dir,
)


def test_get_version():
    """Test version retrieval."""
    version = get_version()
    assert version == "0.1.0"


class TestSetupLogging:
    """Test cases for setup_logging function."""
    
    def test_setup_logging_default(self):
        """Test logging setup with default parameters."""
        with patch('logging.basicConfig') as mock_basic_config:
            setup_logging()
            
            mock_basic_config.assert_called_once()
            args, kwargs = mock_basic_config.call_args
            
            assert kwargs['level'] == logging.INFO
            assert kwargs['force'] is True
    
    def test_setup_logging_custom_level(self):
        """Test logging setup with custom level."""
        with patch('logging.basicConfig') as mock_basic_config:
            setup_logging(level="DEBUG")
            
            mock_basic_config.assert_called_once()
            args, kwargs = mock_basic_config.call_args
            
            assert kwargs['level'] == logging.DEBUG
    
    def test_setup_logging_invalid_level(self):
        """Test logging setup with invalid level."""
        with pytest.raises(ValueError, match="Invalid log level"):
            setup_logging(level="INVALID")
    
    @patch('pathlib.Path.mkdir')
    @patch('logging.FileHandler')
    def test_setup_logging_with_file(self, mock_file_handler, mock_mkdir):
        """Test logging setup with file output."""
        log_file = Path("/tmp/test.log")
        
        with patch('logging.basicConfig') as mock_basic_config:
            setup_logging(log_file=log_file)
            
            # Check that directory creation was attempted
            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
            
            # Check that file handler was created
            mock_file_handler.assert_called_once_with(log_file)


class TestDirectoryFunctions:
    """Test cases for directory utility functions."""
    
    @patch('pathlib.Path.mkdir')
    def test_get_app_data_dir_darwin(self, mock_mkdir):
        """Test app data directory on macOS."""
        with patch('sys.platform', 'darwin'):
            result = get_app_data_dir()
            
            expected = Path.home() / "Library" / "Application Support" / "SkeletonProject"
            assert result == expected
            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
    
    @patch('pathlib.Path.mkdir')
    def test_get_app_data_dir_win32(self, mock_mkdir):
        """Test app data directory on Windows."""
        with patch('sys.platform', 'win32'):
            result = get_app_data_dir()
            
            expected = Path.home() / "AppData" / "Local" / "SkeletonProject"
            assert result == expected
            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
    
    @patch('pathlib.Path.mkdir')
    def test_get_app_data_dir_linux(self, mock_mkdir):
        """Test app data directory on Linux."""
        with patch('sys.platform', 'linux'):
            result = get_app_data_dir()
            
            expected = Path.home() / ".local" / "share" / "skeleton-project"
            assert result == expected
            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
    
    @patch('pathlib.Path.mkdir')
    def test_get_config_dir_darwin(self, mock_mkdir):
        """Test config directory on macOS."""
        with patch('sys.platform', 'darwin'):
            result = get_config_dir()
            
            expected = Path.home() / "Library" / "Preferences" / "SkeletonProject"
            assert result == expected
            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
    
    @patch('pathlib.Path.mkdir')
    def test_get_config_dir_win32(self, mock_mkdir):
        """Test config directory on Windows."""
        with patch('sys.platform', 'win32'):
            result = get_config_dir()
            
            expected = Path.home() / "AppData" / "Local" / "SkeletonProject" / "config"
            assert result == expected
            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
    
    @patch('pathlib.Path.mkdir')
    def test_get_config_dir_linux(self, mock_mkdir):
        """Test config directory on Linux."""
        with patch('sys.platform', 'linux'):
            result = get_config_dir()
            
            expected = Path.home() / ".config" / "skeleton-project"
            assert result == expected
            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True) 