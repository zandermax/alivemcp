# Wiki as Source of Truth — Plan (recreated)

## Purpose

 Treat `docs/wiki/tools/` as the canonical documentation for MCP tools, but use the Python implementations in `ALiveMCP_Remote/tools/` as the actual source of truth for runtime behavior. The repository must enforce two-way parity between code and docs, with tooling that is code-first and wiki-aware:

- The primary authoritative input is the tool implementations and their docstrings under `ALiveMCP_Remote/tools/`.
- The wiki under `docs/wiki/tools/` is a derived documentation artifact; it provides human-friendly explanations and an explicit `Live mapping` field that should be consumed as a direct LOM signal when present.
- Every implemented MCP tool must have a matching wiki page, and each tool implementation should include a standardized docstring linking to its wiki page.

## Goals

- Prevent divergence between documentation and runtime tooling.
- Make the parity checks runnable locally (`make all`, `--check` modes that fail fast).
- Make migration and authoring low-friction (best-effort tools + human review).
- **Removal-first:** prefer deleting duplicate or regenerable docs/JSON in git and pointing consumers at the canonical tree (`docs/wiki/`, `registry.py`, `mcp_tool_defs/`) rather than committing another generated layer — see `planning/cleanup.instructions.md` policy block.

## Scope

- Inputs (code-first): `ALiveMCP_Remote/tools/**` (primary), `ALiveMCP_Remote/tools/core/registry.py` (authoritative list of exported names), `docs/wiki/tools/**/*.md` (secondary — source of `Live mapping` frontmatter), and `mcp_tool_defs/index.json` (existing exported defs).
- Outputs: `docs/tool_manifest.json`, generated `mcp_tool_defs/*` (full + chunked), optional `ALiveMCP_Remote/tools/core/registry_generated.py` (opt-in), and validator scripts/tests.

## Required files / scripts (deliverables)

- `scripts/generate_from_wiki.py` — code-first generator: extract exported tool names, docstrings, and explicit LOM/property accesses from `ALiveMCP_Remote/tools/`, merge with wiki frontmatter (use `Live mapping` when present as a direct mapping source), and emit JSON artifacts; supports `--check` (default) and `--apply` to write outputs. Do not auto-commit.
- `scripts/migrate_wiki_frontmatter.py` — best-effort backfill YAML frontmatter from page content.
- `scripts/validate_wiki_parity.py` — strict verifier that treats `ALiveMCP_Remote/tools/` as authoritative: registry ↔ implementations ↔ wiki parity (exit non-zero on mismatch); report JSON + human summary.
- `scripts/docstring_checker.py` — parse Python source under `ALiveMCP_Remote/tools/` and ensure each exported tool method has the required docstring structure and a `See Also` wiki link; provide `--fix` mode to insert TODO stubs (opt-in only).
- Updates to `docs/wiki/templates/tool.md` to require YAML frontmatter fields and to show the docstring `See Also` example.
- Makefile targets that run the above scripts in `--check` mode by default (pre-merge gate on the developer machine).

## Docstring standard (required for each tool method)

 Every tool implementation function or mixin method must include a docstring in this canonical format (example):

 ```python
 """Set a track's volume level.

     Args:
         track_id: Index of the target track.
         value: Volume level from 0.0 (silent) to 1.0 (unity gain).

     Returns:
         None

     Raises:
         IndexError: If track_id is out of range.

     See Also:
         Wiki: docs/wiki/tools/tracks/set_track_volume.md
     """
```

 Requirements:

- Use triple-quoted docstrings at the top of the function/method.
- Include `See Also` with the relative wiki path to the canonical page.
- Use `Args`, `Returns`, `Raises` sections as shown.

