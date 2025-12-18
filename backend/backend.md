# Backend (FastAPI + SQLite)

Medical directory API providing clinics, doctors, and appointment booking.

## Stack
- FastAPI
- SQLAlchemy 2.0
- SQLite (file: `database.sqlite3`, auto-created on startup)
- Uvicorn (ASGI server)

## Project layout
- `backend/main.py` — app entrypoint, models, DB session, routes.
- `backend/requirements.txt` — dependencies.
- `backend/database.sqlite3` — created at runtime.

## Setup
1. Create venv (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install deps:
   ```bash
   pip install -r backend/requirements.txt
   ```

## Run
From repo root:
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints
- `GET /clinics`
  - Query params: `q` (optional, search clinic name).
  - Returns clinics with embedded doctors.
- `GET /doctors`
  - Query params: `q` (optional, search doctor name), `clinic_id` (optional filter).
- `POST /make-appointmet`
  - Body: `clinic_id`, `doctor_id`, `date`, `time`, `user_name`, `user_phone`.
  - Validates doctor belongs to clinic; stores appointment; returns created appointment.

## Models / Tables
- clinics: `id`, `name`
- doctors: `id`, `clinic_id`, `name`
- appointments: `id`, `clinic_id`, `doctor_id`, `date`, `time`, `user_name`, `user_phone`

## Notes
- Startup auto-creates tables.
- No auth implemented (per requirements).
- Endpoint path keeps provided spelling: `/make-appointmet`.
