# set_punch_out

**Domain:** session

**Summary:** Enable or disable punch-out recording.

**Parameters:**
- `enabled` (bool)

**Live mapping:**
- Writes `song.punch_out = bool(enabled)`.

**Example request:**
```json
{"action":"set_punch_out","enabled":true}
```

**Example response:**
```json
{"ok": true, "punch_out": true}
```
