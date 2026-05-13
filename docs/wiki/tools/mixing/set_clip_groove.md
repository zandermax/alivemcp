# set_clip_groove

**Domain:** mixing (groove)

**Summary:** Assign a groove from the song's groove pool to a clip.

**Parameters:**
- `track_index` (int)
- `clip_index` (int)
- `groove_index` (int)

**Live mapping:**
- Sets `clip.groove = song.groove_pool[groove_index]` when the clip and groove pool are available.

**Example request:**
```json
{"action":"set_clip_groove","track_index":1,"clip_index":0,"groove_index":2}
```

**Example response:**
```json
{"ok": true, "message": "Groove set", "groove_index": 2}
```

**Notes:**
- Validates track and clip indexes and that the selected groove exists.
- Returns an error when the clip or groove property is not available in the host.

**See also:**
- [docs/wiki/tools/mixing/get_groove_pool_grooves.md](docs/wiki/tools/mixing/get_groove_pool_grooves.md)
- [docs/wiki/tools/mixing/set_clip_groove_amount.md](docs/wiki/tools/mixing/set_clip_groove_amount.md)
