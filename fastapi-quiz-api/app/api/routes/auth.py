from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, UserOut
from app.crud.user import create_user, get_user_by_username
from app.core.security import create_access_token
from app.api.dependencies import get_current_active_user

router = APIRouter()

@router.post("/register", response_model=UserOut, status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_username(db, username=user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db=db, user=user)

@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=form_data.username)
    if not db_user or not db_user.verify_password(form_data.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}