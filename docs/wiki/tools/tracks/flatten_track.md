# flatten_track

**Domain:** tracks

**Summary:** Flatten a frozen track into audio if supported.

**Parameters:**
- `track_index` (int)

**Live mapping:**
- If `track.flatten` exists, calls `track.flatten()`.

**Example request:**
```json
{"action": "flatten_track", "track_index": 1}
```

**Example response:**
```json
{"ok": true, "track_index": 1, "message": "Track flattened"}
```
