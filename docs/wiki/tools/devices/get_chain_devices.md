# get_chain_devices

**Domain:** devices (racks)

**Summary:** List devices in a specific chain of a rack.

**Parameters:**
- `track_index` (int)
- `device_index` (int)
- `chain_index` (int)

**Live mapping:**
- Reads `device.chains[chain_index].devices` and returns `name`, `class_name`, and `is_active` for each device.

**Example request:**
```json
{"action":"get_chain_devices","track_index":1,"device_index":0,"chain_index":0}
```

**Example response:**
```json
{"ok": true, "chain_index":0, "devices":[{"name":"Synth","class_name":"Operator","is_active":true}], "count":1}
```

**Notes:**
- Validates chain existence and returns clear errors if the target is not a rack.

**See also:**
- [get_device_chains](tools/devices/get_device_chains.md)
- [set_chain_mute](tools/devices/set_chain_mute.md)
- [set_chain_solo](tools/devices/set_chain_solo.md)
