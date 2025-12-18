"""
Pytest configuration and fixtures for API tests.
"""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.main import app, Base, get_db


# Test database URL (temporary file database)
TEST_DATABASE_URL = "sqlite:///./test_database.sqlite3"

# Create test engine
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Create and drop tables for each test."""
    # Remove test database if exists
    if os.path.exists("./test_database.sqlite3"):
        try:
            os.remove("./test_database.sqlite3")
        except PermissionError:
            pass  # File might be locked, will be removed later
    
    # Create tables
    Base.metadata.create_all(bind=test_engine)
    yield
    # Close all connections
    test_engine.dispose()
    # Drop all tables after test
    Base.metadata.drop_all(bind=test_engine)
    # Remove test database (ignore errors if file is locked)
    try:
        if os.path.exists("./test_database.sqlite3"):
            os.remove("./test_database.sqlite3")
    except (PermissionError, OSError):
        pass  # File might be locked, will be cleaned up on next run


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with dependency override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def seed_test_data(db_session):
    """Seed test data: 2 clinics with 3 doctors each."""
    from backend.main import Clinic, Doctor
    from backend.seed_data import CLINIC_NAMES, DOCTOR_NAMES
    
    clinics = []
    for clinic_name in CLINIC_NAMES[:2]:  # Only 2 clinics for tests
        clinic = Clinic(name=clinic_name)
        db_session.add(clinic)
        db_session.flush()
        clinics.append(clinic)
        
        # Add 3 doctors per clinic
        for doctor_name in DOCTOR_NAMES[:3]:
            doctor = Doctor(name=f"{doctor_name} ({clinic_name})", clinic_id=clinic.id)
            db_session.add(doctor)
    
    db_session.commit()
    return clinics
