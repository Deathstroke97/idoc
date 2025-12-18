# Backend agent notes

## Work completed (FastAPI + SQLite)
- Added backend service under `/backend` using FastAPI and SQLAlchemy with SQLite (`database.sqlite3` created automatically).
- Models: clinics(id, name), doctors(id, clinic_id, name, specialty), appointments(id, clinic_id, doctor_id, date, time, user_name, user_phone).
- Endpoints:
  - `GET /clinics`: list clinics, optional `q` to search by clinic name; returns doctors for each clinic (includes specialty).
  - `GET /doctors`: list doctors; optional `q` to search by name; optional `clinic_id` to filter by clinic; each doctor includes specialty.
  - `POST /make-appointmet`: create appointment with clinic_id, doctor_id, date, time, user_name, user_phone; validates doctor belongs to clinic.
- Files:
  - `/backend/main.py` – app, models, routes, DB setup.
  - `/backend/seed_data.py` – seed lists for clinics (10) and doctors (20 entries with specialties).
  - `/backend/requirements.txt` – dependencies (fastapi, uvicorn, sqlalchemy).
  - `/backend/backend.md` – backend specs and run instructions.

## Notes for other agents
- No auth implemented (per scope).
- SQLite DB file lives in `/backend/database.sqlite3`. Tables auto-created on app startup.
- Ensure front-end calls use the exact path `/make-appointmet` (typo retained intentionally to match contract).
- On startup, if no clinics exist, backend seeds 10 clinics and 20 doctors per clinic (with specialties).

---

# Frontend agent notes (Next.js)

## Work completed
- Added Next.js 14 (App Router, TS) frontend under `/frontend`.
- Pages:
  - `/` landing with hero, featured clinics and doctors.
  - `/clinics` list of all clinics (cards link to detail).
  - `/clinics/[id]` clinic detail showing doctors and “Make appointment” CTA (opens modal).
- Components: Navbar, ClinicCard, DoctorCard, AppointmentModal (client component).
- Styling: `app/globals.css` (tokens, cards, modern minimal look, no gradients), Google font Manrope in `layout.tsx`.
- API client in `frontend/lib/api.ts` with base URL `NEXT_PUBLIC_API_BASE_URL` (defaults to `http://localhost:8000`). Uses `/clinics`, `/doctors`, and `/make-appointmet` endpoints.
- Appointment modal posts to `/make-appointmet`; on submit, modal switches to success state showing appointment details.

## Run frontend
From `/frontend`:
```bash
npm install
npm run dev -- --hostname 0.0.0.0 --port 3000
```
Open http://localhost:3000 (backend at http://localhost:8000 by default).
