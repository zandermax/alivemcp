---
name: "get_groove_amount"
summary: ""
Live mapping: "- Reads `song.groove_amount` when available."
---

# get_groove_amount

**Domain:** mixing (groove)

**Summary:** Get song-level groove amount when supported by the host.

**Parameters:**

- none

**Live mapping:**

- Reads `song.groove_amount` when available.
  **Example request:**

```json
{ "action": "get_groove_amount" }
```

**Example response:**

```json
{ "ok": true, "groove_amount": 0.3 }
```

**See also:**

- [set_groove_amount](tools/mixing/set_groove_amount.md)
