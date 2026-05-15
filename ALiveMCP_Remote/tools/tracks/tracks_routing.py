"""
Tracks routing mixins aggregator.

This module composes focused mixins for fold state, monitoring and routing.
"""

from .tracks_fold import TracksFoldMixin
from .tracks_monitoring import TracksMonitoringMixin
from .tracks_routing_core import TracksRoutingCoreMixin


class TracksRoutingMixin(TracksFoldMixin, TracksMonitoringMixin, TracksRoutingCoreMixin):
    """Aggregator mixin combining fold, monitoring and routing helpers."""

    pass
