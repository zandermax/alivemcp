# create_audio_track

**Domain:** tracks

**Summary:** Create a new audio track at the end of the track list.

**Parameters:**
- `name` (string, optional)

**Live mapping:**
- Calls `song.create_audio_track(index)` and sets `song.tracks[index].name` if provided.
**Example request:**
```json
{"action":"create_audio_track","name":"New Audio"}
```
**Example response:**
```json
{"ok": true, "message": "Audio track created", "track_index": 5, "name": "New Audio"}
```

**Notes:**
- Track is appended to the end of `song.tracks`.

**See also:**
- [create_midi_track](tools/tracks/create_midi_track.md)
- [duplicate_track](tools/tracks/duplicate_track.md)
