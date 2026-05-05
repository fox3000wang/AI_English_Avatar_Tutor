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

## Docker

```bash
docker build -t ai-english-avatar-tutor-backend .
docker run --rm -p 8000:8000 --env-file .env ai-english-avatar-tutor-backend
```
