#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLATFORM="${PLATFORM:-linux/amd64}"
PYTHON_BASE="${PYTHON_BASE:-python:3.10}"

# 国内网络可二选一：
# 1) Docker Desktop → Settings → Docker Engine 配置 registry-mirrors
# 2) export PYTHON_BASE=docker.m.daocloud.io/library/python:3.10

if ! docker info >/dev/null 2>&1; then
  echo "Docker 未运行，请先启动 Docker Desktop" >&2
  exit 1
fi

echo "==> 拉取 ${PYTHON_BASE}"
if ! docker pull --platform "${PLATFORM}" "${PYTHON_BASE}"; then
  echo "拉取 ${PYTHON_BASE} 失败。" >&2
  echo "请配置 Docker 镜像加速，或执行：" >&2
  echo "  export PYTHON_BASE=docker.m.daocloud.io/library/python:3.10" >&2
  echo "  ./build_backend.sh" >&2
  exit 1
fi

BUILD_ARGS=(--platform "${PLATFORM}" --build-arg "PYTHON_BASE=${PYTHON_BASE}" -t ruoyi-backend-pg:latest)
if [[ "${NO_CACHE:-}" == "1" ]]; then
  BUILD_ARGS=(--no-cache "${BUILD_ARGS[@]}")
fi

echo "==> 构建 ruoyi-backend-pg（uv 经 PyPI/清华源安装，无需 ghcr.io）"
docker build "${BUILD_ARGS[@]}" "${SCRIPT_DIR}/ruoyi-fastapi-backend"

echo "==> 完成: ruoyi-backend-pg:latest"
docker images ruoyi-backend-pg:latest
