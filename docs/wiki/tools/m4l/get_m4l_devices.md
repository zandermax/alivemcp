# get_m4l_devices

Get M4L Devices

List all Max for Live devices on a track.

Parameters:
- `track_index` (int)

Returns:
- `ok`: boolean
- `track_index`: int
- `track_name`: string
- `devices`: list of {index, name, class_name, type, is_active, num_parameters}
- `count`: int

Example request:
```json
{"action": "get_m4l_devices", "track_index": 0}
```
