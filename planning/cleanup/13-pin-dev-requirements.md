# 4.4 Pin dev requirements

Plan
1. Add version pins to `requirements-dev.txt` for `pytest`, `pytest-cov`, `ruff`, etc.
2. Optionally add lockfile via `pip-compile`.

Verification
- Reproducible dev environment with pinned dev deps.

Commit message
- chore: pin development requirements for reproducible builds
