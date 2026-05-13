# set_sample_playback_mode

**Domain:** m4l

**Summary:** Set the playback mode on a sample device (e.g., one-shot, loop, slice).

**Parameters:**
- `track_index` (int)
- `device_id` (int or string)
- `mode` (string)

**Live mapping:** Writes the appropriate device parameter to change playback mode.

**Example request:**
```json
{"action":"set_sample_playback_mode","track_index":1,"device_id":0,"mode":"loop"}
```

**Example response:**
```json
{"ok": true, "mode": "loop"}
```
