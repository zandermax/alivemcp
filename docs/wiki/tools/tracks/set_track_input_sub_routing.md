# set_track_input_sub_routing

**Domain:** tracks

**Summary:** Set track input sub-routing (host-dependent; may be limited in Live API).

**Parameters:**
- `track_index` (int)
- `sub_routing` (string)

**Live mapping:**
- If `track.input_sub_routing` is present, attempts to set it or returns a message describing limitations.
**Example request:**
```json
{"action": "set_track_input_sub_routing", "track_index": 1, "sub_routing": "L/R"}
```
**Example response:**
```json
{"ok": true, "message": "Input sub-routing setting is limited in LiveAPI", "requested_sub_routing": "L/R"}
```
