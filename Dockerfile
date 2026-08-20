FROM python:3.14-slim

WORKDIR /app

ENV UV_PROJECT_ENVIRONMENT="/usr/local"
ENV UV_BREAK_SYSTEM_PACKAGES=true
ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

COPY . /app

RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

CMD ["python", "-m", "fastapi", "run", "src/research_agent_backend/__init__.py", "--port", "80"]
