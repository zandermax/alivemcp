# 4.1 Canonical error shape for dispatch layer

Plan
1. Define a canonical error response shape in a shared module (e.g., `ALiveMCP_Remote/tools/core/result.py`).
2. Gate inclusion of traceback behind `MCP_DEBUG` env var.
3. Migrate dispatcher to use helper.

Verification
- API responses have consistent shape; debug traces only when enabled.

Commit message
- refactor: canonicalize tool error response shape and gate traceback
