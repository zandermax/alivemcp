# add_notes

**Domain:** midi

**Summary:** Add MIDI notes into a MIDI clip at a given track/clip slot.

**Parameters:**
- `track_index` (int) — track containing the clip
- `clip_index` (int) — clip slot / scene index on the track
- `notes` (list) — list of note objects: `{ "pitch": int, "start": float, "duration": float, "velocity": int }`

**Live mapping:**
- Validates track/clip indices and `track.has_midi_input`.
- Calls `clip.set_notes(((pitch, start, duration, velocity, False),))` for each note tuple.

**Example request:**
```json
{"action": "add_notes", "track_index": 1, "clip_index": 0, "notes": [{"pitch": 60, "start": 0.0, "duration": 1.0, "velocity": 100}]}
```

**Example response:**
```json
{"ok": true, "message": "Notes added", "track_index": 1, "clip_index": 0, "note_count": 1}
```

**Notes:**
- Performs basic validation on pitch (0-127), velocity (0-127), and duration (>0).
- Uses `clip.set_notes` which replaces/sets notes — callers should manage selection/replace semantics accordingly.

**See also:**
- get_clip_notes, remove_notes, replace_selected_notes