## Phases & Tasks

 Phase 0 — Inventory (quick)

 1. Run an inventory script to list and normalize:
    - All tools in `AVAILABLE_TOOLS` (derive tool count from `ALiveMCP_Remote/tools/core/registry.py` — do not hardcode a number).
    - All implemented tool methods and LOM/property accesses found by parsing `ALiveMCP_Remote/tools/**` (primary signal).
    - All pages under `docs/wiki/tools/` (normalized slugs) and any `Live mapping` frontmatter.
    - All runtime exported tools in `mcp_tool_defs/index.json`.

 Phase 1 — Authoring & Template
 2. Update `docs/wiki/templates/tool.md` to require the following YAML frontmatter fields: `name`, `domain`, `summary`, `schema`, `example_request`, `example_response`, plus metadata (`status`, `live_versions`, `owners`).
 3. Document the docstring standard in `CONTRIBUTING.md` and the template.

 Phase 2 — Migration tooling
 4. Implement `scripts/migrate_wiki_frontmatter.py` (dry-run / apply): extract Parameters and Examples and emit frontmatter candidates for review.

 Phase 3 — Generator implementation
 5. Implement `scripts/generate_from_wiki.py` (code-first generator):
    - Parse Python source under `ALiveMCP_Remote/tools/` to extract exported tool names, docstrings, and explicit LOM/property access traces (e.g., `self.song.tracks[i].mixer_device.volume.value`). Treat this as the primary, highest-fidelity LOM signal.
    - Parse `docs/wiki/tools/**/*.md` frontmatter; when a page contains an explicit `Live mapping` field, use that mapping directly (do not attempt to re-infer the same mapping via heuristics).
    - Combine code-derived traces and wiki `Live mapping` into a consolidated per-tool definition; flag conflicts and unknowns with confidence metadata.
    - Emit `docs/tool_manifest.json` (sorted by name) and `mcp_tool_defs/full.json`.
    - Chunk into `mcp_tool_defs/part_*.json` + `index.json` using existing chunking format.
    - Optionally generate `ALiveMCP_Remote/tools/core/registry_generated.py` (opt-in, reviewed commit required).
    - Default to `--check` (read-only); support `--apply` to write generated files. Never auto-commit or push changes.

 Phase 4 — Parity & docstring verification
 6. Implement `scripts/validate_wiki_parity.py`:
    - Treat `ALiveMCP_Remote/tools/` and `AVAILABLE_TOOLS` (registry) as the authoritative source of implemented tools; verify registry == implemented tool set.
    - Verify every implemented tool has a matching wiki page in `docs/wiki/tools/` (normalized).
    - Verify each implemented tool's docstring includes a `See Also` link to the canonical wiki page.
    - Flag mismatches, conflicting mappings, and missing `Live mapping` fields; produce a JSON report and human summary; exit non-zero on any errors.

 1. Implement `scripts/docstring_checker.py`:
    - Parse Python source under `ALiveMCP_Remote/tools/`.
    - For each exported tool method (by name), ensure docstring exists and matches the template (basic structural checks: has `Args:`, `Returns:`, `Raises:`, and `See Also` with the wiki path).
    - Provide `--fix` mode to insert a TODO docstring stub when safe (recommended only for small, non-destructive edits).

 Phase 5 — Tests, Makefile, local verification
 8. Add Makefile targets:
    - `generate-from-wiki` -> run `scripts/generate_from_wiki.py` (write outputs).
    - `validate-wiki` -> run `scripts/validate_wiki_parity.py`.
    - `validate-docstrings` -> run `scripts/docstring_checker.py`.
    - Chain these under `make all` together with `validate-manifest` so one command runs the full doc/registry gate.

 9. Do **not** rely on GitHub Actions for this repo; remove `.github/workflows/check-wiki-parity.yml` if present (see `planning/cleanup.instructions.md` §5.4). Prefer pre-push hooks or documented `make all` in `CONTRIBUTING.md`.

 Phase 6 — Rollout
 10. Run validator locally; fix mismatches; open a PR with frontmatter edits and generated artifacts. IMPORTANT: the tooling may write generated artifacts when run with `--apply`, but **commits must be made manually by maintainers** — do not auto-commit, stage, or push changes from these scripts or agents.

## Runbook — Developer commands

- Generate artifacts locally (dry-run):

 ```bash
 python3 scripts/generate_from_wiki.py --output-dir mcp_tool_defs --manifest docs/tool_manifest.json --check
 ```

- Apply and write generated artifacts (explicit):

 ```bash
 python3 scripts/generate_from_wiki.py --output-dir mcp_tool_defs --manifest docs/tool_manifest.json --apply
 ```

- Check mode (local pre-merge / pre-push):

 ```bash
 python3 scripts/generate_from_wiki.py --check
 python3 scripts/validate_wiki_parity.py
 python3 scripts/docstring_checker.py --check
 ```

## Success criteria

- Every `AVAILABLE_TOOLS` entry has a matching wiki page under `docs/wiki/tools/`.
- Every wiki page corresponds to an implemented tool exported in `mcp_tool_defs/index.json` or `ALiveMCP_Remote` code.
- All implemented tools contain the required docstring linking to their wiki page.
- `generate_from_wiki.py --check` and `validate_wiki_parity.py` are part of the local gate (`make all` / pytest) and fail on divergence.

## Notes & Risks

- Editor-provided YAML may be imperfect; migration will be best-effort and requires human review.
- Keep runtime Ableton remote script free of third-party deps — generator scripts may depend on `PyYAML`/dev-tools but generated files must be plain JSON/Python and committed.
- Optionally generating `registry_generated.py` must be a conscious, reviewed commit to avoid surprising runtime changes.

## Next immediate step

- Implement `scripts/validate_wiki_parity.py` and `scripts/docstring_checker.py` to get a fast, failing check that reports the current mismatches. Would you like me to scaffold those two scripts now?
