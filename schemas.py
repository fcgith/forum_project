from pydantic import BaseModel

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
    title: str
    content: str
    user_id: int
    topic_id: int
    category_id: int