"""
Clip operations composite: core, properties, quantization, and extras.
"""

from .clips_core import ClipsCoreMixin
from .clips_extras import ClipsExtrasMixin
from .clips_properties import ClipsPropertiesMixin
from .clips_quantize import ClipsQuantizeMixin


class ClipsMixin(ClipsCoreMixin, ClipsPropertiesMixin, ClipsQuantizeMixin, ClipsExtrasMixin):
    pass
