# get_metronome_volume

**Domain:** session

**Summary:** Get the metronome volume when available.

**Parameters:**
- none

**Live mapping:**
- Reads `song.metronome` when exposed as a volume value.

**Example request:**
```json
{"action":"get_metronome_volume"}
```

**Example response:**
```json
{"ok": true, "volume": 0.8}
```
