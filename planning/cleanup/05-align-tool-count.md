# 2.2 Align public tool-count references

Plan
1. Remove hardcoded counts from prose (README, CLAUDE.md, pyproject description).
2. Where needed, derive count from `mcp_tool_defs/index.json` or `registry.py` in generator scripts.

Verification
- No mismatched counts remain across repo docs.

Commit message
- docs: remove hardcoded tool counts; derive from tool index
