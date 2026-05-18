# 3.3 Enforce docstring TODO stubs failure

Plan
1. Tighten `scripts/docstring_checker.py` to fail if docstring contains TODO placeholders.
2. Add `make validate-docstrings` gating to `make all`.

Verification
- `make validate-docstrings` fails on TODO stubs.

Commit message
- test: enforce docstring completeness, fail on TODO stubs
