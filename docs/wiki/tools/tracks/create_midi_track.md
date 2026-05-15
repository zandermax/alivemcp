---
name: "create_midi_track"
summary: ""
Live mapping: "- Calls `song.create_midi_track(index)` and sets `song.tracks[index].name` if provided."
---

# create_midi_track

**Domain:** tracks

**Summary:** Create a new MIDI track at the end of the track list.

**Parameters:**

- `name` (string, optional) — set the track name after creation

**Live mapping:**

- Calls `song.create_midi_track(index)` and sets `song.tracks[index].name` if provided.
  **Example request:**

```json
{ "action": "create_midi_track", "name": "New MIDI" }
```

**Example response:**

```json
{
  "ok": true,
  "message": "MIDI track created",
  "track_index": 5,
  "name": "New MIDI"
}
```

**Notes:**

- Track is appended to the end of `song.tracks`.

**See also:**

- [create_audio_track](tools/tracks/create_audio_track.md)
- [duplicate_track](tools/tracks/duplicate_track.md)
