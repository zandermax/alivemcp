# stop_clip

**Domain:** clips

**Summary:** Stop playback of a clip in a specific clip slot.

**Parameters:**
- `track_index` (int)
- `clip_index` (int)

**Live mapping:**
- Uses `track.clip_slots[clip_index].stop()` to stop the clip.

**Example request:**
```json
{"action": "stop_clip", "track_index": 1, "clip_index": 0}
```

**Example response:**
```json
{"ok": true, "message": "Clip stopped"}
```

**Notes:**
- If no clip exists in the slot an error is returned.

**See also:**
- [docs/wiki/tools/clips/launch_clip.md](docs/wiki/tools/clips/launch_clip.md)
- [docs/wiki/TOOLS_INDEX.md](docs/wiki/TOOLS_INDEX.md)
