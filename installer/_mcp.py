"""Step 2 — Register the MCP server with Claude Code or Claude Desktop."""

import json
import os
import shutil

from installer._ui import MCP_SERVER, SYSTEM, ask, confirm, err, header, info, ok, run_cmd, warn

_CLAUDE_DESKTOP_CONFIG = {
    "Darwin": os.path.expanduser("~/Library/Application Support/Claude/claude_desktop_config.json"),
    "Windows": os.path.expandvars(r"%APPDATA%\Claude\claude_desktop_config.json"),
    "Linux": os.path.expanduser("~/.config/Claude/claude_desktop_config.json"),
}.get(SYSTEM, "")


def _mcp_claude_code():
    info("\nConfiguring for Claude Code…")
    if not shutil.which("claude"):
        warn("'claude' CLI not found in PATH.")
        if not confirm("Continue anyway?", default=False):
            return

    server_path = ask("Path to mcp_server.py", default=MCP_SERVER)
    server_path = os.path.expanduser(os.path.expandvars(server_path))

    cmd = ["claude", "mcp", "add", "alivemcp", "--", "uv", "run", server_path]
    print()
    info(f"About to run:\n    {' '.join(cmd)}")
    if not confirm("Proceed?", default=True):
        info("Skipped.")
        return

    result = run_cmd(cmd)
    if result.returncode == 0:
        ok("MCP server registered with Claude Code.")
        info('Verify with: ask Claude "Check the Ableton connection"')
    else:
        err("Command failed — see output above.")


def _load_desktop_config(config_path):
    """Load existing claude_desktop_config.json, returning {} on missing/invalid."""
    if not os.path.isfile(config_path):
        return {}
    try:
        with open(config_path) as f:
            config = json.load(f)
        ok(f"Loaded existing config from:\n    {config_path}")
        return config
    except (json.JSONDecodeError, OSError) as e:
        warn(f"Could not read existing config: {e}")
        if confirm("Create a fresh config file?", default=True):
            return {}
        return None


def _mcp_claude_desktop():
    info("\nConfiguring for Claude Desktop…")
    config_path = ask("Path to claude_desktop_config.json", default=_CLAUDE_DESKTOP_CONFIG)
    config_path = os.path.expanduser(os.path.expandvars(config_path))

    server_path = ask("Path to mcp_server.py", default=MCP_SERVER)
    server_path = os.path.expanduser(os.path.expandvars(server_path))

    config = _load_desktop_config(config_path)
    if config is None:
        return

    config.setdefault("mcpServers", {})
    config["mcpServers"]["alivemcp"] = {"command": "uv", "args": ["run", server_path]}

    preview = json.dumps(config, indent=2)
    print()
    info(f"About to write to:\n    {config_path}")
    info("\n  Preview:\n")
    for line in preview.splitlines():
        info(f"    {line}")

    if not confirm("\nWrite this file?", default=True):
        info("Skipped.")
        return

    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, "w") as f:
        f.write(preview + "\n")
    ok("Claude Desktop config updated.")
    info("Restart Claude Desktop to apply the changes.")


def step_mcp_server():
    header("Step 2 of 4 — MCP Server Configuration")
    info("Registers the MCP server so Claude can discover and call Live tools.\n")

    info("Which client would you like to configure?")
    info("  1)  Claude Code  (CLI — recommended)")
    info("  2)  Claude Desktop")
    info("  3)  Skip")
    choice = ask("Choice", default="1")

    if choice in ("3", "skip", "s"):
        info("Skipped.")
    elif choice == "1":
        _mcp_claude_code()
    elif choice == "2":
        _mcp_claude_desktop()
    else:
        warn(f"Unknown choice '{choice}' — skipping.")
