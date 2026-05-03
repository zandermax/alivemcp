"""
Device operations, parameters, racks/chains, plugin windows, and utilities.
"""

from .devices_core import DevicesCoreMixin
from .devices_extras import DevicesExtrasMixin
from .devices_rack_contents import DevicesRackContentsMixin
from .devices_racks import DevicesRacksMixin


class DevicesMixin(
    DevicesCoreMixin, DevicesExtrasMixin, DevicesRacksMixin, DevicesRackContentsMixin
):
    pass
