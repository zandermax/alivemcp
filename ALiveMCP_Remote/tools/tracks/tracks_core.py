"""
Tracks core mixins aggregator.

This module keeps the public `TracksCoreMixin` name but composes the implementation
from smaller, focused mixin classes to satisfy the 300-line file limit.
"""

from .tracks_info import TracksInfoMixin
from .tracks_management import TracksManagementMixin
from .tracks_properties import TracksPropertiesMixin


class TracksCoreMixin(TracksManagementMixin, TracksPropertiesMixin, TracksInfoMixin):
    """Aggregator mixin combining track management, properties and info."""

    pass
