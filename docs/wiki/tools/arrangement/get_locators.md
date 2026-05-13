# get_locators

**Domain:** arrangement

**Summary:** List all locators/cue points with index, time, and name.

**Parameters:**
- none

**Live mapping:**
- Iterates `song.cue_points` and returns index, time, name for each.
**Example request:**
```json
{"action":"get_locators"}
```
**Example response:**
```json
{"ok": true, "locators":[{"index":0,"time":0.0,"name":"Intro"}],"count":1}
```
