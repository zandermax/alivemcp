"""Step 4 — Install dev dependencies (ruff, pytest, pytest-cov)."""

import shutil
import sys

from installer._ui import confirm, err, header, info, ok, run_cmd


def step_dev_deps():
    header("Step 4 of 4 — Developer Dependencies (Optional)")
    info("Installs ruff, pytest, and pytest-cov so you can run tests locally.")
    info("Skip this if you're only using ALiveMCP, not contributing to it.\n")

    if not confirm("Install dev dependencies?", default=True):
        info("Skipped.")
        return

    if shutil.which("uv"):
        cmd = ["uv", "pip", "install", "ruff", "pytest", "pytest-cov"]
    else:
        cmd = [sys.executable, "-m", "pip", "install", "ruff", "pytest", "pytest-cov"]

    info(f"About to run:\n    {' '.join(cmd)}")
    if not confirm("Proceed?", default=True):
        info("Skipped.")
        return

    res = run_cmd(cmd)
    if res.returncode == 0:
        ok("Dev dependencies installed.")
        info("Run tests with:    python -m pytest")
        info("Run linting with:  ruff check .")
    else:
        err("Installation failed — see output above.")
