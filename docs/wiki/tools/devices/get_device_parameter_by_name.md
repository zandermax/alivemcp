---
name: "get_device_parameter_by_name"
summary: ""
Live mapping: "- Iterates `device.parameters` and returns the first matching parameter by `str(param.name)`."
---

# get_device_parameter_by_name

**Domain:** devices

**Summary:** Lookup a device parameter by exact name and return its index and value range.

**Parameters:**

- `track_index` (int)
- `device_index` (int)
- `param_name` (string)

**Live mapping:**

- Iterates `device.parameters` and returns the first matching parameter by `str(param.name)`.
  **Example request:**

```json
{
  "action": "get_device_parameter_by_name",
  "track_index": 1,
  "device_index": 0,
  "param_name": "Cutoff"
}
```

**Example response:**

```json
{
  "ok": true,
  "index": 2,
  "name": "Cutoff",
  "value": 0.5,
  "min": 0.0,
  "max": 1.0
}
```

**Notes:**

- Exact string match is used; consider `get_device_parameters` to inspect available names.

**See also:**

- [set_device_parameter_by_name](tools/devices/set_device_parameter_by_name.md)
