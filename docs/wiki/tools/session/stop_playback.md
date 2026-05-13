# stop_playback

**Domain:** session

**Summary:** Stop Ableton playback.

**Parameters:**
- none

**Live mapping:**
- Calls `song.stop_playing()` when playback is running.
**Example request:**
```json
{"action":"stop_playback"}
```
**Example response:**
```json
{"ok": true}
```

**Example request:**
```json
{"ok": true, "message": "Playback stopped"}
```
