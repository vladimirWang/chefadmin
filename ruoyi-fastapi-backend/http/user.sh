#!/usr/bin/env bash
# 调用 admin 后端登录 / 注册接口（需先启动后端，默认端口 9099）
set -euo pipefail

# 直连后端（与 .env.dev 中 APP_ROOT_PATH=/dev-api 一致）
BASE_URL="${BASE_URL:-http://127.0.0.1:9099/dev-api}"

check_server() {
  if ! curl -sf --connect-timeout 2 "${BASE_URL%/dev-api}/docs" >/dev/null 2>&1; then
    echo "无法连接后端 ${BASE_URL}（9099 未监听）。" >&2
    echo "请先启动: cd private_chef_admin && ./start-dev.sh --backend-only" >&2
    echo "或在 ruoyi-fastapi-backend 下: source .venv/bin/activate && ruoyi app run --env=dev" >&2
    exit 1
  fi
}

# 登录：POST /dev-api/login，Content-Type: application/x-www-form-urlencoded
login() {
  local user="${1:-admin}"
  local pass="${2:-admin123}"
  local code="${3:-}"
  local uuid="${4:-}"

  local data="username=${user}&password=${pass}"
  if [[ -n "${code}" && -n "${uuid}" ]]; then
    data="${data}&code=${code}&uuid=${uuid}"
  fi

  curl -sS -X POST "${BASE_URL}/login" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    --data "${data}" | jq .
}

# 注册：POST /dev-api/register，JSON（字段为 camelCase）
register() {
  curl -sS -X POST "${BASE_URL}/register" \
    -H "Content-Type: application/json" \
    -d "$(jq -n \
      --arg u "${1:-test}" \
      --arg p "${2:-admin123}" \
      --arg c "${3:-}" \
      --arg id "${4:-}" \
      '{username: $u, password: $p, confirmPassword: $p, code: $c, uuid: $id}')" | jq .
}

check_server

case "${1:-login}" in
  login)
    login "${2:-admin}" "${3:-admin123}" "${4:-}" "${5:-}"
    ;;
  register)
    register "${2:-testuser}" "${3:-admin123}" "${4:-}" "${5:-}"
    ;;
  *)
    echo "用法: $0 [login|register] [参数...]" >&2
    echo "  $0 login [username] [password] [code] [uuid]" >&2
    echo "  $0 register [username] [password] [code] [uuid]" >&2
    exit 1
    ;;
esac
