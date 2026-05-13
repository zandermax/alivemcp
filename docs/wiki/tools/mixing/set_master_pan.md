# set_master_pan

**Domain:** mixing

**Summary:** Set the master track pan (-1.0 to 1.0).

**Parameters:**
- `pan` (float)

**Live mapping:**
- Writes `song.master_track.mixer_device.panning.value = pan` when available.

**Example request:**
```json
{"action":"set_master_pan","pan":0.0}
```

**Example response:**
```json
{"ok": true, "pan": 0.0}
```

**Notes:**
- Returns an error when the master mixer device is not available.

**See also:**
- [get_master_track_info](tools/mixing/get_master_track_info.md)
