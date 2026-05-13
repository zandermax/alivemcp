# set_take_lane_name

**Domain:** arrangement (take_lanes)

**Summary:** Rename a take lane (Live 12+).

**Parameters:**
- `track_index` (int)
- `lane_index` (int)
- `name` (string)

**Live mapping:**
- Writes `track.take_lanes[lane_index].name = name` when supported.

**Example request:**
```json
{"action":"set_take_lane_name","track_index":1,"lane_index":0,"name":"Comp A"}
```

**Example response:**
```json
{"ok": true, "name":"Comp A"}
```
