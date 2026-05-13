# set_track_fold_state

**Domain:** tracks

**Summary:** Fold or unfold a foldable/group track.

**Parameters:**
- `track_index` (int)
- `folded` (bool)

**Live mapping:**
- If `track.is_foldable`, sets `track.fold_state = bool(folded)`.
**Example request:**
```json
{"action": "set_track_fold_state", "track_index": 1, "folded": true}
```
**Example response:**
```json
{"ok": true, "fold_state": true}
```
