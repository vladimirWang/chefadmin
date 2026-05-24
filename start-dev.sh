#!/usr/bin/env bash
# 本地开发：启动 admin 后端（uv .venv + ruoyi）与前端
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="${ROOT_DIR}/ruoyi-fastapi-backend"
FRONTEND_DIR="${ROOT_DIR}/ruoyi-fastapi-frontend"
VENV_DIR="${BACKEND_DIR}/.venv"
RUOYI_BIN="${VENV_DIR}/bin/ruoyi"

BACKEND_PID=""
START_FRONTEND=1

usage() {
  echo "用法: $0 [--backend-only]" >&2
  echo "  默认同时启动后端与前端；--backend-only 仅启动后端 API。" >&2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --backend-only|-b)
      START_FRONTEND=0
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "未知参数: $1" >&2
      usage
      exit 1
      ;;
  esac
done

cleanup() {
  if [[ -n "${BACKEND_PID}" ]] && kill -0 "${BACKEND_PID}" 2>/dev/null; then
    echo ""
    echo "正在停止后端 (pid=${BACKEND_PID})..."
    kill "${BACKEND_PID}" 2>/dev/null || true
    wait "${BACKEND_PID}" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

if [[ ! -d "${BACKEND_DIR}" ]]; then
  echo "缺少后端目录: ${BACKEND_DIR}" >&2
  exit 1
fi

if [[ ! -f "${BACKEND_DIR}/.env.dev" ]]; then
  echo "缺少 ${BACKEND_DIR}/.env.dev，请先配置数据库与 Redis。" >&2
  exit 1
fi

if [[ ! -x "${RUOYI_BIN}" ]]; then
  echo "未找到 ${RUOYI_BIN}" >&2
  echo "请先用 uv 安装后端依赖:" >&2
  echo "  cd ruoyi-fastapi-backend" >&2
  echo "  uv venv && source .venv/bin/activate" >&2
  echo "  UV_DEFAULT_INDEX=https://pypi.org/simple uv pip install -r requirements.txt" >&2
  exit 1
fi

if [[ "${START_FRONTEND}" -eq 1 && ! -d "${FRONTEND_DIR}/node_modules" ]]; then
  echo "未找到前端依赖，请先执行其一:" >&2
  echo "  cd ruoyi-fastapi-frontend && pnpm install" >&2
  echo "  cd ruoyi-fastapi-frontend && npm install" >&2
  exit 1
fi

run_backend() {
  cd "${BACKEND_DIR}"
  exec "${RUOYI_BIN}" app run --env=dev
}

run_frontend() {
  cd "${FRONTEND_DIR}"
  if [[ -f pnpm-lock.yaml ]] && command -v pnpm >/dev/null 2>&1; then
    pnpm run dev
  elif [[ -f yarn.lock ]] && command -v yarn >/dev/null 2>&1; then
    yarn dev
  else
    npm run dev
  fi
}

echo "后端: ${RUOYI_BIN} app run --env=dev  →  http://127.0.0.1:9099"
if [[ "${START_FRONTEND}" -eq 1 ]]; then
  echo "前端: pnpm/npm run dev            →  http://localhost:80"
fi
echo "默认账号: admin / admin123"
echo "按 Ctrl+C 停止"
echo ""

run_backend &
BACKEND_PID=$!

if [[ "${START_FRONTEND}" -eq 1 ]]; then
  sleep 1
  run_frontend
else
  wait "${BACKEND_PID}"
fi
