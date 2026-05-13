# get_scene_is_empty

Get Scene Is Empty

Check whether a scene contains no clips.

Parameters:
- `scene_index` (int)

Returns:
- `ok`: boolean
- `is_empty`: boolean

Notes:
- If `scene.is_empty` is not available, the tool falls back to scanning tracks.

**Example request:**

```json
{"action": "get_scene_is_empty", "scene_index": 0}
```

**Example response:**

```json
{"ok": true, "is_empty": false}
```

