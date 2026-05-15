---
name: "set_clip_gain"
summary: ""
---

# set_clip_gain

Set Clip Gain

Set clip gain/volume (audio clips only).

Parameters:

- `track_index` (int)
- `clip_index` (int)
- `gain` (float)

Returns:

- `ok`: boolean
- `gain`: float (new value)
  **Example request:**

```json
{ "action": "set_clip_gain", "track_index": 0, "clip_index": 0, "gain": 0.0 }
```

**Example response:**

```json
{ "ok": true }
```
