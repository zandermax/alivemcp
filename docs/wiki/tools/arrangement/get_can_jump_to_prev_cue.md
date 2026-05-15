---
name: "get_can_jump_to_prev_cue"
summary: ""
Live mapping: "- Reads `song.can_jump_to_prev_cue`."
---

# get_can_jump_to_prev_cue

**Domain:** arrangement

**Summary:** Returns whether playback can jump to the previous cue point.

**Parameters:**

- none

**Live mapping:**

- Reads `song.can_jump_to_prev_cue`.
  **Example request:**

```json
{ "action": "get_can_jump_to_prev_cue" }
```

**Example response:**

```json
{ "ok": true, "can_jump_to_prev_cue": false }
```
