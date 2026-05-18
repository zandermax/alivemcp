# 4.3 Align `ruff` target-version

Plan
1. Update `pyproject.toml` `[tool.ruff] target-version` to `py310`.
2. Run `ruff` to validate no new offenses under new target.

Verification
- `ruff` target matches runtime `requires-python`.

Commit message
- chore: set ruff target-version to py310
