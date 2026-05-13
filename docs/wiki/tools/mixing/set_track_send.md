# set_track_send

**Domain:** mixing

**Summary:** Set a track's send level for a given send index.

**Parameters:**
- `track_index` (int)
- `send_index` (int)
- `value` (float) — typically 0.0–1.0

**Live mapping:**
- Writes `track.mixer_device.sends[send_index].value = value` on the Live Object Model.

**Example request:**
```json
{"action":"set_track_send","track_index":1,"send_index":0,"value":0.5}
```

**Example response:**
```json
{"ok": true, "send_index": 0, "value": 0.5}
```

**Notes:**
- Validates send index and track index; values are cast to float.

**See also:**
- [get_track_sends](tools/mixing/get_track_sends.md)
