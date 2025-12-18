# Room 5

# iDoc
Service where you find the best doctors in your city.

## Backend Setup (FastAPI + SQLite)

### Prerequisites
- Python 3.8+
- pip

### Installation
1. (Recommended) Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

### Run the server
From the repo root:
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### API docs
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

### API endpoints
- `GET /clinics` — list clinics (with doctors, including specialty); optional `q` search on clinic name.
- `GET /doctors` — list doctors (each includes specialty); optional `q` (name search) and `clinic_id` filter.
- `POST /make-appointmet` — create appointment with `clinic_id`, `doctor_id`, `date`, `time`, `user_name`, `user_phone`.

### Data and database
- SQLite database: `backend/database.sqlite3` (auto-created).
- On startup, seeds 10 clinics and 20 doctors per clinic (with specialties) if no clinics exist.

### More info
See `backend/backend.md` for detailed backend notes.
