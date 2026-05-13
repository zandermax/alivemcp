# select_all_notes

**Domain:** midi

**Summary:** Select all notes in a MIDI clip.

**Parameters:**
- `track_index` (int)
- `clip_index` (int)

**Live mapping:**
- Calls `clip.select_all_notes()` after validating clip presence and type.
**Example request:**
```json
{"action": "select_all_notes", "track_index": 1, "clip_index": 0}
```
**Example response:**
```json
{"ok": true, "message": "All notes selected"}
```

**Notes:**
- Useful before `replace_selected_notes` to operate on entire clip.

**See also:**
- [deselect_all_notes](tools/midi/deselect_all_notes.md)
- [replace_selected_notes](tools/midi/replace_selected_notes.md)
