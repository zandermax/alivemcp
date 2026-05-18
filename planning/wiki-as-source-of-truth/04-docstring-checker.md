# 04 Implement `docstring_checker.py`

Plan
1. Implement `scripts/docstring_checker.py` to parse exported tool methods and ensure docstrings follow the template with `See Also` link.
2. Provide `--fix` mode to insert TODO stubs where safe.

Verification
- `docstring_checker.py --check` exits non-zero when docstrings missing or malformed.

Commit message
- feat(docs): add docstring checker for ALiveMCP tool methods
