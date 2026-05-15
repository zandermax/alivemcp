---
name: "set_tempo"
summary: ""
Live mapping: "- Writes `song.tempo = bpm` after validation."
---

# set_tempo

**Domain:** session

**Summary:** Set the session tempo (BPM).

**Parameters:**

- `bpm` (float) — 20–999

**Live mapping:**

- Writes `song.tempo = bpm` after validation.
  **Example request:**

```json
{ "action": "set_tempo", "bpm": 128 }
```

**Example response:**

```json
{ "ok": true }
```

**Example request:**

```json
{ "ok": true, "bpm": 128.0, "message": "Tempo set" }
```
