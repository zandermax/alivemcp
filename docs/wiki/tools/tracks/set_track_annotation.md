# set_track_annotation

**Domain:** tracks

**Summary:** Set a track's annotation text if supported.

**Parameters:**
- `track_index` (int)
- `annotation_text` (string)

**Live mapping:**
- If `track.annotation` exists, sets `track.annotation = str(annotation_text)` and returns the updated annotation.
**Example request:**
```json
{"action": "set_track_annotation", "track_index": 1, "annotation_text": "New notes"}
```
**Example response:**
```json
{"ok": true, "annotation": "New notes"}
```
