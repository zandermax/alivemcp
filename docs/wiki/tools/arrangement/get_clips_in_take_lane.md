# get_clips_in_take_lane

**Domain:** arrangement (take_lanes)

**Summary:** List clips contained in a take lane (Live 12+).

**Parameters:**
- `track_index` (int)
- `lane_index` (int)

**Live mapping:**
- Iterates `lane.clips` and returns basic metadata (name, length, is_midi).
**Example request:**
```json
{"action":"get_clips_in_take_lane","track_index":1,"lane_index":0}
```
**Example response:**
```json
{"ok": true, "count":1, "clips":[{"name":"Take A","length":4.0,"is_midi":false}]}
```
