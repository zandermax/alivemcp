# rename_scene

**Domain:** scenes

**Summary:** Rename a scene by index.

**Parameters:**
- `scene_index` (int)
- `name` (string) — new scene name

**Live mapping:**
- Validates index bounds and sets `self.song.scenes[scene_index].name = str(name)`.

**Example request:**
```json
{"action": "rename_scene", "scene_index": 1, "name": "Chorus"}
```

**Example response:**
```json
{"ok": true, "message": "Scene renamed", "name": "Chorus"}
```

**Notes:**
- Name changes are reflected in the Live UI.

**See also:**
- get_scene_info
