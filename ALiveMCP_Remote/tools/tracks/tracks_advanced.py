"""
Tracks advanced mixins aggregator.

This module composes small focused mixins to keep each file under 300 lines.
"""

from .tracks_annotations import TracksAnnotationsMixin
from .tracks_delay import TracksDelayMixin
from .tracks_freeze import TracksFreezeMixin
from .tracks_group import TracksGroupMixin


class TracksAdvancedMixin(
    TracksGroupMixin, TracksFreezeMixin, TracksAnnotationsMixin, TracksDelayMixin
):
    """Aggregator mixin combining grouping, freeze, annotations and delay."""

    pass
