---
name: "get_track_color"
summary: ""
Live mapping: "- Reads `track.color_index` or `track.color` depending on Live's object model."
---

# get_track_color

**Domain:** tracks

**Summary:** Retrieve a track's color value or color index where supported.

**Parameters:**

- `track_index` (int)

**Live mapping:**

- Reads `track.color_index` or `track.color` depending on Live's object model.
  **Example request:**

```json
{ "action": "get_track_color", "track_index": 1 }
```

**Example response:**

```json
{ "ok": true, "track_index": 1, "color_index": 5 }
```

**Notes:**

- Some Live versions expose `color_index`; others expose `color` — use feature-detection.

**See also:**

- [set_track_color](tools/tracks/set_track_color.md)
