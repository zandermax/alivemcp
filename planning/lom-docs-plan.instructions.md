# LOM Schema Mining — Claude Code Brief

## Context

I have a Python MCP server called ALiveMCP with 232 tools that expose Ableton Live's Live Object Model (LOM) via the Live API. Each tool implicitly encodes LOM knowledge: which object it operates on, what property or method it targets, whether it reads or writes, what parameters it takes, and what it returns.

The goal is to mine these tool definitions and produce a structured JSON schema of the LOM — objects, properties, methods, types, writability, and observability — that can be committed to git and diffed across Live versions.

## What to Do

### Step 1 — Discover the tool definitions

See the definitions in the wiki docs for the source of truth.

Print a summary of what you find before proceeding: how tools are registered, what metadata is available per tool (name, description, parameters, return type), and where docstrings live.

### Step 2 — Extract per-tool LOM signals

For each tool, extract:

| Field | How to get it |
| --- | --- |
| `tool_name` | The registered MCP tool name |
| `description` | Docstring or description field |
| `parameters` | Input schema (names, types, optionality) |
| `return_type` | Return annotation or description |
| `raw_text` | Full docstring + parameter names concatenated — used for heuristic parsing |

Do not infer LOM structure yet — just collect clean records. Write these to `lom_mining/01_raw_tool_records.json`.

### Step 3 — Infer LOM object and member from tool name + description

Apply heuristics to map each tool to a LOM node. The LOM is a tree of objects (`Song`, `Track`, `Clip`, `Device`, `DeviceParameter`, `ClipSlot`, `Scene`, etc.).

**Naming heuristics to try, in order:**

1. **Prefix match** — tool names often encode the object: `get_track_volume` → `Track.volume`, `set_clip_name` → `Clip.name`, `fire_clip` → `Clip.fire()`
2. **Keyword scan in description** — look for known LOM class names as tokens
3. **Parameter name scan** — a parameter named `track_id` or `device_id` implies the operating object
4. **Verb classification**:
   - `get_*` → read property
   - `set_*` → write property
   - `add_*_listener` / `remove_*_listener` → observable property
   - `create_*` / `delete_*` / `fire_*` / `stop_*` → method

For each tool produce:

```json
{
  "tool_name": "set_track_volume",
  "lom_object": "Track",
  "lom_member": "volume",
  "member_kind": "property",
  "writable": true,
  "observable": null,
  "param_types": { "track_id": "int", "value": "float" },
  "return_type": "None",
  "confidence": "high | medium | low",
  "inference_path": "prefix_match"
}
```

Flag anything that doesn't cleanly map as `"lom_object": "UNKNOWN"` — don't discard it.

Write results to `lom_mining/02_tool_lom_mappings.json`.

### Step 4 — Aggregate into LOM object schema

Group by `lom_object`. For each object, collect all its members and deduplicate. Where multiple tools target the same member (e.g. a getter and a setter), merge them into one entry:

```json
{
  "Song": {
    "properties": {
      "tempo": {
        "writable": true,
        "observable": true,
        "types_seen": ["float"],
        "source_tools": ["get_song_tempo", "set_song_tempo", "add_tempo_listener"]
      }
    },
    "methods": {
      "create_midi_track": {
        "params": { "index": "int" },
        "return_type": "Track",
        "source_tools": ["create_midi_track"]
      }
    },
    "collections": {
      "tracks": {
        "item_type": "Track",
        "source_tools": ["get_tracks"]
      }
    }
  }
}
```

Observability: if `add_X_listener` exists for a property, set `"observable": true`. If only get/set exist, set `"observable": false`. If unknown, `null`.

Write to `lom_mining/03_lom_schema_draft.json`.

### Step 5 — Produce a gap and confidence report

Write `lom_mining/04_gap_report.md` containing:

1. **Coverage summary** — how many tools mapped cleanly vs. UNKNOWN
2. **UNKNOWN tools list** — full records, for manual review
3. **Low-confidence mappings** — list with the tool name and why confidence was low
4. **Inferred but unconfirmed observability** — properties where observable status couldn't be determined from tool names alone
5. **Missing LOM objects** — known LOM classes not represented by any tool: `Song`, `Track`, `MidiTrack`, `AudioTrack`, `ReturnTrack`, `MasterTrack`, `Clip`, `MidiClip`, `AudioClip`, `ClipSlot`, `Scene`, `Device`, `Instrument`, `RackDevice`, `DrumRack`, `DeviceParameter`, `Chain`, `MixerDevice`, `Send`, `Application`, `View`

### Step 6 — Commit artifacts

If a git repo is present, commit the four output files under `lom_mining/` with a message like:

```text
feat(lom): initial schema mining from ALiveMCP tool definitions

232 tools parsed. X objects identified, Y tools unmapped.
See lom_mining/04_gap_report.md for coverage details.
```

---

## Output File Summary

| File | Contents |
| --- | --- |
| `lom_mining/01_raw_tool_records.json` | Raw extracted metadata per tool |
| `lom_mining/02_tool_lom_mappings.json` | Per-tool LOM inference results |
| `lom_mining/03_lom_schema_draft.json` | Aggregated object schema |
| `lom_mining/04_gap_report.md` | Coverage gaps and low-confidence flags |

---

## Notes

- Do not hallucinate LOM structure. If a mapping is uncertain, flag it — don't guess silently.
- Prefer `"confidence": "low"` over `"lom_object": "UNKNOWN"` when there's a plausible but unconfirmed match.
- The JSON artifacts should be human-readable with tab indentation — they'll be read as git diffs.
- If the tool definitions are spread across multiple files, process all of them and note the source file in each record.
