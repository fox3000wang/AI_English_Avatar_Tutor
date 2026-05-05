# Backend

FastAPI backend skeleton for the AI English Avatar Tutor project.

## Requirements

- Python 3.11+
- PostgreSQL connection string in `DATABASE_URL`
- Redis connection string in `REDIS_URL`

## Local Setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

## Run

```bash
uvicorn app.main:app --reload
```

When running the backend directly on your machine instead of through Docker Compose, set local
service URLs in `backend/.env`:

```text
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/avatar_tutor
REDIS_URL=redis://localhost:6379/0
```

The API health check is available at:

```text
GET /api/v1/health
```

## Test

```bash
pytest
```

## Lint

```bash
ruff check .
```

## Database Migrations

Alembic reads the database connection from `DATABASE_URL`, using the same settings module as the
FastAPI app.

Create a migration after changing SQLAlchemy models:

```bash
alembic revision --autogenerate -m "create users table"
```

Apply migrations:

```bash
alembic upgrade head
```

With Docker Compose running, execute migrations inside the backend container:

```bash
docker compose -f ../infra/docker-compose.yml exec backend alembic upgrade head
```

## Docker

```bash
docker build -t ai-english-avatar-tutor-backend .
docker run --rm -p 8000:8000 --env-file .env ai-english-avatar-tutor-backend
```

## Docker Compose

From the project root:

```bash
docker compose -f infra/docker-compose.yml up --build
```

The Compose environment starts:

- FastAPI backend on `http://localhost:8000`
- PostgreSQL on `localhost:5432`
- Redis on `localhost:6379`

Verify the backend after startup:

```bash
curl http://localhost:8000/api/v1/health
```
