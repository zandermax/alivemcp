# Wiki as Source of Truth — Instructions

## Purpose

Make `docs/wiki/tools/` the single canonical, machine-readable source for all tool documentation and use it to generate the repo's runtime artifacts (MCP defs, manifest, registry, API reference).

## Scope

- Authoritative source: `docs/wiki/tools/**/*.md` (one page per tool).
- Generated artifacts: `docs/tool_manifest.json`, `mcp_tool_defs/full.json`, `mcp_tool_defs/part_*.json`, `mcp_tool_defs/index.json`, and the `AVAILABLE_TOOLS` registry used by the code/tests.
- Tests, CI and contributor docs that validate and enforce the above.

## Deliverables

- `scripts/generate_from_wiki.py` — parse wiki pages and emit JSON artifacts.
- `scripts/migrate_wiki_frontmatter.py` — best-effort backfill YAML frontmatter into existing pages for review.
- Small updates to existing generators/tests to consume the wiki-backed manifest.
- Makefile/CI changes to run generator and fail on diffs.
- CONTRIBUTING/README guidance for authors.

## Success criteria

1. Running the generator produces identical output to committed artifacts (no diffs).
2. All `docs/wiki/tools/*` pages include validated YAML frontmatter with required fields: `name`, `domain`, `summary`, `schema` (JSON Schema), and canonical examples.
3. Tests/CI fail if generated artifacts diverge or a tool page is missing required metadata.

## Plan — Phases & Steps

Phase 1 — Authoring standardization

1. Update template: modify `docs/wiki/templates/tool.md` to include required YAML frontmatter schema and a minimal example frontmatter block.
2. Define required frontmatter fields and validation rules (document in this plan):
   - `name` (string)
   - `domain` (string)
   - `summary` (string)
   - `schema` (object, JSON Schema for parameters)
   - `example_request` (object)
   - `example_response` (object)

Phase 2 — Migration tooling

3. Implement `scripts/migrate_wiki_frontmatter.py`:
   - Parse existing pages, extract human-readable sections (Parameters, Example request/response) and emit best-effort YAML frontmatter.
   - Support `--dry-run` and `--apply` modes; always write changes to a branch or separate files for review.

Phase 3 — Generator implementation

4. Implement `scripts/generate_from_wiki.py` (core generator):
   - Walk `docs/wiki/tools/**.md`, parse YAML frontmatter (use `yaml.safe_load`) and validate required fields.
   - Build `docs/tool_manifest.json` (sorted by name) containing name, description, schema, and provenance.
   - Emit `mcp_tool_defs/full.json` and chunk into `part_*.json` + `index.json` (matching current chunking format).
   - Optionally produce a generated registry file `ALiveMCP_Remote/tools/core/registry_generated.py` (or update `registry.py` in a controlled way) containing `AVAILABLE_TOOLS` derived from wiki. Prefer a generated module to avoid manual edits.
   - Support `--check` mode that exits non-zero when generated output differs from repository files (for CI/pre-commit).

Phase 4 — Tests, CI, and repo hooks

5. Update tests to treat the wiki (or the generator output) as canonical:
   - `tests/test_tool_manifest_parity.py` and `tests/test_tool_metadata_parity.py` should derive expected items from `docs/tool_manifest.json` generated from the wiki.
   - Add a test that every `docs/wiki/tools/**.md` contains valid frontmatter and that `schema` is a JSON object.
6. Update `maint/verify_docs_tools.py` and `Makefile`:
   - `make validate-manifest` runs the generator in `--check` mode and fails on diffs.
   - Add `make generate-from-wiki` to produce artifacts locally.
7. Add a CI job to run the generator and fail if committed artifacts are out of date.

Phase 5 — Documentation and rollout

8. Update `CONTRIBUTING.md` and `README.md` with the authoring workflow:
   - Edit tool pages under `docs/wiki/tools/` using the template.
   - Run `make generate-from-wiki` locally and commit both the page and generated artifacts.
9. Migration PR & review:
   - Run the migration locally, open a PR that contains frontmatter edits and generated artifacts.
   - Ask reviewers to sanity-check frontmatter and examples; iterate until green.

## Runbook — Local commands

1. Generate artifacts locally:

```bash
python3 scripts/generate_from_wiki.py --output-dir mcp_tool_defs --manifest docs/tool_manifest.json
```

2. Check mode (CI/pre-commit):

```bash
python3 scripts/generate_from_wiki.py --check
```

## Notes & Risks

- Editor-provided YAML may be imperfect; migration will be best-effort and requires human review.
- Keep the runtime Ableton remote script free of third-party deps — the generator can depend on `PyYAML`/dev-tools but generated files must be plain JSON/Python and committed.

## Next immediate step

Implement `scripts/generate_from_wiki.py` (Phase 3, step 4). Once implemented, run it in `--check` mode in CI.
