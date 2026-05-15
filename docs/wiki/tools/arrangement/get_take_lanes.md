---
name: "get_take_lanes"
summary: ""
Live mapping: "- Iterates `track.take_lanes` when available and returns index/name."
---

# get_take_lanes

**Domain:** arrangement (take_lanes)

**Summary:** List take lanes for a track (Live 12+).

**Parameters:**

- `track_index` (int)

**Live mapping:**

- Iterates `track.take_lanes` when available and returns index/name.
  **Example request:**

```json
{ "action": "get_take_lanes", "track_index": 1 }
```

**Example response:**

```json
{ "ok": true, "count": 2, "take_lanes": [{ "index": 0, "name": "Take 1" }] }
```
