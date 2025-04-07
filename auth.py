from sqlalchemy.orm import Session
from fastapi import HTTPException, APIRouter, Depends, Form

from db import get_db
from models import Users
from schemas import RegisterResponse, UserCreate, LoginResponse, UserResponse
from utils import hash_password, verify_password, create_access_token, verify_unique, get_current_user

router = APIRouter(
    tags=["auth"]
)

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