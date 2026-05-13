# set_clip_annotation

Set Clip Annotation

Set the annotation text for a clip.

Parameters:
- `track_index` (int)
- `clip_index` (int)
- `annotation_text` (string)

Returns:
- `ok`: boolean
- `annotation`: string (new value)

Example request:
```json
{"action": "set_clip_annotation", "track_index": 0, "clip_index": 0, "annotation_text": "Verse"}
```
