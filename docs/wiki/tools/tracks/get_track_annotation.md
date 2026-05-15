---
name: "get_track_annotation"
summary: ""
Live mapping: "- If `track.annotation` exists, returns it as a string."
---

# get_track_annotation

**Domain:** tracks

**Summary:** Get a track's annotation text if available.

**Parameters:**

- `track_index` (int)

**Live mapping:**

- If `track.annotation` exists, returns it as a string.
  **Example request:**

```json
{ "action": "get_track_annotation", "track_index": 1 }
```

**Example response:**

```json
{ "ok": true, "annotation": "Recorded live" }
```
