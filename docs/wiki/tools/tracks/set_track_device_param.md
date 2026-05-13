# set_track_device_param

**Domain:** tracks

**Summary:** Set a device parameter value by index on a track, clamped to the parameter's min/max.

**Parameters:**
- `track_index` (int)
- `device_index` (int)
- `param_index` (int)
- `value` (number)

**Live mapping:**
- Validates indices, clamps `value` to `param.min`/`param.max`, and sets `param.value`.
**Example request:**
```json
{"action": "set_track_device_param", "track_index": 1, "device_index": 0, "param_index": 2, "value": 0.75}
```
**Example response:**
```json
{"ok": true, "track_index": 1, "device_name": "EQ","param_name":"Freq","value": 0.75}
```
