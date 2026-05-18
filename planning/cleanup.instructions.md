# ALiveMCP Cleanup Meta-Plan

This document catalogues known technical debt and structural issues for planning purposes.
Items are grouped by priority tier. Address code debt before reorganization.

## Policy — redundant generated artifacts

When something **could be generated from a canonical source** or is a **duplicate** of that source, **remove it** from the repository rather than keeping a second committed copy.

After removal, **refactor all references**: links in READMEs, imports in tests/scripts, Makefile targets, agent docs, and any prose that pointed at the old path must target the **single source of truth** (e.g. wiki pages, `registry.py`, `mcp_tool_defs/`, or code under `ALiveMCP_Remote/tools/`).

**Do not** replace one stale generated file with another long-lived duplicate layer. Prefer deletion + refactors; use one-off build output only in scratch directories or release packaging if truly needed, not as a permanently tracked twin.

---


## Priority 1 — Critical / Correctness

### 1.1 `make check-length` does not actually check any files

`scripts/check_file_length.py` reads `sys.argv[1:]` for paths. The `Makefile` `check-length` target calls the script with **no arguments**, so it always exits 0 and validates nothing.

**Fix:** Update the `check-length` Makefile target to pass tracked Python files:

```makefile
check-length:
	git ls-files '*.py' | xargs python scripts/check_file_length.py
```

### 1.2 `TOOL_DEFS` load failure is silent

In `mcp_server_tool_defs.py`, if `mcp_tool_defs/index.json` or any part file is missing or corrupt, the bare `except Exception` sets `TOOL_DEFS = []`. The MCP server then starts with zero tools and no error message. This is a silent operational failure.

**Fix:** Re-raise or log a loud startup error when `TOOL_DEFS` is empty due to load failure. Consider failing at import time.

### 1.3 `server_version` hardcoded separately from `pyproject.toml`

`mcp_server.py` hardcodes `server_version="2.0.0"` independently of `pyproject.toml version = "2.0.0"`. These can drift.

**Fix:** Read version from `importlib.metadata` or a shared constants module rather than duplicating the string.

---

## Priority 2 — Documentation Accuracy

### 2.1 `API_REFERENCE.md` missing 10 tool entries

`registry.py` has 230 tools. `docs/API_REFERENCE.md` has headings for only 220. The 10 missing entries:

- `get_master_chain_summary`
- `get_master_device_param_info`
- `get_master_device_params`
- `get_track_chain_summary`
- `get_track_device_params`
- `get_track_index_by_name`
- `set_master_device_param`
- `set_master_device_param_by_name`
- `set_track_device_param`
- `set_track_device_param_by_name`

Note: `maint/verify_docs_tools.py` (checks `docs/wiki/tools/`) exits 0 — wiki pages are in sync. Only the monolithic `API_REFERENCE.md` is stale.

**Fix:** **Delete** `docs/API_REFERENCE.md` per the policy above; point humans and links to `docs/wiki/INDEX.md` and `docs/wiki/tools/`. Refactor any external or in-repo references (README, CONTRIBUTING, deep links) to the wiki paths. Do not replace it with another committed generated monolith unless a consumer absolutely cannot use the wiki — then generate **only** at release into a non-tracked artifact, not as a permanent second doc.

*(Historical note: ten tools were missing from the monolith vs registry; wiki is already complete — removing the monolith resolves the drift.)*

### 2.2 Public tool-count inconsistency

Three sources disagree on the number of tools:

| Source                                                            | Count   |
| ----------------------------------------------------------------- | ------- |
| `registry.py` / `tool_manifest.json` / `mcp_tool_defs/index.json` | **230** |
| `README.md` (lines 3, 31)                                         | **232** |
| `pyproject.toml` description                                      | **220** |
| `CLAUDE.md`                                                       | **232** |

**Fix:** Align prose to the real count (230). Prefer **no hardcoded number**: derive for display from `mcp_tool_defs/index.json` `count` or `len(AVAILABLE_TOOLS)` in any script or doc that needs it, so the string cannot drift.

