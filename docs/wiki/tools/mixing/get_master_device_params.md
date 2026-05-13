# get_master_device_params

Get Master Device Params

Get enriched parameter info for a device on the master track.

Parameters:
- `device_index` (int)

Returns:
- `ok`: boolean
- `device_name`: string
- `count`: int
- `parameters`: list of {index, name, raw_value, display_value, min, max, is_quantized, value_items}

Example request:
```json
{"action": "get_master_device_params", "device_index": 0}
```

