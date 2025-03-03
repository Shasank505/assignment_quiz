from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.user import get_user, get_users, create_user
from app.schemas.user import UserCreate, UserResponse
from app.core.security import get_current_active_user, get_current_active_admin

router = APIRouter()

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