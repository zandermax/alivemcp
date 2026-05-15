---
name: "set_arrangement_overdub"
summary: ""
Live mapping: "- Writes `song.arrangement_overdub = bool(enabled)`."
---

# set_arrangement_overdub

**Domain:** session

**Summary:** Enable or disable arrangement overdub.

**Parameters:**

- `enabled` (bool)

**Live mapping:**

- Writes `song.arrangement_overdub = bool(enabled)`.

**Example request:**

```json
{ "action": "set_arrangement_overdub", "enabled": true }
```

**Example response:**

```json
{ "ok": true, "arrangement_overdub": true }
```
