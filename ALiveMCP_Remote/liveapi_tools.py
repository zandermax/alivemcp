"""
LiveAPI Tools Implementation for ALiveMCP Remote Script
Implements all LiveAPI operations for controlling Ableton Live

Composed from domain-specific mixin modules in the tools/ package.

Author: Claude Code
License: MIT
"""

from .tools.arrangement.arrangement import ArrangementMixin
from .tools.arrangement.arrangement_locators import ArrangementLocatorsMixin
from .tools.arrangement.arrangement_view import ArrangementViewMixin
from .tools.arrangement.take_lanes import TakeLanesMixin
from .tools.automation.automation import AutomationMixin
from .tools.clips.clips import ClipsMixin
from .tools.clips.clips_color import ClipsColorMixin
from .tools.clips.clips_follow_actions import ClipsFollowActionsMixin
from .tools.core.base import BaseMixin
from .tools.core.builtin import BuiltinMixin
from .tools.core.registry import AVAILABLE_TOOLS
from .tools.devices.devices import DevicesMixin
from .tools.devices.devices_ui import DevicesUIMixin
from .tools.m4l.m4l import M4LMixin
from .tools.midi.midi import MidiMixin
from .tools.mixing.mixing import MixingMixin
from .tools.mixing.mixing_master_devices import MixingMasterDevicesMixin
from .tools.properties.app_properties import AppPropertiesMixin
from .tools.scenes.scenes import ScenesMixin
from .tools.session.session_transport import SessionTransportMixin
from .tools.tracks.tracks import TracksMixin
from .tools.tracks.tracks_devices import TracksDevicesMixin


class LiveAPITools(
    BaseMixin,
    BuiltinMixin,
    SessionTransportMixin,
    TracksMixin,
    TracksDevicesMixin,
    ClipsMixin,
    ClipsColorMixin,
    ClipsFollowActionsMixin,
    MidiMixin,
    DevicesMixin,
    DevicesUIMixin,
    MixingMixin,
    MixingMasterDevicesMixin,
    ScenesMixin,
    ArrangementMixin,
    ArrangementLocatorsMixin,
    ArrangementViewMixin,
    TakeLanesMixin,
    AutomationMixin,
    M4LMixin,
    AppPropertiesMixin,
):
    """
    Comprehensive implementation of LiveAPI operations.

    Composed from domain-specific mixins:
    - SessionTransportMixin: play/stop/record/tempo/transport/automation/metronome
    - TracksMixin: create/delete/arm/solo/mute/routing/groups/freeze/annotations
    - TracksDevicesMixin: enriched track device parameters with display values
    - ClipsMixin: create/delete/launch/stop/looping/color/fades/follow actions
    - MidiMixin: add/remove/select notes, CC, program change
    - DevicesMixin: add/remove/parameters/racks/chains/plugin windows
    - MixingMixin: sends/master/return/crossfader/groove/quantization
    - ScenesMixin: create/delete/launch/color
    - ArrangementMixin: project/arrangement/view/loop/locator/browser/color
    - AutomationMixin: clip automation envelopes
    - M4LMixin: Max for Live device/audio/sample/simpler operations
    - TakeLanesMixin: take lane operations (feature-gated by Live capabilities)
    - AppPropertiesMixin: application/version and miscellaneous property queries
    """

    def get_available_tools(self):
        """Get list of all available tool names"""
        return AVAILABLE_TOOLS
