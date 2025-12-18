"""
API tests for GET /clinics endpoint.
"""
import pytest
from fastapi import status


def test_get_clinics_empty(client):
    """Test GET /clinics returns empty list when no clinics exist."""
    response = client.get("/clinics")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_clinics_with_data(client, seed_test_data):
    """Test GET /clinics returns clinics with doctors."""
    response = client.get("/clinics")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2  # 2 clinics seeded
    
    # Check first clinic structure
    clinic = data[0]
    assert "id" in clinic
    assert "name" in clinic
    assert "doctors" in clinic
    assert isinstance(clinic["doctors"], list)
    assert len(clinic["doctors"]) == 3  # 3 doctors per clinic
    
    # Check doctor structure
    doctor = clinic["doctors"][0]
    assert "id" in doctor
    assert "name" in doctor
    assert "clinic_id" in doctor
    assert doctor["clinic_id"] == clinic["id"]


def test_get_clinics_search(client, seed_test_data):
    """Test GET /clinics?q=... searches clinics by name."""
    # Search for first clinic
    first_clinic_name = seed_test_data[0].name
    search_term = first_clinic_name.split()[0]  # First word of clinic name
    
    response = client.get(f"/clinics?q={search_term}")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert len(data) >= 1
    assert any(clinic["name"] == first_clinic_name for clinic in data)


def test_get_clinics_search_no_results(client, seed_test_data):
    """Test GET /clinics?q=... returns empty list for non-matching search."""
    response = client.get("/clinics?q=NonexistentClinic12345")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_clinics_search_case_insensitive(client, seed_test_data):
    """Test GET /clinics?q=... search is case insensitive."""
    first_clinic_name = seed_test_data[0].name
    search_term = first_clinic_name.split()[0].lower()  # Lowercase first word
    
    response = client.get(f"/clinics?q={search_term}")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert len(data) >= 1

