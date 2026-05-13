# get_clip_automation_envelope

**Domain:** automation

**Summary:** Check whether a clip contains an automation envelope for a device parameter and return basic metadata.

**Parameters:**
- `track_index` (int)
- `clip_index` (int)
- `device_index` (int)
- `param_index` (int)

**Live mapping:**
- Uses `clip.automation_envelope(param)` to obtain the envelope object when available.

**Example request:**
```json
{"action":"get_clip_automation_envelope","track_index":0,"clip_index":0,"device_index":0,"param_index":1}
```

**Example response:**
```json
{"ok": true, "has_envelope": true, "parameter_name":"Filter Frequency","device_name":"AutoFilter"}
```

**Notes:**
- Returns `has_envelope: false` when no envelope exists; returns an error if the host lacks `automation_envelope` support.

**See also:**
- [docs/wiki/tools/automation/create_automation_envelope.md](docs/wiki/tools/automation/create_automation_envelope.md)
- [docs/wiki/tools/automation/get_automation_envelope_values.md](docs/wiki/tools/automation/get_automation_envelope_values.md)
