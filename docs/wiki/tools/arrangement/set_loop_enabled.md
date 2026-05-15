---
name: "set_loop_enabled"
summary: ""
Live mapping: "- Writes `song.loop = bool(enabled)`."
---

# set_loop_enabled

**Domain:** arrangement (loop)

**Summary:** Enable or disable the song loop.

**Parameters:**

- `enabled` (bool)

**Live mapping:**

- Writes `song.loop = bool(enabled)`.
  **Example request:**

```json
{ "action": "set_loop_enabled", "enabled": true }
```

**Example response:**

```json
{ "ok": true, "loop_enabled": true }
```
