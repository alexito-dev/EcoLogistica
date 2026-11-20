#!/bin/sh
# Arranque del servicio de producción: aplica las migraciones (si hay base de datos) y levanta la API.
set -e
if [ -n "$DATABASE_URL" ]; then
  alembic -c alembic.ini upgrade head
fi
exec python -m uvicorn app.main:app --app-dir src --host 0.0.0.0 --port "${PORT:-8000}" \
  --proxy-headers --forwarded-allow-ips='*'
