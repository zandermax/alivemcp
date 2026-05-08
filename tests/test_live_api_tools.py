"""
Tests for LiveAPITools: get_available_tools and mixin composition.
"""

from ALiveMCP_Remote.liveapi_tools import LiveAPITools


def test_get_available_tools_returns_list(tools):
    result = tools.get_available_tools()
    assert isinstance(result, list)
    assert len(result) > 0


def test_get_available_tools_contains_builtins(tools):
    tools_list = tools.get_available_tools()
    assert "ping" in tools_list
    assert "health_check" in tools_list


def test_get_available_tools_contains_domain_tools(tools):
    tools_list = tools.get_available_tools()
    assert "start_playback" in tools_list
    assert "stop_playback" in tools_list
    assert "create_midi_track" in tools_list
    assert "create_midi_clip" in tools_list
    assert "add_notes" in tools_list
    assert "add_device" in tools_list
    assert "set_track_send" in tools_list
    assert "create_scene" in tools_list
    assert "get_project_root_folder" in tools_list
    assert "get_clip_automation_envelope" in tools_list
    assert "is_max_device" in tools_list


def test_live_api_tools_is_composed_of_all_mixins(song, c_instance):
    from ALiveMCP_Remote.tools.arrangement.arrangement import ArrangementMixin
    from ALiveMCP_Remote.tools.arrangement.arrangement_locators import ArrangementLocatorsMixin
    from ALiveMCP_Remote.tools.arrangement.arrangement_view import ArrangementViewMixin
    from ALiveMCP_Remote.tools.arrangement.take_lanes import TakeLanesMixin
    from ALiveMCP_Remote.tools.automation.automation import AutomationMixin
    from ALiveMCP_Remote.tools.clips.clips import ClipsMixin
    from ALiveMCP_Remote.tools.core.base import BaseMixin
    from ALiveMCP_Remote.tools.core.builtin import BuiltinMixin
    from ALiveMCP_Remote.tools.devices.devices import DevicesMixin
    from ALiveMCP_Remote.tools.m4l.m4l import M4LMixin
    from ALiveMCP_Remote.tools.midi.midi import MidiMixin
    from ALiveMCP_Remote.tools.mixing.mixing import MixingMixin
    from ALiveMCP_Remote.tools.properties.app_properties import AppPropertiesMixin
    from ALiveMCP_Remote.tools.scenes.scenes import ScenesMixin
    from ALiveMCP_Remote.tools.session.session_transport import SessionTransportMixin
    from ALiveMCP_Remote.tools.tracks.tracks import TracksMixin

    t = LiveAPITools(song, c_instance)
    assert isinstance(t, BaseMixin)
    assert isinstance(t, BuiltinMixin)
    assert isinstance(t, SessionTransportMixin)
    assert isinstance(t, TracksMixin)
    assert isinstance(t, ClipsMixin)
    assert isinstance(t, MidiMixin)
    assert isinstance(t, DevicesMixin)
    assert isinstance(t, MixingMixin)
    assert isinstance(t, ScenesMixin)
    assert isinstance(t, ArrangementMixin)
    assert isinstance(t, ArrangementLocatorsMixin)
    assert isinstance(t, ArrangementViewMixin)
    assert isinstance(t, TakeLanesMixin)
    assert isinstance(t, AutomationMixin)
    assert isinstance(t, M4LMixin)
    assert isinstance(t, AppPropertiesMixin)
