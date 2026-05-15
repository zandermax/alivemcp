---
name: "get_current_time"
summary: ""
Live mapping: "- Reads `song.current_song_time` and `song.is_playing`."
---

# get_current_time

**Domain:** session

**Summary:** Get current playback position and whether the host is playing.

**Parameters:**

- none

**Live mapping:**

- Reads `song.current_song_time` and `song.is_playing`.
  **Example request:**

```json
{ "action": "get_current_time" }
```

**Example response:**

```json
{ "ok": true, "current_song_time": 12.5, "is_playing": false }
```
