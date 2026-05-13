# undo

**Domain:** session

**Summary:** Undo the last action in the host.

**Parameters:**
- none

**Live mapping:**
- Calls `song.undo()`.
**Example request:**
```json
{"action":"undo"}
```
**Example response:**
```json
{"ok": true, "message": "Undo executed"}
```