### 2.3 `liveapi_tools.py` class docstring incomplete

The class docstring does not mention `DevicesUIMixin`, `ClipsColorMixin`, or `ClipsFollowActionsMixin`, all of which are in the actual MRO.

**Fix:** Add the missing mixin names to the class docstring.

---

## Priority 3 — Test Quality

### 3.1 `test_live_api_tools.py` mixin list is stale

The test that checks `isinstance` against mixins does not include:

- `DevicesUIMixin`
- `TracksDevicesMixin`
- `MixingMasterDevicesMixin`
- `ClipsColorMixin`
- `ClipsFollowActionsMixin`

New mixins added to `liveapi_tools.py` will not be covered by the guard.

**Fix:** Derive the expected mixin list programmatically from `liveapi_tools.LiveAPITools.__mro__` rather than maintaining a hardcoded list.

### 3.2 No coverage for `mcp_server.py` / `ableton_client.py`

`pyproject.toml` pytest config uses `--cov=ALiveMCP_Remote`, which excludes the MCP host layer. Failures in `mcp_server.py` (wrong tool def loading, bad serialization, version mismatches) are not caught by tests.

**Fix:** Add `--cov-append` or expand coverage source to include `mcp_server` and `ableton_client` modules. Add at least smoke tests for `list_tools` and `call_tool` handlers.

### 3.3 Docstring TODO stubs not systematically tracked

Many tool methods have machine-generated docstubs with `TODO: describe parameters. / Returns / Raises` sections. `make validate-docstrings` exists but is not verified to fail on these stubs.

**Fix:** Check whether `validate-docstrings` rejects TODO stubs; if not, tighten the checker or Makefile target so unfilled stubs fail `make validate-docstrings`.

---

## Priority 4 — Code Quality / Consistency

### 4.1 Two error shapes from dispatch layer

Tools return `{"ok": False, "error": str(e)}`. The top-level dispatcher (`_process_command`) returns `{"ok": False, "error": ..., "traceback": traceback.format_exc()}` — a different shape with an extra field that may leak implementation details to clients.

**Fix:** Define a single canonical error response shape. If traceback is included, document it as an intentional debug field and gate it behind a debug flag.

### 4.2 No centralized result builder

`{"ok": True, ...}` / `{"ok": False, "error": str(e)}` is duplicated in every tool method. There is no shared helper, so any schema change requires touching all 230 tools.

**Fix:** Add `ok_result(**fields)` and `err_result(e)` helpers to `BaseMixin` or a shared utility, then migrate incrementally.

### 4.3 `ruff` target-version mismatch

`pyproject.toml` sets `[tool.ruff] target-version = "py37"` but `requires-python = ">=3.10"`. The ruff target is below the actual runtime requirement.

**Fix:** Align `target-version = "py310"` to match `requires-python`.

### 4.4 `requirements-dev.txt` has no version pins

`pytest`, `pytest-cov`, `ruff` are listed without version pins. Builds are not reproducible without a lockfile.

**Fix:** Pin versions in `requirements-dev.txt` (or switch to a lockfile approach via `pip-compile` / `uv lock`).

### 4.5 Python 2-runtime / Python 3.6 split not documented at top level

`CLAUDE.md` notes Ableton bundles Python 3.6 for `ALiveMCP_Remote`, while the MCP server venv requires Python ≥3.10. This split is architecturally important but is only described deep in `CLAUDE.md`.

**Fix:** Add a prominent callout in `README.md` (or a new `docs/ARCHITECTURE.md` section) distinguishing the two runtimes: Remote Script (Python 3.6, no external deps, runs inside Live) vs MCP Server (Python 3.10+, `mcp` package, runs in venv).

---

## Priority 5 — Tooling / local validation gaps

### 5.1 `examples/mock_server.py` at 424 lines, explicitly excluded

