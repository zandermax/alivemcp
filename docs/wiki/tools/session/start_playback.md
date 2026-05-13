# start_playback

**Domain:** session

**Summary:** Start Ableton playback.

**Parameters:**
- none

**Live mapping:**
- Calls `song.start_playing()` when playback isn't already running.
**Example request:**
```json
{"action":"start_playback"}
```
**Example response:**
```json
{"ok": true}
```

**Example request:**
```json
{"ok": true, "message": "Playback started"}
```
