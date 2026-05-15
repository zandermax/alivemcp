---
name: "get_take_lane_name"
summary: ""
Live mapping: "- Reads `track.take_lanes[lane_index].name` when available."
---

# get_take_lane_name

**Domain:** arrangement (take_lanes)

**Summary:** Get the name of a take lane (Live 12+).

**Parameters:**

- `track_index` (int)
- `lane_index` (int)

**Live mapping:**

- Reads `track.take_lanes[lane_index].name` when available.
  **Example request:**

```json
{ "action": "get_take_lane_name", "track_index": 1, "lane_index": 0 }
```

**Example response:**

```json
{ "ok": true, "name": "Take 1" }
```
