---
name: "set_track_device_param_by_name"
summary: ""
Live mapping: "- Finds the first parameter matching `param_name`. If `value` is string and parameter is quantized, looks up index in `param.value_items`. Otherwise clamps numeric values to `param.min`/`param.max` and sets `param.value`."
---

# set_track_device_param_by_name

**Domain:** tracks

**Summary:** Set a device parameter by name. For quantized parameters pass a string matching a `value_item`, otherwise pass a numeric value (clamped).

**Parameters:**

- `track_index` (int)
- `device_index` (int)
- `param_name` (string)
- `value` (string|number)

**Live mapping:**

- Finds the first parameter matching `param_name`. If `value` is string and parameter is quantized, looks up index in `param.value_items`. Otherwise clamps numeric values to `param.min`/`param.max` and sets `param.value`.
  **Example request:**

```json
{
  "action": "set_track_device_param_by_name",
  "track_index": 1,
  "device_index": 0,
  "param_name": "Mode",
  "value": "4:1"
}
```

**Example response:**

```json
{
  "ok": true,
  "track_index": 1,
  "device_name": "Compressor",
  "param_name": "Mode",
  "value": 3,
  "display_value": "4:1"
}
```
