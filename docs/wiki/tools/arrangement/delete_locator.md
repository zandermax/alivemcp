# delete_locator

**Domain:** arrangement

**Summary:** Delete a locator/cue point by index.

**Parameters:**
- `locator_index` (int)

**Live mapping:**
- Calls `cue_point.delete()` when `song.cue_points` and `cue_point.delete` are available.

**Example request:**
```json
{"action":"delete_locator","locator_index":0}
```

**Example response:**
```json
{"ok": true, "message":"Locator deleted","locator_index":0}
```
