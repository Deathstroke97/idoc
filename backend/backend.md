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
- `backend/seed_data.py` — static seed data for clinics and doctors.

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
  - Returns clinics with embedded doctors (each doctor includes specialty).
- `GET /doctors`
  - Query params: `q` (optional, search doctor name), `clinic_id` (optional filter).
  - Each doctor includes `specialty`.
- `POST /make-appointmet`
  - Body: `clinic_id`, `doctor_id`, `date`, `time`, `user_name`, `user_phone`.
  - Validates doctor belongs to clinic; stores appointment; returns created appointment.

## Models / Tables
- clinics: `id`, `name`
- doctors: `id`, `clinic_id`, `name`, `specialty`
- appointments: `id`, `clinic_id`, `doctor_id`, `date`, `time`, `user_name`, `user_phone`

## Notes
- Startup auto-creates tables.
- On startup, seed data inserts 10 clinics and 20 doctors per clinic (with specialties) if no clinics exist yet.
- No auth implemented (per requirements).
- Endpoint path keeps provided spelling: `/make-appointmet`.
