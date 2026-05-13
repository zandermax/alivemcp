# set_track_current_monitoring_state

**Domain:** tracks

**Summary:** Set track monitoring state (0=In, 1=Auto, 2=Off).

**Parameters:**
- `track_index` (int)
- `state` (int)

**Live mapping:**
- If `track.can_be_armed`, sets `track.current_monitoring_state = int(state)` and returns the new state.
**Example request:**
```json
{"action": "set_track_current_monitoring_state", "track_index": 1, "state": 1}
```
**Example response:**
```json
{"ok": true, "monitoring_state": 1}
```
