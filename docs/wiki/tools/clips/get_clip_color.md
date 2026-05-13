# get_clip_color

Get Clip Color

Get a clip's color or color index.

Parameters:
- `track_index` (int)
- `clip_index` (int)

Returns:
- `ok`: boolean
- `color_index` or `color`: int

Notes: Some Live versions expose `color_index`, others `color`.

Example request:
```json
{"action": "get_clip_color", "track_index": 0, "clip_index": 0}
```

