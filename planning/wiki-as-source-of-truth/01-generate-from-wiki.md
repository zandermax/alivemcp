# 01 Implement `generate_from_wiki.py`

Plan
1. Implement `scripts/generate_from_wiki.py` to parse `ALiveMCP_Remote/tools/`, merge wiki frontmatter, and emit `mcp_tool_defs/` and `docs/tool_manifest.json` in `--apply` mode; default `--check`.
2. Keep generator idempotent and non-auto-committing.

Verification
- `--check` reports parity; `--apply` writes artifacts that can be regenerated.

Commit message
- feat(docs): add generate_from_wiki.py generator (check/apply)
