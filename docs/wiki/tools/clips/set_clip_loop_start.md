Set Clip Loop Start

Set the loop start position of a clip.

Parameters:
- `track_index` (int)
- `clip_index` (int)
- `loop_start` (float)

Returns:
- `ok`: boolean
- `loop_start`: float (new value)

Example request:
```json
{"action": "set_clip_loop_start", "track_index": 0, "clip_index": 0, "loop_start": 0.0}
```
