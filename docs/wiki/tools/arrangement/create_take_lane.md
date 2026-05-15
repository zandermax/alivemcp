---
name: "create_take_lane"
summary: ""
Live mapping: "- Calls `track.create_take_lane()` and optionally sets its `name`."
---

# create_take_lane

**Domain:** arrangement (take_lanes)

**Summary:** Create a new take lane on a track (Live 12+).

**Parameters:**

- `track_index` (int)
- `name` (string, optional)

**Live mapping:**

- Calls `track.create_take_lane()` and optionally sets its `name`.
  **Example request:**

```json
{ "action": "create_take_lane", "track_index": 1, "name": "Comp A" }
```

**Example response:**

```json
{ "ok": true, "message": "Take lane created", "name": "Comp A" }
```
