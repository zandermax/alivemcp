#!/usr/bin/env python3
"""Generate a minimal API reference `docs/API_REFERENCE.md`.

This generator creates a short, auto-generated landing page that points
users to the canonical per-tool wiki pages and the generated tool
manifest. Keeping this short avoids duplicating large per-tool
documentation while still providing a single entrypoint.

Usage:
  python3 scripts/generate_api_reference.py [--output PATH] [--check]

Options:
  --output PATH   Write output to PATH (default: docs/API_REFERENCE.md)
  --check         Compare generated output with committed file and exit
                  non-zero if they differ.
"""

import argparse
import os
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DEFAULT_OUT = BASE / "docs" / "API_REFERENCE.md"
MANIFEST = BASE / "docs" / "tool_manifest.json"


def build_md():
    # Return the exact minimal landing page content used in the repo so
    # the generator is deterministic and matches the committed file.
    return """<!-- AUTO-GENERATED. Do not edit by hand. -->

# API Reference

This file is auto-generated. For detailed, per-tool documentation, see the `docs/wiki/tools/` pages.

- Per-tool docs: docs/wiki/tools/
- Machine manifest: docs/tool_manifest.json

If you need a compact machine-readable listing, use `docs/tool_manifest.json` or the
`mcp_tool_defs/` parts (loaded at runtime by `mcp_server_tool_defs.py`).

To regenerate this file locally:

```bash
python3 scripts/generate_tool_manifest.py
python3 scripts/generate_api_reference.py
```
"""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", "-o", help="Write output to path", default=str(DEFAULT_OUT))
    p.add_argument(
        "--check",
        action="store_true",
        help="Compare generated vs committed file and exit non-zero if different",
    )
    args = p.parse_args()
    md = build_md()
    out_path = Path(args.output)

    if args.check:
        if not out_path.exists():
            print(f"Expected {out_path} to exist for --check", file=sys.stderr)
            sys.exit(2)
        old = out_path.read_text(encoding="utf-8")
        if old == md:
            print("API reference up-to-date")
            return 0
        else:
            print("API reference is out of date. Generated output differs from committed file.")
            sys.exit(1)

    os.makedirs(out_path.parent, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    sys.exit(main() or 0)
