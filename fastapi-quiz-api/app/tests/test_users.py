from fastapi.testclient import TestClient
from app.main import app
from app.db.models.user import User
from app.db.session import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
import pytest

client = TestClient(app)

@pytest.fixture(scope="module")
def db():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()

def test_create_user(db: Session):
    response = client.post("/register", json={"username": "testuser", "password": "testpassword", "role": "participant"})
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"

def test_login_user(db: Session):
    response = client.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_get_user_info(db: Session):
    response = client.get("/users/me")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_admin_role(db: Session):
    response = client.post("/register", json={"username": "adminuser", "password": "adminpassword", "role": "admin"})
    assert response.status_code == 201
    assert response.json()["role"] == "admin"