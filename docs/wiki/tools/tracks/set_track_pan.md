# set_track_pan

**Domain:** tracks

**Summary:** Set a track's pan (-1.0 to 1.0).

**Parameters:**
- `track_index` (int)
- `pan` (float) — -1.0 (left) to 1.0 (right)

**Live mapping:**
- Writes `track.mixer_device.panning.value = pan`.

**Example request:**
```json
{"action":"set_track_pan","track_index":1,"pan":0.0}
```

**Example response:**
```json
{"ok": true, "message": "Track pan set", "track_index": 1, "pan": 0.0}
```

**Notes:**
- Pan is clamped to [-1.0, 1.0]; returns error otherwise.

**See also:**
- [set_track_volume](tools/tracks/set_track_volume.md)
- [get_track_info](tools/tracks/get_track_info.md)
