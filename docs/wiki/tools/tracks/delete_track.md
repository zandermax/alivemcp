---
name: "delete_track"
summary: ""
Live mapping: "- Calls `song.delete_track(track_index)` on the Live Object Model."
---

# delete_track

**Domain:** tracks

**Summary:** Delete a track by index.

**Parameters:**

- `track_index` (int)

**Live mapping:**

- Calls `song.delete_track(track_index)` on the Live Object Model.
  **Example request:**

```json
{ "action": "delete_track", "track_index": 3 }
```

**Example response:**

```json
{ "ok": true, "message": "Track deleted" }
```

**Notes:**

- Validates the index; returns an error for invalid indexes.

**See also:**

- [duplicate_track](tools/tracks/duplicate_track.md)
- [rename_track](tools/tracks/rename_track.md)
