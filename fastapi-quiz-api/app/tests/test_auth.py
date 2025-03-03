from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_db
from app.db.models.user import User
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session

client = TestClient(app)

def override_get_db():
    # This function will be used to override the database session for testing
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def test_register_user():
    response = client.post("/register", json={"username": "testuser", "password": "testpassword", "role": "participant"})
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"

def test_login_user():
    client.post("/register", json={"username": "testuser", "password": "testpassword", "role": "participant"})
    response = client.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_user():
    response = client.post("/login", data={"username": "invaliduser", "password": "wrongpassword"})
    assert response.status_code == 401

def test_register_user_existing():
    client.post("/register", json={"username": "testuser", "password": "testpassword", "role": "participant"})
    response = client.post("/register", json={"username": "testuser", "password": "testpassword", "role": "participant"})
    assert response.status_code == 400
    assert "detail" in response.json()