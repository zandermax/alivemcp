# get_device_chains

**Domain:** devices (racks)

**Summary:** Get chains from a rack device (e.g., instrument/effect rack).

**Parameters:**
- `track_index` (int)
- `device_index` (int)

**Live mapping:**
- Checks `device.chains` and returns per-chain metadata: `index`, `name`, `mute`, `solo`, and `num_devices`.
**Example request:**
```json
{"action":"get_device_chains","track_index":1,"device_index":0}
```
**Example response:**
```json
{"ok": true, "chains": [{"index":0,"name":"Chain 1","mute":false,"solo":false,"num_devices":2}], "count":1}
```

**Notes:**
- Returns an error if the device has no `chains` attribute (not a rack).

**See also:**
- [get_chain_devices](tools/devices/get_chain_devices.md)
