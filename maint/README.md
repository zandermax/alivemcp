Verify docs/wiki/tool pages

This `maint` tool verifies that every tool name listed in `ALiveMCP_Remote/tools/core/registry.py`
has a corresponding Markdown page under `docs/wiki/tools/*/*.md`, and that there are no stray
tool pages that are not present in the registry.

Usage

Run from the repository root:

```bash
python3 maint/verify_docs_tools.py
```

Exit codes

- `0` — OK: registry and docs match
- `1` — Mismatch found (missing or extra pages)
- `2` — Repo layout error (missing registry or docs folder)

CI / Agents

CI jobs and agents must run this verifier before merging documentation changes. The job should
fail if the script exits with non-zero. Keep `docs/wiki/tools` and `AVAILABLE_TOOLS` in sync.
