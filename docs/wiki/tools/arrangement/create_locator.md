---
name: "create_locator"
summary: ""
Live mapping: "- Calls `song.create_cue_point(time)` when supported by host."
---

# create_locator

**Domain:** arrangement

**Summary:** Create a locator/cue point at a specified time.

**Parameters:**

- `time_in_beats` (float)
- `name` (string, optional)

**Live mapping:**

- Calls `song.create_cue_point(time)` when supported by host.
  **Example request:**

```json
{ "action": "create_locator", "time_in_beats": 32.0, "name": "Drop" }
```

**Example response:**

```json
{ "ok": true, "message": "Cue point created", "time": 32.0, "name": "Drop" }
```
