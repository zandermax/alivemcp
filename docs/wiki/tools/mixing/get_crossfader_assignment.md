# get_crossfader_assignment

**Domain:** mixing

**Summary:** Get a track's crossfader assignment (None/A/B).

**Parameters:**
- `track_index` (int)

**Live mapping:**
- Reads `track.mixer_device.crossfade_assign` when available and returns both numeric and friendly assignment name.

**Example request:**
```json
{"action":"get_crossfader_assignment","track_index":1}
```

**Example response:**
```json
{"ok": true, "track_index":1, "crossfader_assignment":1, "assignment_name":"A"}
```

**See also:**
- [set_crossfader_assignment](tools/mixing/set_crossfader_assignment.md)
