#!/usr/bin/env bash
set -euo pipefail

# Mac 本地：build_image → build_save → 上传 tar.gz → 远程 compose_only
#
# 用法：
#   ./build_backend.sh           # 构建 + 导出 + 部署（默认）
#   ./build_backend.sh build     # 仅构建并导出 tar.gz
#   ./build_backend.sh deploy    # 仅上传已有 tar.gz 并在服务器 load + 启动
#
# 环境变量：
#   REMOTE_USER_HOST  默认 root@139.224.68.145
#   REMOTE_DIR        默认 ~/chefadmin
#   NO_CACHE=1        传给 build_image.sh，无缓存构建
#   PARALLEL_REDIS=1  构建/部署时与远程启动 ruoyi-redis 并行（默认 0，暂时关闭）

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

PARALLEL_REDIS="${PARALLEL_REDIS:-0}"

REMOTE_USER_HOST="${REMOTE_USER_HOST:-root@139.224.68.145}"
REMOTE_DIR="${REMOTE_DIR:-~/chefadmin}"
TAR_FILE="${SCRIPT_DIR}/ruoyi-backend-pg.tar.gz"
REMOTE_DEPLOY_FILES=(
  docker-compose.yml
  start-prod-redis.sh
  compose_only.sh
)

sync_remote_deploy_files() {
  echo "==> 同步部署脚本 -> ${REMOTE_USER_HOST}:${REMOTE_DIR}/"
  ssh "${REMOTE_USER_HOST}" "mkdir -p ${REMOTE_DIR}"
  scp "${REMOTE_DEPLOY_FILES[@]}" "${REMOTE_USER_HOST}:${REMOTE_DIR}/"
}

run_start_redis_remote() {
  echo "==> 远程启动 ruoyi-redis"
  ssh "${REMOTE_USER_HOST}" "cd ${REMOTE_DIR} && bash start-prod-redis.sh"
}

run_start_redis_remote_async() {
  REDIS_REMOTE_LOG="$(mktemp "${TMPDIR:-/tmp}/ruoyi-redis-remote.XXXXXX")"
  run_start_redis_remote >"${REDIS_REMOTE_LOG}" 2>&1 &
  REDIS_REMOTE_PID=$!
}

wait_redis_remote_async() {
  if ! wait "${REDIS_REMOTE_PID}"; then
    echo "==> 远程启动 ruoyi-redis 失败" >&2
    cat "${REDIS_REMOTE_LOG}" >&2
    rm -f "${REDIS_REMOTE_LOG}"
    exit 1
  fi
  cat "${REDIS_REMOTE_LOG}"
  rm -f "${REDIS_REMOTE_LOG}"
}

run_build() {
  "${SCRIPT_DIR}/build_image.sh"
  "${SCRIPT_DIR}/build_save.sh"
}

run_build_with_optional_redis() {
  if [[ "${PARALLEL_REDIS}" == "1" ]]; then
    sync_remote_deploy_files
    echo "==> 并行: 本地构建镜像 || 远程启动 ruoyi-redis"
    run_start_redis_remote_async
    run_build
    wait_redis_remote_async
  else
    run_build
  fi
}

run_deploy() {
  if [[ ! -f "${TAR_FILE}" ]]; then
    echo "缺少 ${TAR_FILE}，请先执行 ./build_backend.sh build" >&2
    exit 1
  fi

  sync_remote_deploy_files

  if [[ "${PARALLEL_REDIS}" == "1" ]]; then
    echo "==> 并行: 上传镜像包 || 远程启动 ruoyi-redis"
    run_start_redis_remote_async
    echo "==> 上传 ${TAR_FILE} -> ${REMOTE_USER_HOST}:${REMOTE_DIR}/"
    scp "${TAR_FILE}" "${REMOTE_USER_HOST}:${REMOTE_DIR}/"
    wait_redis_remote_async
  else
    echo "==> 上传 ${TAR_FILE} -> ${REMOTE_USER_HOST}:${REMOTE_DIR}/"
    scp "${TAR_FILE}" "${REMOTE_USER_HOST}:${REMOTE_DIR}/"
  fi

  echo "==> 远程 load 并启动 ruoyi-backend-pg"
  ssh "${REMOTE_USER_HOST}" "cd ${REMOTE_DIR} && bash compose_only.sh"
}

ACTION="${1:-all}"

case "${ACTION}" in
  build)
    run_build
    echo "==> 本地构建完成: ${TAR_FILE}"
    ;;
  deploy)
    run_deploy
    echo "==> 远程部署完成: ${REMOTE_USER_HOST}:${REMOTE_DIR}"
    ;;
  all)
    run_build_with_optional_redis
    run_deploy
    echo "==> 构建并部署完成"
    ;;
  *)
    echo "用法: $0 [build|deploy|all]" >&2
    exit 1
    ;;
esac
