# set_track_output_sub_routing

**Domain:** tracks

**Summary:** Set track output sub-routing (host-dependent; may be limited in Live API).

**Parameters:**
- `track_index` (int)
- `sub_routing` (string)

**Live mapping:**
- If `track.output_sub_routing` is present, attempts to set it or returns a message describing limitations.
**Example request:**
```json
{"action": "set_track_output_sub_routing", "track_index": 1, "sub_routing": "Mono"}
```
**Example response:**
```json
{"ok": true, "message": "Output sub-routing setting is limited in LiveAPI", "requested_sub_routing": "Mono"}
```
