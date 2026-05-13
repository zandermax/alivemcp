# set_chain_mute

**Domain:** devices (racks)

**Summary:** Mute or unmute a chain inside a rack device.

**Parameters:**
- `track_index` (int)
- `device_index` (int)
- `chain_index` (int)
- `mute` (bool)

**Live mapping:**
- Sets `chain.mute = mute` when `chain` exposes a `mute` attribute.
**Example request:**
```json
{"action":"set_chain_mute","track_index":1,"device_index":0,"chain_index":0,"mute":true}
```
**Example response:**
```json
{"ok": true, "chain_index":0, "mute": true}
```

**Notes:**
- Returns an error if the device is not a rack or chain mute is unsupported.

**See also:**
- [set_chain_solo](tools/devices/set_chain_solo.md)
