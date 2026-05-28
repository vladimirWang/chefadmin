FROM python:3.10
WORKDIR /app

# 配置清华镜像源
ENV UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple

# 安装 uv（与本地一样用 lock 文件）
COPY --from=ghcr.io/astral-sh/uv:0.11.7 /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# 复制源代码
COPY . .

# 安装项目本身（包括 cli 模块）
RUN uv pip install -e .

# 暴露端口
EXPOSE 9099

# 启动命令
CMD ["uv", "run", "--no-sync", "ruoyi", "app", "run", "--env=dockerpg"]
