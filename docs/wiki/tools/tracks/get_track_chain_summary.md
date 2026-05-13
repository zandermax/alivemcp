# get_track_chain_summary

**Domain:** tracks

**Summary:** Return a summary of all devices on a track with enriched parameter lists for each device.

**Parameters:**
- `track_index` (int)

**Live mapping:**
- Iterates devices and their parameters, returning `index`, `name`, `class_name`, `is_active` and full enriched `parameters` arrays.

**Example request:**
```json
{"action": "get_track_chain_summary", "track_index": 1}
```

**Example response:**
```json
{"ok": true, "track_index": 1, "track_name": "Lead", "count": 2, "devices": [{"index":0,"name":"AutoFilter","class_name":"AutoFilterDevice","is_active":true,"parameters":[]}]}
```
