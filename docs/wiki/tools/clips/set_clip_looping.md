---
name: "set_clip_looping"
summary: ""
---

# set_clip_looping

Set Clip Looping

Enable or disable looping on a clip.

Parameters:

- `track_index` (int)
- `clip_index` (int)
- `looping` (boolean)

Returns:

- `ok`: boolean
- `looping`: boolean (new value)
  **Example request:**

```json
{
  "action": "set_clip_looping",
  "track_index": 0,
  "clip_index": 0,
  "looping": true
}
```

**Example response:**

```json
{ "ok": true }
```
