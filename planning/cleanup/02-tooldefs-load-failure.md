# 1.2 Fail loudly when `TOOL_DEFS` load fails

Problem
- `mcp_server_tool_defs.py` silences load errors and sets `TOOL_DEFS = []`.

Plan
1. In `mcp_server_tool_defs.py`, catch exceptions but log error and raise SystemExit with message.
2. Add unit test that simulates missing/corrupt `mcp_tool_defs/index.json` and asserts process exit.

Verification
- Server fails fast on startup with clear error.

Commit message
- fix(mcp): surface error when TOOL_DEFS cannot be loaded
