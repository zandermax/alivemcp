# unfreeze_track

**Domain:** tracks

**Summary:** Unfreeze a frozen track.

**Parameters:**
- `track_index` (int)

**Live mapping:**
- If `track.freeze_state` is present, sets `track.freeze_state = 0`.
**Example request:**
```json
{"action": "unfreeze_track", "track_index": 1}
```
**Example response:**
```json
{"ok": true, "track_index": 1, "frozen": false}
```
