# group_tracks

**Domain:** tracks

**Summary:** Group tracks between `start_index` and `end_index` (inclusive) by creating a group track.

**Parameters:**
- `start_index` (int)
- `end_index` (int)

**Live mapping:**
- Validates indices and calls `self.song.create_group_track(end_index + 1)` to create a group track covering the range.
**Example request:**
```json
{"action": "group_tracks", "start_index": 1, "end_index": 3}
```
**Example response:**
```json
{"ok": true, "message": "Tracks grouped", "start_index": 1, "end_index": 3}
```
