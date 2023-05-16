from fastapi import APIRouter, Depends, Form

from sqlalchemy.orm import Session

from typing import Annotated

from controllers.security_controller import get_current_user

from controllers.feed_controller import like_user, get_user_matches, get_user_feed

from dependecies import get_db

from schemas import TokenData, UsersLikesMatches, Matches, UsersForm

feed = APIRouter(
    prefix='/api/feed',
    tags=['user feed']
)


@feed.post('/user/like', response_model=UsersLikesMatches)
def api_like_user(db: Annotated[Session, Depends(get_db)],
                  to_user_id: Annotated[int, Form()],
                  current_user: Annotated[TokenData, Depends(get_current_user)]):
    """
    Эндпоинт для установки лайка пользователю.
    :param db: Сессия БД.
    :param to_user_id: Id пользователя, которому ставят лайк.
    :param current_user: Текущий пользователь.
    :return: Результат работы соответствующего метода.
    """
    return like_user(db, current_user.user_id, to_user_id)


@feed.get('/user/matches', response_model=list[Matches])
def api_like_user(db: Annotated[Session, Depends(get_db)],
                  current_user: Annotated[TokenData, Depends(get_current_user)]):
    """
    Эндпоинт для получения списка мэтчей пользователя.
    :param db: Сессия БД.
    :param current_user: Текущий пользователь.
    :return: Результат работы соответствующего метода.
    """
    return get_user_matches(db, current_user.user_id)


@feed.get('/user/feed', response_model=list[UsersForm])
def api_get_user_feed(db: Annotated[Session, Depends(get_db)],
                      current_user: Annotated[TokenData, Depends(get_current_user)]):
    """
    Эндпоинт для получения ленты пользователя.
    :param db: Сессия БД.
    :param current_user: Текущий пользователь.
    :return: Результат работы соответствующего метода.
    """
    return get_user_feed(db, current_user.user_id)
