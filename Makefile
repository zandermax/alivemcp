.PHONY: help install-dev lint lint-fix format format-check test test-cov check-length mock ui

VENV ?= .venv
PYTHON ?= python3

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


install-dev: venv
	$(VENV)/bin/python -m pip install -r requirements-dev.txt

venv:
	python3 -m venv $(VENV)
	$(VENV)/bin/python -m pip install --upgrade pip setuptools wheel

lint:
	ruff check .

lint-md:
	@echo "Linting tracked Markdown files in alivemcp..."
	git ls-files -z '*.md' | xargs -0 npx --yes --prefix ../Music markdownlint-cli2 -c ./.markdownlint.json || true

lint-fix:
	ruff check . --fix

format:
	ruff format .

format-check:
	ruff format --check .

test:
	if [ -x "$(VENV)/bin/pytest" ]; then $(VENV)/bin/pytest; else pytest; fi

test-cov:
	if [ -x "$(VENV)/bin/pytest" ]; then $(VENV)/bin/pytest --cov=ALiveMCP_Remote --cov-report=term-missing; else pytest --cov=ALiveMCP_Remote --cov-report=term-missing; fi

validate-manifest:
	python3 scripts/generate_tool_manifest.py
	python3 scripts/validate_tool_manifest.py
	if [ -x "$(VENV)/bin/pytest" ]; then $(VENV)/bin/pytest -q tests/test_tool_manifest_parity.py; else pytest -q tests/test_tool_manifest_parity.py; fi

generate-manifest:
	python3 scripts/generate_tool_manifest.py

check-length:
	$(PYTHON) scripts/check_file_length.py

mock:
	python3 examples/mock_server.py

ui:
	uvicorn examples.ui.server:app --port 8080

all:
	$(MAKE) venv
	$(MAKE) install-dev
	$(MAKE) lint
	$(MAKE) lint-md
	$(MAKE) format-check
	$(MAKE) check-length
	$(MAKE) test
	$(MAKE) generate-from-wiki
	$(MAKE) generate-manifest
	$(MAKE) validate-manifest
	$(MAKE) validate-wiki
	$(MAKE) validate-docstrings

# Wiki parity targets
generate-from-wiki:
	python3 scripts/generate_from_wiki.py --apply --output-dir mcp_tool_defs --manifest docs/tool_manifest.json

validate-wiki:
	python3 scripts/generate_from_wiki.py --check
	python3 scripts/validate_wiki_parity.py --check
	python3 scripts/docstring_checker.py --check

validate-docstrings:
	python3 scripts/docstring_checker.py --check


docs-check:
	# Generate the canonical manifest, then ensure API reference matches it and wiki parity holds.
	python3 scripts/generate_tool_manifest.py
	python3 scripts/generate_api_reference.py --check
	python3 scripts/validate_wiki_parity.py --check
