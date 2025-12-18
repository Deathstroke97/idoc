# Backend agent notes

## Work completed (FastAPI + SQLite)
- Added backend service under `/backend` using FastAPI and SQLAlchemy with SQLite (`database.sqlite3` created automatically).
- Models: clinics(id, name), doctors(id, clinic_id, name), appointments(id, clinic_id, doctor_id, date, time, user_name, user_phone).
- Endpoints:
  - `GET /clinics`: list clinics, optional `q` to search by clinic name; returns doctors for each clinic.
  - `GET /doctors`: list doctors; optional `q` to search by name; optional `clinic_id` to filter by clinic.
  - `POST /make-appointmet`: create appointment with clinic_id, doctor_id, date, time, user_name, user_phone; validates doctor belongs to clinic.
- Files:
  - `/backend/main.py` – app, models, routes, DB setup.
  - `/backend/requirements.txt` – dependencies (fastapi, uvicorn, sqlalchemy).
  - `/backend/backend.md` – backend specs and run instructions.

## Notes for other agents
- No auth implemented (per scope).
- SQLite DB file lives in `/backend/database.sqlite3`. Tables auto-created on app startup.
- Ensure front-end calls use the exact path `/make-appointmet` (typo retained intentionally to match contract).
