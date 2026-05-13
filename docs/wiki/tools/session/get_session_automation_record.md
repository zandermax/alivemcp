# get_session_automation_record

**Domain:** session (automation)

**Summary:** Get whether session automation recording is enabled.

**Parameters:**
- none

**Live mapping:**
- Reads `song.session_automation_record`.

**Example request:**
```json
{"action":"get_session_automation_record"}
```

**Example response:**
```json
{"ok": true, "session_automation_record": false}
```
