"""
Ableton Live TCP client.

Single responsibility: low-level TCP socket communication with the ALiveMCP
Remote Script. Exposes a single callable `_call_ableton(action, params)`
and the connection constants HOST / PORT.
"""

import json
import socket

HOST = "127.0.0.1"
PORT = 9004


def _call_ableton(action: str, params: dict) -> dict:
    """Send one command to the ALiveMCP Remote Script and return the JSON response."""
    command = {"action": action, **params}
    try:
        with socket.create_connection((HOST, PORT), timeout=10) as sock:
            sock.sendall((json.dumps(command) + "\n").encode("utf-8"))
            buf = b""
            while b"\n" not in buf:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                buf += chunk
        return json.loads(buf.decode("utf-8").strip())
    except ConnectionRefusedError:
        return {
            "ok": False,
            "error": (
                f"Cannot connect to Ableton on {HOST}:{PORT}. "
                "Is Ableton running with the ALiveMCP Remote Script loaded?"
            ),
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}
