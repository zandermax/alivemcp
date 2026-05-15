---
name: "get_sample_playback_mode"
summary: ""
Live mapping: "Reads the device parameter describing playback mode and returns a normalized string."
---

# get_sample_playback_mode

**Domain:** m4l

**Summary:** Return the playback mode of a sample device (e.g., one-shot, loop, slice).

**Parameters:**

- `track_index` (int)
- `device_id` (int or string)

**Live mapping:** Reads the device parameter describing playback mode and returns a normalized string.
**Example request:**

```json
{ "action": "get_sample_playback_mode", "track_index": 1, "device_id": 0 }
```

**Example response:**

```json
{ "ok": true }
```

**Example request:**

```json
{ "ok": true, "mode": "loop" }
```
