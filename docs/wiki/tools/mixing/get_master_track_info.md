# get_master_track_info

**Domain:** mixing

**Summary:** Retrieve master track information: name, volume, pan, and device count.

**Parameters:**
- none

**Live mapping:**
- Reads `song.master_track` fields and `master.mixer_device` properties when available.

**Example request:**
```json
{"action":"get_master_track_info"}
```

**Example response:**
```json
{"ok": true, "name": "Master", "volume": 0.9, "pan": 0.0, "num_devices": 2}
```

**Notes:**
- Some hosts may not expose a `mixer_device` on the master track; feature-detect accordingly.

**See also:**
- [docs/wiki/tools/mixing/set_master_volume.md](docs/wiki/tools/mixing/set_master_volume.md)
- [docs/wiki/tools/mixing/get_master_devices.md](docs/wiki/tools/mixing/get_master_devices.md)
