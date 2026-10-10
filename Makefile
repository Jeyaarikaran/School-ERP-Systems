.PHONY: up down lint typecheck test setup migrate

up:
	docker compose up -d

down:
	docker compose down

setup:
	cd backend && uv sync

lint:
	cd backend && uv run ruff check app/ tests/ && uv run ruff format --check app/ tests/

typecheck:
	cd backend && uv run mypy app/

test:
	cd backend && uv run pytest tests/

migrate:
	cd backend && uv run alembic upgrade head
