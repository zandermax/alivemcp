# set_clip_groove_amount

**Domain:** mixing (groove)

**Summary:** Set a clip's groove amount (0.0–1.0) if the clip supports groove.

**Parameters:**
- `track_index` (int)
- `clip_index` (int)
- `amount` (float)

**Live mapping:**
- Writes `clip.groove_amount = amount` when `clip` exposes `groove_amount`.

**Example request:**
```json
{"action":"set_clip_groove_amount","track_index":1,"clip_index":0,"amount":0.5}
```

**Example response:**
```json
{"ok": true, "groove_amount": 0.5}
```

**Notes:**
- Clip must support groove; otherwise returns an error.

**See also:**
- [docs/wiki/tools/mixing/set_clip_groove.md](docs/wiki/tools/mixing/set_clip_groove.md)
