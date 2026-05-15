#!/usr/bin/env python3
"""Run parity and docstring validators and write a combined report.

This imports helper functions from `validate_wiki_parity.py` safely and
produces `scripts/validation_report.json` for inspection.
"""

import json
import os


def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    vp_path = os.path.join(repo_root, "scripts", "validate_wiki_parity.py")
    # Import by path
    import importlib.util

    spec = importlib.util.spec_from_file_location("validate_wiki_parity", vp_path)
    vp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vp)

    registry_path = os.path.join(repo_root, "ALiveMCP_Remote", "tools", "core", "registry.py")
    tools_root = os.path.join(repo_root, "ALiveMCP_Remote", "tools")
    wiki_root = os.path.join(repo_root, "docs", "wiki", "tools")

    available = vp.load_available_tools(registry_path)
    defined = vp.find_defined_symbols(tools_root)
    pages = vp.find_wiki_pages(wiki_root)
    docstrings = vp.find_docstrings(tools_root)

    missing_impl = sorted([t for t in available if t not in defined])
    missing_wiki = sorted([t for t in available if t not in pages])
    missing_docstrings = sorted([t for t in available if not docstrings.get(t)])
    missing_see_also = []
    for t in available:
        d = docstrings.get(t)
        if d:
            if "See Also" not in d or "docs/wiki/tools" not in d:
                missing_see_also.append(t)

    report = {
        "available_tools_count": len(available),
        "defined_symbols_count": len(defined),
        "wiki_pages_count": len(pages),
        "missing_impl": missing_impl,
        "missing_wiki": missing_wiki,
        "missing_docstrings": missing_docstrings,
        "missing_see_also": missing_see_also,
    }
    out = os.path.join(os.path.dirname(__file__), "validation_report.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print("Wrote", out)


if __name__ == "__main__":
    main()
