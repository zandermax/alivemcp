# get_track_is_foldable

Get Track Is Foldable

Check whether a track is foldable (group track folding support).

Parameters:
- `track_index` (int)

Returns:
- `ok`: boolean
- `is_foldable`: boolean (when available)

**Example request:**

```json
{"action": "get_track_is_foldable", "track_index": 2}
```

**Example response:**

```json
{"ok": true, "is_foldable": true}
```

