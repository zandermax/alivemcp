---
name: "set_loop_start"
summary: ""
Live mapping: "- Writes `song.loop_start = position`."
---

# set_loop_start

**Domain:** session

**Summary:** Set the song loop start position (in beats).

**Parameters:**

- `position` (float)

**Live mapping:**

- Writes `song.loop_start = position`.

**Example request:**

```json
{ "action": "set_loop_start", "position": 0.0 }
```

**Example response:**

```json
{ "ok": true, "loop_start": 0.0 }
```
