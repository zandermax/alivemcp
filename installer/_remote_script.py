"""Step 1 — Copy ALiveMCP_Remote into Ableton's Remote Scripts folder."""

import glob
import os
import shutil

from installer._ui import (
    REMOTE_SCRIPT_SRC,
    SYSTEM,
    C,
    ask,
    confirm,
    err,
    header,
    info,
    ok,
    warn,
)

_KNOWN_RS_PATHS = {
    "Darwin": [
        os.path.expanduser("~/Music/Ableton/User Library/Remote Scripts"),
        os.path.expanduser("~/Documents/Ableton/User Library/Remote Scripts"),
    ],
    "Windows": [
        os.path.expandvars(r"%USERPROFILE%\Documents\Ableton\User Library\Remote Scripts"),
        os.path.expandvars(r"%USERPROFILE%\Music\Ableton\User Library\Remote Scripts"),
    ],
    "Linux": [
        os.path.expanduser("~/Music/Ableton/User Library/Remote Scripts"),
        os.path.expanduser("~/Documents/Ableton/User Library/Remote Scripts"),
    ],
}


def _find_remote_scripts_path():
    """Return the first existing Ableton Remote Scripts directory, or None."""
    for path in _KNOWN_RS_PATHS.get(SYSTEM, []):
        if os.path.isdir(path):
            return path
    for pattern in [
        os.path.expanduser("~/Music/Ableton/*/Remote Scripts"),
        os.path.expanduser("~/Documents/Ableton/*/Remote Scripts"),
    ]:
        for found in glob.glob(pattern):
            if os.path.isdir(found):
                return found
    return None


def _resolve_target_dir():
    """Auto-detect or prompt for the Remote Scripts directory. Returns path or None."""
    print(f"  {C.DIM}Searching for Ableton Remote Scripts folder…{C.RESET}")
    detected = _find_remote_scripts_path()

    if detected:
        ok(f"Found:  {detected}")
        if confirm("Use this path?", default=True):
            return detected
        return ask("Enter path to Remote Scripts folder") or None

    warn("Could not auto-detect Ableton Remote Scripts folder.")
    info("Common locations:")
    info("  macOS / Linux:  ~/Music/Ableton/User Library/Remote Scripts")
    info(r"  Windows:        %USERPROFILE%\Documents\Ableton\User Library\Remote Scripts")
    return ask("Enter path to Remote Scripts folder") or None


def _choose_mode(dest):
    """Handle existing installation and ask for copy/symlink. Returns mode or None to skip."""
    already_exists = os.path.isdir(dest) or os.path.islink(dest)
    if already_exists:
        link_note = " (symlink)" if os.path.islink(dest) else ""
        info(f"\nALiveMCP_Remote already exists{link_note} at:\n    {dest}")
        action = ask("What would you like to do? [update / skip]", default="update").lower()
        if action not in ("update", "u"):
            info("Skipping — existing installation left unchanged.")
            return None

    print()
    info("Installation mode:")
    info("  copy    — standalone copy, no dependency on this repo folder")
    info("  symlink — live link to this repo (edits here take effect immediately)")
    mode = ask("Mode", default="copy").lower()
    while mode not in ("copy", "symlink"):
        mode = ask("Please enter 'copy' or 'symlink'", default="copy").lower()
    return mode


def _perform_install(dest, target_dir, mode):
    """Remove any existing installation and copy/symlink the remote script."""
    if os.path.islink(dest):
        os.unlink(dest)
    elif os.path.isdir(dest):
        shutil.rmtree(dest)

    os.makedirs(target_dir, exist_ok=True)

    try:
        if mode == "symlink":
            os.symlink(REMOTE_SCRIPT_SRC, dest)
        else:
            shutil.copytree(REMOTE_SCRIPT_SRC, dest)
        ok(f"ALiveMCP_Remote installed to:\n    {dest}")
    except OSError as e:
        err(f"Failed: {e}")
        if SYSTEM == "Windows":
            warn("On Windows, symlinks may require Developer Mode or admin privileges.")
        return

    print()
    info("Next: in Ableton Live, open Preferences → Link Tempo MIDI,")
    info("      set a Control Surface slot to ALiveMCP_Remote, then restart Ableton.")


def step_remote_script():
    header("Step 1 of 4 — Remote Script Installation")
    info("Copies ALiveMCP_Remote into Ableton's Remote Scripts folder.")
    info("Afterwards, select it as a Control Surface in Ableton Preferences.\n")

    target_dir = _resolve_target_dir()
    if not target_dir:
        warn("No path provided — skipping Remote Script installation.")
        return

    target_dir = os.path.expanduser(os.path.expandvars(target_dir))
    dest = os.path.join(target_dir, "ALiveMCP_Remote")

    mode = _choose_mode(dest)
    if mode is None:
        return

    verb = "Copy" if mode == "copy" else "Symlink"
    print()
    info(f"About to {verb.lower()}:")
    info(f"  FROM: {REMOTE_SCRIPT_SRC}")
    info(f"  TO:   {dest}")
    if not confirm("Proceed?", default=True):
        info("Skipped.")
        return

    _perform_install(dest, target_dir, mode)
