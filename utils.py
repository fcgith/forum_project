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

not_found = HTTPException \
(
        status_code=404,
        detail="The requested resource could not be found."
)

def hash_password(password: str) -> str:
    """
    Hashes a password
    """
    return hashlib.sha256(password.encode()).hexdigest()

def create_access_token(data: dict) -> str:
    """
    Creates an access token for the provided user (data)
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60*8) # 8 hours
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)
) -> Type[Users]:
    """
    Checks if the provided access token is invalid or expired and returns user data if valid
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
    """
    # Checks if the logged-in user, if such, is an admin
    if not current_user.admin:
        raise access_denied
    return current_user

# CONTENT

def can_user_see_category(user: Users,
                          category: Type[Category],
                          db: Session
) -> bool:
    """
    Checks if user is logged in, if so checks if they have the permission to view the category
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
    if topic:
        category = db.query(Category).filter(Category.id.__eq__(topic.category_id)).first()
        if not can_user_see_category(user, category, db):
            raise access_denied
        return True
    raise not_found