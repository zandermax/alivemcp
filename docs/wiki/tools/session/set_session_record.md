# set_session_record

**Domain:** session (automation)

**Summary:** Enable or disable session record.

**Parameters:**
- `enabled` (bool)

**Live mapping:**
- Writes `song.session_record = bool(enabled)`.

**Example request:**
```json
{"action":"set_session_record","enabled":true}
```

**Example response:**
```json
{"ok": true, "session_record": true}
```
