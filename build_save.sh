#!/bin/bash
set -euo pipefail

docker save ruoyi-backend-pg:latest | gzip > ruoyi-backend-pg.tar.gz
