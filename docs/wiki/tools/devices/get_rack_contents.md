# get_rack_contents

**Domain:** devices (rack contents)

**Summary:** Retrieve the contents of a rack (chains and chain devices) for inspection.

**Parameters:**
- `track_index` (int)
- `device_index` (int)

**Live mapping:**
- Uses `device.chains` and `chain.devices` to build a nested representation of rack contents.
**Example request:**
```json
{"action":"get_rack_contents","track_index":1,"device_index":0}
```
**Example response:**
```json
{"ok": true, "rack_contents": {"chains": [{"index":0,"name":"Chain 1","devices":[{"name":"Synth","class_name":"Operator"}]}]}}
```

**Notes:**
- Useful for inspecting complex rack structures programmatically.

**See also:**
- [get_device_chains](tools/devices/get_device_chains.md)
