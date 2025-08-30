from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_create_item():
    unique_name = f"Test-{uuid.uuid4()}"
    response = client.post("/items/", json={"name": unique_name, "description": "A test"})
    assert response.status_code == 201
    assert response.json()["name"] == unique_name

def test_read_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
