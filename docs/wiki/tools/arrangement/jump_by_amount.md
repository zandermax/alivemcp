---
name: "jump_by_amount"
summary: ""
Live mapping: "- Reads `song.current_song_time` and writes a new time after adding the amount."
---

# jump_by_amount

**Domain:** arrangement

**Summary:** Jump playback position by a relative amount in beats (positive or negative).

**Parameters:**

- `amount_in_beats` (float)

**Live mapping:**

- Reads `song.current_song_time` and writes a new time after adding the amount.
  **Example request:**

```json
{ "action": "jump_by_amount", "amount_in_beats": 4.0 }
```

**Example response:**

```json
{ "ok": true, "old_time": 10.0, "new_time": 14.0, "jumped_by": 4.0 }
```
