from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_db
from app.db.models.user import User
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
import pytest

client = TestClient(app)

@pytest.fixture(scope="module")
def db():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()

def test_register_user(db: Session):
    response = client.post("/register", json={"username": "testuser", "password": "testpassword", "role": "participant"})
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"

def test_login_user(db: Session):
    client.post("/register", json={"username": "testuser", "password": "testpassword", "role": "participant"})
    response = client.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_user(db: Session):
    response = client.post("/login", data={"username": "invaliduser", "password": "wrongpassword"})
    assert response.status_code == 401

def test_register_user_existing(db: Session):
    client.post("/register", json={"username": "testuser", "password": "testpassword", "role": "participant"})
    response = client.post("/register", json={"username": "testuser", "password": "testpassword", "role": "participant"})
    assert response.status_code == 400
    assert "detail" in response.json()