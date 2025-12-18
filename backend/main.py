from typing import Generator, List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, func, select, text
from sqlalchemy.orm import Session, declarative_base, relationship, selectinload, sessionmaker

from .seed_data import CLINIC_NAMES, DOCTOR_ENTRIES


DATABASE_URL = "sqlite:///./database.sqlite3"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Clinic(Base):
    __tablename__ = "clinics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    doctors = relationship("Doctor", back_populates="clinic", cascade="all, delete-orphan")


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    clinic_id = Column(Integer, ForeignKey("clinics.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String, nullable=False)
    specialty = Column(String, nullable=False)

    clinic = relationship("Clinic", back_populates="doctors")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    clinic_id = Column(Integer, ForeignKey("clinics.id", ondelete="CASCADE"), nullable=False, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(String, nullable=False)
    time = Column(String, nullable=False)
    user_name = Column(String, nullable=False)
    user_phone = Column(String, nullable=False)


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class DoctorOut(BaseModel):
    id: int
    name: str
    clinic_id: int
    specialty: str

    class Config:
        orm_mode = True


class ClinicOut(BaseModel):
    id: int
    name: str
    doctors: List[DoctorOut] = []

    class Config:
        orm_mode = True


class AppointmentCreate(BaseModel):
    clinic_id: int
    doctor_id: int
    date: str = Field(..., description="Date of appointment")
    time: str = Field(..., description="Time of appointment")
    user_name: str
    user_phone: str


class AppointmentOut(BaseModel):
    id: int
    clinic_id: int
    doctor_id: int
    date: str
    time: str
    user_name: str
    user_phone: str

    class Config:
        orm_mode = True


app = FastAPI(title="Medical Directory API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    create_tables()
    with SessionLocal() as db:
        ensure_specialty_column(db)
    with SessionLocal() as db:
        seed_initial_data(db)


def ensure_specialty_column(db: Session) -> None:
    columns = [row[1] for row in db.execute(text("PRAGMA table_info(doctors);")).all()]
    if "specialty" not in columns:
        db.execute(text("ALTER TABLE doctors ADD COLUMN specialty VARCHAR NOT NULL DEFAULT 'General'"))
        db.commit()


def seed_initial_data(db: Session) -> None:
    existing_clinics = db.scalar(select(func.count()).select_from(Clinic))
    if existing_clinics and existing_clinics > 0:
        return

    for clinic_name in CLINIC_NAMES:
        clinic = Clinic(name=clinic_name)
        db.add(clinic)
        db.flush()  # obtain clinic.id

        for entry in DOCTOR_ENTRIES:
            db.add(
                Doctor(
                    name=f"{entry['name']} ({clinic_name})",
                    clinic_id=clinic.id,
                    specialty=entry["specialty"],
                )
            )

    db.commit()


@app.get("/clinics", response_model=List[ClinicOut], summary="List clinics")
def list_clinics(
    q: Optional[str] = Query(None, description="Search clinics by name"),
    db: Session = Depends(get_db),
) -> List[ClinicOut]:
    stmt = select(Clinic).options(selectinload(Clinic.doctors))
    if q:
        stmt = stmt.where(Clinic.name.ilike(f"%{q}%"))
    clinics = db.scalars(stmt).all()
    return clinics


@app.get("/doctors", response_model=List[DoctorOut], summary="List doctors")
def list_doctors(
    q: Optional[str] = Query(None, description="Search doctors by name"),
    clinic_id: Optional[int] = Query(None, description="Filter doctors by clinic"),
    db: Session = Depends(get_db),
) -> List[DoctorOut]:
    stmt = select(Doctor)
    if clinic_id is not None:
        stmt = stmt.where(Doctor.clinic_id == clinic_id)
    if q:
        stmt = stmt.where(Doctor.name.ilike(f"%{q}%"))
    doctors = db.scalars(stmt).all()
    return doctors


@app.post(
    "/make-appointmet",
    response_model=AppointmentOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create appointment",
)
def make_appointment(payload: AppointmentCreate, db: Session = Depends(get_db)) -> AppointmentOut:
    clinic = db.get(Clinic, payload.clinic_id)
    if not clinic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clinic not found")

    doctor = db.get(Doctor, payload.doctor_id)
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")

    if doctor.clinic_id != clinic.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Doctor does not belong to the specified clinic",
        )

    appointment = Appointment(
        clinic_id=payload.clinic_id,
        doctor_id=payload.doctor_id,
        date=payload.date,
        time=payload.time,
        user_name=payload.user_name,
        user_phone=payload.user_phone,
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


@app.post(
    "/make-appointment",
    response_model=AppointmentOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create appointment (alias for misspelling compatibility)",
)
def make_appointment_alias(payload: AppointmentCreate, db: Session = Depends(get_db)) -> AppointmentOut:
    return make_appointment(payload, db)


@app.get("/appointments", response_model=List[AppointmentOut], summary="List appointments")
def list_appointments(
    user_phone: Optional[str] = Query(None, description="Filter appointments by user phone"),
    db: Session = Depends(get_db),
) -> List[AppointmentOut]:
    stmt = select(Appointment)
    if user_phone:
        stmt = stmt.where(Appointment.user_phone == user_phone)
    stmt = stmt.order_by(Appointment.id.desc())
    appointments = db.scalars(stmt).all()
    return appointments


@app.delete(
    "/appointments/{appointment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cancel appointment",
)
def cancel_appointment(appointment_id: int, db: Session = Depends(get_db)) -> None:
    appointment = db.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    db.delete(appointment)
    db.commit()
    return None
