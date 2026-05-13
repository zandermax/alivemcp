# jump_to_prev_cue

**Domain:** arrangement

**Summary:** Move playback to the previous cue point if available.

**Parameters:**
- none

**Live mapping:**
- Calls `song.jump_to_prev_cue()` when `song.can_jump_to_prev_cue` is True.

**Example request:**
```json
{"action":"jump_to_prev_cue"}
```

**Example response:**
```json
{"ok": true, "message": "Jumped to previous cue"}
```
