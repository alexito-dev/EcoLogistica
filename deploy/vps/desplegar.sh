#!/usr/bin/env bash
#
# Despliega EcoLogística al VPS (https://ecologistica.arno.services) con Docker + Traefik (Coolify).
#
#   bash deploy/vps/desplegar.sh          # sube, construye y reinicia
#   bash deploy/vps/desplegar.sh check    # solo revisa el estado, no cambia nada
#
# Solo toca /root/ecologistica y los contenedores ecologistica_*. No toca ningún otro servicio del servidor.
# Las claves se generan UNA vez en el servidor (/root/ecologistica/.env) y el despliegue nunca las pisa.

set -euo pipefail

SERVER="${DEPLOY_SERVER:-root@169.58.235.118}"
REMOTE_DIR="${DEPLOY_REMOTE_DIR:-/root/ecologistica}"
HOST="${DEPLOY_HOST:-ecologistica.arno.services}"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

say()  { printf '==> %s\n' "$*"; }
fail() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }
ssh_run() { ssh -o BatchMode=yes -o ConnectTimeout=15 ${DEPLOY_SSH_OPTS:-} "$SERVER" "$@"; }

check() {
  say "Estado en $SERVER"
  ssh_run "cd '$REMOTE_DIR' 2>/dev/null && docker compose ps --format 'table {{.Name}}\t{{.Status}}' || echo 'EcoLogística aun no esta desplegada'"
  say "Salud pública"
  curl -fsS --max-time 15 "https://$HOST/health" && echo || echo "(sin respuesta aún)"
}

[ "${1:-}" = "check" ] && { check; exit 0; }

for p in Dockerfile backend/src database/migrations frontend/package.json deploy/vps/docker-compose.yml deploy/arranque.sh; do
  [ -e "$p" ] || fail "Falta '$p'. Ejecuta el despliegue desde la raíz completa del repositorio."
done
ssh_run "true" || fail "No pude entrar a $SERVER. Revisa tu clave SSH."

say "Subiendo código..."
tar czf - --exclude='__pycache__' --exclude='*.pyc' --exclude='.venv' --exclude='node_modules' --exclude='dist' \
    --exclude='.pytest_cache' --exclude='.data' --exclude='test-results' --exclude='playwright-report' \
    --exclude='coverage*' --exclude='.coverage' \
    Dockerfile .dockerignore backend/requirements.txt backend/alembic.ini backend/src database frontend deploy \
  | ssh_run "mkdir -p '$REMOTE_DIR' && rm -rf '$REMOTE_DIR/.incoming' && mkdir -p '$REMOTE_DIR/.incoming' \
      && tar xzf - -C '$REMOTE_DIR/.incoming' \
      && rm -rf '$REMOTE_DIR/src' && mv '$REMOTE_DIR/.incoming' '$REMOTE_DIR/src' \
      && cp -f '$REMOTE_DIR/src/deploy/vps/docker-compose.yml' '$REMOTE_DIR/docker-compose.yml'"

say "Preparando claves (solo la primera vez)..."
ssh_run "cd '$REMOTE_DIR' && if [ ! -f .env ]; then
  umask 077
  {
    echo \"PUBLIC_HOST=$HOST\"
    echo \"PUBLIC_URL=https://$HOST\"
    echo \"POSTGRES_PASSWORD=\$(openssl rand -hex 24)\"
    echo \"JWT_SECRET=\$(openssl rand -hex 32)\"
    echo \"TOTP_CLAVE_CIFRADO=\$(head -c 32 /dev/urandom | base64 | tr '+/' '-_')\"
    echo \"DEMO_CLAVE=Eco-\$(openssl rand -hex 6)-Demo1\"
  } > .env
  echo '  .env creado (claves nuevas, solo en el servidor)'
else
  echo '  .env ya existe: no se toca'
fi"

say "Construyendo imagen (compila la interfaz; puede tardar unos minutos)..."
ssh_run "cd '$REMOTE_DIR/src' && docker build -q -t ecologistica:latest ."

say "Arrancando..."
ssh_run "cd '$REMOTE_DIR' && docker compose up -d --remove-orphans"

say "Esperando a que esté sana..."
for i in $(seq 1 40); do
  estado="$(ssh_run "docker inspect -f '{{.State.Health.Status}}' ecologistica_app 2>/dev/null" || true)"
  [ "$estado" = "healthy" ] && break
  sleep 3
done
echo "  estado: ${estado:-desconocido}"
[ "${estado:-}" = "healthy" ] || { ssh_run "docker logs --tail 40 ecologistica_app 2>&1"; fail "La aplicación no quedó sana."; }

say "Verificando desde internet (el primer certificado HTTPS puede tardar un minuto)..."
ok=0
for i in $(seq 1 24); do
  if curl -fsS --max-time 10 "https://$HOST/health" | grep -q '"status":"ok"'; then ok=1; break; fi
  sleep 5
done
[ "$ok" = 1 ] || fail "https://$HOST no respondió. Revisa con: bash deploy/vps/desplegar.sh check"
echo "  OK  https://$HOST/health"
say "Listo."
