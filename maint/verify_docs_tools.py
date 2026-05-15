#!/usr/bin/env python3
"""
Verify that docs/wiki tool pages match the AVAILABLE_TOOLS registry.

Exit code 0 on success (no missing/extra). Exit code 1 if mismatches found.
"""

import importlib.util
import os
import sys


def load_registry(path):
    spec = importlib.util.spec_from_file_location("registry", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "AVAILABLE_TOOLS", [])


def gather_md_files(docs_root):
    md_files = {}
    for root, _, files in os.walk(docs_root):
        for f in files:
            if f.endswith(".md"):
                name = os.path.splitext(f)[0]
                rel = os.path.relpath(os.path.join(root, f), docs_root)
                md_files.setdefault(name, []).append(rel)
    return md_files


def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    registry_path = os.path.join(repo_root, "ALiveMCP_Remote", "tools", "core", "registry.py")
    docs_root = os.path.join(repo_root, "docs", "wiki", "tools")

    if not os.path.exists(registry_path):
        print("Registry file not found:", registry_path, file=sys.stderr)
        return 2
    if not os.path.isdir(docs_root):
        print("Docs tools folder not found:", docs_root, file=sys.stderr)
        return 2

    tools = set(load_registry(registry_path))
    md_map = gather_md_files(docs_root)
    md_names = set(md_map.keys())

    missing = sorted([t for t in tools if t not in md_names])
    extra = sorted([m for m in md_names if m not in tools])

    ok = True
    if missing:
        ok = False
        print("Missing docs for tools (listed in registry but no .md):", file=sys.stderr)
        for m in missing:
            print("  -", m, file=sys.stderr)
    if extra:
        ok = False
        print("Extra doc pages (present in docs but not in registry):", file=sys.stderr)
        for e in extra:
            paths = md_map.get(e, [])
            for p in paths:
                print("  -", e, "->", p, file=sys.stderr)

    if ok:
        print(f"OK: docs/wiki/tools matches AVAILABLE_TOOLS ({len(tools)} tools)")
        return 0
    else:
        print(
            "\nRun this script again after adding/removing docs or updating the registry.",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
