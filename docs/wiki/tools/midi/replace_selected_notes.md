---
name: "replace_selected_notes"
summary: ""
Live mapping: "- Builds a tuple of note tuples and calls `clip.replace_selected_notes(tuple(note_tuples))`."
---

# replace_selected_notes

**Domain:** midi

**Summary:** Replace the currently selected notes in a MIDI clip with a provided set.

**Parameters:**

- `track_index` (int)
- `clip_index` (int)
- `notes` (list) — list of note objects `{ "pitch": int, "start": float, "duration": float, "velocity": int, "muted": bool }`

**Live mapping:**

- Builds a tuple of note tuples and calls `clip.replace_selected_notes(tuple(note_tuples))`.

**Example request:**

```json
{
  "action": "replace_selected_notes",
  "track_index": 1,
  "clip_index": 0,
  "notes": [
    {
      "pitch": 64,
      "start": 0.0,
      "duration": 1.0,
      "velocity": 110,
      "muted": false
    }
  ]
}
```

**Example response:**

```json
{ "ok": true, "message": "Selected notes replaced", "note_count": 1 }
```

**Notes:**

- Operates on the selection; callers should call `select_all_notes` if replacing all notes.

**See also:**

- select_all_notes, add_notes
