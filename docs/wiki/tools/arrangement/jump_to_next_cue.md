# jump_to_next_cue

**Domain:** arrangement

**Summary:** Move playback to the next cue point if available.

**Parameters:**
- none

**Live mapping:**
- Calls `song.jump_to_next_cue()` when `song.can_jump_to_next_cue` is True.
**Example request:**
```json
{"action":"jump_to_next_cue"}
```
**Example response:**
```json
{"ok": true, "message": "Jumped to next cue"}
```
