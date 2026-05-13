# get_build_id

Get Build ID

Get Ableton Live build identifier (Live 12+).

Parameters: None

Returns:
- `ok`: boolean
- `build_id`: string (when `ok` is true)

Notes:
- Requires Live 12+; the tool checks availability at runtime and returns an error if unavailable.

Example request:
```json
{"action": "get_build_id"}
```

