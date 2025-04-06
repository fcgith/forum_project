import hashlib
from datetime import datetime, timedelta
from typing import Type

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from db import get_db
from models import Users, Category, CategoryAccessPrivilege
from schemas import UserCreate

# AUTH

SECRET_KEY = "test-key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password

def verify_unique(db: Session, user: UserCreate):
    username_check = db.query(Users).filter(Users.username.__eq__(user.username)).first()
    email_check = db.query(Users).filter(Users.email.__eq__(user.email)).first()
    if username_check or email_check:
        raise HTTPException(status_code=400, detail=f"User with the provided credentials already exists")

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60*8) # 8 hours
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user\
        (token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Type[Users]:
    # Access token verification, makes sure it's a valid such
    credentials_exception = HTTPException\
    (
        status_code=401,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise credentials_exception

    user = db.query(Users).filter(Users.username.__eq__(username)).first()
    if user is None:
        raise credentials_exception
    return user

def get_admin(current_user: Users = Depends(get_current_user)) -> Users | None:
    # Checks if the logged-in user, if such, is an admin
    if not current_user.admin:
        not_admin = HTTPException\
            (
                status_code=403,
                detail="You do not have permission to access this page."
            )
        raise not_admin
    return current_user

# CONTENT

def can_user_see_category(user: Users, category: Type[Category], db: Session) -> bool:
    # Privileges will be 0/1 or False/True and None when general such apply
    # Admins can see all
    if user.admin:
        return True

    privilege = db.query(CategoryAccessPrivilege).filter\
    (
        CategoryAccessPrivilege.user_id.__eq__(user.id),
        CategoryAccessPrivilege.category_id.__eq__(category.id)
    ).first()

    if not privilege:
        return bool(category.visibility)
    return category.visibility and privilege.permission_type