# Project Wiki: Plan & Instructions

This document is the working plan for creating a project wiki that is compatible with both Fossil and GitHub. It focuses first on documenting which tools do what actions in Ableton Live and linking to the relevant Ableton documentation.

## High-level goal

- Produce a simple, maintainable Markdown-based wiki under `docs/wiki/` that can be consumed on GitHub and exported/used with Fossil.

## Immediate deliverable

- An index of tools mapping each tool name to the Live action(s) it performs, plus links to Ableton docs.

## Recommended repository structure (first pass)

- `docs/wiki/INDEX.md` — top-level landing page and navigation
- `docs/wiki/tools/` — per-domain subfolders (arrangement, clips, midi, tracks, devices, etc.)
- `docs/wiki/tools/<domain>/<tool>.md` — individual tool pages
- `docs/wiki/templates/tool.md` — canonical page template
- `planning/wiki.instructions.md` — this file (plan and checklist)

## Per-tool page template (fields)

- **Tool name**: canonical action name exposed by the server
- **Domain**: which domain/mixin (e.g., `clips`, `tracks`)
- **Summary**: one-line description of what the tool does in Live
- **Parameters**: names, types, and short notes (aliases like `scene_index`)
- **Live mapping**: which Live API call/property/method this touches (main-thread only)
- **Example request**: newline-delimited JSON example
- **Example response**: typical success and failure responses
- **Ableton docs**: authoritative link(s) to Live API / manual pages
- **Notes**: caveats, threading constraints, version differences (Live 11 vs 12)
- **See also**: links to related tools (cross-reference other per-tool pages)

## Plan (steps to create docs structure first)

1. Inventory all tools — generate a list from `ALiveMCP_Remote/tools/core/registry.py`.
2. Map tools → Live actions — for each tool record the Live API mapping.
3. Collect Ableton links — find authoritative docs for each Live area.
4. Define wiki structure — create folders and index layouts under `docs/wiki/`.
5. Create page templates — add `templates/tool.md` and an index template. Ensure the template includes a **See also** section for related tools so every new page contains cross-references.
6. Generate tools index — produce `docs/wiki/INDEX.md` (machine or script-assisted).
7. Populate per-tool pages — create one page per tool using the template.
8. Add Fossil/GitHub notes — document how to view and publish on each VCS.
9. Review and QA — cross-check examples and links; run tests if present.
10. Commit and publish — commit docs, provide publish and export instructions.

## Draft content guidelines (short)

- Use plain Markdown; avoid GitHub-specific extensions that Fossil won't support.
- Keep per-tool pages small and focused (one responsibility per page).
- Prefer explicit stable links to Ableton documentation; annotate Live version when needed.
- Include parameter aliases (e.g., `scene_index` → `clip_index`) per public API.

## Fossil vs GitHub considerations

- Keep files in the repo (under `docs/wiki/`) so GitHub renders them directly.
- For Fossil, the same files can be served or imported; add a small `FOSSIL.md` with instructions if needed.
- Avoid reliance on GitHub wiki UI — prefer repo files so both systems share the same source.

## Next actions (short-term)

- Script the inventory and index generation (optional `scripts/generate_wiki_index.py`).
- Create templates and a first-pass `docs/wiki/INDEX.md` stub.
- Auto-generate per-tool pages for core domains (arrangement, clips, tracks) as examples.

- Add per-tool YAML frontmatter fields: `status`, `live_versions`, `owners`, `tags`, `last_updated`.
- Add `docs/wiki/CONTRIBUTING.md` describing how to regenerate docs and run `maint/verify_docs_tools.py`.
- Add a CI workflow that runs `maint/verify_docs_tools.py`, fails on docs/registry drift, and optionally regenerates stubs.
- Implement automated extraction of the **Live mapping** from `ALiveMCP_Remote/tools/` implementations and include it in generated pages.
- Add `FOSSIL.md` with Fossil-specific publish/import notes and any export tips.
- Run review & QA: cross-check examples, links, run tests (where present), and the docs verifier.
- Commit and publish — add publish/export instructions for maintainers.

---

Created as part of the project wiki planning. Update tasks in the TODO tracker (`manage_todo_list`) as work progresses.

## Gaps / Remaining work

The original plan is a solid baseline but the following items still need to be done to make the wiki maintainable and automatable:

- CI verification & enforcement: add a job that runs `python maint/verify_docs_tools.py` and fails builds on parity drift.
- Generator script: implement `scripts/generate_wiki_index.py` to read `ALiveMCP_Remote/tools/core/registry.py` and `mcp_tool_defs/index.json` and emit `docs/wiki/INDEX.md` plus per-tool stubs.
- Per-page metadata: add YAML frontmatter to every `docs/wiki/tools/...` page (see example below) so automation and search can rely on structured fields.
- Automated Live mapping extraction: synthesize the `Live mapping` field from the tool implementations to avoid manual errors.
- CONTRIBUTING and maintainer workflow: `docs/wiki/CONTRIBUTING.md` should document how to regenerate, verify, and submit docs changes.
- Fossil integration: add `FOSSIL.md` describing any Fossil-specific considerations and how to import/export the repo wiki.
- Decide CI behaviour: choose whether CI should auto-commit/regenerate stubs, open a PR, or simply fail and require a manual update.
- Provide one fully-populated example page (e.g., a `clips/create_midi_clip.md`) as a canonical example for contributors.

## Per-tool frontmatter example

Add a small YAML frontmatter block at the top of each generated page. Example:

---

status: draft
live_versions: [11, 12]
owners: ["maintainer-handle"]
tags: [clips, midi]
last_updated: 2026-05-14

---

Embedding these fields enables CI checks, search indexing, and simple filtering when generating indexes or site outputs.

---

Update tasks are tracked in the TODO tracker (`manage_todo_list`).
