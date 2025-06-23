"""
Setup script for CourtListener SDK.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="courtlistener-sdk",
    version="0.1.0",
    author="CourtListener SDK Team",
    author_email="support@courtlistener.com",
    description="A comprehensive Python SDK for the CourtListener REST API",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/actuallyrizzn/courtlistener-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Legal",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "isort>=5.0.0",
        ],
    },
    keywords="legal, court, api, sdk, courtlistener, case law, dockets, judges",
    project_urls={
        "Bug Reports": "https://github.com/actuallyrizzn/courtlistener-sdk/issues",
        "Source": "https://github.com/actuallyrizzn/courtlistener-sdk",
        "Documentation": "https://github.com/actuallyrizzn/courtlistener-sdk/docs",
    },
) 