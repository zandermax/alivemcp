---
name: "duplicate_clip"
summary: ""
Live mapping: "- Uses `clip_slot.duplicate_clip_to(dest_slot)` where `dest_slot` is the next empty `track.clip_slots` entry."
---

# duplicate_clip

**Domain:** clips

**Summary:** Duplicate a clip to the next available empty slot on the same track.

**Parameters:**

- `track_index` (int)
- `clip_index` (int)

**Live mapping:**

- Uses `clip_slot.duplicate_clip_to(dest_slot)` where `dest_slot` is the next empty `track.clip_slots` entry.
  **Example request:**

```json
{ "action": "duplicate_clip", "track_index": 1, "clip_index": 0 }
```

**Example response:**

```json
{
  "ok": true,
  "message": "Clip duplicated",
  "source_clip_index": 0,
  "destination_clip_index": 2
}
```

**Notes:**

- Fails if there is no empty slot after the source slot on the same track.

**See also:**

- [create_midi_clip](tools/clips/create_midi_clip.md)
- [delete_clip](tools/clips/delete_clip.md)
