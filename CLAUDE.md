# CLAUDE.md — Project Orientation for AI Agents

## What This Project Is

ALiveMCP Remote Script is an Ableton Live Remote Script (Python) that exposes **232 LiveAPI tools** over a TCP socket on `127.0.0.1:9004`. Clients send newline-delimited JSON commands and receive JSON responses. The project is designed for use with AI agents (including Claude via MCP), algorithmic composition tools, and any external software that needs to control Ableton Live programmatically.

---

## Directory Map

```
alivemcp/
├── ALiveMCP_Remote/          # The Remote Script package — installed into Ableton
│   ├── __init__.py            # Entry point: ALiveMCP class + create_instance()
│   ├── liveapi_tools.py       # LiveAPITools: composes all mixin classes
│   ├── socket_server.py       # SocketServerMixin: TCP listener on port 9004
│   └── tools/
│       ├── core/               # base.py, builtin.py, registry.py
│       ├── arrangement/        # arrangement.py, arrangement_view.py, locators/browser
│       ├── automation/         # automation.py
│       ├── session/            # session_transport.py, session_automation.py
│       ├── tracks/             # tracks.py + core/routing/advanced/devices
│       ├── clips/              # clips.py + core/properties/extras/quantize
│       ├── midi/               # midi.py + notes/cc
│       ├── devices/            # devices.py + core/display/extras/racks/rack_contents
│       ├── mixing/             # mixing.py + groove/master_devices
│       ├── m4l/                # m4l.py + m4l device/audio modules
│       ├── scenes/             # scenes.py
│       ├── properties/         # app/version + misc track/clip/scene properties
│       └── (no live12 bucket)  # Live-version-specific behavior is feature-guarded
├── ableton_client.py          # TCP transport: _call_ableton(), HOST, PORT constants
├── mcp_server.py              # MCP protocol wiring (imports ableton_client)
├── mcp_server_tool_defs.py    # Compact JSON tool definitions for mcp_server
├── docs/
│   ├── API_REFERENCE.md       # Complete tool reference
│   ├── ARCHITECTURE.md        # Thread-safety design, sequence diagrams
│   ├── INSTALLATION.md        # Installation steps for macOS/Windows
│   └── TROUBLESHOOTING.md     # Common problems and solutions
├── examples/                  # Standalone client scripts (connect, basic usage, etc.)
├── tests/                     # Pytest test suite (mocked Live module)
├── scripts/
│   ├── check_file_length.py   # Pre-commit: fails if any .py file > 300 lines
│   └── check_version_bump.sh
├── .github/workflows/ci.yml   # CI: lint (ruff), tests, file length, shellcheck
├── README.md
├── MAX4LIVE_INTEGRATION.md
├── CONTRIBUTING.md
└── pyproject.toml
```

---

## How a Tool Call Works (End-to-End)

```
Client                 Socket Thread            Command Queue        Main Thread (update_display)
  |                         |                        |                        |
  |-- JSON + "\n" --------> |                        |                        |
  |                         |-- enqueue(id, cmd) --> |                        |
  |                         |-- wait on resp[id] ----|--------  ~0-16ms ----> |
  |                         |                        |<-- dequeue(id, cmd) ---|
  |                         |                        |         LiveAPI call   |
  |                         |                        |<-- enqueue result -----|
  |<-- JSON + "\n" ---------|<-- dequeue result -----|                        |
```

Key constraint: **All LiveAPI calls must execute on the main thread** (the one that calls `update_display()`). Socket threads only enqueue and wait. This is why the queue exists — Ableton's Python API is not thread-safe.

`update_display()` is called by Ableton at ~60 Hz and processes up to 5 commands per tick.

---

## How to Add a New Tool

1. **Implement the method** in the appropriate mixin file under `ALiveMCP_Remote/tools/<domain>/`. Follow the existing pattern — wrap everything in `try/except` and return `{"ok": True, ...}` or `{"ok": False, "error": str(e)}`. Keep files under **300 lines** (the pre-commit hook enforces this; create a new mixin if needed).

   ```python
   def my_new_tool(self, track_index, some_param):
       """Brief one-line description"""
       try:
           track = self.song.tracks[track_index]
           result = track.some_property
           return {"ok": True, "result": result}
       except Exception as e:
           return {"ok": False, "error": str(e)}
   ```

