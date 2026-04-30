"""
Tutor plugin: landa_library_settings
======================================
Inject LANDA Library app và middleware vào Tutor generated settings cho Production.
Đảm bảo app được load mà không cần sửa edx-platform source code (tránh mất code khi update image).
"""

from tutor import hooks

LANDA_LIBRARY_LMS_SETTINGS = """
# LANDA Library app
if "lms.djangoapps.landa_library" not in INSTALLED_APPS:
    INSTALLED_APPS.append("lms.djangoapps.landa_library")
"""

LANDA_LIBRARY_CMS_SETTINGS = """
# LANDA Library app
if "lms.djangoapps.landa_library" not in INSTALLED_APPS:
    INSTALLED_APPS.append("lms.djangoapps.landa_library")

# LANDA Library CMS middleware
_landa_library_middleware = "lms.djangoapps.landa_library.middleware.LibraryButtonMiddleware"
if _landa_library_middleware not in MIDDLEWARE:
    MIDDLEWARE.append(_landa_library_middleware)
"""

hooks.Filters.ENV_PATCHES.add_items([
    ("openedx-lms-production-settings", LANDA_LIBRARY_LMS_SETTINGS),
    ("openedx-cms-production-settings", LANDA_LIBRARY_CMS_SETTINGS),
])
