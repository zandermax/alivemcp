# get_automation_envelope_values

**Domain:** automation

**Summary:** Retrieve information about a clip's automation envelope values for a device parameter.

**Parameters:**
- `track_index` (int)
- `clip_index` (int)
- `device_index` (int)
- `param_index` (int)

**Live mapping:**
- Calls `clip.automation_envelope(param)` and inspects the envelope; current implementation returns high-level metadata and points callers to `insert_step`/`remove_step` for edits.

**Example request:**
```json
{"action":"get_automation_envelope_values","track_index":0,"clip_index":0,"device_index":0,"param_index":1}
```

**Example response:**
```json
{"ok": true, "parameter_name":"Filter","has_envelope":true, "message":"Use insert_step/remove_step to modify automation"}
```

**Notes:**
- Full breakpoint enumeration isn't implemented; for detailed reads iterate envelope structures in the host where available.

**See also:**
- [docs/wiki/tools/automation/get_clip_automation_envelope.md](docs/wiki/tools/automation/get_clip_automation_envelope.md)
