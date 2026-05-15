---
name: "set_clip_start_time"
summary: ""
---

# set_clip_start_time

Set Clip Start Time

Set clip `start_time` for a clip in a track slot.

Parameters:

- `track_index` (int): track index
- `clip_index` (int): clip slot index
- `start_time` (float): new start time

Returns:

- `ok`: boolean
- `start_time`: float (new value when set)

Notes:

- Fails if the clip slot has no clip or the property is not settable.

**Example request:**

```json
{
  "action": "set_clip_start_time",
  "track_index": 0,
  "clip_index": 0,
  "start_time": 1.0
}
```

**Example response:**

```json
{ "ok": true, "start_time": 1.0 }
```
