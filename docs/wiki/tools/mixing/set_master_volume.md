# set_master_volume

**Domain:** mixing

**Summary:** Set the master track volume (0.0–1.0).

**Parameters:**
- `volume` (float)

**Live mapping:**
- Writes `song.master_track.mixer_device.volume.value = volume` when available.

**Example request:**
```json
{"action":"set_master_volume","volume":0.8}
```

**Example response:**
```json
{"ok": true, "volume": 0.8}
```

**Notes:**
- Returns an error when the master mixer device is not available.

**See also:**
- [docs/wiki/tools/mixing/get_master_track_info.md](docs/wiki/tools/mixing/get_master_track_info.md)
