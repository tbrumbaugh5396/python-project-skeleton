"""
Tests for the core module.
"""

import pytest
from unittest.mock import patch, MagicMock

from skeleton.core import SkeletonApp


class TestSkeletonApp:
    """Test cases for SkeletonApp class."""
    
    def test_init_default_config(self):
        """Test initialization with default configuration."""
        app = SkeletonApp()
        
        assert app.config["app_name"] == "Skeleton Project"
        assert app.config["version"] == "0.1.0"
        assert app.config["debug"] is False
    
    def test_init_custom_config(self):
        """Test initialization with custom configuration."""
        custom_config = {
            "app_name": "Test App",
            "version": "1.0.0",
            "debug": True,
        }
        
        app = SkeletonApp(custom_config)
        
        assert app.config["app_name"] == "Test App"
        assert app.config["version"] == "1.0.0"
        assert app.config["debug"] is True
    
    def test_run_success(self):
        """Test successful application run."""
        app = SkeletonApp()
        
        with patch.object(app, '_execute_main_logic', return_value="success"):
            result = app.run()
            
        assert result == 0
    
    def test_run_exception_debug_mode(self):
        """Test exception handling in debug mode."""
        app = SkeletonApp({"debug": True})
        
        with patch.object(app, '_execute_main_logic', side_effect=Exception("Test error")):
            with pytest.raises(Exception, match="Test error"):
                app.run()
    
    def test_run_exception_normal_mode(self):
        """Test exception handling in normal mode."""
        app = SkeletonApp({"debug": False})
        
        with patch.object(app, '_execute_main_logic', side_effect=Exception("Test error")):
            result = app.run()
            
        assert result == 1
    
    def test_execute_main_logic(self):
        """Test main logic execution."""
        app = SkeletonApp()
        
        result = app._execute_main_logic()
        
        assert result == "Hello from Skeleton Project!"
    
    def test_get_status(self):
        """Test status retrieval."""
        config = {
            "app_name": "Test App",
            "version": "1.0.0",
            "debug": True,
        }
        app = SkeletonApp(config)
        
        status = app.get_status()
        
        assert status["app_name"] == "Test App"
        assert status["version"] == "1.0.0"
        assert status["debug"] is True
        assert status["config"] == config


@pytest.fixture
def sample_app():
    """Fixture providing a sample SkeletonApp instance."""
    return SkeletonApp({
        "app_name": "Test Application",
        "version": "0.1.0",
        "debug": False,
    })


def test_app_lifecycle(sample_app):
    """Test complete application lifecycle."""
    # Check initial state
    status = sample_app.get_status()
    assert status["app_name"] == "Test Application"
    
    # Run application
    with patch.object(sample_app, '_execute_main_logic', return_value="test result"):
        result = sample_app.run()
    
    assert result == 0 