#!/usr/bin/env bash
# 本地开发：同时启动 admin 后端与前端（与 README 默认方式一致）
# 后端: ruoyi app run --env=dev  →  app.py + uvicorn
# 前端: npm run dev              →  Vite (http://localhost:80)
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="${ROOT_DIR}/ruoyi-fastapi-backend"
FRONTEND_DIR="${ROOT_DIR}/ruoyi-fastapi-frontend"

BACKEND_PID=""

cleanup() {
  if [[ -n "${BACKEND_PID}" ]] && kill -0 "${BACKEND_PID}" 2>/dev/null; then
    echo ""
    echo "正在停止后端 (pid=${BACKEND_PID})..."
    kill "${BACKEND_PID}" 2>/dev/null || true
    wait "${BACKEND_PID}" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

activate_backend_venv() {
  if [[ -f "${BACKEND_DIR}/.venv/bin/activate" ]]; then
    # shellcheck disable=SC1091
    source "${BACKEND_DIR}/.venv/bin/activate"
  fi
}

if [[ ! -d "${BACKEND_DIR}" || ! -d "${FRONTEND_DIR}" ]]; then
  echo "请在 private_chef_admin 根目录运行本脚本。" >&2
  exit 1
fi

if [[ ! -f "${BACKEND_DIR}/.env.dev" ]]; then
  echo "缺少 ${BACKEND_DIR}/.env.dev，请先配置数据库与 Redis。" >&2
  exit 1
fi

if [[ ! -d "${FRONTEND_DIR}/node_modules" ]]; then
  echo "未找到前端依赖，请先执行:" >&2
  echo "  cd ruoyi-fastapi-frontend && npm install" >&2
  exit 1
fi

activate_backend_venv
if ! command -v ruoyi >/dev/null 2>&1; then
  echo "未找到 ruoyi 命令。请在后端目录安装依赖:" >&2
  echo "  cd ruoyi-fastapi-backend && pip3 install -r requirements.txt" >&2
  exit 1
fi

run_backend() {
  cd "${BACKEND_DIR}"
  activate_backend_venv
  exec ruoyi app run --env=dev
}

run_frontend() {
  cd "${FRONTEND_DIR}"
  if [[ -f yarn.lock ]] && command -v yarn >/dev/null 2>&1; then
    yarn dev
  else
    npm run dev
  fi
}

echo "后端: ruoyi app run --env=dev  →  http://127.0.0.1:9099"
echo "前端: npm run dev              →  http://localhost:80"
echo "默认账号: admin / admin123"
echo "按 Ctrl+C 停止前后端"
echo ""

run_backend &
BACKEND_PID=$!

sleep 1
run_frontend
