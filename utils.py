import hashlib
from datetime import datetime, timedelta
from typing import Type

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from db import get_db
from models import Users

SECRET_KEY = "test-key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60*8) # 8 hours
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user\
        (token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Type[Users]:

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
    if not current_user.admin:
        not_admin = HTTPException\
            (
                status_code=403,
                detail="You do not have permission to access this page."
            )
        raise not_admin
    return current_user