---
name: "continue_playing"
summary: ""
Live mapping: "- Calls `song.continue_playing()`."
---

# continue_playing

**Domain:** session

**Summary:** Continue playback from current position.

**Parameters:**

- none

**Live mapping:**

- Calls `song.continue_playing()`.
  **Example request:**

```json
{ "action": "continue_playing" }
```

**Example response:**

```json
{ "ok": true, "message": "Playback continued" }
```
