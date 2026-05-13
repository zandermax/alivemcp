# get_crossfader_position

**Domain:** mixing

**Summary:** Get the master crossfader position (-1.0 to 1.0) when available.

**Parameters:**
- none

**Live mapping:**
- Reads `song.master_track.mixer_device.crossfader.value` when supported.
**Example request:**
```json
{"action":"get_crossfader_position"}
```
**Example response:**
```json
{"ok": true, "position": 0.0}
```

**Notes:**
- Returns an error if the crossfader is not available in the host.

**See also:**
- [set_crossfader_assignment](tools/mixing/set_crossfader_assignment.md)
