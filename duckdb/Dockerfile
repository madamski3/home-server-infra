FROM python:3.12-slim

# Install uv via official binary (recommended Docker pattern from Astral)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

# Create .venv and install deps; --no-cache keeps image layer small
RUN uv sync --no-cache

COPY start.py ./

CMD [".venv/bin/python", "start.py"]
