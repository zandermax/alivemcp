# set_time_signature

**Domain:** session

**Summary:** Set the session time signature.

**Parameters:**
- `numerator` (int)
- `denominator` (int) — 1,2,4,8,16

**Live mapping:**
- Writes `song.signature_numerator` and `song.signature_denominator` after validation.
**Example request:**
```json
{"action":"set_time_signature","numerator":4,"denominator":4}
```
**Example response:**
```json
{"ok": true}
```

**Example request:**
```json
{"ok": true, "numerator":4, "denominator":4, "message":"Time signature set"}
```
