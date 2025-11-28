SHELL := /bin/bash

PYTHON ?= python3
PHP ?= php
COMPOSER ?= composer

PYTHON_DIR := python
PHP_DIR := php
DOCS_DIR := docs
TOOLS_DIR := tools
DIST_DIR := dist

.DEFAULT_GOAL := help

.PHONY: help bootstrap lint test build docs release clean \
	python-lint python-test python-build python-docs python-release \
	php-lint php-test php-build php-docs php-release

help: ## Print available targets
	@printf "Available targets:\n"
	@grep -E '^[a-zA-Z0-9_.-]+:.*##' Makefile | awk 'BEGIN {FS=":.*##"} {printf "  %-18s %s\n", $$1, $$2}'

bootstrap: ## Install dev dependencies for both SDKs
	cd $(PYTHON_DIR) && $(PYTHON) -m pip install --upgrade pip
	cd $(PYTHON_DIR) && $(PYTHON) -m pip install -e ".[dev]"
	cd $(PHP_DIR) && $(COMPOSER) install

lint: python-lint php-lint ## Run all linters

python-lint: ## Run Python formatters and static analysis
	cd $(PYTHON_DIR) && $(PYTHON) -m black --check courtlistener tests
	cd $(PYTHON_DIR) && $(PYTHON) -m flake8 courtlistener tests
	cd $(PYTHON_DIR) && $(PYTHON) -m mypy courtlistener

php-lint: ## Run PHPStan analysis
	cd $(PHP_DIR) && $(COMPOSER) stan

test: python-test php-test ## Run the full test suites

python-test: ## Run Python tests
	cd $(PYTHON_DIR) && $(PYTHON) -m pytest

php-test: ## Run PHP tests
	cd $(PHP_DIR) && $(COMPOSER) test

build: python-build php-build ## Build distributable artifacts

python-build: ## Build Python packages (sdist/wheel)
	cd $(PYTHON_DIR) && $(PYTHON) -m build

php-build: ## Optimize Composer autoloader
	cd $(PHP_DIR) && $(COMPOSER) install
	cd $(PHP_DIR) && $(COMPOSER) dump-autoload -o

docs: python-docs php-docs ## Validate documentation links

python-docs: ## Validate docs referencing the Python SDK
	$(PYTHON) $(TOOLS_DIR)/check_docs.py $(DOCS_DIR) $(PYTHON_DIR)/README.md

php-docs: ## Validate docs referencing the PHP SDK
	$(PYTHON) $(TOOLS_DIR)/check_docs.py $(DOCS_DIR) $(PHP_DIR)/README.md

release: python-release php-release ## Run release preparation steps

python-release: python-build ## Validate Python artifacts with Twine
	cd $(PYTHON_DIR) && $(PYTHON) -m twine check dist/*

php-release: php-build ## Package PHP SDK as a zip archive
	cd $(PHP_DIR) && $(COMPOSER) validate --strict
	mkdir -p $(DIST_DIR)/php
	cd $(PHP_DIR) && $(COMPOSER) archive --format=zip --dir=../$(DIST_DIR)/php --file=courtlistener-php

clean: ## Remove build and cache artifacts
	rm -rf $(PYTHON_DIR)/.pytest_cache $(PYTHON_DIR)/.mypy_cache $(PYTHON_DIR)/build $(PYTHON_DIR)/dist
	rm -rf $(PHP_DIR)/vendor $(PHP_DIR)/.phpunit.result.cache $(DIST_DIR)
