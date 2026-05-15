---
name: "set_session_record"
summary: ""
Live mapping: "- Writes `song.session_record = bool(enabled)`."
---

# set_session_record

**Domain:** session (automation)

**Summary:** Enable or disable session record.

**Parameters:**

- `enabled` (bool)

**Live mapping:**

- Writes `song.session_record = bool(enabled)`.
  **Example request:**

```json
{ "action": "set_session_record", "enabled": true }
```

**Example response:**

```json
{ "ok": true }
```

**Example request:**

```json
{ "ok": true, "session_record": true }
```
