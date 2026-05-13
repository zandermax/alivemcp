Set Clip Follow Action

Configure follow actions A/B and chance for a clip.

Parameters:
- `track_index` (int)
- `clip_index` (int)
- `action_A` (int 0-8)
- `action_B` (int 0-8)
- `chance_A` (float, optional, default 1.0)

Returns:
- `ok`: boolean
- `follow_action_A`: int (when available)
- `follow_action_B`: int (when available)

Example request:
```json
{"action": "set_clip_follow_action", "track_index": 0, "clip_index": 0, "action_A": 1, "action_B": 0, "chance_A": 0.5}
```
