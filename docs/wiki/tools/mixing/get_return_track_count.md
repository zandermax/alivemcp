# get_return_track_count

**Domain:** mixing

**Summary:** Return the number of return (send) tracks in the project.

**Parameters:**
- none

**Live mapping:**
- Returns `len(song.return_tracks)`.

**Example request:**

```json
{"action":"get_return_track_count"}
```

**Example response:**

```json
{"ok": true, "count": 2}
```

**See also:**
- [get_return_track_info](tools/mixing/get_return_track_info.md)
