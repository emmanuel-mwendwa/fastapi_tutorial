from pydantic import BaseModel, EmailStr

from datetime import datetime

from typing import Optional

from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(PostBase):
    pass


class User(BaseModel):
    email: EmailStr
    created_at: datetime
    id: int

    class Config:
        from_attributes = True


class Post(PostBase):
    id: int
    user_id: int
    # returns the pydantic model user 
    user: User
    created_at: datetime
    # convert sqlalchemy model to pydantic model
    class Config:
        from_attributes = True


class CreateUser(BaseModel):
    email: EmailStr
    password: str


class UserLogin(CreateUser):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)