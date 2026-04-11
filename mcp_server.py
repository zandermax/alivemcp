#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["mcp>=1.0.0"]
# ///
"""
ALiveMCP MCP Server - Exposes Ableton Live control to AI agents via Model Context Protocol.

Bridges MCP to the ALiveMCP Remote Script TCP socket on 127.0.0.1:9004.
Ableton Live must be running with the ALiveMCP Remote Script loaded.
"""

import asyncio
import json
import socket

import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions

HOST = "127.0.0.1"
PORT = 9004

_INT = "integer"
_NUM = "number"
_STR = "string"
_BOOL = "boolean"


def _p(type_: str, desc: str) -> dict:
    return {"type": type_, "description": desc}


def _schema(props: dict, required: list | None = None) -> dict:
    s: dict = {"type": "object", "properties": props}
    if required:
        s["required"] = required
    return s


def _call_ableton(action: str, params: dict) -> dict:
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


# (name, description, input_schema)
TOOL_DEFS: list[tuple[str, str, dict]] = [
    # ── Utility ───────────────────────────────────────────────────────────────
    ("ping", "Check that the ALiveMCP Remote Script is running in Ableton.", _schema({})),
    ("health_check", "Get health status: Ableton version, queue depth, tool count.", _schema({})),
    # ── Session Control ───────────────────────────────────────────────────────
    ("start_playback", "Start Ableton playback (no-op if already playing).", _schema({})),
    ("stop_playback", "Stop Ableton playback (no-op if not playing).", _schema({})),
    ("start_recording", "Enable record mode and start playback.", _schema({})),
    ("stop_recording", "Disable record mode (does not stop playback).", _schema({})),
    ("continue_playing", "Continue playback from the current position.", _schema({})),
    (
        "get_session_info",
        "Get a full snapshot of the session state (tempo, tracks, scenes, playback status).",
        _schema({}),
    ),
    (
        "set_tempo",
        "Set the session tempo. Valid range: 20–999 BPM.",
        _schema({"bpm": _p(_NUM, "Tempo in BPM (20–999)")}, required=["bpm"]),
    ),
    (
        "set_time_signature",
        "Set the session time signature.",
        _schema(
            {
                "numerator": _p(_INT, "Numerator (1–99)"),
                "denominator": _p(_INT, "Denominator: 1, 2, 4, 8, or 16"),
            },
            required=["numerator", "denominator"],
        ),
    ),
    (
        "set_loop_start",
        "Set arrangement loop start position in beats.",
        _schema({"position": _p(_NUM, "Position in beats")}, required=["position"]),
    ),
    (
        "set_loop_length",
        "Set arrangement loop length in beats.",
        _schema({"length": _p(_NUM, "Length in beats")}, required=["length"]),
    ),
    (
        "set_metronome",
        "Enable or disable the metronome.",
        _schema({"enabled": _p(_BOOL, "True to enable")}, required=["enabled"]),
    ),
    ("tap_tempo", "Send a tap-tempo pulse.", _schema({})),
    ("undo", "Undo the last action in Ableton.", _schema({})),
    ("redo", "Redo the last undone action in Ableton.", _schema({})),
    # ── Transport ─────────────────────────────────────────────────────────────
    (
        "jump_to_time",
        "Move the playback position to a specific beat.",
        _schema({"time_in_beats": _p(_NUM, "Target position in beats")}, required=["time_in_beats"]),
    ),
    ("get_current_time", "Get the current playback position and playing state.", _schema({})),
    (
        "set_arrangement_overdub",
        "Enable or disable arrangement overdub.",
        _schema({"enabled": _p(_BOOL, "True to enable overdub")}, required=["enabled"]),
    ),
    (
        "set_back_to_arranger",
        "Enable or disable Back to Arrangement mode.",
        _schema({"enabled": _p(_BOOL, "True to enable")}, required=["enabled"]),
    ),
    (
        "set_punch_in",
        "Enable or disable punch-in recording.",
        _schema({"enabled": _p(_BOOL, "True to enable punch-in")}, required=["enabled"]),
    ),
    (
        "set_punch_out",
        "Enable or disable punch-out recording.",
        _schema({"enabled": _p(_BOOL, "True to enable punch-out")}, required=["enabled"]),
    ),
    ("nudge_up", "Nudge the playback position up.", _schema({})),
    ("nudge_down", "Nudge the playback position down.", _schema({})),
    # ── Automation ────────────────────────────────────────────────────────────
    ("re_enable_automation", "Re-enable all overridden automation.", _schema({})),
    ("get_session_automation_record", "Get whether session automation recording is enabled.", _schema({})),
    (
        "set_session_automation_record",
        "Enable or disable session automation recording.",
        _schema({"enabled": _p(_BOOL, "True to enable")}, required=["enabled"]),
    ),
    ("get_session_record", "Get the session record state.", _schema({})),
    (
        "set_session_record",
        "Enable or disable session recording.",
        _schema({"enabled": _p(_BOOL, "True to enable")}, required=["enabled"]),
    ),
    ("capture_midi", "Capture the last-played MIDI notes into a clip.", _schema({})),
    # ── Track Management ──────────────────────────────────────────────────────
    (
        "create_midi_track",
        "Create a new MIDI track at the end of the track list.",
        _schema({"name": _p(_STR, "Optional track name")}),
    ),
    (
        "create_audio_track",
        "Create a new audio track at the end of the track list.",
        _schema({"name": _p(_STR, "Optional track name")}),
    ),
    ("create_return_track", "Create a new return track.", _schema({})),
    (
        "delete_track",
        "Delete a track by index.",
        _schema({"track_index": _p(_INT, "0-based track index")}, required=["track_index"]),
    ),
    (
        "duplicate_track",
        "Duplicate a track; copy inserted immediately after the original.",
        _schema({"track_index": _p(_INT, "0-based track index")}, required=["track_index"]),
    ),
    (
        "rename_track",
        "Rename a track.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "name": _p(_STR, "New name")},
            required=["track_index", "name"],
        ),
    ),
    (
        "set_track_volume",
        "Set a track's volume (0.0 to 1.0).",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "volume": _p(_NUM, "Volume 0.0–1.0")},
            required=["track_index", "volume"],
        ),
    ),
    (
        "set_track_pan",
        "Set a track's panning (-1.0 full left to 1.0 full right).",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "pan": _p(_NUM, "Pan -1.0 to 1.0")},
            required=["track_index", "pan"],
        ),
    ),
    (
        "arm_track",
        "Arm or disarm a track for recording.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "armed": _p(_BOOL, "True to arm (default true)")},
            required=["track_index"],
        ),
    ),
    (
        "solo_track",
        "Solo or unsolo a track.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "solo": _p(_BOOL, "True to solo (default true)")},
            required=["track_index"],
        ),
    ),
    (
        "mute_track",
        "Mute or unmute a track.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "mute": _p(_BOOL, "True to mute (default true)")},
            required=["track_index"],
        ),
    ),
    (
        "get_track_info",
        "Get detailed information about a track (name, volume, pan, devices, clips, etc.).",
        _schema({"track_index": _p(_INT, "0-based track index")}, required=["track_index"]),
    ),
    (
        "set_track_color",
        "Set a track's color using an Ableton color index.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "color_index": _p(_INT, "Ableton color index")},
            required=["track_index", "color_index"],
        ),
    ),
    # ── Track Routing & Monitoring ────────────────────────────────────────────
    (
        "set_track_fold_state",
        "Fold or unfold a group track.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "folded": _p(_BOOL, "True to fold")},
            required=["track_index", "folded"],
        ),
    ),
    (
        "set_track_input_routing",
        "Set a track's input routing type.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "routing_type_name": _p(_STR, "Routing type name"),
                "routing_channel": _p(_INT, "Channel index (default 0)"),
            },
            required=["track_index", "routing_type_name"],
        ),
    ),
    (
        "set_track_output_routing",
        "Set a track's output routing type.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "routing_type_name": _p(_STR, "Routing type name")},
            required=["track_index", "routing_type_name"],
        ),
    ),
    (
        "set_track_send",
        "Set a send level for a track (0.0 to 1.0).",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "send_index": _p(_INT, "0-based return track index"),
                "value": _p(_NUM, "Send level 0.0–1.0"),
            },
            required=["track_index", "send_index", "value"],
        ),
    ),
    (
        "get_track_sends",
        "Get all send levels for a track.",
        _schema({"track_index": _p(_INT, "0-based track index")}, required=["track_index"]),
    ),
    (
        "set_track_current_monitoring_state",
        "Set track monitoring state: 0=In, 1=Auto, 2=Off.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "state": _p(_INT, "0=In, 1=Auto, 2=Off")},
            required=["track_index", "state"],
        ),
    ),
    (
        "get_track_available_input_routing_types",
        "List available input routing type names for a track.",
        _schema({"track_index": _p(_INT, "0-based track index")}, required=["track_index"]),
    ),
    (
        "get_track_available_output_routing_types",
        "List available output routing type names for a track.",
        _schema({"track_index": _p(_INT, "0-based track index")}, required=["track_index"]),
    ),
    (
        "get_track_input_routing_type",
        "Get the current input routing type for a track.",
        _schema({"track_index": _p(_INT, "0-based track index")}, required=["track_index"]),
    ),
    (
        "get_track_output_routing",
        "Get the current output routing configuration for a track.",
        _schema({"track_index": _p(_INT, "0-based track index")}, required=["track_index"]),
    ),
    (
        "set_track_input_sub_routing",
        "Set a track's input sub-routing channel.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "sub_routing": _p(_STR, "Sub-routing channel name")},
            required=["track_index", "sub_routing"],
        ),
    ),
    (
        "set_track_output_sub_routing",
        "Set a track's output sub-routing channel.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "sub_routing": _p(_STR, "Sub-routing channel name")},
            required=["track_index", "sub_routing"],
        ),
    ),
    # ── Track Groups ──────────────────────────────────────────────────────────
    (
        "create_group_track",
        "Create a new empty group track.",
        _schema({"name": _p(_STR, "Optional group name")}),
    ),
    (
        "group_tracks",
        "Group a range of tracks together.",
        _schema(
            {
                "start_index": _p(_INT, "First track to group"),
                "end_index": _p(_INT, "Last track to group (inclusive)"),
            },
            required=["start_index", "end_index"],
        ),
    ),
    (
        "get_track_is_grouped",
        "Check whether a track is a member of a group.",
        _schema({"track_index": _p(_INT, "0-based track index")}, required=["track_index"]),
    ),
    (
        "ungroup_track",
        "Ungroup a group track.",
        _schema({"group_track_index": _p(_INT, "Index of the group track")}, required=["group_track_index"]),
    ),
    # ── Track Freeze / Flatten ────────────────────────────────────────────────
    (
        "freeze_track",
        "Freeze a track to reduce CPU usage.",
        _schema({"track_index": _p(_INT, "0-based track index")}, required=["track_index"]),
    ),
    (
        "unfreeze_track",
        "Unfreeze a frozen track.",
        _schema({"track_index": _p(_INT, "0-based track index")}, required=["track_index"]),
    ),
    (
        "flatten_track",
        "Flatten a frozen track to audio. Track must be frozen first.",
        _schema({"track_index": _p(_INT, "0-based track index")}, required=["track_index"]),
    ),
    # ── Track Annotations ─────────────────────────────────────────────────────
    (
        "get_track_annotation",
        "Get the annotation text for a track.",
        _schema({"track_index": _p(_INT, "0-based track index")}, required=["track_index"]),
    ),
    (
        "set_track_annotation",
        "Set the annotation text for a track.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "annotation_text": _p(_STR, "Annotation text")},
            required=["track_index", "annotation_text"],
        ),
    ),
    # ── Track Delay ───────────────────────────────────────────────────────────
    (
        "get_track_delay",
        "Get a track's delay compensation value in samples.",
        _schema({"track_index": _p(_INT, "0-based track index")}, required=["track_index"]),
    ),
    (
        "set_track_delay",
        "Set a track's delay compensation in samples.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "delay_samples": _p(_NUM, "Delay in samples")},
            required=["track_index", "delay_samples"],
        ),
    ),
    # ── Clip Operations ───────────────────────────────────────────────────────
    (
        "create_midi_clip",
        "Create a new empty MIDI clip in a Session view slot. The slot must be empty.",
        _schema(
            {
                "track_index": _p(_INT, "0-based MIDI track index"),
                "scene_index": _p(_INT, "0-based scene (row) index — slot must be empty"),
                "length": _p(_NUM, "Clip length in beats (default 4.0)"),
            },
            required=["track_index", "scene_index"],
        ),
    ),
    (
        "delete_clip",
        "Delete the clip in a session slot.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "scene_index": _p(_INT, "0-based scene index")},
            required=["track_index", "scene_index"],
        ),
    ),
    (
        "duplicate_clip",
        "Duplicate the clip in a slot.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "scene_index": _p(_INT, "0-based scene index")},
            required=["track_index", "scene_index"],
        ),
    ),
    (
        "launch_clip",
        "Launch (fire) a clip.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "scene_index": _p(_INT, "0-based scene index")},
            required=["track_index", "scene_index"],
        ),
    ),
    (
        "stop_clip",
        "Stop clips on a track (all clips on the track are stopped).",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "scene_index": _p(_INT, "0-based scene index")},
            required=["track_index", "scene_index"],
        ),
    ),
    ("stop_all_clips", "Stop all playing clips across all tracks.", _schema({})),
    (
        "get_clip_info",
        "Get information about a clip (name, length, loop, MIDI/audio type, playing state, color).",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "scene_index": _p(_INT, "0-based scene index")},
            required=["track_index", "scene_index"],
        ),
    ),
    (
        "set_clip_name",
        "Rename a clip.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "scene_index": _p(_INT, "0-based scene index"),
                "name": _p(_STR, "New clip name"),
            },
            required=["track_index", "scene_index", "name"],
        ),
    ),
    # ── Clip Properties ───────────────────────────────────────────────────────
    (
        "set_clip_looping",
        "Enable or disable looping for a clip.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "looping": _p(_BOOL, "True to loop"),
            },
            required=["track_index", "clip_index", "looping"],
        ),
    ),
    (
        "set_clip_loop_start",
        "Set the loop start position within a clip in beats.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "loop_start": _p(_NUM, "Position in beats"),
            },
            required=["track_index", "clip_index", "loop_start"],
        ),
    ),
    (
        "set_clip_loop_end",
        "Set the loop end position within a clip in beats.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "loop_end": _p(_NUM, "Position in beats"),
            },
            required=["track_index", "clip_index", "loop_end"],
        ),
    ),
    (
        "set_clip_start_marker",
        "Set the start marker (playback start point) of a clip in beats.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "start_marker": _p(_NUM, "Position in beats"),
            },
            required=["track_index", "clip_index", "start_marker"],
        ),
    ),
    (
        "set_clip_end_marker",
        "Set the end marker (playback end point) of a clip in beats.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "end_marker": _p(_NUM, "Position in beats"),
            },
            required=["track_index", "clip_index", "end_marker"],
        ),
    ),
    (
        "set_clip_muted",
        "Mute or unmute a clip.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "muted": _p(_BOOL, "True to mute"),
            },
            required=["track_index", "clip_index", "muted"],
        ),
    ),
    (
        "set_clip_gain",
        "Set clip gain (audio clips only).",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "gain": _p(_NUM, "Gain value"),
            },
            required=["track_index", "clip_index", "gain"],
        ),
    ),
    (
        "set_clip_pitch_coarse",
        "Transpose a clip by semitones.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "semitones": _p(_INT, "Semitones to transpose"),
            },
            required=["track_index", "clip_index", "semitones"],
        ),
    ),
    (
        "set_clip_pitch_fine",
        "Fine-tune a clip's pitch in cents.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "cents": _p(_INT, "Cents to adjust"),
            },
            required=["track_index", "clip_index", "cents"],
        ),
    ),
    (
        "set_clip_signature_numerator",
        "Set a clip's local time signature numerator.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "numerator": _p(_INT, "Time signature numerator"),
            },
            required=["track_index", "clip_index", "numerator"],
        ),
    ),
    (
        "set_clip_color",
        "Set a clip's color using an Ableton color index.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "color_index": _p(_INT, "Ableton color index"),
            },
            required=["track_index", "clip_index", "color_index"],
        ),
    ),
    # ── Clip Annotations ──────────────────────────────────────────────────────
    (
        "get_clip_annotation",
        "Get annotation text for a clip.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "clip_index": _p(_INT, "0-based scene index")},
            required=["track_index", "clip_index"],
        ),
    ),
    (
        "set_clip_annotation",
        "Set annotation text for a clip.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "annotation_text": _p(_STR, "Annotation text"),
            },
            required=["track_index", "clip_index", "annotation_text"],
        ),
    ),
    # ── Clip Fades ────────────────────────────────────────────────────────────
    (
        "get_clip_fade_in",
        "Get the fade-in time for an audio clip.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "clip_index": _p(_INT, "0-based scene index")},
            required=["track_index", "clip_index"],
        ),
    ),
    (
        "set_clip_fade_in",
        "Set the fade-in time for an audio clip.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "fade_time": _p(_NUM, "Fade time"),
            },
            required=["track_index", "clip_index", "fade_time"],
        ),
    ),
    (
        "get_clip_fade_out",
        "Get the fade-out time for an audio clip.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "clip_index": _p(_INT, "0-based scene index")},
            required=["track_index", "clip_index"],
        ),
    ),
    (
        "set_clip_fade_out",
        "Set the fade-out time for an audio clip.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "fade_time": _p(_NUM, "Fade time"),
            },
            required=["track_index", "clip_index", "fade_time"],
        ),
    ),
    # ── Clip RAM Mode ─────────────────────────────────────────────────────────
    (
        "get_clip_ram_mode",
        "Check whether an audio clip is loaded into RAM.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "clip_index": _p(_INT, "0-based scene index")},
            required=["track_index", "clip_index"],
        ),
    ),
    (
        "set_clip_ram_mode",
        "Control whether an audio clip streams from disk or loads into RAM.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "ram_mode": _p(_BOOL, "True to load into RAM"),
            },
            required=["track_index", "clip_index", "ram_mode"],
        ),
    ),
    # ── Follow Actions ────────────────────────────────────────────────────────
    (
        "get_clip_follow_action",
        "Get the follow action for a clip. Codes: 0=Stop, 1=Play Again, 2=Previous, 3=Next, 4=First, 5=Last, 6=Any, 7=Other, 8=Jump.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "clip_index": _p(_INT, "0-based scene index")},
            required=["track_index", "clip_index"],
        ),
    ),
    (
        "set_clip_follow_action",
        "Set follow actions for a clip. Codes: 0=Stop, 1=Play Again, 2=Previous, 3=Next, 4=First, 5=Last, 6=Any, 7=Other, 8=Jump.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "action_A": _p(_INT, "Follow action A code (0–8)"),
                "action_B": _p(_INT, "Follow action B code (0–8)"),
                "chance_A": _p(_NUM, "Probability for action A, 0.0–1.0 (default 1.0)"),
            },
            required=["track_index", "clip_index", "action_A", "action_B"],
        ),
    ),
    (
        "set_follow_action_time",
        "Set the time before the follow action triggers, in bars.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "time_in_bars": _p(_NUM, "Time in bars"),
            },
            required=["track_index", "clip_index", "time_in_bars"],
        ),
    ),
    # ── MIDI Notes ────────────────────────────────────────────────────────────
    (
        "add_notes",
        "Add MIDI notes to a clip. Each note: {pitch (0-127), start (beats), duration (beats), velocity (0-127)}.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "scene_index": _p(_INT, "0-based scene index"),
                "notes": {
                    "type": "array",
                    "description": "List of notes with pitch (0-127), start (beats), duration (beats), velocity (0-127)",
                    "items": {
                        "type": "object",
                        "properties": {
                            "pitch": {"type": "integer", "description": "MIDI note 0–127"},
                            "start": {"type": "number", "description": "Start time in beats"},
                            "duration": {"type": "number", "description": "Duration in beats (> 0)"},
                            "velocity": {"type": "integer", "description": "Velocity 0–127"},
                        },
                        "required": ["pitch", "start", "duration", "velocity"],
                    },
                },
            },
            required=["track_index", "scene_index", "notes"],
        ),
    ),
    (
        "get_clip_notes",
        "Get all MIDI notes from a clip.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "clip_index": _p(_INT, "0-based scene index")},
            required=["track_index", "clip_index"],
        ),
    ),
    (
        "remove_notes",
        "Remove MIDI notes from a clip within a pitch and time range.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "pitch_from": _p(_INT, "Lowest pitch to remove (default 0)"),
                "pitch_to": _p(_INT, "Highest pitch to remove (default 127)"),
                "time_from": _p(_NUM, "Start time in beats (default 0.0)"),
                "time_to": _p(_NUM, "End time in beats (default 999.0)"),
            },
            required=["track_index", "clip_index"],
        ),
    ),
    (
        "select_all_notes",
        "Select all notes in a MIDI clip.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "clip_index": _p(_INT, "0-based scene index")},
            required=["track_index", "clip_index"],
        ),
    ),
    (
        "deselect_all_notes",
        "Deselect all notes in a MIDI clip.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "clip_index": _p(_INT, "0-based scene index")},
            required=["track_index", "clip_index"],
        ),
    ),
    (
        "replace_selected_notes",
        "Replace the currently selected notes with new notes.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "notes": {
                    "type": "array",
                    "description": "Replacement notes with pitch, start, duration, velocity, optional muted",
                    "items": {"type": "object"},
                },
            },
            required=["track_index", "clip_index", "notes"],
        ),
    ),
    (
        "get_notes_extended",
        "Get MIDI notes filtered by time and pitch range.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "start_time": _p(_NUM, "Filter start time in beats"),
                "time_span": _p(_NUM, "Duration of filter window in beats"),
                "start_pitch": _p(_INT, "Lowest pitch to include"),
                "pitch_span": _p(_INT, "Number of pitches to include"),
            },
            required=["track_index", "clip_index", "start_time", "time_span", "start_pitch", "pitch_span"],
        ),
    ),
    # ── MIDI CC / Program Change ──────────────────────────────────────────────
    (
        "send_midi_cc",
        "Send a MIDI Control Change message.",
        _schema(
            {
                "track_index": _p(_INT, "Track index (required but unused for routing)"),
                "cc_number": _p(_INT, "CC number 0–127"),
                "cc_value": _p(_INT, "CC value 0–127"),
                "channel": _p(_INT, "MIDI channel 0-based (default 0 = ch 1)"),
            },
            required=["track_index", "cc_number", "cc_value"],
        ),
    ),
    (
        "send_program_change",
        "Send a MIDI Program Change message.",
        _schema(
            {
                "track_index": _p(_INT, "Track index (required but unused for routing)"),
                "program_number": _p(_INT, "Program number 0–127"),
                "channel": _p(_INT, "MIDI channel 0-based (default 0)"),
            },
            required=["track_index", "program_number"],
        ),
    ),
    # ── Devices ───────────────────────────────────────────────────────────────
    (
        "add_device",
        "Request adding a device to a track by name.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "device_name": _p(_STR, "Device name to add")},
            required=["track_index", "device_name"],
        ),
    ),
    (
        "get_track_devices",
        "Get all devices on a track.",
        _schema({"track_index": _p(_INT, "0-based track index")}, required=["track_index"]),
    ),
    (
        "set_device_param",
        "Set a device parameter by index.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "device_index": _p(_INT, "0-based device index"),
                "param_index": _p(_INT, "0-based parameter index"),
                "value": _p(_NUM, "Parameter value"),
            },
            required=["track_index", "device_index", "param_index", "value"],
        ),
    ),
    (
        "set_device_on_off",
        "Enable or disable a device.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "device_index": _p(_INT, "0-based device index"),
                "enabled": _p(_BOOL, "True to enable"),
            },
            required=["track_index", "device_index", "enabled"],
        ),
    ),
    (
        "get_device_parameters",
        "Get all parameters for a device.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "device_index": _p(_INT, "0-based device index")},
            required=["track_index", "device_index"],
        ),
    ),
    (
        "get_device_parameter_by_name",
        "Find a device parameter by name.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "device_index": _p(_INT, "0-based device index"),
                "param_name": _p(_STR, "Parameter name"),
            },
            required=["track_index", "device_index", "param_name"],
        ),
    ),
    (
        "set_device_parameter_by_name",
        "Set a device parameter by name.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "device_index": _p(_INT, "0-based device index"),
                "param_name": _p(_STR, "Parameter name"),
                "value": _p(_NUM, "New value"),
            },
            required=["track_index", "device_index", "param_name", "value"],
        ),
    ),
    (
        "delete_device",
        "Delete a device from a track.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "device_index": _p(_INT, "0-based device index")},
            required=["track_index", "device_index"],
        ),
    ),
    (
        "get_device_presets",
        "Get available presets for a device.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "device_index": _p(_INT, "0-based device index")},
            required=["track_index", "device_index"],
        ),
    ),
    (
        "set_device_preset",
        "Load a preset for a device by index.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "device_index": _p(_INT, "0-based device index"),
                "preset_index": _p(_INT, "0-based preset index"),
            },
            required=["track_index", "device_index", "preset_index"],
        ),
    ),
    (
        "randomize_device_parameters",
        "Randomize all non-quantized parameters of a device.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "device_index": _p(_INT, "0-based device index")},
            required=["track_index", "device_index"],
        ),
    ),
    (
        "randomize_device",
        "Randomize all enabled, non-quantized parameters of a device (richer response).",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "device_index": _p(_INT, "0-based device index")},
            required=["track_index", "device_index"],
        ),
    ),
    # ── Rack / Chain ──────────────────────────────────────────────────────────
    (
        "get_device_chains",
        "Get the chains of an instrument/effect rack device.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "device_index": _p(_INT, "0-based rack device index")},
            required=["track_index", "device_index"],
        ),
    ),
    (
        "get_chain_devices",
        "Get all devices within a specific rack chain.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "device_index": _p(_INT, "0-based rack device index"),
                "chain_index": _p(_INT, "0-based chain index"),
            },
            required=["track_index", "device_index", "chain_index"],
        ),
    ),
    (
        "set_chain_mute",
        "Mute or unmute a rack chain.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "device_index": _p(_INT, "0-based rack device index"),
                "chain_index": _p(_INT, "0-based chain index"),
                "mute": _p(_BOOL, "True to mute"),
            },
            required=["track_index", "device_index", "chain_index", "mute"],
        ),
    ),
    (
        "set_chain_solo",
        "Solo or unsolo a rack chain.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "device_index": _p(_INT, "0-based rack device index"),
                "chain_index": _p(_INT, "0-based chain index"),
                "solo": _p(_BOOL, "True to solo"),
            },
            required=["track_index", "device_index", "chain_index", "solo"],
        ),
    ),
    # ── Plugin Windows ────────────────────────────────────────────────────────
    (
        "show_plugin_window",
        "Show the editor window for a device/plugin.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "device_index": _p(_INT, "0-based device index")},
            required=["track_index", "device_index"],
        ),
    ),
    (
        "hide_plugin_window",
        "Hide the editor window for a device/plugin.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "device_index": _p(_INT, "0-based device index")},
            required=["track_index", "device_index"],
        ),
    ),
    # ── Device Utilities ──────────────────────────────────────────────────────
    (
        "get_device_class_name",
        "Get the internal class name of a device (e.g. 'OriginalSimpler', 'Compressor2').",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "device_index": _p(_INT, "0-based device index")},
            required=["track_index", "device_index"],
        ),
    ),
    (
        "get_device_type",
        "Get the device type: 0=audio_effect, 1=instrument, 2=midi_effect.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "device_index": _p(_INT, "0-based device index")},
            required=["track_index", "device_index"],
        ),
    ),
    # ── Master Track ──────────────────────────────────────────────────────────
    ("get_master_track_info", "Get master track information (name, volume, pan, devices).", _schema({})),
    (
        "set_master_volume",
        "Set master track volume (0.0 to 1.0).",
        _schema({"volume": _p(_NUM, "Volume 0.0–1.0")}, required=["volume"]),
    ),
    (
        "set_master_pan",
        "Set master track pan (-1.0 to 1.0).",
        _schema({"pan": _p(_NUM, "Pan -1.0 to 1.0")}, required=["pan"]),
    ),
    ("get_master_devices", "Get all devices on the master track.", _schema({})),
    # ── Return Tracks ─────────────────────────────────────────────────────────
    ("get_return_track_count", "Get the number of return tracks.", _schema({})),
    (
        "get_return_track_info",
        "Get information about a return track.",
        _schema({"return_index": _p(_INT, "0-based return track index")}, required=["return_index"]),
    ),
    (
        "set_return_track_volume",
        "Set a return track's volume (0.0 to 1.0).",
        _schema(
            {"return_index": _p(_INT, "0-based return track index"), "volume": _p(_NUM, "Volume 0.0–1.0")},
            required=["return_index", "volume"],
        ),
    ),
    # ── Crossfader ────────────────────────────────────────────────────────────
    (
        "get_crossfader_assignment",
        "Get a track's crossfader assignment: 0=None, 1=A, 2=B.",
        _schema({"track_index": _p(_INT, "0-based track index")}, required=["track_index"]),
    ),
    (
        "set_crossfader_assignment",
        "Set a track's crossfader assignment: 0=None, 1=A, 2=B.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "assignment": _p(_INT, "0=None, 1=A, 2=B")},
            required=["track_index", "assignment"],
        ),
    ),
    ("get_crossfader_position", "Get the master crossfader position (-1.0 to 1.0).", _schema({})),
    # ── Groove & Quantize ─────────────────────────────────────────────────────
    (
        "set_clip_groove_amount",
        "Set groove amount for a clip (0.0 to 1.0).",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "amount": _p(_NUM, "Groove amount 0.0–1.0"),
            },
            required=["track_index", "clip_index", "amount"],
        ),
    ),
    (
        "quantize_clip",
        "Quantize a MIDI clip to a grid value (e.g. 0.25 for 16th notes).",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "quantize_to": _p(_NUM, "Grid size in beats (e.g. 0.25 for 16th notes)"),
            },
            required=["track_index", "clip_index", "quantize_to"],
        ),
    ),
    (
        "quantize_clip_pitch",
        "Quantize MIDI clip pitch to a target pitch.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "pitch": _p(_INT, "Target pitch MIDI note (default 60)"),
            },
            required=["track_index", "clip_index"],
        ),
    ),
    ("get_groove_amount", "Get the global song groove amount.", _schema({})),
    (
        "set_groove_amount",
        "Set the global song groove amount (0.0 to 1.0).",
        _schema({"amount": _p(_NUM, "Groove amount 0.0–1.0")}, required=["amount"]),
    ),
    # ── Groove Pool ───────────────────────────────────────────────────────────
    ("get_groove_pool_grooves", "List all grooves in the groove pool.", _schema({})),
    (
        "set_clip_groove",
        "Assign a groove pool groove to a clip.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "groove_index": _p(_INT, "Index into groove pool"),
            },
            required=["track_index", "clip_index", "groove_index"],
        ),
    ),
    # ── Scenes ────────────────────────────────────────────────────────────────
    (
        "create_scene",
        "Create a new scene at the end of the scene list.",
        _schema({"name": _p(_STR, "Optional scene name")}),
    ),
    (
        "delete_scene",
        "Delete a scene by index.",
        _schema({"scene_index": _p(_INT, "0-based scene index")}, required=["scene_index"]),
    ),
    (
        "duplicate_scene",
        "Duplicate a scene; copy inserted immediately after the original.",
        _schema({"scene_index": _p(_INT, "0-based scene index")}, required=["scene_index"]),
    ),
    (
        "launch_scene",
        "Launch (fire) all clips in a scene.",
        _schema({"scene_index": _p(_INT, "0-based scene index")}, required=["scene_index"]),
    ),
    (
        "rename_scene",
        "Rename a scene.",
        _schema(
            {"scene_index": _p(_INT, "0-based scene index"), "name": _p(_STR, "New scene name")},
            required=["scene_index", "name"],
        ),
    ),
    (
        "get_scene_info",
        "Get information about a scene (name, color, tempo, time signature).",
        _schema({"scene_index": _p(_INT, "0-based scene index")}, required=["scene_index"]),
    ),
    (
        "get_scene_color",
        "Get a scene's color index.",
        _schema({"scene_index": _p(_INT, "0-based scene index")}, required=["scene_index"]),
    ),
    (
        "set_scene_color",
        "Set a scene's color.",
        _schema(
            {"scene_index": _p(_INT, "0-based scene index"), "color_index": _p(_INT, "Ableton color index")},
            required=["scene_index", "color_index"],
        ),
    ),
    # ── Project & Arrangement ─────────────────────────────────────────────────
    ("get_project_root_folder", "Get the project root folder path.", _schema({})),
    (
        "trigger_session_record",
        "Trigger session recording with an optional fixed length in beats.",
        _schema({"length": _p(_NUM, "Recording length in beats; omit for open-ended")}),
    ),
    ("get_can_jump_to_next_cue", "Check whether there is a next cue point to jump to.", _schema({})),
    ("get_can_jump_to_prev_cue", "Check whether there is a previous cue point to jump to.", _schema({})),
    ("jump_to_next_cue", "Jump playback to the next cue point.", _schema({})),
    ("jump_to_prev_cue", "Jump playback to the previous cue point.", _schema({})),
    # ── Arrangement View Clips ────────────────────────────────────────────────
    (
        "get_arrangement_clips",
        "Get all clips in the arrangement view for a track.",
        _schema({"track_index": _p(_INT, "0-based track index")}, required=["track_index"]),
    ),
    (
        "duplicate_to_arrangement",
        "Duplicate a session clip to the arrangement view at the current playback position.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "clip_index": _p(_INT, "0-based scene index")},
            required=["track_index", "clip_index"],
        ),
    ),
    (
        "consolidate_clip",
        "Initiate consolidation of arrangement clips in a time range.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "start_time": _p(_NUM, "Start time in beats"),
                "end_time": _p(_NUM, "End time in beats"),
            },
            required=["track_index", "start_time", "end_time"],
        ),
    ),
    # ── View / Navigation ─────────────────────────────────────────────────────
    ("show_clip_view", "Switch to the Session view.", _schema({})),
    ("show_arrangement_view", "Switch to the Arrangement view.", _schema({})),
    (
        "focus_track",
        "Select and focus a track in the current view.",
        _schema({"track_index": _p(_INT, "0-based track index")}, required=["track_index"]),
    ),
    (
        "scroll_view_to_time",
        "Request the arrangement view to scroll to a specific time.",
        _schema({"time_in_beats": _p(_NUM, "Time in beats")}, required=["time_in_beats"]),
    ),
    # ── Loop & Locators ───────────────────────────────────────────────────────
    (
        "set_loop_enabled",
        "Enable or disable the arrangement loop.",
        _schema({"enabled": _p(_BOOL, "True to enable loop")}, required=["enabled"]),
    ),
    ("get_loop_enabled", "Get the current arrangement loop state and bounds.", _schema({})),
    (
        "create_locator",
        "Create a cue point (locator) at a specific time.",
        _schema(
            {
                "time_in_beats": _p(_NUM, "Position in beats"),
                "name": _p(_STR, "Locator name (default 'Locator')"),
            },
            required=["time_in_beats"],
        ),
    ),
    (
        "delete_locator",
        "Delete a cue point by index.",
        _schema({"locator_index": _p(_INT, "0-based locator index")}, required=["locator_index"]),
    ),
    ("get_locators", "Get all cue points.", _schema({})),
    (
        "jump_by_amount",
        "Move the playback position by a relative offset in beats (negative to go backward).",
        _schema({"amount_in_beats": _p(_NUM, "Offset in beats")}, required=["amount_in_beats"]),
    ),
    # ── Browser ───────────────────────────────────────────────────────────────
    ("browse_devices", "List Ableton device categories available in the browser.", _schema({})),
    (
        "browse_plugins",
        "Get plugin browsing status.",
        _schema({"plugin_type": _p(_STR, "Plugin type (default 'vst')")}),
    ),
    (
        "load_device_from_browser",
        "Load a device from the browser onto a track by name.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "device_name": _p(_STR, "Device name")},
            required=["track_index", "device_name"],
        ),
    ),
    (
        "get_browser_items",
        "Get browser items for a category: devices, plugins, instruments, audio_effects, midi_effects.",
        _schema({"category": _p(_STR, "Category name (default 'devices')")}),
    ),
    # ── Color Utilities ───────────────────────────────────────────────────────
    (
        "get_clip_color",
        "Get the color of a clip.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "clip_index": _p(_INT, "0-based scene index")},
            required=["track_index", "clip_index"],
        ),
    ),
    (
        "get_track_color",
        "Get the color of a track.",
        _schema({"track_index": _p(_INT, "0-based track index")}, required=["track_index"]),
    ),
    # ── Clip Automation Envelopes ─────────────────────────────────────────────
    (
        "get_clip_automation_envelope",
        "Check whether an automation envelope exists for a device parameter in a clip.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "device_index": _p(_INT, "0-based device index"),
                "param_index": _p(_INT, "0-based parameter index"),
            },
            required=["track_index", "clip_index", "device_index", "param_index"],
        ),
    ),
    (
        "create_automation_envelope",
        "Create an automation envelope for a device parameter in a clip.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "device_index": _p(_INT, "0-based device index"),
                "param_index": _p(_INT, "0-based parameter index"),
            },
            required=["track_index", "clip_index", "device_index", "param_index"],
        ),
    ),
    (
        "clear_automation_envelope",
        "Clear (delete) the automation envelope for a device parameter in a clip.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "device_index": _p(_INT, "0-based device index"),
                "param_index": _p(_INT, "0-based parameter index"),
            },
            required=["track_index", "clip_index", "device_index", "param_index"],
        ),
    ),
    (
        "insert_automation_step",
        "Insert an automation breakpoint at a specific time and value.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "device_index": _p(_INT, "0-based device index"),
                "param_index": _p(_INT, "0-based parameter index"),
                "time": _p(_NUM, "Time in beats"),
                "value": _p(_NUM, "Automation value"),
            },
            required=["track_index", "clip_index", "device_index", "param_index", "time", "value"],
        ),
    ),
    (
        "remove_automation_step",
        "Remove an automation breakpoint at a specific time.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "device_index": _p(_INT, "0-based device index"),
                "param_index": _p(_INT, "0-based parameter index"),
                "time": _p(_NUM, "Time in beats of breakpoint to remove"),
            },
            required=["track_index", "clip_index", "device_index", "param_index", "time"],
        ),
    ),
    (
        "get_automation_envelope_values",
        "Check whether an automation envelope has any breakpoints.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "device_index": _p(_INT, "0-based device index"),
                "param_index": _p(_INT, "0-based parameter index"),
            },
            required=["track_index", "clip_index", "device_index", "param_index"],
        ),
    ),
    # ── Audio Clips (Warp) ────────────────────────────────────────────────────
    (
        "get_clip_warp_mode",
        "Get the warp mode for an audio clip. 0=Beats, 1=Tones, 2=Texture, 3=Re-Pitch, 4=Complex, 5=Complex Pro.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "clip_index": _p(_INT, "0-based scene index")},
            required=["track_index", "clip_index"],
        ),
    ),
    (
        "set_clip_warp_mode",
        "Set the warp mode for an audio clip. 0=Beats, 1=Tones, 2=Texture, 3=Re-Pitch, 4=Complex, 5=Complex Pro.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "warp_mode": _p(_INT, "Warp mode 0–5"),
            },
            required=["track_index", "clip_index", "warp_mode"],
        ),
    ),
    (
        "get_clip_file_path",
        "Get the file path of the audio sample for an audio clip.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "clip_index": _p(_INT, "0-based scene index")},
            required=["track_index", "clip_index"],
        ),
    ),
    (
        "set_clip_warping",
        "Enable or disable warping for an audio clip.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "warping": _p(_BOOL, "True to enable warping"),
            },
            required=["track_index", "clip_index", "warping"],
        ),
    ),
    (
        "get_warp_markers",
        "Get all warp markers from an audio clip.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "clip_index": _p(_INT, "0-based scene index")},
            required=["track_index", "clip_index"],
        ),
    ),
    # ── Sample / Simpler ──────────────────────────────────────────────────────
    (
        "get_sample_length",
        "Get the raw sample length of an audio clip.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "clip_index": _p(_INT, "0-based scene index")},
            required=["track_index", "clip_index"],
        ),
    ),
    (
        "get_sample_playback_mode",
        "Get the playback mode of a Simpler or Sampler device.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "device_index": _p(_INT, "0-based device index")},
            required=["track_index", "device_index"],
        ),
    ),
    (
        "set_sample_playback_mode",
        "Set the playback mode of a Simpler or Sampler device.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "device_index": _p(_INT, "0-based device index"),
                "mode": _p(_INT, "Playback mode"),
            },
            required=["track_index", "device_index", "mode"],
        ),
    ),
    # ── Max for Live ──────────────────────────────────────────────────────────
    (
        "is_max_device",
        "Check whether a device is a Max for Live device.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "device_index": _p(_INT, "0-based device index")},
            required=["track_index", "device_index"],
        ),
    ),
    (
        "get_m4l_devices",
        "List all Max for Live devices on a track.",
        _schema({"track_index": _p(_INT, "0-based track index")}, required=["track_index"]),
    ),
    (
        "set_device_param_by_name",
        "Set a device parameter value by name (works with any device including M4L).",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "device_index": _p(_INT, "0-based device index"),
                "param_name": _p(_STR, "Parameter name"),
                "value": _p(_NUM, "New value"),
            },
            required=["track_index", "device_index", "param_name", "value"],
        ),
    ),
    (
        "get_m4l_param_by_name",
        "Get a device parameter value by name.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "device_index": _p(_INT, "0-based device index"),
                "param_name": _p(_STR, "Parameter name"),
            },
            required=["track_index", "device_index", "param_name"],
        ),
    ),
    (
        "get_cv_tools_devices",
        "List all CV Tools devices on a track (filtered by name containing 'CV').",
        _schema({"track_index": _p(_INT, "0-based track index")}, required=["track_index"]),
    ),
    # ── Metronome Volume ──────────────────────────────────────────────────────
    ("get_metronome_volume", "Get the metronome volume.", _schema({})),
    (
        "set_metronome_volume",
        "Set the metronome volume (0.0 to 1.0).",
        _schema({"volume": _p(_NUM, "Volume 0.0–1.0")}, required=["volume"]),
    ),
    # ── Take Lanes (Live 12+) ─────────────────────────────────────────────────
    (
        "get_take_lanes",
        "Get all take lanes on a track. Requires Live 12+.",
        _schema({"track_index": _p(_INT, "0-based track index")}, required=["track_index"]),
    ),
    (
        "create_take_lane",
        "Create a new take lane on a track. Requires Live 12+.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "name": _p(_STR, "Optional lane name")},
            required=["track_index"],
        ),
    ),
    (
        "get_take_lane_name",
        "Get the name of a specific take lane. Requires Live 12+.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "lane_index": _p(_INT, "0-based lane index")},
            required=["track_index", "lane_index"],
        ),
    ),
    (
        "set_take_lane_name",
        "Set the name of a take lane. Requires Live 12+.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "lane_index": _p(_INT, "0-based lane index"),
                "name": _p(_STR, "New lane name"),
            },
            required=["track_index", "lane_index", "name"],
        ),
    ),
    (
        "create_audio_clip_in_lane",
        "Create an audio clip inside a take lane. Requires Live 12+.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "lane_index": _p(_INT, "0-based lane index"),
                "length": _p(_NUM, "Clip length in beats (default 4.0)"),
            },
            required=["track_index", "lane_index"],
        ),
    ),
    (
        "create_midi_clip_in_lane",
        "Create a MIDI clip inside a take lane. Requires Live 12+.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "lane_index": _p(_INT, "0-based lane index"),
                "length": _p(_NUM, "Clip length in beats (default 4.0)"),
            },
            required=["track_index", "lane_index"],
        ),
    ),
    (
        "get_clips_in_take_lane",
        "Get all clips inside a take lane. Requires Live 12+.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "lane_index": _p(_INT, "0-based lane index")},
            required=["track_index", "lane_index"],
        ),
    ),
    (
        "delete_take_lane",
        "Delete a take lane. Requires Live 12+.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "lane_index": _p(_INT, "0-based lane index")},
            required=["track_index", "lane_index"],
        ),
    ),
    # ── Application Info (Live 12+) ───────────────────────────────────────────
    ("get_build_id", "Get the Ableton Live build identifier. Requires Live 12+.", _schema({})),
    ("get_variant", "Get the Ableton Live edition (e.g. 'Suite', 'Standard', 'Intro'). Requires Live 12+.", _schema({})),
    (
        "show_message_box",
        "Show a message dialog box to the user in Ableton. Requires Live 12+.",
        _schema(
            {"message": _p(_STR, "Message text"), "title": _p(_STR, "Dialog title (default 'Message')")},
            required=["message"],
        ),
    ),
    ("get_application_version", "Get full Ableton Live version information.", _schema({})),
    # ── Device Parameter Display Values (Live 12+) ────────────────────────────
    (
        "get_device_param_display_value",
        "Get a parameter's value as displayed in the Live UI (e.g. '128 Hz'). Falls back to string on older Live.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "device_index": _p(_INT, "0-based device index"),
                "param_index": _p(_INT, "0-based parameter index"),
            },
            required=["track_index", "device_index", "param_index"],
        ),
    ),
    (
        "get_all_param_display_values",
        "Get display values for all parameters of a device.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "device_index": _p(_INT, "0-based device index")},
            required=["track_index", "device_index"],
        ),
    ),
    # ── Additional Properties ─────────────────────────────────────────────────
    (
        "get_clip_start_time",
        "Get the start time property of a clip in the arrangement.",
        _schema(
            {"track_index": _p(_INT, "0-based track index"), "clip_index": _p(_INT, "0-based scene index")},
            required=["track_index", "clip_index"],
        ),
    ),
    (
        "set_clip_start_time",
        "Set the start time of a clip.",
        _schema(
            {
                "track_index": _p(_INT, "0-based track index"),
                "clip_index": _p(_INT, "0-based scene index"),
                "start_time": _p(_NUM, "Start time in beats"),
            },
            required=["track_index", "clip_index", "start_time"],
        ),
    ),
    (
        "get_track_is_foldable",
        "Check whether a track is foldable (i.e. is a group track).",
        _schema({"track_index": _p(_INT, "0-based track index")}, required=["track_index"]),
    ),
    (
        "get_track_is_frozen",
        "Check whether a track is currently frozen.",
        _schema({"track_index": _p(_INT, "0-based track index")}, required=["track_index"]),
    ),
    (
        "get_scene_is_empty",
        "Check whether a scene has no clips across all tracks.",
        _schema({"scene_index": _p(_INT, "0-based scene index")}, required=["scene_index"]),
    ),
    (
        "get_scene_tempo",
        "Get the tempo override set on a scene, if any.",
        _schema({"scene_index": _p(_INT, "0-based scene index")}, required=["scene_index"]),
    ),
    ("get_arrangement_overdub", "Get the current arrangement overdub state.", _schema({})),
    (
        "set_record_mode",
        "Set session or arrangement record mode: 0=session, 1=arrangement.",
        _schema({"mode": _p(_INT, "0=session, 1=arrangement")}, required=["mode"]),
    ),
    ("get_signature_numerator", "Get the global time signature numerator.", _schema({})),
    ("get_signature_denominator", "Get the global time signature denominator.", _schema({})),
]

# ── Server ────────────────────────────────────────────────────────────────────

server = Server("alivemcp")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(name=name, description=desc, inputSchema=schema)
        for name, desc, schema in TOOL_DEFS
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    result = await asyncio.get_event_loop().run_in_executor(
        None, _call_ableton, name, arguments or {}
    )
    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]


async def main() -> None:
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="alivemcp",
                server_version="2.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
