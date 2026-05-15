---
name: "set_loop_length"
summary: ""
Live mapping: "- Writes `song.loop_length = length`."
---

# set_loop_length

**Domain:** session

**Summary:** Set the song loop length (in beats).

**Parameters:**

- `length` (float)

**Live mapping:**

- Writes `song.loop_length = length`.

**Example request:**

```json
{ "action": "set_loop_length", "length": 4.0 }
```

**Example response:**

```json
{ "ok": true, "loop_length": 4.0 }
```
