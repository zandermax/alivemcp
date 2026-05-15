"""
Clips properties aggregator.

This module keeps the `ClipsPropertiesMixin` name but composes the
implementation from smaller mixins so each file stays under 300 lines.
"""

from .clips_looping import ClipsLoopingMixin
from .clips_markers import ClipsMarkersMixin
from .clips_misc import ClipsMiscMixin


class ClipsPropertiesMixin(ClipsLoopingMixin, ClipsMarkersMixin, ClipsMiscMixin):
    """Aggregator combining looping, marker and misc clip property mixins."""

    pass
