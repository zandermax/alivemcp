---
name: "get_clip_start_time"
summary: ""
---

# get_clip_start_time

Get Clip Start Time

Get clip `start_time` for a clip in a track slot (Live 12+ observable).

Parameters:

- `track_index` (int): track index
- `clip_index` (int): clip slot index

Returns:

- `ok`: boolean
- `start_time`: float (when available)

Notes:

- Returns an error when the clip slot has no clip or the property is unavailable.
  **Example request:**

```json
{ "action": "get_clip_start_time", "track_index": 0, "clip_index": 0 }
```

**Example response:**

```json
{ "ok": true }
```
