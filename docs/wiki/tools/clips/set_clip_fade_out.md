Set Clip Fade Out

Set the fade-out time for an audio clip.

Parameters:
- `track_index` (int)
- `clip_index` (int)
- `fade_time` (float)

Returns:
- `ok`: boolean
- `fade_out_time`: float (new value)

Example request:
```json
{"action": "set_clip_fade_out", "track_index": 0, "clip_index": 0, "fade_time": 0.05}
```
