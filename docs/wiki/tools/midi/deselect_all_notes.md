# deselect_all_notes

**Domain:** midi

**Summary:** Deselect all notes in a MIDI clip.

**Parameters:**
- `track_index` (int)
- `clip_index` (int)

**Live mapping:**
- Calls `clip.deselect_all_notes()`.

**Example request:**
```json
{"action": "deselect_all_notes", "track_index": 1, "clip_index": 0}
```

**Example response:**
```json
{"ok": true, "message": "All notes deselected"}
```

**See also:**
- select_all_notes
