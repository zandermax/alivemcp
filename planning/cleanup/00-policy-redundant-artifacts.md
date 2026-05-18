# Policy — redundant generated artifacts

Summary
- Remove committed artifacts that can be regenerated from canonical sources. Prefer deletion + refactor over adding another generated layer.

Plan
1. Inventory generated artifacts referenced in docs or code (example: `docs/tool_manifest.json`, `mcp_tool_defs/full.json`).
2. For each artifact: verify reproducibility from code/wiki/build step.
3. Remove artifact, update `.gitignore`, update docs/scripts to reference SoT.

Verification
- Run `make all` or targeted generator scripts to ensure outputs can be recreated.

Commit message
- chore: remove redundant generated artifact <path>
