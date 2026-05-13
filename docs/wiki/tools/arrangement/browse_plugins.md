# browse_plugins

**Domain:** arrangement (browser)

**Summary:** Attempt to list available plugins; LiveAPI provides limited support.

**Parameters:**
- `plugin_type` (string, optional) — e.g., `vst`, `au`

**Live mapping:**
- Returns a message noting plugin browsing limitations; host may not expose full lists.

**Example request:**
```json
{"action":"browse_plugins","plugin_type":"vst"}
```

**Example response:**
```json
{"ok": true, "message":"Plugin browsing via LiveAPI is limited","plugin_type":"vst"}
```
