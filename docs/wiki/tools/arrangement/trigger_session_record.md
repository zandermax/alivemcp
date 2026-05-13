# trigger_session_record

**Domain:** arrangement

**Summary:** Trigger session record; optionally supply a fixed length.

**Parameters:**
- `length` (float, optional) — length in beats or seconds as supported by host

**Live mapping:**
- Calls `song.trigger_session_record()` with or without a length argument.
**Example request:**
```json
{"action":"trigger_session_record","length":8.0}
```
**Example response:**
```json
{"ok": true, "message": "Session record triggered"}
```

**Notes:**
- Behavior depends on Live's session-record implementation.
