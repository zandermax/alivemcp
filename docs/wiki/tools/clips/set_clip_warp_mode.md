---
name: "set_clip_warp_mode"
summary: ""
Live mapping: "Writes `clip.warp_mode = warp_mode` or uses the appropriate Live API setter to change the clip's warp mode."
---

# set_clip_warp_mode

**Domain:** clips

**Summary:** Set the warp mode for an audio clip.

**Parameters:**

- `track_index` (int)
- `clip_index` (int)
- `warp_mode` (string)

**Live mapping:** Writes `clip.warp_mode = warp_mode` or uses the appropriate Live API setter to change the clip's warp mode.
**Example request:**

```json
{
  "action": "set_clip_warp_mode",
  "track_index": 1,
  "clip_index": 0,
  "warp_mode": "beats"
}
```

**Example response:**

```json
{ "ok": true, "message": "Warp mode set", "warp_mode": "beats" }
```

**See also:**

- [get_clip_warp_mode](tools/clips/get_clip_warp_mode.md)
- [set_clip_warping](tools/clips/set_clip_warping.md)
