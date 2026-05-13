# set_clip_ram_mode

Set Clip RAM Mode

Set whether an audio clip should be loaded into RAM or streamed from disk.

Parameters:
- `track_index` (int)
- `clip_index` (int)
- `ram_mode` (boolean)

Returns:
- `ok`: boolean
- `ram_mode`: boolean (new value)

Example request:
```json
{"action": "set_clip_ram_mode", "track_index": 0, "clip_index": 0, "ram_mode": true}
```
