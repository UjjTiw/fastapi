from pydantic import BaseModel, EmailStr, conint, Field
from datetime  import datetime
from typing import Optional

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool=True
    owner_id: int
    created_at: datetime
    owner: UserResponse
    # rating: Optional[int] = None
    class Config:
        orm_mode = True
class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True

class PostUpdate(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True

class PostWithVotes(BaseModel):
    Post: Post
    votes: int

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserCreds(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)