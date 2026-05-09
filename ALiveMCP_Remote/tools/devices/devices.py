"""
Device operations composite: composes all device-domain mixins.

Imports: core, extras (plugin windows), display values, racks/chains, rack contents.
"""

from .devices_core import DevicesCoreMixin
from .devices_display import DevicesDisplayMixin
from .devices_extras import DevicesExtrasMixin
from .devices_rack_contents import DevicesRackContentsMixin
from .devices_racks import DevicesRacksMixin


class DevicesMixin(
    DevicesCoreMixin,
    DevicesDisplayMixin,
    DevicesExtrasMixin,
    DevicesRacksMixin,
    DevicesRackContentsMixin,
):
    pass
