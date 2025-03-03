from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_db
from app.db.models.quiz import Quiz
from app.db.models.user import User
from sqlalchemy.orm import Session

client = TestClient(app)

def test_create_quiz(db: Session):
    response = client.post("/quizzes/", json={"title": "Sample Quiz", "description": "This is a sample quiz."})
    assert response.status_code == 201
    assert response.json()["title"] == "Sample Quiz"

def test_get_quiz(db: Session):
    response = client.get("/quizzes/1")
    assert response.status_code == 200
    assert "title" in response.json()

def test_update_quiz(db: Session):
    response = client.put("/quizzes/1", json={"title": "Updated Quiz", "description": "Updated description."})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Quiz"

def test_delete_quiz(db: Session):
    response = client.delete("/quizzes/1")
    assert response.status_code == 204
    response = client.get("/quizzes/1")
    assert response.status_code == 404

def test_list_quizzes(db: Session):
    response = client.get("/quizzes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)