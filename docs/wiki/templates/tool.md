---
name: "{{TOOL_NAME}}"
domain: "{{DOMAIN}}"
summary: "One-line summary of what the tool does"
schema:
	type: object
	properties: {}
example_request: |
	{ "action": "{{TOOL_NAME}}", "...": "..." }
example_response: |
	{ "ok": true, "...": "..." }
status: draft
live_versions: [11, 12]
owners: []
tags: []
last_updated: 2026-05-14
---

# {{TOOL_NAME}}

**Domain**: {{DOMAIN}}

**Summary**: One-line description of what the tool does.

**Parameters**:

- `param_name` (type): Description and notes. Include aliases like `scene_index` → `clip_index`.

**Live mapping**:

- Which Live Object Model property/method this uses (main-thread only). Example: `song.tracks[<i>].clip_slots[<j>]`.

**Example request**:

```json
{ "action": "{{TOOL_NAME}}", "...": "..." }
```

**Example response**:

```json
{ "ok": true, "...": "..." }
```

**Notes**: threading constraints, version diffs, edge cases.

**See also**: links to related tool pages.

## Tool page template

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
- Threading: All interactions with the Live Object Model must execute on the main thread; do not call from socket threads.

---

## Docstring and `See Also` guidance

Every implementation must include a canonical docstring that points to the wiki page. Example:

```python
"""Set a track's volume level.

Args:
  track_id: Index of the target track.
  value: Volume level from 0.0 (silent) to 1.0 (unity gain).

Returns:
  None

Raises:
  IndexError: If track_id is out of range.

See Also:
  Wiki: docs/wiki/tools/tracks/set_track_volume.md
"""
```

Guidelines:

- Include exactly one `**Example request:**` and one `**Example response:**`.
- Authors must fill the `schema` frontmatter with a JSON Schema describing parameters when possible.
- Use `example_request` and `example_response` YAML scalars for canonical examples.

---

## Examples (canonical format)

- Leave one blank line before `**Example request:**` and one blank line between the heading and the fenced code block.
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

## Related Live Object Model entities and references

- [Live Object Model overview (Cycling '74)](https://docs.cycling74.com/max8/vignettes/live_api_overview)
- [Live Object Model doc archive (community)](https://nsuspray.github.io/Live_API_Doc/)
- [Live 12 release notes (Ableton)](https://www.ableton.com/en/release-notes/live-12/)

---

## Notes

- {NOTES}

## See also

- {RELATED_TOOLS}
