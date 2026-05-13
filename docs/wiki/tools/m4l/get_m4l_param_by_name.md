# get_m4l_param_by_name

Get M4L Param By Name

Get a parameter value from a Max for Live device by parameter name.

Parameters:
- `track_index` (int)
- `device_index` (int)
- `param_name` (string)

Returns:
- `ok`: boolean
- `param_index`: int
- `name`: string
- `value`: float
- `min`: float
- `max`: float
- `is_enabled`: boolean

**Example request:**
```json
{"action": "get_m4l_param_by_name", "track_index": 0, "device_index": 0, "param_name": "Rate"}
```

**Example request:**
```json
{"ok": true, "param_index": 1, "name": "Rate", "value": 0.5, "min": 0.0, "max": 1.0, "is_enabled": true}
```

