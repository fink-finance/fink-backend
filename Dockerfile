# Use slim Python image for smaller footprint
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install essential system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl \
 && rm -rf /var/lib/apt/lists/*

# Environment variables for Python runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy dependency manifests (for caching)
COPY pyproject.toml poetry.lock ./

# Install dependencies using pip
RUN pip install --no-cache-dir \
    fastapi==0.116.1 \
    uvicorn[standard]==0.35.0 \
    pydantic-settings==2.10.1 \
    sqlalchemy==2.0.43 \
    asyncpg==0.30.0 \
    alembic==1.16.5 \
    redis==6.4.0 \
    httpx==0.28.1

# Copy project source code
COPY . .

# Expose application port
EXPOSE 8000

# Default startup command (production mode)
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
