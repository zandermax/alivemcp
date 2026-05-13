# set_session_automation_record

**Domain:** session (automation)

**Summary:** Enable or disable session automation recording.

**Parameters:**
- `enabled` (bool)

**Live mapping:**
- Writes `song.session_automation_record = bool(enabled)`.
**Example request:**
```json
{"action":"set_session_automation_record","enabled":true}
```
**Example response:**
```json
{"ok": true}
```

**Example request:**
```json
{"ok": true, "session_automation_record": true}
```
