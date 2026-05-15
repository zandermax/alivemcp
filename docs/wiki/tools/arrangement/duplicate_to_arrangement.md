---
name: "duplicate_to_arrangement"
summary: ""
Live mapping: "- Calls `clip.duplicate_loop()` on the session clip when available."
---

# duplicate_to_arrangement

**Domain:** arrangement

**Summary:** Duplicate a session clip to the arrangement (if supported).

**Parameters:**

- `track_index` (int)
- `clip_index` (int)

**Live mapping:**

- Calls `clip.duplicate_loop()` on the session clip when available.
  **Example request:**

```json
{ "action": "duplicate_to_arrangement", "track_index": 1, "clip_index": 0 }
```

**Example response:**

```json
{ "ok": true, "message": "Clip duplicated to arrangement" }
```
