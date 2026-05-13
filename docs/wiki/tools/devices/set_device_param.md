# set_device_param

**Domain:** devices

**Summary:** Set a device parameter by numeric parameter index.

**Parameters:**
- `track_index` (int)
- `device_index` (int)
- `param_index` (int)
- `value` (number)

**Live mapping:**
- Writes `device.parameters[param_index].value = value` after validation.

**Example request:**
```json
{"action":"set_device_param","track_index":1,"device_index":0,"param_index":2,"value":0.5}
```

**Example response:**
```json
{"ok": true, "message": "Parameter set", "value": 0.5}
```

**Notes:**
- Parameter index must be valid for the device; value is cast to float.

**See also:**
- [get_device_parameters](tools/devices/get_device_parameters.md)
- [set_device_parameter_by_name](tools/devices/set_device_parameter_by_name.md)
