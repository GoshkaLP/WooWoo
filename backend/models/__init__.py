"""
Модуль для работы с БД.
"""

from .db import SessionLocal

from .models import Users, Cities, Interests, Matches, UsersInterests, UsersForm, \
    UsersPhotos, UsersLikes

