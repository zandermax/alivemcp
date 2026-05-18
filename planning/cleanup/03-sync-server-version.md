# 1.3 Sync `server_version` with `pyproject.toml`

Plan
1. Replace hardcoded `server_version` in `mcp_server.py` with `importlib.metadata.version(__package__)` or read from `pyproject.toml` via `importlib.metadata`.
2. Add test ensuring value matches `pyproject.toml` on CI.

Verification
- `mcp_server.__version__` equals `pyproject.toml` version.

Commit message
- fix(mcp): derive server version from package metadata
