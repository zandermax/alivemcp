# set_device_parameter_by_name

**Domain:** devices

**Summary:** Set a device parameter by name. Supports quantized string value lookups and numeric clamping.

**Parameters:**
- `track_index` (int)
- `device_index` (int)
- `param_name` (string)
- `value` (string|number)

**Live mapping:**
- Finds parameter by name; if `value` is a string it looks up `param.value_items` and sets the parameter index; otherwise clamps numeric value to `param.min`/`param.max` and writes `param.value`.

**Example request (numeric):**
```json
{"action":"set_device_parameter_by_name","track_index":1,"device_index":0,"param_name":"Drive","value":0.8}
```

**Example request (quantized):**
```json
{"action":"set_device_parameter_by_name","track_index":1,"device_index":0,"param_name":"Mode","value":"Classic"}
```

**Example response:**
```json
{"ok": true, "name": "Drive", "value": 0.8, "display_value": "0.8"}
```

**Notes:**
- Returns clear errors when string lookups fail or parameter has no `value_items`.

**See also:**
- [docs/wiki/tools/devices/get_device_parameter_by_name.md](docs/wiki/tools/devices/get_device_parameter_by_name.md)
- [docs/wiki/tools/devices/set_device_param.md](docs/wiki/tools/devices/set_device_param.md)
