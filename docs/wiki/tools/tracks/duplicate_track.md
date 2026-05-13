# duplicate_track

**Domain:** tracks

**Summary:** Duplicate a track by index.

**Parameters:**
- `track_index` (int)

**Live mapping:**
- Calls `song.duplicate_track(track_index)` which creates a copy next to the source.

**Example request:**
```json
{"action":"duplicate_track","track_index":2}
```

**Example response:**
```json
{"ok": true, "message": "Track duplicated", "new_index": 3}
```

**Notes:**
- May duplicate devices, clips, and automation depending on Live's behavior.

**See also:**
- [docs/wiki/tools/tracks/create_midi_track.md](docs/wiki/tools/tracks/create_midi_track.md)
- [docs/wiki/tools/tracks/get_track_info.md](docs/wiki/tools/tracks/get_track_info.md)
