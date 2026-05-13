# get_track_is_grouped

**Domain:** tracks

**Summary:** Check if a track is part of a group and whether it is a group track.

**Parameters:**
- `track_index` (int)

**Live mapping:**
- Uses `hasattr(track, "group_track")` and `hasattr(track, "is_foldable")` to determine grouping and foldability; returns `group_track_index` when available.
**Example request:**
```json
{"action": "get_track_is_grouped", "track_index": 2}
```
**Example response:**
```json
{"ok": true, "track_index": 2, "is_grouped": true, "is_group_track": false, "group_track_index": 5}
```
