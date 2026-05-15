"""
M4L audio mixins aggregator.

This module composes smaller mixins to stay within the file length limit.
"""

from .m4l_clip_warp import M4LClipWarpMixin
from .m4l_file import M4LFileMixin
from .m4l_sample import M4LSampleMixin


class M4LAudioMixin(M4LClipWarpMixin, M4LFileMixin, M4LSampleMixin):
    """Aggregator combining clip warp, file and sample mixins."""

    pass
