---
name: "get_scene_info"
summary: ""
Live mapping: "- Validates index bounds and reads `scene.name`, `scene.color` (if available), `scene.tempo` (if available), and `scene.time_signature_numerator` (if available)."
---

# get_scene_info

**Domain:** scenes

**Summary:** Return information about a scene: name, color, tempo, and time signature numerator (when available).

**Parameters:**

- `scene_index` (int)

**Live mapping:**

- Validates index bounds and reads `scene.name`, `scene.color` (if available), `scene.tempo` (if available), and `scene.time_signature_numerator` (if available).
  **Example request:**

```json
{ "action": "get_scene_info", "scene_index": 0 }
```

**Example response:**

```json
{
  "ok": true,
  "scene_index": 0,
  "name": "Intro",
  "color": null,
  "tempo": null,
  "time_signature_numerator": null
}
```

**Notes:**

- Some Live builds expose additional scene properties; this tool uses `hasattr` guards and returns `null` for unavailable fields.

**See also:**

- get_scene_color, set_scene_color, rename_scene
