# ping

**Domain:** session

**Summary:** Lightweight health ping; responds to verify the MCP server is reachable.

**Parameters:** None

**Live mapping:** No Live API calls — returns a simple `ok` JSON payload for connectivity checks.

**Example request:**
```json
{"action": "ping"}
```

**Example response:**
```json
{"ok": true, "message": "pong"}
```

**See also:**
- [health_check](tools/session/health_check.md)
