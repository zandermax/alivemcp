# solo_track

**Domain:** tracks

**Summary:** Solo or unsolo a track.

**Parameters:**
- `track_index` (int)
- `solo` (bool, default=true)

**Live mapping:**
- Sets `song.tracks[track_index].solo = solo`.

**Example request:**
```json
{"action":"solo_track","track_index":1,"solo":true}
```

**Example response:**
```json
{"ok": true, "message": "Track soloed"}
```

**Notes:**
- Use with caution in live contexts; other track solo states are unaffected.

**See also:**
- [docs/wiki/tools/tracks/mute_track.md](docs/wiki/tools/tracks/mute_track.md)
- [docs/wiki/tools/tracks/get_track_info.md](docs/wiki/tools/tracks/get_track_info.md)
