# arm_track

**Domain:** tracks

**Summary:** Arm or disarm a track for recording.

**Parameters:**
- `track_index` (int)
- `armed` (bool, default=true)

**Live mapping:**
- Sets `track.arm = armed` if `track.can_be_armed`.
**Example request:**
```json
{"action":"arm_track","track_index":1,"armed":true}
```
**Example response:**
```json
{"ok": true, "message": "Track armed", "armed": true}
```

**Notes:**
- Returns an error if the track cannot be armed.

**See also:**
- [get_track_info](tools/tracks/get_track_info.md)
