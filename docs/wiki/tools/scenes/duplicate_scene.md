# duplicate_scene

**Domain:** scenes

**Summary:** Duplicate a scene by index.

**Parameters:**
- `scene_index` (int) — index of the scene to duplicate

**Live mapping:**
- Validates index bounds and calls `self.song.duplicate_scene(scene_index)`. Returns the expected new index (`scene_index + 1`).

**Example request:**
```json
{"action": "duplicate_scene", "scene_index": 1}
```

**Example response:**
```json
{"ok": true, "message": "Scene duplicated", "new_index": 2}
```

**Notes:**
- Duplicating shifts subsequent scene indices.

**See also:**
- [create_scene](tools/scenes/create_scene.md)
- [delete_scene](tools/scenes/delete_scene.md)
