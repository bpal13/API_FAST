from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Annotated


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None            # Optional[str] = None
    

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(le=1)]


class PostOut(BaseModel):
    Posts: Post   # It's 'Posts' because the sqlalchemy model is 'Posts'
    votes: int 

    class Config:
        orm_mode = True