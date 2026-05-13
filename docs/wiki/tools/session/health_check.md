# health_check

**Domain:** session

**Summary:** Performs a lightweight diagnostic check of the MCP service and returns version/uptime info.

**Parameters:** None

**Live mapping:** No Live API calls; returns diagnostic info such as server version and uptime. Useful for monitoring.

**Example request:**
```json
{"action": "health_check"}
```

**Example response:**
```json
{"ok": true, "version": "0.0.0", "uptime_seconds": 123}
```

**See also:**
- [ping](tools/session/ping.md)
