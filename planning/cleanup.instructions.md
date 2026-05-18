# ALiveMCP Cleanup Meta-Plan

This document catalogues known technical debt and structural issues for planning purposes.
Items are grouped by priority tier. Address code debt before reorganization.

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

**Fix:** Add the 10 missing `### \`tool_name\``sections to`docs/API_REFERENCE.md`, or regenerate it from wiki sources.

### 2.2 Public tool-count inconsistency

Three sources disagree on the number of tools:

| Source                                                            | Count   |
| ----------------------------------------------------------------- | ------- |
| `registry.py` / `tool_manifest.json` / `mcp_tool_defs/index.json` | **230** |
| `README.md` (lines 3, 31)                                         | **232** |
| `pyproject.toml` description                                      | **220** |
| `CLAUDE.md`                                                       | **232** |

**Fix:** Align all user-facing documentation to 230 (the actual count). Update `README.md` and `pyproject.toml` description. Consider generating this number from the registry to prevent future drift.

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

**Fix:** Check whether `validate-docstrings` rejects TODO stubs; if not, update the checker or the CI target to block on unfilled stubs.

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

## Priority 5 — Tooling / CI Gaps

### 5.1 `examples/mock_server.py` at 424 lines, explicitly excluded

The pre-commit hook excludes `examples/` from the 300-line check. `mock_server.py` is 424 lines and growing. While the exclusion is intentional, the file should either be split or a comment explaining the exemption should be added.

**Fix:** Either split `examples/mock_server.py` into smaller modules, or add an explicit inline note explaining why it is exempt.

### 5.2 `check-version-bump` only runs on pre-push

The version bump check is a pre-push hook, not a CI step. It can be skipped silently with `--no-verify` or when pushing via tooling.

**Note:** Evaluate whether this check should also be a CI gate (Makefile `all:` target).

### 5.3 Makefile `all:` dependencies not verified in CI

`make all` chains validators (`validate-manifest`, `validate-wiki`, `validate-docstrings`, `check-length`). Confirm these are wired to whatever CI system is used; the repo has no `.github/workflows/` visible — document or add CI config.

---

## Priority 6 — Reorganization (after debt is addressed)

Reorganization should happen after Priorities 1–5 are stable.

### 6.1 `API_REFERENCE.md` vs wiki regeneration strategy

There are two documentation surfaces: the monolithic `docs/API_REFERENCE.md` and the `docs/wiki/tools/` per-tool pages. Keeping both in sync manually is fragile. Consider designating the wiki pages as the source of truth and generating `API_REFERENCE.md` from them automatically (a script already partially exists in `maint/`).

### 6.2 Result helper refactor scope

If §4.2 result builders are adopted, a systematic migration across all 230 tool methods is a large but mechanical refactor. Plan as a standalone pass after helpers are settled.

### 6.3 Feature-gate audit for Live 12

Take Lanes and other Live 12 features are guarded inline across multiple files. A dedicated audit to catalog all version gates (and remove deprecated Live 11 fallbacks if support is dropped) would reduce ongoing maintenance cost.

---

## Reference — Key Files

| File                                 | Why relevant                                                     |
| ------------------------------------ | ---------------------------------------------------------------- |
| `Makefile`                           | Broken `check-length` target (§1.1)                              |
| `mcp_server_tool_defs.py`            | Silent TOOL_DEFS failure (§1.2)                                  |
| `mcp_server.py`                      | Hardcoded version (§1.3), no test coverage (§3.2)                |
| `docs/API_REFERENCE.md`              | 10 missing tools (§2.1)                                          |
| `README.md`                          | Tool count drift (§2.2)                                          |
| `pyproject.toml`                     | Count in description (§2.2), ruff target (§4.3), dep pins (§4.4) |
| `ALiveMCP_Remote/liveapi_tools.py`   | Stale class docstring (§2.3)                                     |
| `tests/test_live_api_tools.py`       | Stale mixin list (§3.1)                                          |
| `ALiveMCP_Remote/__init__.py`        | Error shape / dispatch (§4.1)                                    |
| `ALiveMCP_Remote/tools/core/base.py` | Candidate for result helpers (§4.2)                              |
| `examples/mock_server.py`            | 424 lines, hook-excluded (§5.1)                                  |
