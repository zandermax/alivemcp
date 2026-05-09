# Impact Map — Tool Surface (ALiveMCP)

## Overview

This document describes the risks, invariants, and validation needed when changing the set of tools exposed by ALiveMCP (tool names, parameters, schemas).

## Trigger Files

- `ALiveMCP_Remote/tools/core/registry.py` (primary source of tool names)
- `mcp_server_tool_defs.py` (MCP definitions used by `mcp_server.py`)
- `ALiveMCP_Remote/liveapi_tools.py` (composition and `get_available_tools()`)

## Invariants

- The set of tool names reported by `get_available_tools()` must match the MCP-definitions served by `mcp_server`.
- Backward-compatibility aliases (e.g. `scene_index` → `clip_index`) must remain unless explicitly deprecated.
- Tool schemas must validate against the serialized `TOOL_DEFS_JSON` used by MCP server.

## Required Validation Commands

- `pytest tests/test_live_api_tools.py -q` (live API tool composition)
- `pytest tests/test_mcp_server.py -q` (mcp tool list and call correctness)
- `flake8` / `ruff` style checks as configured in `pyproject.toml`

## Regression Signatures

- Tests asserting tool list equality fail.
- MCC server responses do not include expected `inputSchema` fields.

## Rollback Strategy

- Revert manifest/registry edits and regenerate `mcp_server_tool_defs.py` from the canonical manifest.
- Run parity tests before re-releasing.

## Where to Start

- Inspect `ALiveMCP_Remote/tools/core/registry.py` and `mcp_server_tool_defs.py` side-by-side.
- Use `tests/test_live_api_tools.py` to verify composition.
