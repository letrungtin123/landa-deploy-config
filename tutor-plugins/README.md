# LANDA Deploy Config

Repo này chứa cấu hình deploy cho LANDA Open edX/Tutor.

## Tutor Plugin

### tutor-plugins/landa_cors.py

Plugin cấu hình CORS/CSRF cho FE custom LANDA.

Allowed origins:

- http://192.168.0.226:5173
- http://192.168.0.226.nip.io:5173

## Cài trên server

```bash
mkdir -p "$(tutor plugins printroot)"
cp tutor-plugins/landa_cors.py "$(tutor plugins printroot)/landa_cors.py"

tutor plugins enable landa_cors
tutor config save

docker compose \
  -f ~/.local/share/tutor/env/local/docker-compose.yml \
  -f ~/.local/share/tutor/env/local/docker-compose.prod.yml \
  -f ~/landa-platform/tutor-prod-mount.yml \
  --project-name tutor_local \
  up -d lms cms lms-worker cms-worker

docker restart tutor_local-lms-1 tutor_local-cms-1 tutor_local-lms-worker-1 tutor_local-cms-worker-1