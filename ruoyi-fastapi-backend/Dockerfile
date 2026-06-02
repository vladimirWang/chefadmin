# 国内构建可传: --build-arg PYTHON_BASE=docker.m.daocloud.io/library/python:3.10
ARG PYTHON_BASE=python:3.10
FROM ${PYTHON_BASE}
WORKDIR /app

# 配置清华镜像源
ENV UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple

# 用 PyPI 安装 uv，避免构建时访问 ghcr.io（国内易超时）
RUN pip install --no-cache-dir uv==0.11.7 \
  -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# 复制源代码
COPY . .

# 安装项目本身（包括 cli 模块）
RUN uv pip install -e .

# 暴露端口
EXPOSE 9099

# 启动命令
CMD ["uv", "run", "--no-sync", "ruoyi", "app", "run", "--env=prod"]
