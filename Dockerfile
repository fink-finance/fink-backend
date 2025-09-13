# Use slim Python image for smaller footprint
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install essential system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl \
 && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Environment variables for Python runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Copy dependency manifests (for caching)
COPY pyproject.toml poetry.lock ./

# Install dependencies using Poetry
RUN poetry install --only=main --no-root && rm -rf $POETRY_CACHE_DIR

# Copy project source code
COPY . .

# Expose application port
EXPOSE 8000

# Default startup command (production mode)
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
