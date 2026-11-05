"""Compatibility shim.

All project metadata, dependencies and tool configuration live in
``pyproject.toml``. This file exists only so that older tooling which still
invokes ``setup.py`` continues to work.
"""

from setuptools import setup

setup()
