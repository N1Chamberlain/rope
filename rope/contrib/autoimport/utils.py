"""Utility functions for the autoimport code."""

import pathlib
import sys
import pytest

from unittest.mock import MagicMock
from rope.contrib.autoimport.utils import get_package_source
from rope.contrib.autoimport.defs import Source

def make_project(path: str):
    """Return a minimal mock Project whose .address is the given path."""
    project = MagicMock()
    project.address = path
    return project

class TestVenvInsideProject:
    """
    Packages found under <project>/.venv/.../site-packages/ must be
    classified as SITE_PACKAGE, not PROJECT.
    """
    def test_venv_site_packages_is_site_package(self, tmp_path):
        project = make_project(str(tmp_path))
        pkg_path = tmp_path / ".venv" / "lib" / "python3.11" / "site-packages" / "requests"
        pkg_path.mkdir(parents=True)
        result = get_package_source(pkg_path, project, "requests")
        assert result == Source.SITE_PACKAGE, (
            f"Expected SITE_PACKAGE for a .venv package, got {result}. "
        )

    def test_venv_named_env_site_packages_is_site_package(self, tmp_path):
        """Works for venvs not named .venv (e.g. 'env', 'venv')."""
        project = make_project(str(tmp_path))
        pkg_path = tmp_path / "env" / "lib" / "python3.11" / "site-packages" / "flask"
        pkg_path.mkdir(parents=True)
        result = get_package_source(pkg_path, project, "flask")
        assert result == Source.SITE_PACKAGE

    def test_venv_nested_package_is_site_package(self, tmp_path):
        """A sub-package inside a venv dependency is also SITE_PACKAGE."""
        project = make_project(str(tmp_path))
        pkg_path = tmp_path / ".venv" / "lib" / "python3.11" / "site-packages" / "urllib3" / "util"
        pkg_path.mkdir(parents=True)
        result = get_package_source(pkg_path, project, "util")
        assert result == Source.SITE_PACKAGE

class TestNoRegression:
    """
    Make sure the fix does not break classification of real project files
    or external site-packages.
    """
    def test_project_source_file_is_project(self, tmp_path):
        """A module that lives directly in the project (not in site-packages) is PROJECT."""
        project = make_project(str(tmp_path))
        pkg_path = tmp_path / "myapp" / "models"
        pkg_path.mkdir(parents=True)
        result = get_package_source(pkg_path, project, "models")
        assert result == Source.PROJECT

    def test_external_site_packages_is_site_package(self):
        """Packages in a venv outside the project are still SITE_PACKAGE."""
        project = make_project("/home/user/myproject")
        pkg_path = pathlib.Path("/home/user/.virtualenvs/global/lib/python3.11/site-packages/numpy")
        result = get_package_source(pkg_path, project, "numpy")
        assert result == Source.SITE_PACKAGE

    def test_builtin_module_is_builtin(self, tmp_path):
        """Built-in modules (e.g. sys, os) are always BUILTIN regardless of path."""
        project = make_project(str(tmp_path))
        builtin_name = sys.builtin_module_names[0]
        pkg_path = tmp_path / builtin_name
        result = get_package_source(pkg_path, project, builtin_name)
        assert result == Source.BUILTIN

    def test_no_project_context_site_packages_is_site_package(self):
        """Passing project=None still correctly identifies site-packages."""
        pkg_path = pathlib.Path("/usr/local/lib/python3.11/site-packages/flask")
        result = get_package_source(pkg_path, None, "flask")
        assert result == Source.SITE_PACKAGE
