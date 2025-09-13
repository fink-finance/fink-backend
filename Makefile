SHELL := /bin/bash

# Tools / services
DC           := docker compose
API_SERVICE  := api
DB_SERVICE   := postgres

.PHONY: up down build rebuild restart ps logs sh dbsh fmt fmt-check lint type test cov \
        mig-new mig-autogen mig-up db-tables db-url

## --- Compose lifecycle ---
up:
	$(DC) up -d

down:
	$(DC) down

build:
	$(DC) build $(API_SERVICE)

rebuild:
	$(DC) build --no-cache $(API_SERVICE)

restart:
	$(DC) restart $(API_SERVICE)

ps:
	$(DC) ps

logs:
	$(DC) logs -f $(API_SERVICE)

sh:
	# open a shell inside the API container
	$(DC) exec $(API_SERVICE) sh -lc 'bash || sh'

dbsh:
	# open psql inside the Postgres container
	$(DC) exec $(DB_SERVICE) bash -lc 'psql -U fink -d fink'

## --- Dev quality (host, via Poetry) ---
fmt:
	poetry run black app

fmt-check:
	poetry run black --check app

lint:
	poetry run ruff check app

type:
	poetry run mypy app

test:
	poetry run pytest -q

cov:
	poetry run coverage run -m pytest && poetry run coverage html && poetry run coverage xml

## --- Alembic (run inside API container) ---
mig-new:
	@ : $${m:?"Usage: make mig-new m=\"your message\""}
	$(DC) exec $(API_SERVICE) alembic revision -m "$(m)"

mig-autogen:
	@ : $${m:?"Usage: make mig-autogen m=\"your message\""}
	$(DC) exec $(API_SERVICE) alembic revision --autogenerate -m "$(m)"

mig-up:
	$(DC) exec $(API_SERVICE) alembic upgrade head

## --- DB helpers ---
db-tables:
	$(DC) exec $(DB_SERVICE) psql -U fink -d fink -c "\dt"

db-url:
	@echo "postgresql://fink:fink@localhost:5432/fink"
