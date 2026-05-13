# set_clip_start_marker

Set Clip Start Marker

Set the start marker position of a clip.

Parameters:
- `track_index` (int)
- `clip_index` (int)
- `start_marker` (float)

Returns:
- `ok`: boolean
- `start_marker`: float (new value)
**Example request:**
```json
{"action": "set_clip_start_marker", "track_index": 0, "clip_index": 0, "start_marker": 0.0}
```
**Example response:**
```json
{"ok": true}
```


