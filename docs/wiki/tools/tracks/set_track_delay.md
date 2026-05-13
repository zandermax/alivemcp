# set_track_delay

**Domain:** tracks

**Summary:** Set a track's delay compensation in samples if available.

**Parameters:**
- `track_index` (int)
- `delay_samples` (number)

**Live mapping:**
- If `track.delay` exists, sets `track.delay = float(delay_samples)` and returns the updated value.
**Example request:**
```json
{"action": "set_track_delay", "track_index": 1, "delay_samples": 128}
```
**Example response:**
```json
{"ok": true, "delay": 128.0}
```
