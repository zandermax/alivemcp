# 6.6 `mcp_tool_defs` owner and `full.json`

Plan
1. Pick owner script for `mcp_tool_defs/` generation.
2. Remove `full.json` if derivable; keep parts + index as authoritative.

Verification
- Consumers updated to use parts+index.

Commit message
- chore(tool-defs): unify generator ownership for mcp_tool_defs
