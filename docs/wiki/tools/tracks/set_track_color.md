# set_track_color

**Domain:** tracks

**Summary:** Set a track's color index where supported.

**Parameters:**
- `track_index` (int)
- `color_index` (int)

**Live mapping:**
- Sets `track.color = color_index` when `track` supports `color`.

**Example request:**
```json
{"action":"set_track_color","track_index":1,"color_index":5}
```

**Example response:**
```json
{"ok": true, "message": "Track color set", "color": 5}
```

**Notes:**
- Returns an error if track color is not supported by the Live object.
