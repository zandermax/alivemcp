"""
Application-level and miscellaneous track/clip/scene property queries.

This file composes smaller mixins to keep each module under the
300-line limit enforced by project pre-commit checks.
"""

from .app_info import AppInfoMixin
from .app_misc_properties import AppMiscPropertiesMixin


class AppPropertiesMixin(AppInfoMixin, AppMiscPropertiesMixin):
    """Aggregate application and miscellaneous property mixins."""

    pass
