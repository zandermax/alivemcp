---
name: "get_can_jump_to_next_cue"
summary: ""
Live mapping: "- Reads `song.can_jump_to_next_cue`."
---

# get_can_jump_to_next_cue

**Domain:** arrangement

**Summary:** Returns whether playback can jump to the next cue point.

**Parameters:**

- none

**Live mapping:**

- Reads `song.can_jump_to_next_cue`.
  **Example request:**

```json
{ "action": "get_can_jump_to_next_cue" }
```

**Example response:**

```json
{ "ok": true, "can_jump_to_next_cue": true }
```
