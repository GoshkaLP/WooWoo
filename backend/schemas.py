from pydantic import BaseModel, Field, BaseConfig

from pydantic.fields import ModelField
from pydantic.typing import is_union, get_args, get_origin

from datetime import datetime

from typing import Optional


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
    city_title: str


class Interests(BaseDB):
    interest_title: str


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


class UsersLikes(BaseDB):
    from_user_id: int
    to_user_id: int


class Matches(BaseDB):
    first_user_id: int
    second_user_id: int


class UsersLikesMatches(BaseModel):
    like: UsersLikes
    match: Optional[Matches]

