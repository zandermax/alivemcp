# tap_tempo

**Domain:** session

**Summary:** Tap tempo (one tap registers a tempo change in the host).

**Parameters:**
- none

**Live mapping:**
- Calls `song.tap_tempo()`.
**Example request:**
```json
{"action":"tap_tempo"}
```
**Example response:**
```json
{"ok": true, "message": "Tempo tapped"}
```
