---
name: "get_clip_file_path"
summary: ""
Live mapping: "Reads `clip.file_path` or the closest Live API property and returns the absolute path to the source audio file."
---

# get_clip_file_path

**Domain:** clips

**Summary:** Return the filesystem path of the audio file backing an audio clip, when available.

**Parameters:**

- `track_index` (int)
- `clip_index` (int)

**Live mapping:** Reads `clip.file_path` or the closest Live API property and returns the absolute path to the source audio file.
**Example request:**

```json
{ "action": "get_clip_file_path", "track_index": 1, "clip_index": 0 }
```

**Example response:**

```json
{ "ok": true, "file_path": "/path/to/sample.wav" }
```

**Notes:**

- Not all clips are backed by files (e.g., MIDI or consolidated clips). Returns an error if not applicable.

**See also:**

- [get_clip_warp_mode](tools/clips/get_clip_warp_mode.md)
- [get_warp_markers](tools/clips/get_warp_markers.md)
