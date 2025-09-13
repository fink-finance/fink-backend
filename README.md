# Fink Backend

A modern FastAPI backend application with PostgreSQL, Redis, and Docker support.

## 🚀 Features

-   **FastAPI** - Modern, fast web framework for building APIs
-   **PostgreSQL** - Robust relational database with async support
-   **Redis** - In-memory data store for caching and sessions
-   **Docker** - Containerized development and deployment
-   **Alembic** - Database migrations
-   **Poetry** - Dependency management
-   **Pre-commit hooks** - Code quality and formatting
-   **Testing** - Pytest with async support

## 📋 Prerequisites

-   Python 3.11+
-   Poetry
-   Docker & Docker Compose

## 🛠️ Setup

### 1. Clone and Install Dependencies

```bash
git clone <repository-url>
cd fink-backend
poetry install
```

### 2. Environment Configuration

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Start Services with Docker

```bash
# Start PostgreSQL and Redis
make up

# Or manually:
docker-compose up -d postgres redis
```

### 4. Database Setup

```bash
# Run migrations
make mig-up

# Or manually:
poetry run alembic upgrade head
```

### 5. Run the Application

```bash
# Development mode
poetry run uvicorn app.main:app --reload

# Or with Docker
docker-compose up api
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

-   **Swagger UI**: http://localhost:8000/docs
-   **ReDoc**: http://localhost:8000/redoc

## 🧪 Testing

```bash
# Run all tests
make test

# Run with coverage
make cov

# Run specific test file
poetry run pytest tests/test_health.py
```

## 🔧 Development

### Code Quality

```bash
# Format code
make fmt

# Check formatting
make fmt-check

# Lint code
make lint

# Type checking
make type
```

### Database Migrations

```bash
# Create new migration
make mig-new m="description"

# Auto-generate migration from models
make mig-autogen m="description"

# Apply migrations
make mig-up
```

### Docker Commands

```bash
# Start all services
make up

# Stop services
make down

# View logs
make logs
```

## 📁 Project Structure

```
fink-backend/
├── app/                    # Application code
│   ├── api/               # API routes and dependencies
│   ├── core/              # Core settings and configuration
│   ├── db/                # Database models and session
│   ├── domain/            # Domain logic
│   ├── repositories/      # Data access layer
│   ├── schemas/           # Pydantic models
│   ├── services/          # Business logic
│   └── workers/           # Background tasks
├── migrations/            # Database migrations
├── tests/                 # Test files
├── docs/                  # Documentation
└── scripts/               # Utility scripts
```

## 🌍 Environment Variables

See `.env.example` for all available environment variables.

Key variables:

-   `DATABASE_URL` - PostgreSQL connection string
-   `REDIS_URL` - Redis connection string
-   `SECRET_KEY` - JWT secret key
-   `DEBUG` - Enable debug mode

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📞 Support

For support, please open an issue in the repository.
