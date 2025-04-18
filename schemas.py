from typing import Optional

from pydantic import BaseModel

from models import Post


# AUTH

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

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    username: str
    email: str
    age: int
    nickname: str | None = None
    admin: bool

# ADMIN

class AdminResponse(BaseModel):
    username: str
    email: str
    age: int
    nickname: str
    admin: bool

# CONTENT

class CategorySchema(BaseModel):
    id: int
    name: str
    description: str
    locked: bool = False

class TopicSchema(BaseModel):
    id: int
    title: str
    description: str | None
    locked: bool
    user_id: int
    category_id: int


class PostSchema(BaseModel):
    id: int
    content: str
    user_id: int
    topic_id: int
    category_id: int

    class Config:
        from_attributes = True

class PostViewSchema(BaseModel):
    post: PostSchema
    interactions: int
    user_vote: Optional[bool] = None

    class Config:
        from_attributes = True