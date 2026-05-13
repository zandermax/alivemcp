# get_track_info

**Domain:** tracks

**Summary:** Retrieve comprehensive information about a track.

**Parameters:**
- `track_index` (int)

**Live mapping:**
- Reads many `track` properties including `name`, `color`, `is_foldable`, `mute`, `solo`, `arm`, `has_midi_input`, `has_audio_input`, `mixer_device.volume.value`, `mixer_device.panning.value`, number of devices and clips.

**Example request:**
```json
{"action":"get_track_info","track_index":1}
```

**Example response:**
```json
{
  "ok": true,
  "track_index": 1,
  "name": "Synth",
  "color": null,
  "is_foldable": false,
  "mute": false,
  "solo": false,
  "arm": true,
  "has_midi_input": true,
  "has_audio_input": false,
  "volume": 0.8,
  "pan": 0.0,
  "num_devices": 3,
  "num_clips": 2
}
```

**Notes:**
- Some properties may not exist depending on Live version (use feature-detection).

**See also:**
- [tools/tracks/set_track_color.md](tools/tracks/set_track_color.md)
- [tools/tracks/set_track_volume.md](tools/tracks/set_track_volume.md)
- [tools/tracks/set_track_pan.md](tools/tracks/set_track_pan.md)
