# set_clip_warping

**Domain:** clips

**Summary:** Enable or disable warping for an audio clip and optionally set warp markers.

**Parameters:**
- `track_index` (int)
- `clip_index` (int)
- `warping` (bool)
- `warp_markers` (optional list) — when provided, applies markers after enabling warping

**Live mapping:** Sets `clip.warping` (or the appropriate Live API property). If `warp_markers` provided, updates the clip's warp markers accordingly.

**Example request:**
```json
{"action":"set_clip_warping","track_index":1,"clip_index":0,"warping":true}
```

**Example response:**
```json
{"ok": true, "warping": true}
```

**See also:**
- [get_clip_warp_mode](tools/clips/get_clip_warp_mode.md)
- [get_warp_markers](tools/clips/get_warp_markers.md)
