"""
API tests for GET /doctors endpoint.
"""
import pytest
from fastapi import status


def test_get_doctors_empty(client):
    """Test GET /doctors returns empty list when no doctors exist."""
    response = client.get("/doctors")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_doctors_with_data(client, seed_test_data):
    """Test GET /doctors returns all doctors."""
    response = client.get("/doctors")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 6  # 2 clinics × 3 doctors = 6 doctors
    
    # Check doctor structure
    doctor = data[0]
    assert "id" in doctor
    assert "name" in doctor
    assert "clinic_id" in doctor
    assert isinstance(doctor["id"], int)
    assert isinstance(doctor["clinic_id"], int)


def test_get_doctors_filter_by_clinic_id(client, seed_test_data):
    """Test GET /doctors?clinic_id=... filters doctors by clinic."""
    clinic_id = seed_test_data[0].id
    
    response = client.get(f"/doctors?clinic_id={clinic_id}")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert len(data) == 3  # 3 doctors per clinic
    assert all(doctor["clinic_id"] == clinic_id for doctor in data)


def test_get_doctors_filter_by_nonexistent_clinic(client, seed_test_data):
    """Test GET /doctors?clinic_id=999 returns empty list for non-existent clinic."""
    response = client.get("/doctors?clinic_id=999")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_doctors_search_by_name(client, seed_test_data):
    """Test GET /doctors?q=... searches doctors by name."""
    # Get a doctor name
    response_all = client.get("/doctors")
    doctor_name = response_all.json()[0]["name"]
    search_term = doctor_name.split()[1]  # Second word (e.g., "Alex" from "Dr. Alex Morgan")
    
    response = client.get(f"/doctors?q={search_term}")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert len(data) >= 1
    assert any(search_term.lower() in doctor["name"].lower() for doctor in data)


def test_get_doctors_search_no_results(client, seed_test_data):
    """Test GET /doctors?q=... returns empty list for non-matching search."""
    response = client.get("/doctors?q=NonexistentDoctor12345")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_doctors_combined_filters(client, seed_test_data):
    """Test GET /doctors?q=...&clinic_id=... combines search and filter."""
    clinic_id = seed_test_data[0].id
    
    # Get doctors for this clinic
    response_clinic = client.get(f"/doctors?clinic_id={clinic_id}")
    doctor_name = response_clinic.json()[0]["name"]
    search_term = doctor_name.split()[1] if len(doctor_name.split()) > 1 else doctor_name[0]
    
    response = client.get(f"/doctors?q={search_term}&clinic_id={clinic_id}")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert len(data) >= 1
    assert all(doctor["clinic_id"] == clinic_id for doctor in data)

