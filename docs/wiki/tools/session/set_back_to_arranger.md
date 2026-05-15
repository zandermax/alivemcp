---
name: "set_back_to_arranger"
summary: ""
Live mapping: "- Writes `song.back_to_arranger = bool(enabled)`."
---

# set_back_to_arranger

**Domain:** session

**Summary:** Enable or disable "back to arranger" behavior.

**Parameters:**

- `enabled` (bool)

**Live mapping:**

- Writes `song.back_to_arranger = bool(enabled)`.
  **Example request:**

```json
{ "action": "set_back_to_arranger", "enabled": true }
```

**Example response:**

```json
{ "ok": true, "back_to_arranger": true }
```
