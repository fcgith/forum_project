from sqlalchemy.orm import Session
from fastapi import HTTPException, APIRouter, Depends, Form

from db import get_db
from models import Users
from schemas import RegisterResponse, UserCreate, LoginResponse
from utils import hash_password, create_access_token

router = APIRouter(
    tags=["auth"]
)

def verify_unique(db: Session, user: UserCreate) -> None:
    """
    Verifies that a user does not exist in the database with the provided username and email or raises an error
    """
    username_check = db.query(Users).filter(Users.username.__eq__(user.username)).first()
    email_check = db.query(Users).filter(Users.email.__eq__(user.email)).first()
    if username_check or email_check:
        raise HTTPException(status_code=400, detail=f"Invalid credentials")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if a hashed password matches with the provided non-hashed one
    """
    return hash_password(plain_password) == hashed_password

@router.post("/register", response_model=RegisterResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)) -> RegisterResponse:
    """
    Creating a new user
    """
    verify_unique(db, user)
    hashed_password = hash_password(user.password)

    new_user = Users\
    (
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

    return RegisterResponse(message="User created successfully")

@router.post("/login", response_model=LoginResponse)
def login_user(username: str = Form(...),
               password: str = Form(...),
               db: Session = Depends(get_db)
) -> LoginResponse:
    """
    Registered user authentication
    """
    user = db.query(Users).filter(Users.username.__eq__(username)).first()

    if not all((user, verify_password(password, user.hashed_password))):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": username})
    return LoginResponse(access_token=access_token, token_type="bearer")


# @router.get("/login_test", response_model=UserResponse)
# def get_user_profile(current_user: Users = Depends(get_current_user)) -> UserResponse:
#     """
#     Testing login token
#     """
#     result = UserResponse\
#     (
#         username=current_user.username,
#         email=current_user.email,
#         age=current_user.age,
#         nickname=current_user.nickname,
#         admin=current_user.admin
#     )
#
#     return result