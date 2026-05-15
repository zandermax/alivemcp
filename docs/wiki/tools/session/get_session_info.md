---
name: "get_session_info"
summary: ""
Live mapping: "- Reads multiple `song` properties such as `is_playing`, `tempo`, `signature_numerator`, `current_song_time`, `loop_start`, `loop_length`, `num_tracks`, `num_scenes`, `record_mode`, `metronome`, `nudge_up`, `nudge_down`."
---

# get_session_info

**Domain:** session

**Summary:** Return session-level state (playback, tempo, time signature, loop, counts, recording state, metronome, nudge).

**Parameters:**

- none

**Live mapping:**

- Reads multiple `song` properties such as `is_playing`, `tempo`, `signature_numerator`, `current_song_time`, `loop_start`, `loop_length`, `num_tracks`, `num_scenes`, `record_mode`, `metronome`, `nudge_up`, `nudge_down`.
  **Example request:**

```json
{ "action": "get_session_info" }
```

**Example response:**

```json
{ "ok": true, "is_playing": false, "tempo": 128.0, "current_song_time": 12.5 }
```
