# 6.5 Resolve `docs/tool_manifest.json` collision

Plan
1. Decide single generator ownership of `docs/tool_manifest.json` or remove it and use `registry.py` + `mcp_tool_defs` in tests.
2. Update `make all` to call only chosen generator.

Verification
- No generator overwrites the manifest in conflicting ways.

Commit message
- chore(docs): pick single generator for tool_manifest or remove manifest
