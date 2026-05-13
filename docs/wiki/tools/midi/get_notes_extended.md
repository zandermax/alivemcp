# get_notes_extended

**Domain:** midi

**Summary:** Query notes from a MIDI clip with time and pitch range filters.

**Parameters:**
- `track_index` (int)
- `clip_index` (int)
- `start_time` (float)
- `time_span` (float)
- `start_pitch` (int)
- `pitch_span` (int)

**Live mapping:**
- Calls `clip.get_notes_extended(from_time=..., from_pitch=..., time_span=..., pitch_span=...)` and returns structured notes.

**Example request:**
```json
{"action": "get_notes_extended", "track_index": 1, "clip_index": 0, "start_time": 0.0, "time_span": 4.0, "start_pitch": 60, "pitch_span": 12}
```

**Example response:**
```json
{"ok": true, "notes": [{"pitch": 60, "start_time": 0.0, "duration": 1.0, "velocity": 100, "muted": false}], "count": 1}
```

**Notes:**
- Useful for efficient, bounded queries over large clips.

**See also:**
- [get_clip_notes](tools/midi/get_clip_notes.md)
