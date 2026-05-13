# create_return_track

**Domain:** tracks

**Summary:** Create a new return (send) track.

**Parameters:**
- none

**Live mapping:**
- Calls `song.create_return_track()`; returns the new return track index.
**Example request:**
```json
{"action":"create_return_track"}
```
**Example response:**
```json
{"ok": true, "message": "Return track created", "return_index": 2}
```

**Notes:**
- Return tracks are appended to `song.return_tracks`.

**See also:**
- [delete_track](tools/tracks/delete_track.md)
