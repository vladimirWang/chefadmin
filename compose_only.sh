#!/bin/bash
set -euo pipefail

gunzip -c ruoyi-backend-pg.tar.gz | docker load
docker images | grep ruoyi-backend-pg

docker network inspect private_chef_network >/dev/null 2>&1 \
  || docker network create private_chef_network

# 旧 backend 容器可能仍引用已删除的网络 ID，直接 up 会报 network ... not found
docker rm -f ruoyi-backend-pg 2>/dev/null || true

docker compose -f docker-compose.yml -p chef-ruoyi-prod up -d ruoyi-backend-pg
docker logs ruoyi-backend-pg --tail 30
