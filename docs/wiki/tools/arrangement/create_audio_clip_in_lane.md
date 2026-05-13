# create_audio_clip_in_lane

**Domain:** arrangement (take_lanes)

**Summary:** Create an audio clip inside a take lane (Live 12+).

**Parameters:**
- `track_index` (int)
- `lane_index` (int)
- `length` (float, optional)

**Live mapping:**
- Calls `lane.create_audio_clip(length)` when supported.
**Example request:**
```json
{"action":"create_audio_clip_in_lane","track_index":1,"lane_index":0,"length":4.0}
```
**Example response:**
```json
{"ok": true, "message":"Audio clip created in take lane","length":4.0}
```
