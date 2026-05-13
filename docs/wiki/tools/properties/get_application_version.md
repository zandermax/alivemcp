# get_application_version

Get Application Version

Get full Ableton Live version information.

Parameters: None

Returns:
- `ok`: boolean
- `major_version`: int
- `minor_version`: int
- `bugfix_version`: int
- `build_id`: string (optional)
- `variant`: string (optional)

Example request:
```json
{"action": "get_application_version"}
```
