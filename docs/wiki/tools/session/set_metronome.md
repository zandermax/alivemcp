---
name: "set_metronome"
summary: ""
Live mapping: "- Writes `song.metronome = bool(enabled)`."
---

# set_metronome

**Domain:** session

**Summary:** Enable or disable the metronome.

**Parameters:**

- `enabled` (bool)

**Live mapping:**

- Writes `song.metronome = bool(enabled)`.
  **Example request:**

```json
{ "action": "set_metronome", "enabled": true }
```

**Example response:**

```json
{ "ok": true, "metronome": true }
```
