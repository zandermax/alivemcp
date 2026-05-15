---
name: "get_scene_tempo"
summary: ""
---

# get_scene_tempo

Get Scene Tempo

Get a scene's tempo override if set.

Parameters:

- `scene_index` (int)

Returns:

- `ok`: boolean
- `tempo`: float or null
- `has_tempo`: boolean

Notes:

- Returns an error when scene `tempo` property is unavailable.
  **Example request:**

```json
{ "action": "get_scene_tempo", "scene_index": 0 }
```

**Example response:**

```json
{ "ok": true }
```
