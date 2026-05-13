# set_master_device_param

Set Master Device Param

Set a device parameter on the master track by index.

Parameters:
- `device_index` (int)
- `param_index` (int)
- `value` (number or string for quantized params)

Returns:
- `ok`: boolean
- `device_name`: string
- `param_name`: string
- `value`: float

**Example request:**

```json
{"action": "set_master_device_param", "device_index": 0, "param_index": 1, "value": 0.5}
```

**Example response:**

```json
{"ok": true}
```


