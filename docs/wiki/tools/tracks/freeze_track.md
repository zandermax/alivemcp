# freeze_track

**Domain:** tracks

**Summary:** Freeze a track if freeze is available to reduce CPU usage.

**Parameters:**
- `track_index` (int)

**Live mapping:**
- If `track.freeze_available` and `track.freeze_state` are present, sets `track.freeze_state = 1`.
**Example request:**
```json
{"action": "freeze_track", "track_index": 1}
```
**Example response:**
```json
{"ok": true, "track_index": 1, "frozen": true}
```