The pre-commit hook excludes `examples/` from the 300-line check. `mock_server.py` is 424 lines and growing. While the exclusion is intentional, the file should either be split or a comment explaining the exemption should be added.

**Fix:** Either split `examples/mock_server.py` into smaller modules, or add an explicit inline note explaining why it is exempt.

### 5.2 `check-version-bump` only runs on pre-push

The version bump check is a pre-push hook. It can be skipped with `--no-verify`. No remote automation — rely on habit, `make all` before release, or strengthen local hooks if needed.

### 5.3 Make validation the single local gate

`make all` chains `generate-from-wiki`, `generate-manifest`, `validate-manifest`, `validate-wiki`, `validate-docstrings`, `check-length`, etc. That is the intended pre-merge checklist — not GitHub Actions.

**Fix:** Document in `README.md` / `CONTRIBUTING.md` that contributors run `make all` (or the subset they touch). Optionally fold extra checks into `Makefile` (see §6.7) so one command covers everything.

### 5.4 Remove GitHub Actions (if rejecting CI)

The repo currently ships **one workflow**: `.github/workflows/check-wiki-parity.yml` (wiki parity + docstring checks). If the project standard is **no CI**, delete that file and scrub docs that mention it (`GITHUB_SETUP.md`, `CONTRIBUTING.md`, or any prose that says “the workflow runs …”).

**Leave alone (not CI):** `.github/ISSUE_TEMPLATE/*`, `.github/PULL_REQUEST_TEMPLATE.md` — those are templates only; remove only if you want zero `.github/` footprint.

---

## Priority 6 — Documentation / Tool Surface Consolidation

This is a dedicated area of structural debt worth planning as a standalone pass. There are currently **7 overlapping surfaces** that describe available tools, several with diverging data. The goal is **one authoritative source per concern**; remove duplicate or regenerable files and point consumers at those sources (see **Policy — redundant generated artifacts** at the top of this document).

See also: `planning/wiki-as-source-of-truth.instructions.md` — an existing plan that defines the intended hierarchy. The items below reflect what remains unimplemented or misaligned with that plan.

### 6.1 Current surface inventory

| Surface | What it contains | How maintained | Primary consumer |
|---------|-----------------|----------------|-----------------|
| `registry.py` (`AVAILABLE_TOOLS`) | Names only | Hand-edited | Runtime dispatch |
| `mcp_tool_defs/part_*.json` | Name + description + JSON schema | Committed generated data | `mcp_server.py` (MCP protocol) |
| `docs/tool_manifest.json` | Name + schema + parity | Generated — **candidate to remove** if tests use registry + `mcp_tool_defs` (§6.5) | Agents / tests |
| `docs/wiki/tools/*.md` | Full narrative, params, examples, Live mapping | Hand-authored | Humans + `generate_from_wiki.py` |
| `docs/wiki/TOOLS_INDEX.md` | Flat name list (pending **delete** §6.4) | Redundant | Humans |
| `docs/wiki/INDEX.md` | Navigable hub, taxonomy, links | Mixed (partial generation) | Humans |
| `docs/API_REFERENCE.md` | Monolithic (pending **delete** §6.3) | Refactor links → wiki |

**The problem:** `API_REFERENCE.md` and `TOOLS_INDEX.md` are hand-maintained duplicates of information that exists in better form elsewhere. Two generator scripts (`generate_from_wiki.py --apply` and `generate_tool_manifest.py`) both write `docs/tool_manifest.json` with different schemas — the final output is order-dependent in `make all`. The tool count "232" appears in 7+ prose files but the actual count is 230.

### 6.2 Proposed source-of-truth hierarchy

Following the model in `wiki-as-source-of-truth.instructions.md`:

