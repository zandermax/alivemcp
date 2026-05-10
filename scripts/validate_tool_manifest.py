#!/usr/bin/env python3
import json
import os
import sys


def main():
    base = os.path.dirname(os.path.dirname(__file__))  # repo root
    manifest_path = os.path.join(base, "docs", "tool_manifest.json")
    if not os.path.exists(manifest_path):
        print(f"Missing manifest at {manifest_path}", file=sys.stderr)
        return 2
    try:
        with open(manifest_path, encoding="utf-8") as fh:
            m = json.load(fh)
    except Exception as e:
        print(f"Failed to parse tool_manifest.json: {e}", file=sys.stderr)
        return 2

    required = ["version", "generated_from", "tools"]
    missing = [k for k in required if k not in m]
    if missing:
        print("Missing keys in manifest: " + ", ".join(missing), file=sys.stderr)
        return 2

    gen_from = m.get("generated_from") or []
    missing_files = [p for p in gen_from if not os.path.exists(os.path.join(base, p))]
    if missing_files:
        print("Warning: generated_from files missing: " + ", ".join(missing_files), file=sys.stderr)

    tools = m.get("tools", [])
    if not isinstance(tools, list):
        print("Field `tools` must be an array", file=sys.stderr)
        return 2

    # Ensure tools are sorted deterministically by their `name` field
    if tools:
        names = [t.get("name", "") for t in tools]
        if names != sorted(names):
            print(
                "tools list is not sorted by `name`; sort for deterministic manifest",
                file=sys.stderr,
            )
            return 2

    if not tools:
        print("Warning: manifest.tools is empty; run generation in Phase 2", file=sys.stderr)

    print("tool_manifest.json validation OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
