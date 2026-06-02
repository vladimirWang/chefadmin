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
#   REMOTE_DIR        默认 ~/private_chef_admin
#   NO_CACHE=1        传给 build_image.sh，无缓存构建

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

REMOTE_USER_HOST="${REMOTE_USER_HOST:-root@139.224.68.145}"
REMOTE_DIR="${REMOTE_DIR:-~/chefadmin}"
TAR_FILE="${SCRIPT_DIR}/ruoyi-backend-pg.tar.gz"

run_build() {
  "${SCRIPT_DIR}/build_image.sh"
  "${SCRIPT_DIR}/build_save.sh"
}

run_deploy() {
  if [[ ! -f "${TAR_FILE}" ]]; then
    echo "缺少 ${TAR_FILE}，请先执行 ./build_backend.sh build" >&2
    exit 1
  fi

  echo "==> 上传 ${TAR_FILE} -> ${REMOTE_USER_HOST}:${REMOTE_DIR}/"
  ssh "${REMOTE_USER_HOST}" "mkdir -p ${REMOTE_DIR}"
  scp "${TAR_FILE}" "${REMOTE_USER_HOST}:${REMOTE_DIR}/"

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
    run_build
    run_deploy
    echo "==> 构建并部署完成"
    ;;
  *)
    echo "用法: $0 [build|deploy|all]" >&2
    exit 1
    ;;
esac
