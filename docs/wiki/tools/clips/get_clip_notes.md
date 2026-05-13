# get_clip_notes

**Domain:** midi (clip MIDI notes)

**Summary:** Retrieve all MIDI notes from a clip.

**Parameters:**
- `track_index` (int)
- `clip_index` (int)

**Live mapping:**
- Calls `clip.get_notes(0, 0, clip.length, 128)` and returns tuples as note dicts.

**Example request:**
```json
{"action":"get_clip_notes","track_index":1,"clip_index":0}
```

**Example response:**
```json
{"ok": true, "track_index": 1, "clip_index": 0, "notes": [{"pitch":60,"start_time":0.0,"duration":1.0,"velocity":100,"muted":false}], "count":1}
```

**Notes:**
- Only valid for MIDI clips; returns an error for audio clips.

**See also:**
- [docs/wiki/tools/clips/add_notes.md](docs/wiki/tools/clips/add_notes.md)
- [docs/wiki/tools/clips/remove_notes.md](docs/wiki/tools/clips/remove_notes.md)
