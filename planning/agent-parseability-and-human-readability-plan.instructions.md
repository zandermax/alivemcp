# Agent Instructions: Parseability and Readability Improvement Plan (alivemcp)

## Purpose

This plan makes the alivemcp codebase easier to parse for coding agents and humans by enforcing a single source of truth for tool metadata and by adding machine-readable navigation artifacts.

## Why This Plan Exists

The repository has excellent architecture docs, but tool surface data currently appears in multiple places.
This increases drift risk and can break agent reasoning or user trust when counts, names, or docs disagree.

## Scope

In scope:

1. Canonical tool metadata source definition.
2. Deterministic generation of downstream tool definitions and docs.
3. Consistency checks that fail fast on drift.
4. Agent-readable repository map and impact documentation.

Out of scope:

1. Expanding LiveAPI feature coverage.
2. Behavioral changes to existing tool semantics.
3. Network/protocol redesign.

## Hard Constraints

1. Keep main-thread-only execution model unchanged.
2. Preserve Python 3.6 compatibility constraints for Remote Script code.
3. Maintain file length policy and single-responsibility guidance.
4. Do not remove `scene_index` compatibility alias behavior.

## Success Criteria

This plan is successful when all are true:

1. Tool names and counts are generated from a single canonical source.
2. MCP exposed tool set, registry list, and API reference are parity-checked.
3. README and example docs do not contain stale tool counts.
4. A machine-readable index exists for agent routing.
5. Test suite includes at least one drift-prevention test for tool parity.

## Deliverables

### D1: Canonical Tool Manifest

Create: `docs/tool_manifest.json`

Required shape:

1. `tools`: array of tool records with `name`, `description`, `schema_ref` or inline schema key.
2. `categories`: optional grouping metadata.
3. `aliases`: compatibility parameter alias metadata.
4. `version`: manifest schema version.

Rules:

1. Sorted deterministically by tool name.
2. JSON only, ASCII, stable formatting.
3. Canonical for counts and names; other artifacts derive from this.

### D2: Generators for Derived Artifacts

Create scripts in `scripts/`:

1. `generate_mcp_tool_defs.py` -> writes `mcp_server_tool_defs.py`.
2. `generate_api_reference.py` -> writes or updates `docs/API_REFERENCE.md` sections generated from manifest.
3. Optional: `generate_registry.py` if registry can be safely generated.

Rules:

1. Generators must be idempotent.
2. Generated sections must be clearly bounded with markers if partial-file generation is used.
3. Preserve hand-authored narrative sections outside generated boundaries.

### D3: Parity and Drift Tests

Add tests that enforce:

1. Registry tool names == MCP tool def names.
2. Manifest tool names == registry tool names.
3. README and key examples do not hardcode stale counts unless generated or validated.

Recommended test files:

1. `tests/test_tool_metadata_parity.py`
2. Extend `tests/test_mcp_server.py` with a parity assertion against manifest-derived names.

### D4: Machine-Readable Agent Index

Create: `docs/AGENT_INDEX.json`

Required fields:

1. `repo`: metadata.
2. `entrypoints`: server start, install, test commands.
3. `source_of_truth`: files that are canonical for tool surface.
4. `high_risk_paths`: thread-safety, dispatch, socket transport, registry/tool defs.
5. `validation_matrix`: file-pattern to required checks.

### D5: Impact Maps

Create:

1. `docs/IMPACT_MAP_TOOL_SURFACE.md`
2. `docs/IMPACT_MAP_RUNTIME_DISPATCH.md`

Must include:

1. Trigger paths.
2. Invariants.
3. Required validation commands.
4. Common regressions and detection points.

## Implementation Phases

## Phase 1: Canonicalization Setup

Tasks:

1. Add `docs/tool_manifest.json` with all current tool names.
2. Define schema and ordering policy in a short contributor note.
3. Remove hardcoded count claims from hand-written docs where practical.

Exit criteria:

1. Manifest contains complete current tool set.
2. All tool count claims are generated or validated.

## Phase 2: Generation Pipeline

Tasks:

1. Implement generator for `mcp_server_tool_defs.py`.
2. Implement API reference generation for tool list sections.
3. Add a make target or script command to run generators.

Exit criteria:

1. Running generators with no source changes yields no diff.
2. Generated outputs are stable across runs.

## Phase 3: Enforcement

Tasks:

1. Add parity tests for names and counts.
2. Add a CI step that fails if generated files are out of date.
3. Add contributor guidance: run generators before commit.

Exit criteria:

1. CI fails on manifest/output drift.
2. Test failures clearly identify missing/extra tool names.

## Phase 4: Navigation and Onboarding Optimization

Tasks:

1. Add `docs/AGENT_INDEX.json` and both impact maps.
2. Link these from `README.md` and `CLAUDE.md`.
3. Add one "first 10 minutes" section for maintainers.

Exit criteria:

1. New maintainer can find canonical files and validation commands from one entry point.
2. Agent can resolve source-of-truth without scanning long prose.

## Validation Matrix

When tool manifest or generators change:

1. `pytest tests/test_tool_metadata_parity.py -q`
2. `pytest tests/test_mcp_server.py -q`
3. `pytest -q`

When runtime dispatch or socket code changes:

1. `pytest tests/test_mcp_server.py -q`
2. `pytest tests/test_alivemcp_socket.py -q`
3. `pytest -q`

When docs and generated outputs change:

1. Run generation commands.
2. Ensure git diff is clean after a second generation run.

## Risk Register

1. Risk: Partial migration leaves two active sources of truth.
Mitigation: Explicitly mark canonical source and add parity tests.

2. Risk: Generator overwrites hand-authored docs.
Mitigation: Generate only bounded sections with markers.

3. Risk: Contributor workflow friction.
Mitigation: Provide one command to regenerate all derived artifacts.

4. Risk: Hidden stale references in examples.
Mitigation: Add lightweight grep-based stale-count check in tests.

## Done Definition

Work is complete only when:

1. `planning/agent-parseability-and-human-readability-plan.instructions.md` remains as baseline plan.
2. D1 through D5 artifacts exist.
3. Parity checks are passing and enforced in CI.
4. README and CLAUDE link to new machine-readable and impact docs.

## Strict Execution Order

1. D1 manifest
2. D2 generators
3. D3 parity tests and CI hook
4. D4 agent index
5. D5 impact maps
6. final full validation

## Non-Goals Reminder

Do not use this plan to justify broad refactors. Keep changes centered on parseability, drift prevention, and discoverability.