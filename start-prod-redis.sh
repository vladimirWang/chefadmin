#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

RUOYI_COMPOSE_FILE="${RUOYI_COMPOSE_FILE:-docker-compose.yml}"

if [[ ! -f "${RUOYI_COMPOSE_FILE}" ]]; then
  echo "缺少 compose 文件: ${RUOYI_COMPOSE_FILE}" >&2
  exit 1
fi

docker network inspect private_chef_network >/dev/null 2>&1 \
  || docker network create private_chef_network

echo "启动 ruoyi-redis（项目: chef-ruoyi-prod）..."
docker compose -f "${RUOYI_COMPOSE_FILE}" -p chef-ruoyi-prod up -d ruoyi-redis

echo "等待 Redis 就绪..."
for _ in $(seq 1 30); do
  if docker exec ruoyi-redis redis-cli ping 2>/dev/null | grep -q PONG; then
    echo "ruoyi-redis 已就绪 (PONG)"
    exit 0
  fi
  sleep 1
done

echo "ruoyi-redis 启动超时，请检查日志: docker logs ruoyi-redis" >&2
exit 1
