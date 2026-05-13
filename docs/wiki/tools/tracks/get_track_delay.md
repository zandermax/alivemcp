# get_track_delay

**Domain:** tracks

**Summary:** Get a track's delay compensation in samples if available.

**Parameters:**
- `track_index` (int)

**Live mapping:**
- If `track.delay` exists, returns `float(track.delay)`.
**Example request:**
```json
{"action": "get_track_delay", "track_index": 1}
```
**Example response:**
```json
{"ok": true, "delay": 0.0}
```
