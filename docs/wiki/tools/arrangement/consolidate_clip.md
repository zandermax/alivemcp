# consolidate_clip

**Domain:** arrangement

**Summary:** Request consolidation of arrangement clips in a time range.

**Parameters:**
- `track_index` (int)
- `start_time` (float)
- `end_time` (float)

**Live mapping:**
- Current implementation returns a confirmation message; full consolidation uses host APIs where available.
**Example request:**
```json
{"action":"consolidate_clip","track_index":0,"start_time":0.0,"end_time":4.0}
```
**Example response:**
```json
{"ok": true, "message": "Clip consolidation initiated","start_time":0.0,"end_time":4.0}
```
