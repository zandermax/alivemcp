# get_clip_annotation

Get Clip Annotation

Get the annotation text for a clip.

Parameters:
- `track_index` (int)
- `clip_index` (int)

Returns:
- `ok`: boolean
- `annotation`: string (when available)

Notes: Some Ableton versions may not expose `annotation`.

Example request:
```json
{"action": "get_clip_annotation", "track_index": 0, "clip_index": 0}
```

