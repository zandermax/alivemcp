---
name: "start_recording"
summary: ""
Live mapping: "- Sets `song.record_mode = True` and calls `song.start_playing()` if not playing."
---

# start_recording

**Domain:** session

**Summary:** Start recording (sets `record_mode` and starts playback if needed).

**Parameters:**

- none

**Live mapping:**

- Sets `song.record_mode = True` and calls `song.start_playing()` if not playing.
  **Example request:**

```json
{ "action": "start_recording" }
```

**Example response:**

```json
{ "ok": true, "message": "Recording started" }
```
