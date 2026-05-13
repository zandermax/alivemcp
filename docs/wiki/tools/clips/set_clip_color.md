# set_clip_color

Set Clip Color

Set a clip's color (index) when supported by the Ableton version.

Parameters:
- `track_index` (int)
- `clip_index` (int)
- `color_index` (int)

Returns:
- `ok`: boolean
- `color_index` or `color`: int (new value)

Example request:
```json
{"action": "set_clip_color", "track_index": 0, "clip_index": 0, "color_index": 5}
```

