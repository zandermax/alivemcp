# launch_clip

**Domain:** clips

**Summary:** Launch (fire) a clip in a clip slot.

**Parameters:**
- `track_index` (int)
- `clip_index` (int)

**Live mapping:**
- Calls `clip_slot.fire()` on the Live Object Model to launch the clip.

**Example request:**
```json
{"action": "launch_clip", "track_index": 1, "clip_index": 0}
```

**Example response:**
```json
{"ok": true, "message": "Clip launched"}
```

**Notes:**
- Returns an error if no clip is present in the specified slot.

**See also:**
- [stop_clip](tools/clips/stop_clip.md)
- [get_clip_info](tools/clips/get_clip_info.md)
