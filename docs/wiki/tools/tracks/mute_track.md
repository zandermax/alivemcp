---
name: "mute_track"
summary: ""
Live mapping: "- Sets `song.tracks[track_index].mute = mute`."
---

# mute_track

**Domain:** tracks

**Summary:** Mute or unmute a track.

**Parameters:**

- `track_index` (int)
- `mute` (bool, default=true)

**Live mapping:**

- Sets `song.tracks[track_index].mute = mute`.
  **Example request:**

```json
{ "action": "mute_track", "track_index": 1, "mute": true }
```

**Example response:**

```json
{ "ok": true, "message": "Track muted" }
```

**Notes:**

- Returns an error for invalid track indexes.

**See also:**

- [solo_track](tools/tracks/solo_track.md)
