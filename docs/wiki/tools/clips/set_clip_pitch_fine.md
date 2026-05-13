Set Clip Pitch Fine

Fine-tune clip pitch in cents.

Parameters:
- `track_index` (int)
- `clip_index` (int)
- `cents` (int)

Returns:
- `ok`: boolean
- `pitch_fine`: int (new value)

Example request:
```json
{"action": "set_clip_pitch_fine", "track_index": 0, "clip_index": 0, "cents": 10}
```
