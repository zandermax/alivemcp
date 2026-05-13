#!/usr/bin/env python3
"""Generate chunked MCP tool definition files from the embedded tool blob.

Usage: python3 scripts/generate_tool_defs_chunked.py [--chunk-size N] [--remove-alias]

This script reads `mcp_server_tool_defs.py`, extracts the `TOOL_DEFS_JSON`
string, parses it to a Python list, optionally removes a legacy alias, and
writes chunk files into `mcp_tool_defs/` plus an `index.json` and `full.json`.
"""

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "mcp_server_tool_defs.py"
OUT_DIR = ROOT / "mcp_tool_defs"

ALIAS_TO_REMOVE = None


def _extract_tool_defs_from_blob(text: str):
    m = re.search(r"TOOL_DEFS_JSON\s*=\s*r?([\'\"]{3})(.*?)\1", text, re.S)
    if not m:
        return None
    return m.group(2)


def get_tool_defs():
    """Return the tool defs as a Python list.

    Tries three strategies in order:
    1. Extract embedded `TOOL_DEFS_JSON` triple-quoted string (legacy).
    2. Import `mcp_server_tool_defs` and use the runtime `TOOL_DEFS` export.
    3. Fail with RuntimeError.
    """
    text = SRC.read_text(encoding="utf-8")
    blob = _extract_tool_defs_from_blob(text)
    if blob is not None:
        return json.loads(blob)

    # Fallback: import the module and read TOOL_DEFS runtime export
    try:
        import importlib.util

        spec = importlib.util.spec_from_file_location("mcp_server_tool_defs", str(SRC))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)  # type: ignore
        defs = list(getattr(mod, "TOOL_DEFS"))
        # Ensure JSON-serializable structure (lists)
        return [[n, d, s] for n, d, s in defs]
    except Exception:
        raise RuntimeError("Could not obtain tool defs from mcp_server_tool_defs.py")


def chunk_and_write(defs, chunk_size: int = 200):
    OUT_DIR.mkdir(exist_ok=True)
    parts = []
    for i in range(0, len(defs), chunk_size):
        part = defs[i : i + chunk_size]
        name = f"part_{i//chunk_size:03d}.json"
        p = OUT_DIR / name
        p.write_text(json.dumps(part, indent=2, ensure_ascii=False))
        parts.append(name)
    index = {"parts": parts, "count": len(defs)}
    (OUT_DIR / "index.json").write_text(json.dumps(index, indent=2, ensure_ascii=False))
    (OUT_DIR / "full.json").write_text(json.dumps(defs, indent=2, ensure_ascii=False))
    print(f"Wrote {len(parts)} parts ({len(defs)} tools) to {OUT_DIR}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--chunk-size", type=int, default=200)
    p.add_argument("--remove-alias", action="store_true", help="Remove legacy alias from defs")
    args = p.parse_args()

    defs = get_tool_defs()

    if args.remove_alias and ALIAS_TO_REMOVE:
        before = len(defs)
        defs = [d for d in defs if d and d[0] != ALIAS_TO_REMOVE]
        print(f"Removed alias '{ALIAS_TO_REMOVE}' if present. {before} -> {len(defs)}")

    # Deterministic ordering
    defs.sort(key=lambda x: x[0])

    chunk_and_write(defs, chunk_size=args.chunk_size)


if __name__ == "__main__":
    main()
