from typing import Annotated

from fastapi import APIRouter, Depends, status, Form, HTTPException

from schemas import Users, Token, TokenData

from sqlalchemy.orm import Session

from dependecies import get_db

from controllers.security_controller import create_access_token, authenticate_user, get_current_user, \
    register_user


users = APIRouter(
    prefix='/users',
    tags=['users']
)


@users.post('/login', response_model=Token)
def api_login(db: Annotated[Session, Depends(get_db)], email: Annotated[str, Form()], password: Annotated[str, Form()]):
    """
    Эндпоинт для авторизации пользователя.
    :param db: Сессия БД.
    :param email: Электронная почта пользователя.
    :param password: Пароль.
    :return: Результат работы соответствующего метода.
    """
    try:
        user = authenticate_user(db, email, password)
        access_token = create_access_token(
            data={'user_id': user.id, 'email': user.email}
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:
        raise e


@users.post('/register', response_model=Token)
def api_register(db: Annotated[Session, Depends(get_db)],
                 email: Annotated[str, Form()], password: Annotated[str, Form()],
                 repeat_password: Annotated[str, Form()]):
    """
    Эндпоинт для регистрации пользователя.
    :param db: Сессия БД.
    :param email: Электронная почта.
    :param password: Пароль.
    :param repeat_password: Пароль еще раз.
    :return: Результат работы соответствующего метода.
    """
    try:
        user = register_user(db, email, password, repeat_password)
        access_token = create_access_token(
            data={'user_id': user.id, 'email': user.email}
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:
        raise e


@users.get('/me', response_model=TokenData)
def api_me(current_user: Annotated[TokenData, Depends(get_current_user)]):
    """
    Эндпоинт получения текущего пользователя.
    :param current_user: Текущий пользователь.
    :return: Результат работы соответствующего метода.
    """
    return current_user
