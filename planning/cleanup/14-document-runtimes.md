# 4.5 Document runtime split (Remote Script vs MCP Server)

Plan
1. Add short callout in top-level README or `docs/ARCHITECTURE.md` explaining:
   - Remote Script: Ableton-bundled Python 3.6, no external deps.
   - MCP Server: venv Python >=3.10, uses `mcp` package.

Verification
- README/called docs contain clear runtime guidance.

Commit message
- docs: document Remote Script vs MCP Server runtime differences
