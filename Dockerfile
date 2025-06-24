# Based on https://docs.astral.sh/uv/guides/integration/fastapi/#deployment

FROM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock /app

# Install the application dependencies.
RUN uv sync --frozen --no-cache

# Copy the application into the container.
COPY src/ /app/src

# Run the application.
CMD ["/app/.venv/bin/fastapi", "run", "src/api_example.py", "--port", "80", "--host", "0.0.0.0"]
