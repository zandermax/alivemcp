# get_track_sends

**Domain:** mixing

**Summary:** Retrieve all send levels for a track.

**Parameters:**
- `track_index` (int)

**Live mapping:**
- Iterates `track.mixer_device.sends` returning `index`, `value`, and `name` when available.

**Example request:**
```json
{"action":"get_track_sends","track_index":1}
```

**Example response:**
```json
{"ok": true, "track_index":1, "sends": [{"index":0,"value":0.5,"name":"A"}], "count":1}
```

**Notes:**
- Names may be synthesized ("Send A", "Send B") if not exposed by the Live object.

**See also:**
- [docs/wiki/tools/mixing/set_track_send.md](docs/wiki/tools/mixing/set_track_send.md)
