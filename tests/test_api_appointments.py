"""
API tests for POST /make-appointmet endpoint.
"""
import pytest
from fastapi import status


def test_create_appointment_success(client, seed_test_data):
    """Test POST /make-appointmet creates appointment with valid data."""
    clinic_id = seed_test_data[0].id
    
    # Get a doctor from this clinic
    response_doctors = client.get(f"/doctors?clinic_id={clinic_id}")
    doctor_id = response_doctors.json()[0]["id"]
    
    payload = {
        "clinic_id": clinic_id,
        "doctor_id": doctor_id,
        "date": "2025-02-15",
        "time": "10:00",
        "user_name": "John Doe",
        "user_phone": "+1234567890"
    }
    
    response = client.post("/make-appointmet", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    
    data = response.json()
    assert "id" in data
    assert data["clinic_id"] == clinic_id
    assert data["doctor_id"] == doctor_id
    assert data["date"] == "2025-02-15"
    assert data["time"] == "10:00"
    assert data["user_name"] == "John Doe"
    assert data["user_phone"] == "+1234567890"


def test_create_appointment_clinic_not_found(client, seed_test_data):
    """Test POST /make-appointmet returns 404 when clinic doesn't exist."""
    # Get a doctor
    response_doctors = client.get("/doctors")
    doctor_id = response_doctors.json()[0]["id"]
    
    payload = {
        "clinic_id": 999,  # Non-existent clinic
        "doctor_id": doctor_id,
        "date": "2025-02-15",
        "time": "10:00",
        "user_name": "John Doe",
        "user_phone": "+1234567890"
    }
    
    response = client.post("/make-appointmet", json=payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Clinic not found" in response.json()["detail"]


def test_create_appointment_doctor_not_found(client, seed_test_data):
    """Test POST /make-appointmet returns 404 when doctor doesn't exist."""
    clinic_id = seed_test_data[0].id
    
    payload = {
        "clinic_id": clinic_id,
        "doctor_id": 999,  # Non-existent doctor
        "date": "2025-02-15",
        "time": "10:00",
        "user_name": "John Doe",
        "user_phone": "+1234567890"
    }
    
    response = client.post("/make-appointmet", json=payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Doctor not found" in response.json()["detail"]


def test_create_appointment_doctor_wrong_clinic(client, seed_test_data):
    """Test POST /make-appointmet returns 400 when doctor doesn't belong to clinic."""
    clinic1_id = seed_test_data[0].id
    clinic2_id = seed_test_data[1].id
    
    # Get a doctor from clinic2
    response_doctors = client.get(f"/doctors?clinic_id={clinic2_id}")
    doctor_id = response_doctors.json()[0]["id"]
    
    # Try to create appointment with clinic1 but doctor from clinic2
    payload = {
        "clinic_id": clinic1_id,
        "doctor_id": doctor_id,
        "date": "2025-02-15",
        "time": "10:00",
        "user_name": "John Doe",
        "user_phone": "+1234567890"
    }
    
    response = client.post("/make-appointmet", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Doctor does not belong to the specified clinic" in response.json()["detail"]


def test_create_appointment_missing_fields(client, seed_test_data):
    """Test POST /make-appointmet returns 422 when required fields are missing."""
    clinic_id = seed_test_data[0].id
    
    # Missing user_phone
    payload = {
        "clinic_id": clinic_id,
        "doctor_id": 1,
        "date": "2025-02-15",
        "time": "10:00",
        "user_name": "John Doe"
        # user_phone missing
    }
    
    response = client.post("/make-appointmet", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_appointment_invalid_data_types(client, seed_test_data):
    """Test POST /make-appointmet returns 422 when data types are invalid."""
    clinic_id = seed_test_data[0].id
    
    # Invalid clinic_id (string instead of int)
    payload = {
        "clinic_id": "not_an_int",
        "doctor_id": 1,
        "date": "2025-02-15",
        "time": "10:00",
        "user_name": "John Doe",
        "user_phone": "+1234567890"
    }
    
    response = client.post("/make-appointmet", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

