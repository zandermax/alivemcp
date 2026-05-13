# get_scene_color

**Domain:** scenes

**Summary:** Return the scene color index if supported by the host.

**Parameters:**
- `scene_index` (int)

**Live mapping:**
- Reads `scene.color` if `hasattr(scene, "color")` and returns it as an integer.

**Example request:**
```json
{"action": "get_scene_color", "scene_index": 0}
```

**Example response:**
```json
{"ok": true, "color": 5}
```

**Notes:**
- If the `color` attribute is not available on the host, the tool returns `{"ok": false, "error": "Scene color not available"}`.

**See also:**
- set_scene_color, get_scene_info
