# randomize_device

**Domain:** devices

**Summary:** Randomize a device's parameters (delegated by `randomize_device_parameters`).

**Parameters:**
- `track_index` (int)
- `device_index` (int)

**Live mapping:**
- Randomizes enabled, non-quantized parameters using uniform random sampling between `param.min` and `param.max`.
**Example request:**
```json
{"action":"randomize_device","track_index":1,"device_index":0}
```
**Example response:**
```json
{"ok": true, "track_index":1, "device_index":0, "device_name":"Synth","randomized_parameters":7}
```

**Notes:**
- Deterministic behavior isn't guaranteed; randomness is useful for creative exploration but should be used carefully in performance contexts.

**See also:**
- [randomize_device_parameters](tools/devices/randomize_device_parameters.md)
