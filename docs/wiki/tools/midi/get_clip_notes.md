# get_clip_notes

**Domain:** midi

**Summary:** Retrieve all MIDI notes from a MIDI clip.

**Parameters:**
- `track_index` (int)
- `clip_index` (int)

**Live mapping:**
- Validates indices and `track.has_midi_input`.
- Calls `clip.get_notes(0, 0, clip.length, 128)` and returns structured note objects.

**Example request:**
```json
{"action": "get_clip_notes", "track_index": 1, "clip_index": 0}
```

**Example response:**
```json
{"ok": true, "track_index": 1, "clip_index": 0, "notes": [{"pitch": 60, "start_time": 0.0, "duration": 1.0, "velocity": 100, "muted": false}], "count": 1}
```

**Notes:**
- Returns times in beats as floats. If no clip or not a MIDI clip, returns an error.

**See also:**
- add_notes, get_notes_extended
