# randomize_device_parameters

**Domain:** devices

**Summary:** Randomize all (continuous) parameters of a device.

**Parameters:**
- `track_index` (int)
- `device_index` (int)

**Live mapping:**
- Iterates `device.parameters` and assigns random values within `param.min` and `param.max` for enabled, non-quantized parameters.

**Example request:**
```json
{"action":"randomize_device_parameters","track_index":1,"device_index":0}
```

**Example response:**
```json
{"ok": true, "track_index":1, "device_index":0, "device_name":"Filter","randomized_parameters":5}
```

**Notes:**
- Skips quantized parameters and parameters that cannot be randomized safely.

**See also:**
- [randomize_device](tools/devices/randomize_device.md)
