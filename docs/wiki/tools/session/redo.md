# redo

**Domain:** session

**Summary:** Redo the last undone action in the host.

**Parameters:**
- none

**Live mapping:**
- Calls `song.redo()`.

**Example request:**
```json
{"action":"redo"}
```

**Example response:**
```json
{"ok": true, "message": "Redo executed"}
```
