"""
Tutor plugin: landa_cors
========================
Cấu hình CORS/CSRF cho FE custom LANDA trên Open edX production.

Config-driven: đọc danh sách origins từ Tutor config key
  LANDA_FE_CORS_ORIGINS

Đổi domain FE bằng lệnh:
  tutor config save --set 'LANDA_FE_CORS_ORIGINS=["https://fe.example.com"]'

Không sửa source code edx-platform.
Không overwrite settings cũ — chỉ append origin nếu chưa tồn tại.

Cách dùng:
  1. Copy file này vào: ~/.local/share/tutor-plugins/landa_cors.py
  2. tutor plugins enable landa_cors
  3. tutor config save
  4. Restart containers qua docker compose custom mount
"""

from tutor import hooks

# ── Đăng ký config key với giá trị mặc định ──
# User có thể override bằng:
#   tutor config save --set 'LANDA_FE_CORS_ORIGINS=["https://fe.example.com"]'
hooks.Filters.CONFIG_DEFAULTS.add_items([
    (
        "LANDA_FE_CORS_ORIGINS",
        [
            "http://192.168.0.226:5173",
            "http://192.168.0.226.nip.io:5173",
        ],
    )
])

# ── Settings code inject vào production.py ──
# Tutor render Jinja2 template → {{ LANDA_FE_CORS_ORIGINS }} thành list Python.
LANDA_CORS_SETTINGS = """
# ── LANDA CORS/CSRF (injected by landa_cors plugin) ──
LANDA_FE_ORIGINS = {{ LANDA_FE_CORS_ORIGINS }}

try:
    CORS_ORIGIN_WHITELIST
except NameError:
    CORS_ORIGIN_WHITELIST = []

try:
    CSRF_TRUSTED_ORIGINS
except NameError:
    CSRF_TRUSTED_ORIGINS = []

for _origin in LANDA_FE_ORIGINS:
    if _origin not in CORS_ORIGIN_WHITELIST:
        CORS_ORIGIN_WHITELIST.append(_origin)

    if _origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(_origin)

CORS_ALLOW_CREDENTIALS = True
"""

# ── Inject vào LMS + CMS production settings ──
hooks.Filters.ENV_PATCHES.add_items([
    ("openedx-lms-production-settings", LANDA_CORS_SETTINGS),
    ("openedx-cms-production-settings", LANDA_CORS_SETTINGS),
])