2. **Register the name** in `ALiveMCP_Remote/tools/core/registry.py` by adding the method name string to `AVAILABLE_TOOLS`.

3. **Dispatch is automatic.** `ALiveMCP._process_command()` uses `getattr(self.tools, action, None)` — no dispatcher switch-case needed.

4. **Write tests** in the `tests/` directory following the existing pattern. The `Live` module is mocked via `tests/conftest.py`.

5. **Add documentation** to `docs/API_REFERENCE.md`.

6. **Run the docs/tools verifier**: after adding/removing a tool or changing docs, run `maint/verify_docs_tools.py` from the repository root and ensure it exits `0`. If it fails, either add the missing `.md` pages under `docs/wiki/tools/` or update `ALiveMCP_Remote/tools/core/registry.py` so both the registry and docs are in sync.

7. **CI / Agent requirement**: CI and any automation/agents must run the verifier as part of their checks and must fail the job or halt edits if the verifier returns a non-zero exit code. Agents performing edits should not merge or finalize changes until the verifier passes.

---

## Key Constraints

| Constraint                   | Detail                                                                                                                                                                                                                                                                                                                                                                          |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Main thread only**         | Never call `self.song.*` from a socket thread. Use the queue.                                                                                                                                                                                                                                                                                                                   |
| **300-line limit**           | Each `.py` file in `ALiveMCP_Remote/` must be ≤ 300 lines. Many files are already near the limit — split into a new mixin if needed.                                                                                                                                                                                                                                            |
| **Single responsibility**    | Every `.py` file must have one well-defined concern. Mixed responsibilities must be split before merging — check existing mixin docstrings.                                                                                                                                                                                                                                     |
| **Python 3.6+ syntax**       | Ableton Live 11 and 12 bundle Python 3.6.x. Avoid Python 3.8+ syntax (walrus operators, positional-only params). f-strings and type annotations are fine.                                                                                                                                                                                                                       |
| **No external dependencies** | The Remote Script runs inside Ableton's bundled Python. Standard library only — no `pip install`.                                                                                                                                                                                                                                                                               |
| **Localhost only**           | The socket binds to `127.0.0.1`, not `0.0.0.0`. Remote access requires an SSH tunnel or explicit reconfiguration.                                                                                                                                                                                                                                                               |
| **`scene_index` alias**      | For clip-slot operations (`create_midi_clip`, `delete_clip`, `duplicate_clip`, `launch_clip`, `stop_clip`, `get_clip_info`, `set_clip_name`, `add_notes`), the canonical parameter is `clip_index`. Legacy clients sending `scene_index` are still supported via `PARAM_ALIASES` in `ALiveMCP_Remote/__init__.py`. **Do not remove this alias** — it is part of the public API. |

---

## Protocol Quick Reference

**Request:**
```json
{"action": "set_tempo", "bpm": 128}
```

**Success response:**
```json
{"ok": true, "bpm": 128.0, "message": "Tempo set"}
```

**Error response:**
```json
{"ok": false, "error": "BPM must be between 20 and 999"}
```

Messages are newline-delimited (`\n`), UTF-8 encoded.

---

## Full Tool List

See [`docs/API_REFERENCE.md`](docs/API_REFERENCE.md) for all 232 tools with parameters and response fields.

For a navigable wiki index of tools, see [docs/wiki/INDEX.md](docs/wiki/INDEX.md).

For a quick list of tool names only, see [`ALiveMCP_Remote/tools/core/registry.py`](ALiveMCP_Remote/tools/core/registry.py).

---

## Dependency Maintenance

**Last dep check: 2026-05-09**

At the start of any session, compare today's date to the timestamp above.
If 15 or more days have passed:
1. Run `pip list --outdated` in the venv and bump safe (non-major) versions in `pyproject.toml` and `requirements-dev.txt`
2. Run `make test` to validate
3. Commit with message `chore: update deps`
4. Update the timestamp above to today's date

Skip if the session is focused on a time-sensitive fix — but do it in the next session.
