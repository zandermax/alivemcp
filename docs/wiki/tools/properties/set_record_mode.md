# set_record_mode

Set Record Mode

Set global record mode (0=session, 1=arrangement) when supported.

Parameters:
- `mode` (int): 0 for session, 1 for arrangement

Returns:
- `ok`: boolean
- `record_mode`: int (new value when set)

Example request:
```json
{"action": "set_record_mode", "mode": 1}
```

