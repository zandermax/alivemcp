# set_chain_solo

**Domain:** devices (racks)

**Summary:** Solo or unsolo a chain inside a rack device.

**Parameters:**
- `track_index` (int)
- `device_index` (int)
- `chain_index` (int)
- `solo` (bool)

**Live mapping:**
- Sets `chain.solo = solo` when `chain` exposes a `solo` attribute.

**Example request:**
```json
{"action":"set_chain_solo","track_index":1,"device_index":0,"chain_index":0,"solo":true}
```

**Example response:**
```json
{"ok": true, "chain_index":0, "solo": true}
```

**Notes:**
- Returns an error if the device is not a rack or chain solo is unsupported.

**See also:**
- [docs/wiki/tools/devices/set_chain_mute.md](docs/wiki/tools/devices/set_chain_mute.md)
