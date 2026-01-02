# PostgreSQL Monitoring API - Backend

FastAPI backend for monitoring PostgreSQL databases.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

3. **Run the server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## API Endpoints

- **GET /api/databases** - List all databases
- **GET /api/databases/{name}** - Get database details
- **GET /api/databases/{name}/tables** - Get table listing
- **GET /api/health** - Health check

## Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Access the Swagger UI at http://localhost:8000/docs to test all endpoints interactively.

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── db_client.py      # Database connection logic
│   ├── models.py         # Pydantic models
│   └── routers/
│       └── databases.py  # Database API endpoints
├── config/
│   └── settings.py       # Application settings
├── requirements.txt
└── .env.example
```

## Issue

This implements [Issue #3: Backend API Foundation](https://github.com/PATCoder97/db-monitoring-dashboard/issues/3)
