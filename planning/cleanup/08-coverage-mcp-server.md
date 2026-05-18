# 3.2 Add coverage and smoke tests for MCP host layer

Plan
1. Expand pytest coverage settings to include `mcp_server` and `ableton_client` modules.
2. Add smoke tests for `list_tools` and `call_tool` handlers using mocked `ALiveMCP_Remote`.

Verification
- CI / local test run includes host layer coverage.

Commit message
- test: add smoke tests for mcp_server and include host layer in coverage