```
PRIMARY:    ALiveMCP_Remote/tools/ (implementations + docstrings)
            registry.py (AVAILABLE_TOOLS — authoritative name list)
            docs/wiki/tools/*.md (Live mapping frontmatter — human enrichment)

RUNTIME / MACHINE:  mcp_tool_defs/part_*.json + index.json  →  mcp_server_tool_defs.TOOL_DEFS
                    (single JSON pipeline; drop duplicate bundled outputs — e.g. omit committed
                     `full.json` if it is strictly derivable from parts + index)

AGENTS / TESTS:     Prefer reading registry + mcp_tool_defs in code; remove committed
                    `docs/tool_manifest.json` if parity tests can assert the same facts without it.

HUMAN DOCS:         docs/wiki/ only — no parallel monolithic API_REFERENCE in-repo.

VALIDATED:          registry == wiki == mcp_tool_defs  (pytest + `make all`; manifest optional if removed)
```

### 6.3 `docs/API_REFERENCE.md` — **remove** (preferred)

The monolith duplicates `docs/wiki/tools/`, lags by 10 tools, and still says "232 tools".

**Fix:** Delete `docs/API_REFERENCE.md`. Refactor every reference (README, CONTRIBUTING, `GITHUB_SETUP.md`, bookmarks, planning text in §6.9) to `docs/wiki/INDEX.md` and per-tool pages under `docs/wiki/tools/`. Do not keep a regenerated copy in git unless an external publication pipeline requires it — publish from wiki sources there instead. Wiki is the human source of truth; **no** parallel monolith in-repo.

---

### 6.4 `docs/wiki/TOOLS_INDEX.md` — **remove** (preferred)

Flat name list redundant with `registry.py` sectioning and `docs/wiki/INDEX.md`.

**Fix:** Delete the file. Update any links to it → `docs/wiki/INDEX.md` or the registry. Do not replace with a second auto-generated committed index unless navigation truly needs it; if it does, generate **only** in `make docs` output dir or fold headings into `INDEX.md` generation from one script.

---

### 6.5 `docs/tool_manifest.json` and script collision — collapse to one output or drop manifest

`generate_from_wiki.py --apply` and `generate_tool_manifest.py` both touch `docs/tool_manifest.json` with incompatible shapes; order in `make all` masks the bug.

**Fix (in order):**

1. **If parity tests can compare** `registry.py` + `mcp_tool_defs` **directly** — remove committed `docs/tool_manifest.json`, refactor `tests/test_tool_manifest_parity.py` (and related) to use those sources. Then delete `generate_tool_manifest.py` or narrow it to emit **non-tracked** build output only.
2. **If tests still need a merged view** — exactly **one** script writes `docs/tool_manifest.json`; remove the other script's write path entirely; intermediate wiki-only JSON should go to a **different temp/output filename** or only exist in memory during the pipeline.

Do not leave two generators fighting for one path.

### 6.6 `mcp_tool_defs` — one generator; drop redundant `full.json` if derivable

`scripts/generate_tool_defs_chunked.py` refreshes `mcp_tool_defs/part_*.json`, `index.json`, and `full.json`. It is **not wired into any Makefile target** and references the old `TOOL_DEFS_JSON` embedded blob. `generate_from_wiki.py --apply` may also write `full.json`.

**Fix:**

- Pick **one** owner for `mcp_tool_defs/`.
- If `full.json` is strictly derivable from `index.json` + `part_*.json`, **remove** it from version control and build it in Makefile/dev when needed — or keep only parts + index as authoritative and update any consumer that still reads `full.json`.
- Add `make generate-tool-defs` (or fold into `generate-from-wiki`) for the chosen path.
- Update `docs/IMPACT_MAP_TOOL_SURFACE.md` (still describes embedded `TOOL_DEFS_JSON`).

### 6.7 Fold `maint/verify_docs_tools.py` + `validate-manifest` into the Makefile gate

`maint/verify_docs_tools.py` (registry ↔ wiki basename set) and **`make validate-manifest`** are easy to forget because they are not part of the same default chain as `validate-wiki`.

**Fix:** Call both from one documented path — e.g. extend `make validate-wiki` or `make all` to run `python3 maint/verify_docs_tools.py` after other checks, and document the combined command in `CONTRIBUTING.md`. No remote runners — local only.

