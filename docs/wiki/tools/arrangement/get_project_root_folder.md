# get_project_root_folder

**Domain:** arrangement

**Summary:** Return the project's root folder path when available.

**Parameters:**
- none

**Live mapping:**
- Reads `song.project_root_folder` when the host exposes it.
**Example request:**
```json
{"action":"get_project_root_folder"}
```
**Example response:**
```json
{"ok": true, "project_root_folder": "/Users/you/Music/Ableton/Projects/MySet"}
```

**Notes:**
- Some Live builds may not expose this property.
