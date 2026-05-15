"""
Mixing operations: composed from focused mixin modules.

This file aggregates smaller mixin modules to keep each file under
the project's 300-line limit.
"""

from .mixing_crossfader import MixingCrossfaderMixin
from .mixing_groove import MixingGrooveMixin
from .mixing_master import MixingMasterMixin
from .mixing_return import MixingReturnMixin
from .mixing_sends import MixingSendsMixin


class MixingMixin(
    MixingGrooveMixin,
    MixingSendsMixin,
    MixingMasterMixin,
    MixingReturnMixin,
    MixingCrossfaderMixin,
):
    """Aggregate mixing-related mixins."""

    pass
