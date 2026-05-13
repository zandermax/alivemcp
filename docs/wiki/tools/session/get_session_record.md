# get_session_record

**Domain:** session (automation)

**Summary:** Get whether session record is enabled.

**Parameters:**
- none

**Live mapping:**
- Reads `song.session_record`.
**Example request:**
```json
{"action":"get_session_record"}
```
**Example response:**
```json
{"ok": true, "session_record": false}
```
