# send_program_change

**Domain:** midi

**Summary:** Send a MIDI Program Change message via Live's `send_midi` hook.

**Parameters:**
- `track_index` (int) — track index (API symmetry)
- `program_number` (int) — program/bank number
- `channel` (int) — MIDI channel (default 0)

**Live mapping:**
- Calls `self.song.send_midi((status_byte, program_number))` where `status_byte = 192 + channel`.

**Example request:**
```json
{"action": "send_program_change", "track_index": 0, "program_number": 10, "channel": 0}
```

**Example response:**
```json
{"ok": true, "program_number": 10, "channel": 0, "message": "MIDI Program Change sent"}
```

**Notes:**
- Requires `song.send_midi`; returns `{"ok": false, "error": "send_midi not available"}` if missing.

**See also:**
- send_midi_cc
