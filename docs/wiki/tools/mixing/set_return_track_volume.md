# set_return_track_volume

**Domain:** mixing

**Summary:** Set the volume for a return (send) track.

**Parameters:**
- `return_index` (int)
- `volume` (float)

**Live mapping:**
- Writes `song.return_tracks[return_index].mixer_device.volume.value = volume`.

**Example request:**
```json
{"action":"set_return_track_volume","return_index":0,"volume":0.7}
```

**Example response:**
```json
{"ok": true, "return_index":0, "volume":0.7}
```

**Notes:**
- Volume is clamped to a valid range and `return_index` is validated.

**See also:**
- [docs/wiki/tools/mixing/get_return_track_info.md](docs/wiki/tools/mixing/get_return_track_info.md)
