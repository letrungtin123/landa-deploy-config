"""
Tutor plugin: landa_cors
========================
Cấu hình CORS/CSRF cho FE custom LANDA trên Open edX production.

Cho phép FE tại các origin sau gọi API cross-origin tới LMS/CMS:
  - http://192.168.0.226:5173
  - http://192.168.0.226.nip.io:5173

Không sửa source code edx-platform.
Không overwrite settings cũ — chỉ append origin nếu chưa tồn tại.

Cách dùng:
  1. Copy file này vào: ~/.local/share/tutor-plugins/landa_cors.py
  2. tutor plugins enable landa_cors
  3. tutor config save
  4. Restart containers qua docker compose custom mount
"""

from tutor import hooks

LANDA_CORS_SETTINGS = """
LANDA_FE_ORIGINS = [
    "http://192.168.0.226:5173",
    "http://192.168.0.226.nip.io:5173",
]

try:
    CORS_ORIGIN_WHITELIST
except NameError:
    CORS_ORIGIN_WHITELIST = []

try:
    CSRF_TRUSTED_ORIGINS
except NameError:
    CSRF_TRUSTED_ORIGINS = []

for origin in LANDA_FE_ORIGINS:
    if origin not in CORS_ORIGIN_WHITELIST:
        CORS_ORIGIN_WHITELIST.append(origin)

    if origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(origin)

CORS_ALLOW_CREDENTIALS = True
"""

hooks.Filters.ENV_PATCHES.add_items([
    ("openedx-lms-production-settings", LANDA_CORS_SETTINGS),
    ("openedx-cms-production-settings", LANDA_CORS_SETTINGS),
])
