# quantize_clip

Quantize Clip

Quantize a MIDI clip to a grid value.

Parameters:
- `track_index` (int)
- `clip_index` (int)
- `quantize_to` (float)

Returns:
- `ok`: boolean
- `message`: status
- `quantize_to`: supplied value

Example request:
```json
{"action": "quantize_clip", "track_index": 0, "clip_index": 0, "quantize_to": 0.25}
```

