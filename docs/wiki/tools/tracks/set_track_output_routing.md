# set_track_output_routing

**Domain:** tracks

**Summary:** Set track output routing type (host-dependent).

**Parameters:**
- `track_index` (int)
- `routing_type_name` (string)

**Live mapping:**
- Validates index and returns a message; actual routing depends on host implementation.
**Example request:**
```json
{"action": "set_track_output_routing", "track_index": 1, "routing_type_name": "Master"}
```
**Example response:**
```json
{"ok": true, "message": "Output routing set (requires routing configuration)", "routing_type": "Master"}
```
