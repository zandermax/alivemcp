# stop_recording

**Domain:** session

**Summary:** Stop recording (clears `record_mode`).

**Parameters:**
- none

**Live mapping:**
- Sets `song.record_mode = False`.

**Example request:**
```json
{"action":"stop_recording"}
```

**Example response:**
```json
{"ok": true, "message": "Recording stopped"}
```
