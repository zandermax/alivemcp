---
name: "set_scene_color"
summary: ""
Live mapping: '- If `hasattr(scene, "color")`, sets `scene.color = int(color_index)` and returns the updated color.'
---

# set_scene_color

**Domain:** scenes

**Summary:** Set the scene color index if supported by the host.

**Parameters:**

- `scene_index` (int)
- `color_index` (int)

**Live mapping:**

- If `hasattr(scene, "color")`, sets `scene.color = int(color_index)` and returns the updated color.
  **Example request:**

```json
{ "action": "set_scene_color", "scene_index": 0, "color_index": 3 }
```

**Example response:**

```json
{ "ok": true, "color": 3 }
```

**Notes:**

- Returns an error if the `color` attribute is not present on the host.

**See also:**

- get_scene_color, get_scene_info
