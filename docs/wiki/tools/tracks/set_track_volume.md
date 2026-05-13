# set_track_volume

**Domain:** tracks

**Summary:** Set a track's mixer volume (0.0–1.0).

**Parameters:**
- `track_index` (int)
- `volume` (float) — 0.0 to 1.0

**Live mapping:**
- Writes `track.mixer_device.volume.value = volume`.

**Example request:**
```json
{"action":"set_track_volume","track_index":1,"volume":0.8}
```

**Example response:**
```json
{"ok": true, "message": "Track volume set", "track_index": 1, "volume": 0.8}
```

**Notes:**
- Volume is clamped to [0.0, 1.0]; returns error otherwise.

**See also:**
- [set_track_pan](tools/tracks/set_track_pan.md)
- [get_track_info](tools/tracks/get_track_info.md)
