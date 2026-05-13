# delete_take_lane

**Domain:** arrangement (take_lanes)

**Summary:** Delete a take lane from a track (Live 12+).

**Parameters:**
- `track_index` (int)
- `lane_index` (int)

**Live mapping:**
- Calls `track.delete_take_lane(lane_index)` when supported.

**Example request:**
```json
{"action":"delete_take_lane","track_index":1,"lane_index":0}
```

**Example response:**
```json
{"ok": true, "message":"Take lane deleted"}
```
