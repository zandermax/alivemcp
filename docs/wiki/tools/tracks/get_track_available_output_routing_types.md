# get_track_available_output_routing_types

**Domain:** tracks

**Summary:** Return available output routing types for a track (display names).

**Parameters:**
- `track_index` (int)

**Live mapping:**
- If `track.available_output_routing_types` is present, collects `routing.display_name` for each available routing.
**Example request:**
```json
{"action": "get_track_available_output_routing_types", "track_index": 1}
```
**Example response:**
```json
{"ok": true, "routing_types": ["Master", "Return 1"], "count": 2}
```
