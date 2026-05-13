# set_follow_action_time

Set Follow Action Time

Set the follow-action time for a clip (in bars).

Parameters:
- `track_index` (int)
- `clip_index` (int)
- `time_in_bars` (float)

Returns:
- `ok`: boolean
- `follow_action_time`: float (new value)

Example request:
```json
{"action": "set_follow_action_time", "track_index": 0, "clip_index": 0, "time_in_bars": 1.0}
```

