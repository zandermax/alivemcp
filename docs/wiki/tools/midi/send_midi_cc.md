# send_midi_cc

**Domain:** midi

**Summary:** Send a MIDI Continuous Controller (CC) message via Live's `send_midi` hook.

**Parameters:**
- `track_index` (int) — target track index (unused for transport; retained for API symmetry)
- `cc_number` (int) — CC number (0-127)
- `cc_value` (int) — CC value (0-127)
- `channel` (int) — MIDI channel (default 0)

**Live mapping:**
- Calls `self.song.send_midi((status_byte, cc_number, cc_value))` where `status_byte = 176 + channel`.
- Requires `song.send_midi` to be available on the host.
**Example request:**
```json
{"action": "send_midi_cc", "track_index": 0, "cc_number": 1, "cc_value": 127, "channel": 0}
```
**Example response:**
```json
{"ok": true, "cc_number": 1, "cc_value": 127, "channel": 0, "message": "MIDI CC sent"}
```

**Ableton references:**
- Live API `send_midi` (host-specific)

**Notes:**
- Not all Ableton hosts expose `song.send_midi`; the method checks with `hasattr(self.song, "send_midi")` and returns a helpful error if unavailable.

**See also:**
- [send_program_change](tools/midi/send_program_change.md)
