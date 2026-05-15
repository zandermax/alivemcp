---
name: "set_clip_pitch_coarse"
summary: ""
---

# set_clip_pitch_coarse

Set Clip Pitch Coarse

Transpose a clip by semitones (coarse pitch).

Parameters:

- `track_index` (int)
- `clip_index` (int)
- `semitones` (int)

Returns:

- `ok`: boolean
- `pitch_coarse`: int (new value)

**Example request:**

```json
{
  "action": "set_clip_pitch_coarse",
  "track_index": 0,
  "clip_index": 0,
  "semitones": 2
}
```

**Example response:**

```json
{ "ok": true }
```
