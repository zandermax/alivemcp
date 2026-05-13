# set_device_param_by_name (M4L alias)

**Domain:** m4l / devices

**Summary:** Alias used by Max for Live tools to set device parameter by name (delegates to device parameter name setter where available).

**Parameters:**
- `track_index` (int)
- `device_index` (int)
- `param_name` (string)
- `value` (string|number)

**Live mapping:**
- Implemented in M4L mixin (`m4l_devices`) and sets parameter values by name when supported.

**Example request:**
```json
{"action":"set_device_param_by_name","track_index":1,"device_index":0,"param_name":"Cutoff","value":0.7}
```

**Example response:**
```json
{"ok": true, "name": "Cutoff", "value": 0.7}
```

**Notes:**
- Prefer `set_device_parameter_by_name` for the canonical API; this alias exists for legacy M4L clients.

**See also:**
- [set_device_parameter_by_name](tools/devices/set_device_parameter_by_name.md)
