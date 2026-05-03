import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def post(point1_coords, point2_coords, point1_type="Point", point2_type="Point"):
    """Helper function to make request"""
    return client.post("/api/check-antimeridian", json={
        "point1": {"type": point1_type, "coordinates": point1_coords},
        "point2": {"type": point2_type, "coordinates": point2_coords},
    })


# --- Valid requests ---


def test_response_schema():
    """Response must contain all required fields"""
    res = post([170.5, 45.0], [-175.3, 50.2])
    data = res.json()
    assert "point1" in data
    assert "point2" in data
    assert "crosses_antimeridian" in data
    assert "longitude_difference" in data
    assert isinstance(data["crosses_antimeridian"], bool)
    assert isinstance(data["longitude_difference"], float)


def test_crosses_antimeridian():
    """Should cross antimeridian"""
    res = post([170.5, 45.0], [-175.3, 50.2])
    assert res.status_code == 200
    data = res.json()
    assert data["crosses_antimeridian"] is True
    assert data["longitude_difference"] == pytest.approx(345.8)


def test_does_not_cross():
    """Two points on the same side - should not cross antimeridian"""
    res = post([0, 45.0], [0, 50.2])
    assert res.status_code == 200
    assert res.json()["crosses_antimeridian"] is False


def test_exactly_180_does_not_cross():
    """Exactly 180 difference"""
    res = post([0.0, 0.0], [180.0, 0.0])
    assert res.status_code == 200
    assert res.json()["crosses_antimeridian"] is False


def test_same_point():
    """Same point: diff is 0, should not cross."""
    res = post([100.0, 30.0], [100.0, 30.0])
    assert res.status_code == 200
    assert res.json()["crosses_antimeridian"] is False


def test_same_latitude_different_longitude():
    """Same latitude, poles - should not cross."""
    res = post([180, 90], [180, -90])
    assert res.status_code == 200
    assert res.json()["crosses_antimeridian"] is False


# --- Edge case ---

def test_180_and_minus_180_same_line():
    """-180 and 180 are the same line - diff should be 0, should not cross."""
    res = post([180, 45], [-180, 45])
    assert res.status_code == 200
    data = res.json()
    assert data["crosses_antimeridian"] is False
    assert data["longitude_difference"] == 0


# --- Invalid requests ---

def test_error_message_content():
    """Error response must contain error field"""
    res = post([999, 45.0], [-175.3, 50.2])
    data = res.json()
    assert "error" in data
    assert "999" in data["error"]


def test_invalid_longitude_exceeds_180():
    """999 is an invalid longitude"""
    res = post([999, 45.0], [-175.5, 50.2])
    assert res.status_code == 422


def test_invalid_latitude_exceeds_90():
    """91 is an invalid latitude"""
    res = post([0.0, 91.0], [0.0, 0.0])
    assert res.status_code == 422


def test_longitude_is_string():
    """String coordinate should be rejected"""
    res = client.post("/api/check-antimeridian", json={
        "point1": {"type": "Point", "coordinates": ["", 45.0]},
        "point2": {"type": "Point", "coordinates": [-175.3, 50.2]},
    })
    assert res.status_code == 422


def test_invalid_geo_type():
    """LineString type should be rejected"""
    res = post([1, 20], [-175.3, 50.2], point1_type="LineString")
    assert res.status_code == 422


def test_missing_point1():
    """Request with only one point should be rejected"""
    res = client.post("/api/check-antimeridian", json={
        "point2": {"type": "Point", "coordinates": [-180, 45]}
    })
    assert res.status_code == 422


def test_wrong_coordinates_length():
    """3 coordinates should be rejected"""
    res = client.post("/api/check-antimeridian", json={
        "point1": {"type": "Point", "coordinates": [1.0, 2.0, 3.0]},
        "point2": {"type": "Point", "coordinates": [0.0, 0.0]},
    })
    assert res.status_code == 422
