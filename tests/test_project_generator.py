"""
Tests for the project generator module.
"""

import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from skeleton.project_generator import ProjectGenerator


class TestProjectGenerator:
    """Test cases for ProjectGenerator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.generator = ProjectGenerator()
        self.temp_dir = Path(tempfile.mkdtemp())
        
    def teardown_method(self):
        """Clean up test fixtures."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_init(self):
        """Test generator initialization."""
        assert self.generator is not None
        assert hasattr(self.generator, 'logger')
        assert hasattr(self.generator, 'template_dir')
    
    def test_to_package_name(self):
        """Test package name conversion."""
        assert self.generator._to_package_name("My Project") == "my_project"
        assert self.generator._to_package_name("my-project") == "my_project"
        assert self.generator._to_package_name("MyProject") == "myproject"
        assert self.generator._to_package_name("my_project") == "my_project"
    
    def test_to_class_name(self):
        """Test class name conversion."""
        assert self.generator._to_class_name("my_project") == "MyProject"
        assert self.generator._to_class_name("simple") == "Simple"
        assert self.generator._to_class_name("multi_word_name") == "MultiWordName"
    
    def test_generate_project_minimal(self):
        """Test generating a minimal project."""
        project_name = "test_project"
        metadata = {
            "description": "A test project",
            "author": "Test Author",
            "email": "test@example.com",
            "version": "0.1.0",
            "url": "https://github.com/test/test_project",
            "license_type": "MIT"
        }
        features = {
            "cli": False,
            "gui": False,
            "tests": False,
            "executable": False,
            "pypi_packaging": True,
            "dev_requirements": False,
            "license": False,
            "readme": False,
            "makefile": False,
            "gitignore": False,
            "github_actions": False,
        }
        
        result = self.generator.generate_project(
            project_name=project_name,
            output_dir=self.temp_dir,
            features=features,
            metadata=metadata
        )
        
        assert result is True
        
        project_path = self.temp_dir / project_name
        assert project_path.exists()
        
        # Check core structure
        src_dir = project_path / "src" / "test_project"
        assert src_dir.exists()
        assert (src_dir / "__init__.py").exists()
        assert (src_dir / "core.py").exists()
        assert (src_dir / "utils.py").exists()
        
        # Check PyPI packaging files
        assert (project_path / "setup.py").exists()
        assert (project_path / "pyproject.toml").exists()
        assert (project_path / "requirements.txt").exists()
    
    def test_generate_project_with_cli(self):
        """Test generating a project with CLI feature."""
        project_name = "cli_project"
        metadata = {
            "description": "A CLI project",
            "author": "Test Author",
            "email": "test@example.com",
            "version": "0.1.0",
        }
        features = {
            "cli": True,
            "gui": False,
            "tests": False,
            "executable": False,
            "pypi_packaging": False,
            "dev_requirements": False,
            "license": False,
            "readme": False,
            "makefile": False,
            "gitignore": False,
            "github_actions": False,
        }
        
        result = self.generator.generate_project(
            project_name=project_name,
            output_dir=self.temp_dir,
            features=features,
            metadata=metadata
        )
        
        assert result is True
        
        project_path = self.temp_dir / project_name
        src_dir = project_path / "src" / "cli_project"
        
        # Check CLI file exists
        assert (src_dir / "cli.py").exists()
        
        # Check CLI file content
        cli_content = (src_dir / "cli.py").read_text()
        assert "argparse" in cli_content
        assert "cli_project-cli" in cli_content
    
    def test_generate_project_with_gui(self):
        """Test generating a project with GUI feature."""
        project_name = "gui_project"
        metadata = {
            "description": "A GUI project",
            "author": "Test Author",
            "email": "test@example.com",
            "version": "0.1.0",
        }
        features = {
            "cli": False,
            "gui": True,
            "tests": False,
            "executable": False,
            "pypi_packaging": False,
            "dev_requirements": False,
            "license": False,
            "readme": False,
            "makefile": False,
            "gitignore": False,
            "github_actions": False,
        }
        
        result = self.generator.generate_project(
            project_name=project_name,
            output_dir=self.temp_dir,
            features=features,
            metadata=metadata
        )
        
        assert result is True
        
        project_path = self.temp_dir / project_name
        src_dir = project_path / "src" / "gui_project"
        
        # Check GUI file exists
        assert (src_dir / "gui.py").exists()
        
        # Check GUI file content
        gui_content = (src_dir / "gui.py").read_text()
        assert "wxPython" in gui_content
        assert "wx.Frame" in gui_content
    
    def test_generate_project_with_tests(self):
        """Test generating a project with tests feature."""
        project_name = "test_project"
        metadata = {"description": "A test project", "author": "Test", "email": "test@example.com"}
        features = {
            "cli": False,
            "gui": False,
            "tests": True,
            "executable": False,
            "pypi_packaging": False,
            "dev_requirements": False,
            "license": False,
            "readme": False,
            "makefile": False,
            "gitignore": False,
            "github_actions": False,
        }
        
        result = self.generator.generate_project(
            project_name=project_name,
            output_dir=self.temp_dir,
            features=features,
            metadata=metadata
        )
        
        assert result is True
        
        project_path = self.temp_dir / project_name
        tests_dir = project_path / "tests"
        
        # Check tests directory and files
        assert tests_dir.exists()
        assert (tests_dir / "__init__.py").exists()
        assert (tests_dir / "test_core.py").exists()
        
        # Check test content
        test_content = (tests_dir / "test_core.py").read_text()
        assert "pytest" in test_content
        assert "TestProjectApp" in test_content
    
    def test_generate_project_with_license(self):
        """Test generating a project with license."""
        project_name = "licensed_project"
        metadata = {
            "description": "A licensed project",
            "author": "Test Author",
            "email": "test@example.com",
            "license_type": "MIT"
        }
        features = {
            "cli": False,
            "gui": False,
            "tests": False,
            "executable": False,
            "pypi_packaging": False,
            "dev_requirements": False,
            "license": True,
            "readme": False,
            "makefile": False,
            "gitignore": False,
            "github_actions": False,
        }
        
        result = self.generator.generate_project(
            project_name=project_name,
            output_dir=self.temp_dir,
            features=features,
            metadata=metadata
        )
        
        assert result is True
        
        project_path = self.temp_dir / project_name
        license_file = project_path / "LICENSE"
        
        # Check license file exists and contains expected content
        assert license_file.exists()
        license_content = license_file.read_text()
        assert "MIT License" in license_content
        assert "Test Author" in license_content
        assert "2024" in license_content  # Current year
    
    def test_generate_project_with_readme(self):
        """Test generating a project with README."""
        project_name = "documented_project"
        metadata = {
            "description": "A well-documented project",
            "author": "Test Author",
            "email": "test@example.com",
            "url": "https://github.com/test/project"
        }
        features = {
            "cli": True,
            "gui": True,
            "tests": True,
            "executable": False,
            "pypi_packaging": False,
            "dev_requirements": False,
            "license": False,
            "readme": True,
            "makefile": False,
            "gitignore": False,
            "github_actions": False,
        }
        
        result = self.generator.generate_project(
            project_name=project_name,
            output_dir=self.temp_dir,
            features=features,
            metadata=metadata
        )
        
        assert result is True
        
        project_path = self.temp_dir / project_name
        readme_file = project_path / "README.md"
        
        # Check README file exists and contains expected content
        assert readme_file.exists()
        readme_content = readme_file.read_text()
        assert "documented_project" in readme_content
        assert "A well-documented project" in readme_content
        assert "Command Line Interface" in readme_content
        assert "Graphical User Interface" in readme_content
        assert "Testing" in readme_content
    
    def test_generate_project_invalid_output_dir(self):
        """Test error handling for invalid output directory."""
        with patch.object(self.generator, 'logger') as mock_logger:
            result = self.generator.generate_project(
                project_name="test",
                output_dir=Path("/nonexistent/path"),
                features={},
                metadata={}
            )
            
            assert result is False
            mock_logger.error.assert_called()


@pytest.fixture
def sample_generator():
    """Fixture providing a sample ProjectGenerator instance."""
    return ProjectGenerator()


def test_generator_creation(sample_generator):
    """Test that generator can be created successfully."""
    assert sample_generator is not None
    assert hasattr(sample_generator, 'generate_project') 