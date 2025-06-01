from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# A valid payload to reuse across tests
valid_payload = {
    "transaction_date": 2013.5,
    "house_age": 10.0,
    "distance_to_mrt": 300.0,
    "number_of_convenience_stores": 3,
    "latitude": 24.963,
    "longitude": 121.540
}

def test_health_check_returns_ok(): # liveness of the API 
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}

def test_predict_returns_price_with_valid_input():
    response = client.post("/predict", json=valid_payload)
    data = response.json()

    assert response.status_code == 200
    assert "predicted_price" in data
    assert isinstance(data["predicted_price"], float)
    assert data["predicted_price"] > 0

def test_predict_fails_with_missing_field():
    # Remove one required field from the input
    invalid_payload = valid_payload.copy()
    invalid_payload.pop("latitude")

    response = client.post("/predict", json=invalid_payload)
    assert response.status_code == 422  # FastAPI handles validation via Pydantic

def test_predict_fails_with_wrong_type():
    # Provide a string instead of a numeric value
    invalid_payload = valid_payload.copy()
    invalid_payload["house_age"] = "ten"

    response = client.post("/predict", json=invalid_payload)
    assert response.status_code == 422

def test_predict_handles_large_latitude():
    # Send a latitude value that is out of accepted range
    strange_payload = valid_payload.copy()
    strange_payload["latitude"] = 999.0

    response = client.post("/predict", json=strange_payload)
    assert response.status_code == 422
    assert "latitude" in response.text.lower()

def test_predict_accepts_zero_distance():
    # Set distance to MRT station to zero (edge case)
    zero_payload = valid_payload.copy()
    zero_payload["distance_to_mrt"] = 0.0

    response = client.post("/predict", json=zero_payload)
    assert response.status_code == 200
    assert response.json()["predicted_price"] > 0

def test_predict_with_negative_store_count():
    # Use a negative number for convenience stores
    weird_payload = valid_payload.copy()
    weird_payload["number_of_convenience_stores"] = -5

    response = client.post("/predict", json=weird_payload)
    assert response.status_code == 422
    assert "number_of_convenience_stores" in response.text.lower()
    
def test_predict_rejects_invalid_latitude():
    payload = valid_payload.copy()
    payload["latitude"] = 500.0  # Invalid value: latitude must be ≤ 90

    response = client.post("/predict", json=payload)
    assert response.status_code == 422
    assert "latitude" in response.text.lower()

def test_predict_rejects_invalid_longitude():
    payload = valid_payload.copy()
    payload["longitude"] = -999.0  # Invalid value: longitude must be ≥ -180

    response = client.post("/predict", json=payload)
    assert response.status_code == 422
    assert "longitude" in response.text.lower()