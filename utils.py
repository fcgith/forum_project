import hashlib
from datetime import datetime, timedelta
from typing import Type

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from db import get_db
from models import Users, Category, CategoryAccessPrivilege, Topic
from schemas import UserCreate

# AUTH

SECRET_KEY = "test-key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

access_denied = HTTPException \
(
        status_code=403,
        detail="You do not have permission to access this page."
)

def hash_password(password: str) -> str:
    """
    Hashes a password
    :param password: str
    :return: hashed password
    """
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if a hashed password matches with the provided non-hashed one
    :param plain_password: non-hashed password to compare
    :param hashed_password: hashed password to compare
    :return: bool
    """
    return hash_password(plain_password) == hashed_password

def verify_unique(db: Session, user: UserCreate) -> None:
    """
    Verifies that a user does not exist in the database with the provided username and email, raises error if failed
    :param db: database connection
    :param user: UserCreate schema (has username and password to check)
    :return: None
    """
    username_check = db.query(Users).filter(Users.username.__eq__(user.username)).first()
    email_check = db.query(Users).filter(Users.email.__eq__(user.email)).first()
    if username_check or email_check:
        raise HTTPException(status_code=400, detail=f"User with the provided credentials already exists")

def create_access_token(data: dict) -> str:
    """
    Creates an access token for the provided user (data)
    :param data: dict[user_data]
    :return: str, access token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60*8) # 8 hours
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user\
        (token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Type[Users]:
    """
    Checks if the provided access token is invalid or expired and returns user data if valid
    :param token: str, token
    :param db: database connection
    :return: user data
    """
    # Access token verification, makes sure it's a valid such
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise access_denied
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise access_denied

    user = db.query(Users).filter(Users.username.__eq__(username)).first()
    if user is None:
        raise access_denied
    return user

def get_admin(current_user: Users = Depends(get_current_user)) -> Users | None:
    """
    Checks if user is logged in and if so, verifies that 'admin' is 1/True or raises an error
    :param current_user: Gets current user after verifying access token
    :return: User data or None if verification fails
    """
    # Checks if the logged-in user, if such, is an admin
    if not current_user.admin:
        raise access_denied
    return current_user

# CONTENT

def can_user_see_category(user: Users, category: Type[Category], db: Session) -> bool:
    """
    Checks if user is logged in, if so checks if they have the permission to view the category
    :param user: User data after token verification
    :param category: Category that is being requested
    :param db: Database connection
    :return: True only if user has permission to view it
    """
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

def can_user_see_topic(user: Users, topic: Type[Topic], db: Session) -> bool:
    # TODO: Probably redundant but still a safety net
    category = db.query(Category).filter(Category.id.__eq__(topic.category_id)).first()
    if not can_user_see_category(user, category, db):
        raise access_denied
    return True