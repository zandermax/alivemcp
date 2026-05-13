# Tool page template

Use this template when creating or updating tool documentation pages under `docs/wiki/tools/`.

Replace the placeholders with the tool-specific description, parameters, responses, and examples.

---

## Metadata

- **Tool name:** {TOOL_NAME}
- **Domain:** {DOMAIN}
- **Summary:** {ONE_LINE_SUMMARY}

**Parameters:**
- {param_name} ({type}) — {short description}

**Live mapping:**
- Calls into Live Object Model: {LIVE_CALLS}
- Threading: All Live API calls execute on the main thread; do not call from socket threads.

---

## Examples (canonical format)

- Leave one blank line before `**Example request:**` and one blank line between the heading and the fenced code block.
- There must be exactly one `**Example request:**` and one `**Example response:**` per tool page.
- Use `json` fenced code blocks for both examples when possible.

**Example request:**

```json
{ "action": "tool_name", "param": "value" }
```

**Example response:**

```json
{ "ok": true, "result": "..." }
```

If multiple variants are needed (numeric vs named), keep a single canonical example here and add a short "Variants" appendix below only when necessary.

---

## Ableton references

- Ableton Live API overview (Cycling '74): https://docs.cycling74.com/max8/vignettes/live_api_overview
- Live API Doc Archive (reference): https://nsuspray.github.io/Live_API_Doc/
- Live 12 release notes: https://www.ableton.com/en/release-notes/live-12/

---

## Notes

- {NOTES}

## See also

- {RELATED_TOOLS}
