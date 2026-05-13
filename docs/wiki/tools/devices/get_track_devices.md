# get_track_devices

**Domain:** devices

**Summary:** List devices on a track with basic metadata.

**Parameters:**
- `track_index` (int)

**Live mapping:**
- Iterates `song.tracks[track_index].devices` and reads `device.name`, `device.class_name`, `device.is_active`, and `len(device.parameters)`.
**Example request:**
```json
{"action":"get_track_devices","track_index":1}
```
**Example response:**
```json
{"ok": true, "track_index": 1, "devices": [{"name":"Compressor","class_name":"Compressor2","is_active":true,"num_parameters":12}], "count":1}
```

**Notes:**
- Useful for discovering device indexes before setting parameters.

**See also:**
- [add_device](tools/devices/add_device.md)
- [get_device_parameters](tools/devices/get_device_parameters.md)
