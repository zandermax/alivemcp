---
name: "remove_notes"
summary: ""
Live mapping: "- Calls `clip.remove_notes(time_from, pitch_from, time_span, pitch_span)` on the Live clip object."
---

# remove_notes

**Domain:** midi (clip MIDI notes)

**Summary:** Remove MIDI notes from a clip by pitch/time range.

**Parameters:**

- `track_index` (int)
- `clip_index` (int)
- `pitch_from` (int, default 0)
- `pitch_to` (int, default 127)
- `time_from` (float, default 0.0)
- `time_to` (float, default 999.0)

**Live mapping:**

- Calls `clip.remove_notes(time_from, pitch_from, time_span, pitch_span)` on the Live clip object.
  **Example request:**

```json
{
  "action": "remove_notes",
  "track_index": 1,
  "clip_index": 0,
  "pitch_from": 60,
  "pitch_to": 60
}
```

**Example response:**

```json
{ "ok": true, "message": "Notes removed" }
```

**Notes:**

- Parameters are clamped/validated; operates only on MIDI clips.

**See also:**

- [add_notes](tools/clips/add_notes.md)
- [get_clip_notes](tools/clips/get_clip_notes.md)
