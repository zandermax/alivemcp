# get_master_devices

**Domain:** mixing

**Summary:** List devices present on the master track.

**Parameters:**
- none

**Live mapping:**
- Iterates `song.master_track.devices` and returns `name`, `class_name`, and `is_active`.
**Example request:**
```json
{"action":"get_master_devices"}
```
**Example response:**
```json
{"ok": true, "devices": [{"name":"Limiter","class_name":"Limiter","is_active":true}], "count":1}
```

**Notes:**
- Some Live versions may omit master devices; feature-detect before use.

**See also:**
- [get_master_track_info](tools/mixing/get_master_track_info.md)
