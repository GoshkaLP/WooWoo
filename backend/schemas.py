from pydantic import BaseModel, Field
from datetime import datetime


class TokenData(BaseModel):
    user_id: int
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str


class BaseDB(BaseModel):
    id: int
    created_at: datetime
    deleted: bool

    class Config:
        orm_mode = True


class Users(BaseDB):
    email: str
    password: str


class Cities(BaseDB):
    title: str


class Interests(BaseDB):
    title: str


class UsersForm(BaseDB):
    user_id: int
    name: str
    surname: str
    birth_date: datetime
    sex: bool
    city_title: str


class UsersInterests(BaseDB):
    user_id: int
    interest_title: str


class UsersPhotos(BaseDB):
    user_id: int
    photo_url: str
