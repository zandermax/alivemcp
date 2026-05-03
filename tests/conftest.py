"""
Pytest configuration and shared fixtures.

The `Live` module is only available inside the Ableton runtime, so we stub it
out here before any project code is imported. All test files inherit this
automatically — no explicit import needed.
"""

import sys
from unittest.mock import MagicMock

import pytest

sys.modules["Live"] = MagicMock()


@pytest.fixture
def song():
    """A fully-wired mock song with one track, one scene, and one return track."""
    clip_slot = MagicMock()
    clip_slot.has_clip = True

    device = MagicMock()

    arrangement_clip = MagicMock()

    track = MagicMock()
    track.clip_slots = [clip_slot]
    track.devices = [device]
    track.arrangement_clips = [arrangement_clip]

    cue_point = MagicMock()

    s = MagicMock()
    s.tracks = [track]
    s.scenes = [MagicMock()]
    s.return_tracks = [MagicMock()]
    s.cue_points = [cue_point]
    return s


@pytest.fixture
def c_instance():
    """A mock Ableton ControlSurface instance."""
    return MagicMock()


@pytest.fixture
def tools(song, c_instance):
    """A fully-constructed LiveAPITools instance backed by mock objects."""
    from ALiveMCP_Remote.liveapi_tools import LiveAPITools

    return LiveAPITools(song, c_instance)
