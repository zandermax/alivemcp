"""Step 3 — Configure git to use the .githooks directory."""

import os
import subprocess

from installer._ui import REPO_ROOT, confirm, err, header, info, ok, run_cmd, warn


def step_git_hooks():
    header("Step 3 of 4 — Git Hooks (Development)")
    info("Configures git to run checks automatically:")
    info("  pre-commit  —  ruff lint + format check + 300-line file length limit")
    info("  pre-push    —  full pytest suite + version bump check\n")

    hooks_dir = os.path.join(REPO_ROOT, ".githooks")
    if not os.path.isdir(hooks_dir):
        err(f".githooks/ directory not found at {hooks_dir}")
        return

    hooks = sorted(f for f in os.listdir(hooks_dir) if not f.endswith(".sample"))
    info(f"Hooks present: {', '.join(hooks)}")

    result = subprocess.run(
        ["git", "-C", REPO_ROOT, "config", "core.hooksPath"],
        capture_output=True,
        text=True,
    )
    current = result.stdout.strip()
    if current == ".githooks":
        ok("git hooks are already configured correctly.")
        if not confirm("Re-apply anyway?", default=False):
            return
    elif current:
        warn(f"core.hooksPath is currently set to: {current}")

    print()
    info("About to run:")
    info("    git config core.hooksPath .githooks")
    if not confirm("Proceed?", default=True):
        info("Skipped.")
        return

    res = run_cmd(["git", "-C", REPO_ROOT, "config", "core.hooksPath", ".githooks"])
    if res.returncode == 0:
        ok("Git hooks configured.")
    else:
        err("Failed to configure git hooks.")
