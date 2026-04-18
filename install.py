#!/usr/bin/env python3
"""
ALiveMCP Setup Script

Interactive installer for ALiveMCP — walks through every setup step and asks
for your approval before making any changes.

Usage:
    python3 install.py

Steps:
    1. Copy ALiveMCP_Remote to Ableton Live's Remote Scripts folder
    2. Configure the MCP server with Claude Code or Claude Desktop
    3. Set up git hooks (pre-commit linting, pre-push tests)
    4. Install dev dependencies (optional, for contributors)
"""

import shutil
import sys

from installer._dev_deps import step_dev_deps
from installer._git_hooks import step_git_hooks
from installer._mcp import step_mcp_server
from installer._remote_script import step_remote_script
from installer._ui import C, header, info


def main():
    bar = "═" * 60
    print(f"\n{C.BOLD}{C.CYAN}{bar}{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}   ALiveMCP Setup{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}{bar}{C.RESET}\n")
    info("Interactive setup for ALiveMCP.")
    info("Each step will describe what it does and ask for your approval")
    info("before making any changes. Press Ctrl-C at any time to quit.\n")

    try:
        step_remote_script()
        step_mcp_server()
        step_git_hooks()
        step_dev_deps()
    except KeyboardInterrupt:
        print(f"\n\n  {C.YELLOW}Setup interrupted.{C.RESET}\n")
        sys.exit(1)

    header("All done!")
    info("Reminders:")
    info("  • Select ALiveMCP_Remote as a Control Surface in Ableton Preferences")
    info("  • Restart Ableton Live to activate the Remote Script")
    if shutil.which("claude"):
        info('  • Test the connection: ask Claude "Check the Ableton connection"')
    info("  • See docs/TROUBLESHOOTING.md if anything doesn't work")
    print()


if __name__ == "__main__":
    main()
