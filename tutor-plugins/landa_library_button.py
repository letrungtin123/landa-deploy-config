"""
Tutor plugin: landa_library_button
====================================
Inject nút "📚 Thư viện tài liệu" vào CMS Studio bằng cách
thêm 1 URL catch-all middleware-like view.

Cách hoạt động:
- Inject 1 Django middleware function vào CMS settings
- Middleware chèn floating button HTML trước </body>
- Chỉ hiện cho staff user
- Click → mở /library-admin/

Cài:
  cp landa_library_button.py "$(tutor plugins printroot)/"
  tutor plugins enable landa_library_button
  tutor config save
  docker restart tutor_local-cms-1
"""

from tutor import hooks

# Dùng cùng pattern như la_custom_settings.py — inject settings
hooks.Filters.ENV_PATCHES.add_items([
    (
        "openedx-cms-common-settings",
        """
# ── LANDA Library Button ──
# Thêm middleware class vào MIDDLEWARE list.
# Class được define inline trong settings file (giống cách Django cho phép).

class LandaLibraryButtonMiddleware:
    BUTTON = (
        b'<a id="landa-lib-btn" href="/library-admin/" '
        b'style="position:fixed;bottom:24px;left:24px;z-index:99999;'
        b'display:flex;align-items:center;gap:8px;'
        b'padding:12px 24px;'
        b'background:linear-gradient(135deg,#0075b4,#005a8c);'
        b'color:#fff;font-family:-apple-system,BlinkMacSystemFont,sans-serif;'
        b'font-size:14px;font-weight:600;'
        b'border-radius:12px;box-shadow:0 4px 16px rgba(0,117,180,.4);'
        b'cursor:pointer;text-decoration:none;transition:all .3s ease"'
        b'>&#128218; Thu vien tai lieu</a>'
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        ct = response.get('Content-Type', '')
        if 'text/html' not in ct:
            return response
        if request.path.startswith('/library-admin'):
            return response
        if not getattr(request, 'user', None) or not request.user.is_staff:
            return response
        if hasattr(response, 'content') and b'</body>' in response.content:
            response.content = response.content.replace(
                b'</body>', self.BUTTON + b'</body>'
            )
            if 'Content-Length' in response:
                response['Content-Length'] = len(response.content)
        return response

# Đăng ký middleware — vì class nằm trong settings module,
# import path là: <settings_module>.LandaLibraryButtonMiddleware
# Tutor production settings = lms.envs.tutor.production (cho CMS = cms.envs.tutor.production)
# Nhưng class define inline trong exec'd code nên dùng cách khác:
# Gán vào module globals để Django tìm được.
import sys
_settings_mod = sys.modules[__name__]
setattr(_settings_mod, 'LandaLibraryButtonMiddleware', LandaLibraryButtonMiddleware)
MIDDLEWARE.append(f'{__name__}.LandaLibraryButtonMiddleware')
"""
    ),
])
