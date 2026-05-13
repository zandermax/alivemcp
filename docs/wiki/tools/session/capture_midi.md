# capture_midi

**Domain:** session

**Summary:** Capture MIDI from the most recently played notes.

**Parameters:**
- none

**Live mapping:**
- Calls `song.capture_midi()`; behavior depends on host capabilities.
**Example request:**
```json
{"action":"capture_midi"}
```
**Example response:**
```json
{"ok": true, "message": "MIDI captured"}
```
