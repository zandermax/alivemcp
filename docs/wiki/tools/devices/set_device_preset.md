# set_device_preset

**Domain:** devices

**Summary:** Request loading a device preset by index (browser API required for full implementation).

**Parameters:**
- `track_index` (int)
- `device_index` (int)
- `preset_index` (int)

**Live mapping:**
- Acknowledges preset load intent; actual preset loading requires the Live browser API.

**Example request:**
```json
{"action":"set_device_preset","track_index":1,"device_index":0,"preset_index":2}
```

**Example response:**
```json
{"ok": true, "message": "Device preset loading requires browser API", "preset_index": 2}
```

**Notes:**
- Prefetching or browsing presets is outside the current remote script's scope without browser integration.

**See also:**
- [get_device_presets](tools/devices/get_device_presets.md)
