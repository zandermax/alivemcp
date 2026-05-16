---
name: "add_notes"
summary: ""
Live mapping: "- Uses `clip.set_notes(((pitch, start, duration, velocity, muted),))` for each note on the Live clip object."
---

# add_notes

**Domain:** midi (clip MIDI notes)

**Summary:** Add MIDI notes to an existing MIDI clip.

**Parameters:**

- `track_index` (int)
- `clip_index` (int)
- `notes` (list of dicts) — each with `pitch`, `start`, `duration`, `velocity`, optional `muted`

**Live mapping:**

- Uses `clip.set_notes(((pitch, start, duration, velocity, muted),))` for each note on the Live clip object.
  **Example request:**

```json
{
  "action": "add_notes",
  "track_index": 1,
  "clip_index": 0,
  "notes": [{ "pitch": 60, "start": 0.0, "duration": 1.0, "velocity": 100 }]
}
```

**Example response:**

```json
{
  "ok": true,
  "message": "Notes added",
  "track_index": 1,
  "clip_index": 0,
  "note_count": 1
}
```

**Notes:**

- Validates MIDI range (pitch 0-127, velocity 0-127) and that the target clip is a MIDI clip.

**See also:**

- [get_clip_notes](tools/midi/get_clip_notes.md)
- [remove_notes](tools/midi/remove_notes.md)
