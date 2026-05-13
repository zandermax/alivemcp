# quantize_clip_pitch

Quantize Clip Pitch

Quantize MIDI clip pitch to a specified pitch.

Parameters:
- `track_index` (int)
- `clip_index` (int)
- `pitch` (int)

Returns:
- `ok`: boolean
- `message`: status
- `pitch`: supplied value
**Example request:**
```json
{"action": "quantize_clip_pitch", "track_index": 0, "clip_index": 0, "pitch": 60}
```
**Example response:**
```json
{"ok": true}
```


