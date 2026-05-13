# get_device_parameters

**Domain:** devices

**Summary:** Enumerate parameters for a device with metadata (index, name, value, min, max).

**Parameters:**
- `track_index` (int)
- `device_index` (int)

**Live mapping:**
- Iterates `device.parameters` and returns `index`, `name`, `value`, `min`, `max`, `is_quantized`, and `is_enabled` where available.

**Example request:**
```json
{"action":"get_device_parameters","track_index":1,"device_index":0}
```

**Example response:**
```json
{"ok": true, "track_index":1, "device_index":0, "parameters": [{"index":0,"name":"Gain","value":0.5,"min":0.0,"max":1.0}], "count":1}
```

**Notes:**
- Useful to discover parameter indexes before using `set_device_param`.

**See also:**
- [docs/wiki/tools/devices/get_device_parameter_by_name.md](docs/wiki/tools/devices/get_device_parameter_by_name.md)
- [docs/wiki/tools/devices/set_device_param.md](docs/wiki/tools/devices/set_device_param.md)
