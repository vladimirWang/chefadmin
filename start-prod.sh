#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# 勿用 COMPOSE_FILE：与 Docker Compose 内置环境变量同名，服务器若已 export 会覆盖默认值
RUOYI_COMPOSE_FILE="${RUOYI_COMPOSE_FILE:-docker-compose.pg.yml}"
DIST_DIR="${SCRIPT_DIR}/nginx/html/dist"
SSL_DIR="${SCRIPT_DIR}/nginx/ssl/cert"
SSL_CERT="${SSL_DIR}/chefadmin.hetou.vip.pem"
SSL_KEY="${SSL_DIR}/chefadmin.hetou.vip.key"

if [[ ! -f "${RUOYI_COMPOSE_FILE}" ]]; then
  echo "缺少 compose 文件: ${RUOYI_COMPOSE_FILE}" >&2
  echo "可选: docker-compose.pg.yml / docker-compose.my.yml" >&2
  exit 1
fi

if [[ ! -f "${DIST_DIR}/index.html" ]]; then
  echo "缺少 ${DIST_DIR}/index.html" >&2
  echo "请先在 Mac 本地构建前端并上传到 nginx/html/dist/，例如：" >&2
  echo "  cd ruoyi-fastapi-frontend && ./build-deploy.sh" >&2
  exit 1
fi

if [[ ! -f "${SSL_CERT}" ]] || [[ ! -f "${SSL_KEY}" ]]; then
  echo "缺少 SSL 证书，请放置到 nginx/ssl/：" >&2
  echo "  ${SSL_CERT}" >&2
  echo "  ${SSL_KEY}" >&2
  echo "说明见 nginx/ssl/README.md" >&2
  exit 1
fi

echo "compose: ${RUOYI_COMPOSE_FILE}"
echo "nginx 静态目录: ${DIST_DIR} → /usr/share/nginx/html"
echo "SSL 证书: ${SSL_DIR} → /etc/ssl/cert"
echo "访问: https://admin.hetou.vip:6444  (HTTP: :6443)"
docker compose -f "${RUOYI_COMPOSE_FILE}" -p chef-ruoyi-prod up -d --build
