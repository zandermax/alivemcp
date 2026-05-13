# create_scene

**Domain:** scenes

**Summary:** Create a new scene at the end of the current scenes list (optionally set its name).

**Parameters:**
- `name` (string, optional) — name to assign to the new scene

**Live mapping:**
- Calls `self.song.create_scene(scene_index)` where `scene_index = len(self.song.scenes)`, then sets `song.scenes[scene_index].name` if provided.

**Example request:**
```json
{"action": "create_scene", "name": "New Scene"}
```

**Example response:**
```json
{"ok": true, "message": "Scene created", "scene_index": 3, "name": "New Scene"}
```

**Notes:**
- Returns the created scene index and final name. Index is computed before creation so concurrent operations may shift indices.

**See also:**
- delete_scene, duplicate_scene
