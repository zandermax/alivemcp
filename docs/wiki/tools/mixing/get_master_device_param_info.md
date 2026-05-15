---
name: "get_master_device_param_info"
summary: ""
---

# get_master_device_param_info

Get Master Device Param Info

Get enriched info for a single master track device parameter by name.

Parameters:

- `device_index` (int)
- `param_name` (string)

Returns:

- `ok`: boolean
- `device_name`: string
- `index`: int
- `name`: string
- `raw_value`: float
- `display_value`: string
- `min`: float
- `max`: float
- `is_quantized`: boolean
- `value_items`: list

**Example request:**

```json
{
  "action": "get_master_device_param_info",
  "device_index": 0,
  "param_name": "Threshold"
}
```

**Example response:**

```json
{ "ok": true }
```
