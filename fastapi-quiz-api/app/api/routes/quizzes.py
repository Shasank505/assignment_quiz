from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.quiz import create_quiz, update_quiz, delete_quiz, get_quiz
from app.schemas.quiz import QuizCreate, QuizUpdate, QuizResponse
from app.core.security import get_current_active_user, get_current_active_admin
from app.crud.user import get_user, get_users, create_user
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=QuizResponse, status_code=status.HTTP_201_CREATED)
async def create_new_quiz(quiz: QuizCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if current_user.role != "Admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return create_quiz(db=db, quiz=quiz)

@router.put("/{quiz_id}", response_model=QuizResponse)
async def update_existing_quiz(quiz_id: int, quiz: QuizUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if current_user.role != "Admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return update_quiz(db=db, quiz_id=quiz_id, quiz=quiz)

@router.delete("/{quiz_id}", response_model=dict, status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_quiz(quiz_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if current_user.role != "Admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    delete_quiz(db=db, quiz_id=quiz_id)
    return {"detail": "Quiz deleted successfully"}

@router.get("/{quiz_id}", response_model=QuizResponse)
async def read_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = get_quiz(db=db, quiz_id=quiz_id)
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz

@router.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db=db, user=user)

@router.get("/users/", response_model=list[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_active_admin)):
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/me/", response_model=UserResponse)
def read_user_me(current_user: UserResponse = Depends(get_current_active_user)):
    return current_user