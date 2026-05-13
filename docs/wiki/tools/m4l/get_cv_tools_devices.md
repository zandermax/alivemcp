# get_cv_tools_devices

Get CV (Control Voltage) Tools Devices

List CV (Control Voltage) Tools devices on a track (heuristic by name).

Parameters:
- `track_index` (int)

Returns:
- `ok`: boolean
- `track_index`: int
- `track_name`: string
- `cv_devices`: list of {index, name, class_name, is_active, num_parameters}
- `count`: int

Example request:
```json
{"action": "get_cv_tools_devices", "track_index": 0}
```

