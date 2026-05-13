# get_clip_fade_out

Get Clip Fade Out

Get the fade-out time for an audio clip.

Parameters:
- `track_index` (int)
- `clip_index` (int)

Returns:
- `ok`: boolean
- `fade_out_time`: float (when available)

Example request:
```json
{"action": "get_clip_fade_out", "track_index": 0, "clip_index": 0}
```
