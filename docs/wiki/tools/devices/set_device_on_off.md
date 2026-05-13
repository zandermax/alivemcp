# set_device_on_off

**Domain:** devices

**Summary:** Turn a device on or off (if supported).

**Parameters:**
- `track_index` (int)
- `device_index` (int)
- `enabled` (bool)

**Live mapping:**
- Sets `device.is_active = enabled` when the `is_active` attribute exists.

**Example request:**
```json
{"action":"set_device_on_off","track_index":1,"device_index":0,"enabled":false}
```

**Example response:**
```json
{"ok": true, "is_active": false}
```

**Notes:**
- Returns an error if the device doesn't support on/off.

**See also:**
- [docs/wiki/tools/devices/get_track_devices.md](docs/wiki/tools/devices/get_track_devices.md)
