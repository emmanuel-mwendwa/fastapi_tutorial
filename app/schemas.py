from pydantic import BaseModel, EmailStr
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    # convert sqlalchemy model to pydantic model
    class Config:
        from_attributes = True


class CreateUser(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    email: EmailStr
    created_at: datetime
    id: int

    class Config:
        from_attributes = True


class UserLogin(CreateUser):
    pass