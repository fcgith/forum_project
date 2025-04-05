from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi import HTTPException, APIRouter, Depends, Form

from db import get_db
from models import Users
from utils import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(
    tags=["auth"]
)


class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    age: int
    nickname: str | None = None


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
        admin=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    access_token = create_access_token(data={"sub": user.username})
    return RegisterResponse(message="User created successfully", access_token=access_token, token_type="bearer")

@router.post("/login", response_model=LoginResponse)
def login_user\
        (username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)) -> LoginResponse:
    db_user = db.query(Users).filter(Users.username.__eq__(username)).first()
    if (not db_user or
            not verify_password(password, db_user.hashed_password)):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": username})
    return LoginResponse(access_token=access_token, token_type="bearer")


class UserResponse(BaseModel):
    username: str
    email: str
    age: int
    nickname: str | None = None
    admin: bool


@router.get("/login_test", response_model=UserResponse)
def get_user_profile(current_user: Users = Depends(get_current_user)) -> UserResponse:
    result = UserResponse\
    (
        username=current_user.username,
        email=current_user.email,
        age=current_user.age,
        nickname=current_user.nickname,
        admin=current_user.admin
    )

    return result