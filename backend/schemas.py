from pydantic import BaseModel, Field, BaseConfig

from pydantic.fields import ModelField
from pydantic.typing import is_union, get_args, get_origin

from datetime import datetime

from typing import Optional


class TokenData(BaseModel):
    """
    Схема TokenData.
    """
    user_id: int
    email: str


class Token(BaseModel):
    """
    Схема Token.
    """
    access_token: str
    token_type: str


class BaseDB(BaseModel):
    """
    Схема BaseDB для всех схем, работающих в связке с моделями БД.
    """
    id: int
    created_at: datetime
    deleted: bool

    class Config:
        orm_mode = True


class Users(BaseDB):
    """
    Схема Users.
    """
    email: str
    password: str


class Cities(BaseDB):
    """
    Схема Cities.
    """
    city_title: str


class Interests(BaseDB):
    """
    Схема Interests.
    """
    interest_title: str


class UsersForm(BaseDB):
    """
    Схема UsersForm.
    """
    user_id: int
    name: str
    surname: str
    birth_date: datetime
    sex: bool
    city_title: str


class UsersInterests(BaseDB):
    """
    Схема UsersInterests.
    """
    user_id: int
    interest_title: str


class UsersPhotos(BaseDB):
    """
    Схема UsersPhotos.
    """
    user_id: int
    photo_url: str


class UsersLikes(BaseDB):
    """
    Схема UsersLikes.
    """
    from_user_id: int
    to_user_id: int


class Matches(BaseDB):
    """
    Схема Matches.
    """
    first_user_id: int
    second_user_id: int


class UsersLikesMatches(BaseModel):
    """
    Схема UsersLikesMatches.
    """
    like: UsersLikes
    match: Optional[Matches]
