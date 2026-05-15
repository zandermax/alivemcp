---
name: "jump_to_time"
summary: ""
Live mapping: "- Writes `song.current_song_time = time_in_beats`."
---

# jump_to_time

**Domain:** session

**Summary:** Jump playback to a specific time (in beats).

**Parameters:**

- `time_in_beats` (float)

**Live mapping:**

- Writes `song.current_song_time = time_in_beats`.
  **Example request:**

```json
{ "action": "jump_to_time", "time_in_beats": 32.0 }
```

**Example response:**

```json
{ "ok": true }
```

**Example request:**

```json
{ "ok": true, "time": 32.0 }
```
