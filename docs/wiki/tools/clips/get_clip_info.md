# get_clip_info

**Domain:** clips

**Summary:** Retrieve information about a clip (name, length, looping, type, playback state, color).

**Parameters:**
- `track_index` (int)
- `clip_index` (int)

**Live mapping:**
- Reads properties from `clip = track.clip_slots[clip_index].clip`, including `clip.name`, `clip.length`, `clip.loop_start`, `clip.loop_end`, `clip.is_midi_clip`, `clip.is_audio_clip`, `clip.is_playing`, `clip.muted`, and `clip.color`.

**Example request:**
```json
{"action": "get_clip_info", "track_index": 1, "clip_index": 0}
```

**Example response:**
```json
{
  "ok": true,
  "name": "Clip A",
  "length": 4.0,
  "loop_start": 0.0,
  "loop_end": 4.0,
  "is_midi_clip": true,
  "is_audio_clip": false,
  "is_playing": false,
  "muted": false,
  "color": null
}
```

**Notes:**
- Returns an error if the slot has no clip.

**See also:**
- [set_clip_name](tools/clips/set_clip_name.md)
- [get_clip_notes](tools/clips/get_clip_notes.md)
