---
name: "set_master_device_param_by_name"
summary: ""
---

# set_master_device_param_by_name

Set Master Device Param By Name

Set a master track device parameter by name. For quantized parameters pass a string matching a `value_item`.

Parameters:

- `device_index` (int)
- `param_name` (string)
- `value` (number|string)

Returns:

- `ok`: boolean
- `device_name`: string
- `param_name`: string
- `value`: float
- `display_value`: string

**Example request:**

```json
{
  "action": "set_master_device_param_by_name",
  "device_index": 0,
  "param_name": "Ratio",
  "value": "4:1"
}
```

**Example response:**

```json
{ "ok": true }
```
