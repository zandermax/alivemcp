# remove_notes

**Domain:** midi

**Summary:** Remove MIDI notes from a clip with optional pitch/time ranges.

**Parameters:**
- `track_index` (int)
- `clip_index` (int)
- `pitch_from` (int, default 0)
- `pitch_to` (int, default 127)
- `time_from` (float, default 0.0)
- `time_to` (float, default 999.0)

**Live mapping:**
- Calls `clip.remove_notes(time_from, pitch_from, time_to - time_from, pitch_to - pitch_from)` after validation.

**Example request:**
```json
{"action": "remove_notes", "track_index": 1, "clip_index": 0, "pitch_from": 60, "pitch_to": 60}
```

**Example response:**
```json
{"ok": true, "message": "Notes removed"}
```

**Notes:**
- `time_to` default is large to allow removing across clip length; callers should provide explicit bounds for safety.

**See also:**
- [add_notes](tools/clips/add_notes.md)
- [get_clip_notes](tools/midi/get_clip_notes.md)
