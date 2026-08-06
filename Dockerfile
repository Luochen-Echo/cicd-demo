FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY src ./src
RUN uv sync --frozen --no-dev

CMD ["uv", "run", "python", "-c", "from math_utils import multiply; print(f'math-utils 镜像启动，6 * 7 = {multiply(6, 7)}')"]
