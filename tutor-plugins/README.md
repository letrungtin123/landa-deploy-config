# LANDA Deploy Config

Repo này chứa cấu hình deploy cho LANDA Open edX/Tutor.
Không commit vào edx-platform-current.

## Tutor Plugins

### tutor-plugins/landa_cors.py

Plugin cấu hình CORS/CSRF cho FE custom LANDA.
Config-driven — đọc origins từ Tutor config key, không hardcode trong code.

**Config key:** `LANDA_FE_CORS_ORIGINS`

**Default origins (fallback):**
- `http://192.168.0.226:5173`
- `http://192.168.0.226.nip.io:5173`

---

## Cài trên server

```bash
# 1. Copy plugin
mkdir -p "$(tutor plugins printroot)"
cp tutor-plugins/landa_cors.py "$(tutor plugins printroot)/landa_cors.py"

# 2. Enable + save
tutor plugins enable landa_cors
tutor config save

# 3. Restart containers
docker compose \
  -f ~/.local/share/tutor/env/local/docker-compose.yml \
  -f ~/.local/share/tutor/env/local/docker-compose.prod.yml \
  -f ~/landa-platform/tutor-prod-mount.yml \
  --project-name tutor_local \
  up -d lms cms lms-worker cms-worker

docker restart tutor_local-lms-1 tutor_local-cms-1 tutor_local-lms-worker-1 tutor_local-cms-worker-1
```

---

## Đổi domain FE

Khi deploy lên domain thật (VD: `https://learn.leassociates.vn`):

```bash
tutor config save --set 'LANDA_FE_CORS_ORIGINS=["https://learn.leassociates.vn"]'
```

Nhiều origins:

```bash
tutor config save --set 'LANDA_FE_CORS_ORIGINS=["https://learn.leassociates.vn", "http://192.168.0.226:5173"]'
```

Sau đó restart containers như bước 3 ở trên.

---

## Verify

```bash
# Kiểm tra config đã set
tutor config printvalue LANDA_FE_CORS_ORIGINS

# Kiểm tra settings đã inject vào production.py
grep -n "LANDA_FE_ORIGINS" "$(tutor config printroot)/env/apps/openedx/settings/lms/production.py"

# Test CORS preflight
curl -v -X OPTIONS \
  -H "Origin: http://192.168.0.226:5173" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Authorization, Content-Type, X-CSRFToken" \
  http://192.168.0.226.nip.io/oauth2/access_token
```