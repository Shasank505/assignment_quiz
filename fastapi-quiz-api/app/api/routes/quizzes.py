from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.quiz import create_quiz, update_quiz, delete_quiz, get_quiz
from app.schemas.quiz import QuizCreate, QuizUpdate, QuizResponse
from app.core.security import get_current_active_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=QuizResponse)
async def create_new_quiz(quiz: QuizCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if current_user.role != "Admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return create_quiz(db=db, quiz=quiz)

@router.put("/{quiz_id}", response_model=QuizResponse)
async def update_existing_quiz(quiz_id: int, quiz: QuizUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if current_user.role != "Admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return update_quiz(db=db, quiz_id=quiz_id, quiz=quiz)

@router.delete("/{quiz_id}", response_model=dict)
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