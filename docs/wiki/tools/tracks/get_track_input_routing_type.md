# get_track_input_routing_type

**Domain:** tracks

**Summary:** Get the current input routing type for a track (display name when available).

**Parameters:**
- `track_index` (int)

**Live mapping:**
- If `track.input_routing_type` exists, returns its `display_name` or string representation.
**Example request:**
```json
{"action": "get_track_input_routing_type", "track_index": 1}
```
**Example response:**
```json
{"ok": true, "routing_type": "All Ins"}
```
