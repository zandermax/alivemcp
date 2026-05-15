---
name: "focus_track"
summary: ""
Live mapping: "- Sets `song.view.selected_track = track` when view selection is supported."
---

# focus_track

**Domain:** arrangement (view)

**Summary:** Focus/highlight a specific track in the UI view.

**Parameters:**

- `track_index` (int)

**Live mapping:**

- Sets `song.view.selected_track = track` when view selection is supported.
  **Example request:**

```json
{ "action": "focus_track", "track_index": 2 }
```

**Example response:**

```json
{ "ok": true, "track_index": 2, "message": "Track focused" }
```
