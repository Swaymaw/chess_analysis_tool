FROM python:3.13-slim

WORKDIR /app

# Install uv
RUN pip install uv

COPY pyproject.toml uv.lock .python-version ./

# Build the env fully inside THIS image
RUN uv sync --frozen --no-dev

COPY . .

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
