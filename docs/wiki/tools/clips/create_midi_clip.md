# create_midi_clip

**Domain:** clips

**Summary:** Create a new MIDI clip in a track's clip slot.

**Parameters:**
- `track_index` (int) — target track index
- `clip_index` (int) — target clip slot / scene index (alias: `scene_index` supported by API)
- `length` (float) — length in beats (default 4.0)

**Live mapping:**
- Uses `track.clip_slots[clip_index].create_clip(length)` on the Live Object Model.
- Main-thread only.

**Example request:**
```json
{"action": "create_midi_clip", "track_index": 1, "clip_index": 0, "length": 4.0}
```

**Example response:**
```json
{"ok": true, "message": "MIDI clip created", "track_index": 1, "clip_index": 0, "length": 4.0}
```

**Ableton references:**
- Live API overview: https://docs.cycling74.com/max8/vignettes/live_api_overview
- Live API Doc Archive (clip_slot): https://nsuspray.github.io/Live_API_Doc/

**Notes:**
- Fails if the slot already has a clip or if the track is not a MIDI track.

**See also:**
- [delete_clip](tools/clips/delete_clip.md)
- [duplicate_clip](tools/clips/duplicate_clip.md)
- [add_notes](tools/clips/add_notes.md)
