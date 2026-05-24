#!/bin/bash

docker compose -f docker-compose.yml -p chef-ruoyi-prod --env-file ../.env.prod up -d --build