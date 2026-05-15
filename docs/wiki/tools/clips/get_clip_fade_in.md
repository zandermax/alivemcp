---
name: "get_clip_fade_in"
summary: ""
---

# get_clip_fade_in

Get Clip Fade In

Get the fade-in time for an audio clip.

Parameters:

- `track_index` (int)
- `clip_index` (int)

Returns:

- `ok`: boolean
- `fade_in_time`: float (when available)
  **Example request:**

```json
{ "action": "get_clip_fade_in", "track_index": 0, "clip_index": 0 }
```

**Example response:**

```json
{ "ok": true }
```
