---
name: "scroll_view_to_time"
summary: ""
Live mapping: "- Attempts to use view APIs; implementation may be limited by host."
---

# scroll_view_to_time

**Domain:** arrangement (view)

**Summary:** Request the arrangement view to scroll to a specific time (limited API support).

**Parameters:**

- `time_in_beats` (float)

**Live mapping:**

- Attempts to use view APIs; implementation may be limited by host.
  **Example request:**

```json
{ "action": "scroll_view_to_time", "time_in_beats": 64.0 }
```

**Example response:**

```json
{
  "ok": true,
  "message": "View scroll requested (limited API support)",
  "time": 64.0
}
```
