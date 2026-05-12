.PHONY: help install-dev lint lint-fix format format-check test test-cov check-length mock ui ci

VENV ?= .venv

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Setup"
	@echo "  install-dev     Install dev dependencies (pytest, ruff, etc.)"
	@echo ""
	@echo "Code quality"
	@echo "  lint            Run ruff linter"
	@echo "  lint-fix        Run ruff linter and auto-fix issues"
	@echo "  format          Format code with ruff"
	@echo "  format-check    Check formatting without writing files"
	@echo "  check-length    Check all .py files are <= 300 lines"
	@echo ""
	@echo "Tests"
	@echo "  test            Run pytest with coverage"
	@echo "  test-cov        Run pytest with per-file coverage breakdown"
	@echo ""
	@echo "Dev servers"
	@echo "  mock            Start mock Ableton server on port 9004"
	@echo "  ui              Start web dashboard on port 8080"
	@echo ""
	@echo "  ci              Run all checks (lint, format-check, test, check-length)"

install-dev:
	$(VENV)/bin/python -m pip install -r requirements-dev.txt

venv:
	python3 -m venv $(VENV)
	$(VENV)/bin/python -m pip install --upgrade pip setuptools wheel

lint:
	ruff check .

lint-fix:
	ruff check . --fix

format:
	ruff format .

format-check:
	ruff format --check .

test:
	pytest

test-cov:
	pytest --cov=ALiveMCP_Remote --cov-report=term-missing

validate-manifest:
	python3 scripts/generate_tool_manifest.py
	python3 scripts/validate_tool_manifest.py
	pytest -q tests/test_tool_manifest_parity.py

generate-manifest:
	python3 scripts/generate_tool_manifest.py

check-length:
	python scripts/check_file_length.py

mock:
	python3 examples/mock_server.py

ui:
	uvicorn examples.ui.server:app --port 8080

ci: install-dev lint format-check test check-length
