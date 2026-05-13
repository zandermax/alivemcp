# get_groove_pool_grooves

**Domain:** mixing (groove)

**Summary:** List grooves available in the song's groove pool with basic metadata.

**Parameters:**
- none

**Live mapping:**
- Iterates `song.groove_pool` and returns `index`, `name`, and common groove amounts when available.

**Example request:**
```json
{"action":"get_groove_pool_grooves"}
```

**Example response:**
```json
{"ok": true, "grooves": [{"index":0,"name":"Swing","timing_amount":0.5}], "count":1}
```

**See also:**
- [set_clip_groove](tools/mixing/set_clip_groove.md)
