# get_loop_enabled

**Domain:** arrangement (loop)

**Summary:** Get current loop enabled state and loop boundaries.

**Parameters:**
- none

**Live mapping:**
- Reads `song.loop`, `song.loop_start`, and `song.loop_length`.

**Example request:**
```json
{"action":"get_loop_enabled"}
```

**Example response:**
```json
{"ok": true, "loop_enabled": true, "loop_start":0.0, "loop_length":8.0}
```
