---
name: "set_clip_fade_in"
summary: ""
---

# set_clip_fade_in

Set Clip Fade In

Set the fade-in time for an audio clip.

Parameters:

- `track_index` (int)
- `clip_index` (int)
- `fade_time` (float)

Returns:

- `ok`: boolean
- `fade_in_time`: float (new value)
  **Example request:**

```json
{
  "action": "set_clip_fade_in",
  "track_index": 0,
  "clip_index": 0,
  "fade_time": 0.05
}
```

**Example response:**

```json
{ "ok": true }
```
