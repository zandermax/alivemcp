"""
Max for Live composite tools.

Composes Max device discovery/control and audio/sample/simpler operations.
"""

from .m4l_audio import M4LAudioMixin
from .m4l_devices import M4LDevicesMixin


class M4LMixin(M4LDevicesMixin, M4LAudioMixin):
    pass
