"""
Tutor plugin: la_custom_settings
Bật custom Open edX settings cho LANDA production.
Không sửa source code edx-platform.
"""

from tutor import hooks

hooks.Filters.ENV_PATCHES.add_items([
    (
        "openedx-lms-common-settings",
        """
# LANDA custom setting: enable xblock_view API endpoint
FEATURES["ENABLE_XBLOCK_VIEW_ENDPOINT"] = True
"""
    )
])