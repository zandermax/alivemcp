# rename_track

**Domain:** tracks

**Summary:** Rename a track by index.

**Parameters:**
- `track_index` (int)
- `name` (string)

**Live mapping:**
- Sets `song.tracks[track_index].name = name`.

**Example request:**
```json
{"action":"rename_track","track_index":1,"name":"Bass"}
```

**Example response:**
```json
{"ok": true, "message": "Track renamed", "name": "Bass"}
```

**Notes:**
- Validates the track index.

**See also:**
- [docs/wiki/tools/tracks/get_track_info.md](docs/wiki/tools/tracks/get_track_info.md)
