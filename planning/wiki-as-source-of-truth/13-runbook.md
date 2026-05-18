# Runbook — Developer commands

Commands

Generate artifacts (dry-run):

```bash
python3 scripts/generate_from_wiki.py --output-dir mcp_tool_defs --manifest docs/tool_manifest.json --check
```

Apply artifacts (explicit):

```bash
python3 scripts/generate_from_wiki.py --output-dir mcp_tool_defs --manifest docs/tool_manifest.json --apply
```

Check mode:

```bash
python3 scripts/generate_from_wiki.py --check
python3 scripts/validate_wiki_parity.py
python3 scripts/docstring_checker.py --check
```

Success criteria
- Registry, implementations, wiki parity validated by `validate_wiki_parity.py`.
