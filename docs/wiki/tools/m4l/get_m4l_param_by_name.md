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

Example request:
```json
{"action": "get_m4l_param_by_name", "track_index": 0, "device_index": 0, "param_name": "Rate"}
```
