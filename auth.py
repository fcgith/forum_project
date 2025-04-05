from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timedelta
from fastapi import HTTPException, APIRouter, Depends

from db import get_db
from models import Users
from utils import hash_password, verify_password, create_access_token

router = APIRouter(
    tags=["auth"]
)


class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    age: int
    nickname: str | None = None
    registration_date: str  # expecting a string like "2025-04-05"


class UserLogin(BaseModel):
    username: str
    password: str

class RegisterResponse(BaseModel):
    message: str
    access_token: str
    token_type: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", response_model=RegisterResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)) -> RegisterResponse:
    username_check = db.query(Users).filter(Users.username.__eq__(user.username)).first()
    email_check = db.query(Users).filter(Users.email.__eq__(user.email)).first()
    if username_check or email_check:
        raise HTTPException(status_code=400, detail=f"User with the provided credentials already exists")

    hashed_password = hash_password(user.password)
    new_user = Users(
        username=user.username,
        hashed_password=hashed_password,
        email=user.email,
        age=user.age,
        nickname=user.nickname,
        registration_date=datetime.strptime(user.registration_date, "%Y-%m-%d").date(),
        admin=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    access_token = create_access_token(data={"sub": user.username})
    return RegisterResponse(message="User created successfully", access_token=access_token, token_type="bearer")

@router.post("/login", response_model=LoginResponse)
def login_user(user: UserLogin, db: Session = Depends(get_db)) -> LoginResponse:
    db_user = db.query(Users).filter(Users.username.__eq__(user.username)).first()
    if (not db_user or
            not verify_password(user.password, db_user.hashed_password)):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.username})
    return LoginResponse(access_token=access_token, token_type="bearer")

