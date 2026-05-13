# delete_scene

**Domain:** scenes

**Summary:** Delete a scene by index.

**Parameters:**
- `scene_index` (int) — index of the scene to delete

**Live mapping:**
- Validates index bounds and calls `self.song.delete_scene(scene_index)`.

**Example request:**
```json
{"action": "delete_scene", "scene_index": 2}
```

**Example response:**
```json
{"ok": true, "message": "Scene deleted"}
```

**Notes:**
- Returns an error for invalid indices.

**See also:**
- create_scene, duplicate_scene
