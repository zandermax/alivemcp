# get_clip_warp_mode

**Domain:** clips

**Summary:** Return the warp mode for an audio clip.

**Parameters:**
- `track_index` (int)
- `clip_index` (int)

**Live mapping:** Reads `clip.warp_mode` or equivalent Live API property for an audio clip and returns a string describing the mode (e.g., ‘beats’, ‘textures’, etc.).

**Example request:**

```json
{"action":"get_clip_warp_mode","track_index":1,"clip_index":0}
```

**Example response:**

```json
{"ok": true, "warp_mode": "beats"}
```

**See also:**
- [set_clip_warp_mode](tools/clips/set_clip_warp_mode.md)
- [get_clip_file_path](tools/clips/get_clip_file_path.md)
