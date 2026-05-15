---
name: "get_warp_markers"
summary: ""
Live mapping: "Reads the clip's warp marker information and returns a structured list of marker positions."
---

# get_warp_markers

**Domain:** clips

**Summary:** Return a list of warp markers for an audio clip.

**Parameters:**

- `track_index` (int)
- `clip_index` (int)

**Live mapping:** Reads the clip's warp marker information and returns a structured list of marker positions.
**Example request:**

```json
{ "action": "get_warp_markers", "track_index": 1, "clip_index": 0 }
```

**Example response:**

```json
{
  "ok": true,
  "warp_markers": [
    { "position": 0.0, "beat": 0.0 },
    { "position": 1.0, "beat": 1.0 }
  ]
}
```

**See also:**

- [set_clip_warping](tools/clips/set_clip_warping.md)
- [get_clip_file_path](tools/clips/get_clip_file_path.md)
