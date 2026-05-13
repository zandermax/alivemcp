# get_clip_ram_mode

Get Clip RAM Mode

Get whether an audio clip is loaded in RAM (RAM mode) or streamed.

Parameters:
- `track_index` (int)
- `clip_index` (int)

Returns:
- `ok`: boolean
- `ram_mode`: boolean (when available)

Example request:
```json
{"action": "get_clip_ram_mode", "track_index": 0, "clip_index": 0}
```

