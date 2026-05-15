#!/usr/bin/env python3
"""Docstring checker wrapper that delegates helpers to `scripts.docstring_lib`.

Usage: python3 scripts/docstring_checker.py --check
"""

import argparse
import os
import sys
from pathlib import Path

# Ensure the repo root is on sys.path so `scripts.*` imports work when
# invoking this script directly (not as a package).
repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root))


def _import_docstring_libs():
    # Import package-specific helpers here after ensuring repo root is
    # on sys.path. This avoids ruff's E402 (module level import not at
    # top of file) while still allowing direct script execution.
    from scripts.docstring_lib import (
        check_docstring_structure,
        collect_docstrings,
        fix_missing_sections,
        fix_missing_see_also,
        load_available_tools,
    )

    return (
        check_docstring_structure,
        collect_docstrings,
        fix_missing_sections,
        fix_missing_see_also,
        load_available_tools,
    )


def main(args):
    # Import package-specific helpers lazily to keep module-level imports
    # at the top and satisfy linters (E402).
    (
        check_docstring_structure,
        collect_docstrings,
        fix_missing_sections,
        fix_missing_see_also,
        load_available_tools,
    ) = _import_docstring_libs()

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    registry_path = os.path.join(repo_root, "ALiveMCP_Remote", "tools", "core", "registry.py")
    tools_root = os.path.join(repo_root, "ALiveMCP_Remote", "tools")

    available = load_available_tools(registry_path)
    ds, files_by_symbol = collect_docstrings(tools_root)

    problems = {}
    missing_see_also = []
    for t in available:
        doc = ds.get(t)
        errs = check_docstring_structure(t, doc)
        if errs:
            problems[t] = errs
            if "See Also missing wiki path" in errs:
                missing_see_also.append(t)

    if args.fix and missing_see_also:
        fix_missing_see_also(missing_see_also, files_by_symbol)

    if args.insert_stubs:
        missing_sections = {
            name: [e for e in errs if e in ("missing Args:", "missing Returns:", "missing Raises:")]
            for name, errs in problems.items()
        }
        missing_sections = {k: v for k, v in missing_sections.items() if v}
        if missing_sections:
            fix_missing_sections(missing_sections, files_by_symbol)

    if problems:
        print("Docstring validation issues for exported tools:")
        for name, errs in sorted(problems.items()):
            print(f"- {name}: {', '.join(errs)}")
            fp = files_by_symbol.get(name)
            if fp:
                print(f"  file: {fp}")
        if args.fix:
            print("\nApplied fixes for See Also where possible. Review backups (*.bak).")
            return 2 if problems and not missing_see_also else 0
        return 2
    print("Docstring validation passed for exported tools.")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", default=True)
    parser.add_argument(
        "--fix", action="store_true", default=False, help="Apply minimal See Also docstring fixes"
    )
    parser.add_argument(
        "--insert-stubs",
        action="store_true",
        default=False,
        help="Insert TODO stubs for missing Args/Returns/Raises",
    )
    args = parser.parse_args()
    rc = main(args)
    raise SystemExit(rc)
