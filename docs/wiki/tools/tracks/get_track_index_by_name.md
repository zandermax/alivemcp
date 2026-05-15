---
name: "get_track_index_by_name"
summary: ""
Live mapping: "- Iterates `self.song.tracks` and returns the first index where `needle in track.name.lower()`."
---

# get_track_index_by_name

**Domain:** tracks

**Summary:** Find a track index by case-insensitive partial name match (first result).

**Parameters:**

- `name` (string)

**Live mapping:**

- Iterates `self.song.tracks` and returns the first index where `needle in track.name.lower()`.
  **Example request:**

```json
{ "action": "get_track_index_by_name", "name": "bass" }
```

**Example response:**

```json
{ "ok": true, "track_index": 2, "name": "Bass" }
```
