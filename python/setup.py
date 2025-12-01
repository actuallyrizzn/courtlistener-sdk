"""
Setup script for CourtListener SDK (backward compatibility wrapper).

This file is kept for backward compatibility. The package now uses pyproject.toml
(PEP 517) as the primary configuration. Modern build tools will use pyproject.toml
directly, but this file ensures compatibility with older tools that expect setup.py.
"""

from setuptools import setup

# All configuration is now in pyproject.toml
# This file exists only for backward compatibility
setup() 