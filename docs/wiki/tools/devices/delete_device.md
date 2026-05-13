# delete_device

**Domain:** devices

**Summary:** Delete a device from a track.

**Parameters:**
- `track_index` (int)
- `device_index` (int)

**Live mapping:**
- Calls `track.delete_device(device_index)` to remove the device.
**Example request:**
```json
{"action":"delete_device","track_index":1,"device_index":0}
```
**Example response:**
```json
{"ok": true, "message": "Device deleted"}
```

**Notes:**
- Validates indexes and returns errors for invalid targets.

**See also:**
- [get_track_devices](tools/devices/get_track_devices.md)
