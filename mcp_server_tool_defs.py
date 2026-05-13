"""Chunked MCP tool definitions loader.

This module loads tool definitions from `mcp_tool_defs/index.json` and the
referenced `part_*.json` files. It exports `TOOL_DEFS` as a list of
(name, description, schema) tuples for direct import by `mcp_server.py`.

The repository should commit `mcp_tool_defs/` (generator output). If the
parts are missing, `TOOL_DEFS` will be an empty list.
"""

import json
from pathlib import Path

_parts_dir = Path(__file__).parent / "mcp_tool_defs"
_index_path = _parts_dir / "index.json"

# Exported `TOOL_DEFS`: list of (name, description, schema) tuples.
TOOL_DEFS = []

if _index_path.exists():
    try:
        _idx = json.loads(_index_path.read_text(encoding="utf-8"))
        _all = []
        for part in _idx.get("parts", []):
            _p = _parts_dir / part
            if _p.exists():
                _all.extend(json.loads(_p.read_text(encoding="utf-8")))
        TOOL_DEFS = [(name, desc, schema) for name, desc, schema in _all]
    except Exception:
        TOOL_DEFS = []
else:
    TOOL_DEFS = []
