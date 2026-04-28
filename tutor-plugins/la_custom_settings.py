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
# LANDA custom settings: enable APIs for custom FE
FEATURES["ENABLE_XBLOCK_VIEW_ENDPOINT"] = True
FEATURES["ENABLE_HTML_XBLOCK_STUDENT_VIEW_DATA"] = True
"""
    )
])