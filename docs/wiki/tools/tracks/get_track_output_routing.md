# get_track_output_routing

**Domain:** tracks

**Summary:** Get output routing configuration for a track (type and channel when available).

**Parameters:**
- `track_index` (int)

**Live mapping:**
- Reads `track.output_routing_type` and `track.output_routing_channel` when present and returns display names or string values.

**Example request:**
```json
{"action": "get_track_output_routing", "track_index": 1}
```

**Example response:**
```json
{"ok": true, "track_index": 1, "track_name": "Lead", "output_routing_type": "Master", "output_routing_channel": "Stereo"}
```
