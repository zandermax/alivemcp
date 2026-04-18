"""Shared constants, colours, and interactive UI helpers for the installer."""

import os
import platform
import subprocess
import sys

SYSTEM = platform.system()  # "Darwin", "Windows", "Linux"
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REMOTE_SCRIPT_SRC = os.path.join(REPO_ROOT, "ALiveMCP_Remote")
MCP_SERVER = os.path.join(REPO_ROOT, "mcp_server.py")

# ── Colour support ────────────────────────────────────────────────────────────

_use_color = sys.stdout.isatty() and (
    SYSTEM != "Windows" or os.environ.get("TERM") or os.environ.get("WT_SESSION")
)


class C:
    BOLD = "\033[1m" if _use_color else ""
    GREEN = "\033[92m" if _use_color else ""
    YELLOW = "\033[93m" if _use_color else ""
    RED = "\033[91m" if _use_color else ""
    CYAN = "\033[96m" if _use_color else ""
    DIM = "\033[2m" if _use_color else ""
    RESET = "\033[0m" if _use_color else ""


# ── Output helpers ────────────────────────────────────────────────────────────


def header(text):
    bar = "─" * 60
    print(f"\n{C.BOLD}{C.CYAN}{bar}{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}  {text}{C.RESET}")
    print(f"{C.BOLD}{C.CYAN}{bar}{C.RESET}\n")


def info(text):
    print(f"  {text}")


def ok(text):
    print(f"  {C.GREEN}✓{C.RESET}  {text}")


def warn(text):
    print(f"  {C.YELLOW}!{C.RESET}  {text}")


def err(text):
    print(f"  {C.RED}✗{C.RESET}  {text}")


# ── Input helpers ─────────────────────────────────────────────────────────────


def confirm(question, default=True):
    """Ask a yes/no question; return True for yes."""
    hint = "[Y/n]" if default else "[y/N]"
    while True:
        raw = input(f"\n  {C.BOLD}{question}{C.RESET} {hint}  ").strip().lower()
        if raw == "":
            return default
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("  Please enter y or n.")


def ask(prompt, default=""):
    """Prompt for a string value, showing the default in brackets."""
    hint = f" [{default}]" if default else ""
    raw = input(f"  {C.BOLD}{prompt}{C.RESET}{hint}:  ").strip()
    return raw if raw else default


def run_cmd(cmd):
    return subprocess.run(cmd)
