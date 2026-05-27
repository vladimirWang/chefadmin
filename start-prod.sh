#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# 默认 PostgreSQL 栈；MySQL 可设 COMPOSE_FILE=docker-compose.my.yml
COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.pg.yml}"
DIST_DIR="${SCRIPT_DIR}/nginx/html/dist"
SSL_DIR="${SCRIPT_DIR}/nginx/ssl"
SSL_CERT="${SSL_DIR}/admin.hetou.vip.pem"
SSL_KEY="${SSL_DIR}/admin.hetou.vip.key"

if [[ ! -f "${COMPOSE_FILE}" ]]; then
  echo "缺少 compose 文件: ${COMPOSE_FILE}" >&2
  echo "可选: docker-compose.pg.yml / docker-compose.my.yml" >&2
  exit 1
fi

if [[ ! -f "${DIST_DIR}/index.html" ]]; then
  echo "缺少 ${DIST_DIR}/index.html" >&2
  echo "请先在 Mac 本地构建前端并上传到 nginx/html/dist/，例如：" >&2
  echo "  cd ruoyi-fastapi-frontend && ./build-deploy.sh" >&2
  exit 1
fi

echo "compose: ${COMPOSE_FILE}"
echo "nginx 静态目录: ${DIST_DIR} → /usr/share/nginx/html"
docker compose -f "${COMPOSE_FILE}" -p chef-ruoyi-prod up -d --build