If `.github/workflows/check-wiki-parity.yml` is deleted (§5.4), nothing replaces it automatically; the Makefile + docs become the contract.

### 6.8 Resolve duplicate wiki pages

`docs/wiki/tools/clips/get_clip_notes.md` and `docs/wiki/tools/midi/get_clip_notes.md` are duplicates (same for `remove_notes`). `maint/verify_docs_tools.py` uses basenames so only one "counts". The second page is redundant.

**Fix:** Pick the canonical domain location (likely `midi/` for note operations, `clips/` for clip-level ops — or whichever matches the registry organization). Delete the duplicate and add a redirect note or cross-link in the kept page.

### 6.9 Fix "232" count in prose across all docs

The following files still say "232 tools" or "220 tools" when the actual count is 230:

- `README.md`
- `CLAUDE.md`
- `docs/API_REFERENCE.md`
- `docs/INSTALLATION.md`
- `CONTRIBUTING.md`
- `docs/ARCHITECTURE.md`
- `GITHUB_SETUP.md`
- `pyproject.toml` description field

**Fix:** Do a single pass: remove hardcoded counts from prose where possible; where a sentence must cite a number, derive it from `mcp_tool_defs/index.json` or registry in the generator script that emits that doc — **or** after deleting `docs/API_REFERENCE.md`, drop that file from this list.

---

## Priority 7 — Reorganization (after Priorities 1–6 are stable)

### 7.1 Result helper refactor scope

If §4.2 result builders are adopted, a systematic migration across all 230 tool methods is a large but mechanical refactor. Plan as a standalone pass after helpers are settled.

### 7.2 Feature-gate audit for Live 12

Take Lanes and other Live 12 features are guarded inline across multiple files. A dedicated audit to catalog all version gates (and remove deprecated Live 11 fallbacks if support is dropped) would reduce ongoing maintenance cost.

---

## Reference — Key Files

| File                                 | Why relevant                                                     |
| ------------------------------------ | ---------------------------------------------------------------- |
| `Makefile`                           | Broken `check-length` target (§1.1)                              |
| `mcp_server_tool_defs.py`            | Silent TOOL_DEFS failure (§1.2)                                  |
| `mcp_server.py`                      | Hardcoded version (§1.3), no test coverage (§3.2)                |
| `docs/API_REFERENCE.md`              | Remove §6.3; was missing 10 tools §2.1                           |
| `README.md`                          | Tool count drift (§2.2)                                          |
| `pyproject.toml`                     | Count in description (§2.2), ruff target (§4.3), dep pins (§4.4) |
| `ALiveMCP_Remote/liveapi_tools.py`   | Stale class docstring (§2.3)                                     |
| `tests/test_live_api_tools.py`       | Stale mixin list (§3.1)                                          |
| `ALiveMCP_Remote/__init__.py`        | Error shape / dispatch (§4.1)                                    |
| `ALiveMCP_Remote/tools/core/base.py` | Candidate for result helpers (§4.2)                              |
| `examples/mock_server.py`            | 424 lines, hook-excluded (§5.1)                                  |
| `docs/wiki/TOOLS_INDEX.md`           | Remove §6.4                                                      |
| `docs/tool_manifest.json`            | Collapse or remove §6.5                                          |
| `scripts/generate_tool_defs_chunked.py` | Not in Makefile, stale TOOL_DEFS_JSON refs (§6.6)             |
| `docs/wiki/tools/clips/get_clip_notes.md` | Duplicate wiki page (§6.8)                                |
| `docs/wiki/tools/midi/remove_notes.md` | Duplicate wiki page (§6.8)                                   |
| `docs/IMPACT_MAP_TOOL_SURFACE.md`    | Stale TOOL_DEFS_JSON rollback story (§6.6)                       |
| `.github/workflows/check-wiki-parity.yml` | Remove if no CI; scrub docs (§5.4); fold checks into Makefile (§6.7) |
