#!/bin/bash
set -euo pipefail

gunzip -c ruoyi-backend-pg.tar.gz | docker load
docker images | grep ruoyi-backend-pg

docker network inspect private_chef_network >/dev/null 2>&1 \
  || docker network create private_chef_network

docker compose -f docker-compose.yml -p chef-ruoyi-prod up -d ruoyi-backend-pg
docker logs ruoyi-backend-pg --tail 30
