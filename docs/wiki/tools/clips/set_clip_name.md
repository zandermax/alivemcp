# set_clip_name

**Domain:** clips

**Summary:** Set the name of a clip in a clip slot.

**Parameters:**
- `track_index` (int)
- `clip_index` (int)
- `name` (string)

**Live mapping:**
- Sets `clip_slot.clip.name = name` on the Live Object Model.

**Example request:**
```json
{"action": "set_clip_name", "track_index": 1, "clip_index": 0, "name": "New Name"}
```

**Example response:**
```json
{"ok": true, "message": "Clip renamed", "name": "New Name"}
```

**Notes:**
- Returns an error if the slot has no clip.

**See also:**
- [docs/wiki/tools/clips/get_clip_info.md](docs/wiki/tools/clips/get_clip_info.md)
