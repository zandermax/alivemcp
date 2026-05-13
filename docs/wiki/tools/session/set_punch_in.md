# set_punch_in

**Domain:** session

**Summary:** Enable or disable punch-in recording.

**Parameters:**
- `enabled` (bool)

**Live mapping:**
- Writes `song.punch_in = bool(enabled)`.
**Example request:**
```json
{"action":"set_punch_in","enabled":true}
```
**Example response:**
```json
{"ok": true}
```

**Example request:**
```json
{"ok": true, "punch_in": true}
```
