.PHONY: dev build test lint seed clean

# Development commands
dev:
	docker-compose up --build

dev-detached:
	docker-compose up --build -d

# Build commands
build:
	docker-compose build

# Database commands
seed:
	docker-compose exec api python scripts/seed_data.py

migrate:
	docker-compose exec api alembic upgrade head

# Testing commands
test:
	docker-compose exec api python -m pytest tests/ -v

test-unit:
	docker-compose exec api python -m pytest tests/unit/ -v

test-integration:
	docker-compose exec api python -m pytest tests/integration/ -v

# Linting commands
lint:
	docker-compose exec api python -m black .
	docker-compose exec api python -m isort .
	docker-compose exec api python -m flake8 .
	docker-compose exec web npm run lint

# Cleanup commands
clean:
	docker-compose down -v
	docker system prune -f

# Setup commands
setup:
	cp env.example .env
	docker-compose up -d postgres redis
	sleep 10
	docker-compose exec api alembic upgrade head
	docker-compose exec api python scripts/seed_data.py

# Demo commands
demo:
	docker-compose exec api python scripts/demo.py

# Logs
logs:
	docker-compose logs -f

logs-api:
	docker-compose logs -f api

logs-web:
	docker-compose logs -f web
