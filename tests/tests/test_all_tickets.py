import uuid
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.models.item import Item
from app.routers.item import get_db

client = TestClient(app)


# Helper to get DB session for direct database tests
def get_test_db():
    db: Session = next(get_db())
    return db


# -------------------------------
# Ticket 1: Fix Failing Test for Item Creation
# -------------------------------
def test_create_item():
    unique_name = f"TestItem-{uuid.uuid4()}"
    response = client.post("/items/", json={"name": unique_name, "description": "A test item"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == unique_name
    assert data["description"] == "A test item"


# -------------------------------
# Ticket 3: Fix Database Session Handling
# -------------------------------
def test_database_session_commit():
    db = get_test_db()
    unique_name = f"SessionTest-{uuid.uuid4()}"
    new_item = Item(name=unique_name, description="Testing session commit")
    db.add(new_item)
    db.commit()
    item_in_db = db.query(Item).filter_by(name=unique_name).first()
    assert item_in_db is not None
    assert item_in_db.description == "Testing session commit"
    db.delete(item_in_db)
    db.commit()


# -------------------------------
# Ticket 4: Fix Pydantic Schema for Item
# -------------------------------
def test_read_items_schema():
    response = client.get("/items/")
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    if items:
        assert "name" in items[0]
        assert "description" in items[0]
        assert "id" in items[0]


# -------------------------------
# Ticket 5: Fix Dependency Injection for Database Session
# -------------------------------
def test_dependency_injection():
    unique_name = f"DI_Test-{uuid.uuid4()}"
    response = client.post("/items/", json={"name": unique_name, "description": "Dependency Injection Test"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == unique_name
    db = get_test_db()
    item_in_db = db.query(Item).filter_by(name=unique_name).first()
    if item_in_db:
        db.delete(item_in_db)
        db.commit()


# -------------------------------
# Ticket 2: Fix Database Model Definition
# -------------------------------
def test_model_definition():
    db = get_test_db()
    unique_name = f"ModelTest-{uuid.uuid4()}"
    item = Item(name=unique_name, description="Model Definition Test")
    db.add(item)
    db.commit()
    fetched = db.query(Item).filter_by(name=unique_name).first()
    assert fetched is not None
    assert fetched.description == "Model Definition Test"
    db.delete(fetched)
    db.commit()
