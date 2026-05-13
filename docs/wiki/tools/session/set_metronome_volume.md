# set_metronome_volume

**Domain:** session

**Summary:** Set the metronome volume (0.0–1.0) when available.

**Parameters:**
- `volume` (float)

**Live mapping:**
- Writes `song.metronome = volume` when the host exposes metronome volume.
**Example request:**
```json
{"action":"set_metronome_volume","volume":0.7}
```
**Example response:**
```json
{"ok": true, "volume": 0.7}
```
