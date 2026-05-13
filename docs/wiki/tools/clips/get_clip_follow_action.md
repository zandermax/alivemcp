# get_clip_follow_action

Get Clip Follow Action

Return follow-action configuration for a clip (A/B actions, time, chances).

Parameters:
- `track_index` (int)
- `clip_index` (int)

Returns:
- `ok`: boolean
- `follow_action_A`: int (0-8)
- `follow_action_A_name`: string
- `follow_action_B`: int (0-8)
- `follow_action_B_name`: string
- `follow_action_time`: float
- `follow_action_chance_A`: float
- `follow_action_chance_B`: float

Example request:
```json
{"action": "get_clip_follow_action", "track_index": 0, "clip_index": 0}
```
