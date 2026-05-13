# set_clip_end_marker

Set Clip End Marker

Set the end marker position of a clip.

Parameters:
- `track_index` (int)
- `clip_index` (int)
- `end_marker` (float)

Returns:
- `ok`: boolean
- `end_marker`: float (new value)

Example request:
```json
{"action": "set_clip_end_marker", "track_index": 0, "clip_index": 0, "end_marker": 4.0}
```
