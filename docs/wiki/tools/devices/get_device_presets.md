# get_device_presets

**Domain:** devices

**Summary:** Return available presets for a device (browser API required for full implementation).

**Parameters:**
- `track_index` (int)
- `device_index` (int)

**Live mapping:**
- Currently acknowledges the request; enumerating presets requires the Live browser API.

**Example request:**
```json
{"action":"get_device_presets","track_index":1,"device_index":0}
```

**Example response:**
```json
{"ok": true, "message": "Device preset browsing requires browser API", "device_index": 0}
```

**Notes:**
- See `set_device_preset` for the companion action.

**See also:**
- [docs/wiki/tools/devices/set_device_preset.md](docs/wiki/tools/devices/set_device_preset.md)
