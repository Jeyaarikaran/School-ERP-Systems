# School ERP Backend

Multi-tenant School ERP Backend built with FastAPI, PostgreSQL (asyncpg), and Redis.

## Local Development

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest tests/ -v
```
