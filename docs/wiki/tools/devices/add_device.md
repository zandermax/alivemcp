# add_device

**Domain:** devices

**Summary:** Request adding a device to a track (browser API required for full implementation).

**Parameters:**
- `track_index` (int)
- `device_name` (string) — friendly name or identifier for the device to add

**Live mapping:**
- Currently returns a request acknowledgement; adding devices via the Live browser requires the browser API and is not fully implemented.
**Example request:**
```json
{"action":"add_device","track_index":1,"device_name":"Compressor"}
```
**Example response:**
```json
{"ok": true, "message": "Device add requested (browser API required for full implementation)", "device_name": "Compressor"}
```

**Notes:**
- This endpoint signals intent; actual device insertion via Live's browser is platform-dependent and requires additional browser integration.

**See also:**
- [get_track_devices](tools/devices/get_track_devices.md)
- [get_device_presets](tools/devices/get_device_presets.md)
