# set_crossfader_assignment

**Domain:** mixing

**Summary:** Set a track's crossfader assignment (0=None, 1=A, 2=B).

**Parameters:**
- `track_index` (int)
- `assignment` (int) — 0, 1, or 2

**Live mapping:**
- Writes `track.mixer_device.crossfade_assign = assignment` when supported.

**Example request:**
```json
{"action":"set_crossfader_assignment","track_index":1,"assignment":1}
```

**Example response:**
```json
{"ok": true, "track_index":1, "crossfader_assignment":1}
```

**Notes:**
- Validates assignment range and availability of the crossfader property.

**See also:**
- [docs/wiki/tools/mixing/get_crossfader_assignment.md](docs/wiki/tools/mixing/get_crossfader_assignment.md)
- [docs/wiki/tools/mixing/get_crossfader_position.md](docs/wiki/tools/mixing/get_crossfader_position.md)
