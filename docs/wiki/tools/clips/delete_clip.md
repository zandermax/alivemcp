---
name: "delete_clip"
summary: ""
Live mapping: "- Calls `clip_slot.delete_clip()` on the Live Object Model."
---

# delete_clip

**Domain:** clips

**Summary:** Delete a clip from a clip slot.

**Parameters:**

- `track_index` (int)
- `clip_index` (int)

**Live mapping:**

- Calls `clip_slot.delete_clip()` on the Live Object Model.
  **Example request:**

```json
{ "action": "delete_clip", "track_index": 1, "clip_index": 0 }
```

**Example response:**

```json
{ "ok": true, "message": "Clip deleted" }
```

**Notes:**

- Returns an error if no clip exists in the specified slot.

**See also:**

- [create_midi_clip](tools/clips/create_midi_clip.md)
- [duplicate_clip](tools/clips/duplicate_clip.md)
