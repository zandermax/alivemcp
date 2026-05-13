# get_device_param_display_value

**Domain:** devices

**Summary:** Read a device parameter's UI display string and raw numeric value.

**Parameters:**
- `track_index` (int)
- `device_index` (int)
- `param_index` (int)

**Live mapping:**
- Reads `param.display_value` (Live 12+) when available, falls back to `str(param)` and returns `raw_value`.

**Example request:**
```json
{"action": "get_device_param_display_value", "track_index": 1, "device_index": 0, "param_index": 2}
```

**Example response:**
```json
{"ok": true, "display_value": "-6.0 dB","raw_value": 0.5, "name": "Gain"}
```

**Notes:**
- Use this to show human-friendly parameter text without recomputing formatting client-side.

**See also:**
- get_all_param_display_values
