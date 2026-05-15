#!/usr/bin/env python3
"""Docstring checker wrapper that delegates helpers to `scripts.docstring_lib`.

Usage: python3 scripts/docstring_checker.py --check
"""

import argparse
import os

from scripts.docstring_lib import (
    check_docstring_structure,
    collect_docstrings,
    fix_missing_see_also,
    load_available_tools,
)


def main(args):
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
    args = parser.parse_args()
    rc = main(args)
    raise SystemExit(rc)
