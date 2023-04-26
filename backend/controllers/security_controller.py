from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from fastapi.security import OAuth2PasswordBearer

from fastapi import Depends, status, HTTPException

from typing import Annotated

from models import Users

from schemas import Users as UsersSchema
from schemas import TokenData

from passlib.context import CryptContext
from jose import jwt, JWTError

from datetime import timedelta, datetime

from config import SECRET_KEY, ALGORITHM

from controllers.errors_controller import wrong_credentials_exception, wrong_token_exception, \
    user_not_found_exception, wrong_password_exception, passwords_match_exception, \
    user_not_create_exception, user_exists_exception

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_password(plain_password: str, hashed_password: str):
    """
    Метод для проверки пароля.
    :param plain_password: Пароль без шифрования.
    :param hashed_password: Зашифрованный пароль.
    :return: Результат проверки пароля.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    """
    Метод шифрования пароля.
    :param password: Пароль без шифрования.
    :return: Результат шифрования пароля.
    """
    return pwd_context.hash(password)


def get_user(db: Session, email: str):
    """
    Метод для получения пользователя из БД по почте.
    :param db: Сессия БД.
    :param email: Электронная почта.
    :return: Результат типа Users.
    """
    if user := db.query(Users).filter_by(email=email).first():
        return UsersSchema(**user.__dict__)


def authenticate_user(db: Session, email: str, password: str):
    """
    Метод для аутентификации пользователя.
    :param db: Сессия БД.
    :param email: Электронная почта.
    :param password: Пароль.
    :return: Ошибку авторизации или пользователя типа Users.
    """
    user = get_user(db, email)
    if not user:
        raise user_not_found_exception
    if not verify_password(password, user.password):
        raise wrong_password_exception
    return user


def register_user(db: Session, email: str, password: str, repeat_password: str):
    """
    Метод для регистрации пользователя.
    :param db: Сессия БД.
    :param email: Электронная почта.
    :param password: Пароль.
    :param repeat_password: Пароль еще раз.
    :return: Ошибку регистрации или пользователя типа Users.
    """
    user = get_user(db, email)
    if not user:
        if password != repeat_password:
            raise passwords_match_exception
        new_user = Users(
            email=email,
            password=get_password_hash(password)
        )
        try:
            db.add(new_user)
            db.commit()
            return new_user
        except SQLAlchemyError as e:
            db.rollback()
            # return False
            raise user_not_create_exception
    raise user_exists_exception


def create_access_token(data: dict):
    """
    Метол для создания токена пользователя.
    :param data: Данные для добавления в токен.
    :return: Токен.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=365)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Метод для получения текущего пользователя.
    :param token: Токен пользователя.
    :return: Ошибку или текущего пользователя.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get('user_id')
        email = payload.get('email')
        if not email or not user_id:
            raise wrong_credentials_exception
        token_data = TokenData(user_id=user_id, email=email)
        return token_data
    except JWTError:
        raise wrong_token_exception
