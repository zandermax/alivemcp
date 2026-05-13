# set_clip_muted

Set Clip Muted

Mute or unmute a clip.

Parameters:
- `track_index` (int)
- `clip_index` (int)
- `muted` (boolean)

Returns:
- `ok`: boolean
- `muted`: boolean (new value)

Example request:
```json
{"action": "set_clip_muted", "track_index": 0, "clip_index": 0, "muted": true}
```
