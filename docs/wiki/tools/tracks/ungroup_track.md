---
name: "ungroup_track"
summary: ""
Live mapping: "- Validates index and verifies `track.is_foldable`; returns a message indicating ungroup requested; may require manual steps."
---

# ungroup_track

**Domain:** tracks

**Summary:** Ungroup a group track (best-effort; Live API support may be limited).

**Parameters:**

- `group_track_index` (int)

**Live mapping:**

- Validates index and verifies `track.is_foldable`; returns a message indicating ungroup requested; may require manual steps.
  **Example request:**

```json
{ "action": "ungroup_track", "group_track_index": 4 }
```

**Example response:**

```json
{
  "ok": true,
  "message": "Ungroup operation requested (may require manual implementation)",
  "group_track_index": 4
}
```
