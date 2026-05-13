# set_clip_loop_end

Set Clip Loop End

Set the loop end position of a clip.

Parameters:
- `track_index` (int)
- `clip_index` (int)
- `loop_end` (float)

Returns:
- `ok`: boolean
- `loop_end`: float (new value)

Example request:
```json
{"action": "set_clip_loop_end", "track_index": 0, "clip_index": 0, "loop_end": 4.0}
```

