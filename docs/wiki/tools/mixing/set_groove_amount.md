---
name: "set_groove_amount"
summary: ""
Live mapping: "- Writes `song.groove_amount = amount` when available."
---

# set_groove_amount

**Domain:** mixing (groove)

**Summary:** Set song-level groove amount (0.0–1.0) when supported.

**Parameters:**

- `amount` (float)

**Live mapping:**

- Writes `song.groove_amount = amount` when available.
  **Example request:**

```json
{ "action": "set_groove_amount", "amount": 0.4 }
```

**Example response:**

```json
{ "ok": true, "groove_amount": 0.4 }
```

**See also:**

- [get_groove_amount](tools/mixing/get_groove_amount.md)
