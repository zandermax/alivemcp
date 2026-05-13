# get_arrangement_clips

**Domain:** arrangement

**Summary:** List arrangement-view clips for a track with start/end/length.

**Parameters:**
- `track_index` (int)

**Live mapping:**
- Iterates `track.arrangement_clips` returning name, start_time, end_time, length.
**Example request:**
```json
{"action":"get_arrangement_clips","track_index":1}
```
**Example response:**
```json
{"ok": true, "count":2, "clips":[{"name":"Intro","start_time":0.0,"end_time":16.0,"length":16.0}]}
```
