# get_device_class_name

**Domain:** devices

**Summary:** Return the device's class name (implementation class, e.g., OriginalSimpler).

**Parameters:**
- `track_index` (int)
- `device_index` (int)

**Live mapping:**
- Reads `device.class_name` and returns it as a string when available.
**Example request:**
```json
{"action":"get_device_class_name","track_index":1,"device_index":0}
```
**Example response:**
```json
{"ok": true, "class_name": "OriginalSimpler"}
```

**Notes:**
- Useful for feature detection and device-specific handling.

**See also:**
- [get_device_type](tools/devices/get_device_type.md)
