# --- Build stage ---
FROM python:3.13-slim AS build

WORKDIR /app

# Install uv
RUN pip install uv

COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --frozen --no-dev

COPY . .
RUN uv sync --frozen --no-dev

# --- Runtime stage ---
FROM python:3.13-slim

WORKDIR /app

RUN pip install uv

COPY --from=build /app/.venv ./.venv
COPY --from=build /app .

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
