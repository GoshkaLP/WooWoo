from typing import Annotated

from sqlalchemy.orm import Session

from dependecies import get_db

from fastapi import APIRouter, Depends, Form, HTTPException, File
from fastapi.responses import StreamingResponse

from io import BytesIO

from schemas import Cities, Interests, UsersForm, UsersInterests, UsersPhotos, TokenData


from controllers.security_controller import get_current_user

from controllers.forms_controller import create_city, get_cities, create_interest, create_form, get_interests, \
    add_user_interests, get_user_interests, get_user_form, add_user_photos, get_user_photos, get_photo_url

forms = APIRouter(
    prefix='/api/forms',
    tags=['users forms']
)


@forms.post('/cities', response_model=Cities)
def api_create_city(db: Annotated[Session, Depends(get_db)],
                    city_title: Annotated[str, Form()],
                    current_user: Annotated[TokenData, Depends(get_current_user)]):
    """
    Эндпоинт для добавления города.
    :param db: Сессия БД.
    :param city_title: Наименование города.
    :param current_user: Текущий пользователь.
    :return: Результат работы соответствующего метода.
    """
    try:
        return create_city(db, city_title)
    except HTTPException as e:
        raise e


@forms.get('/cities', response_model=list[Cities])
def api_get_cities(db: Annotated[Session, Depends(get_db)],
                   current_user: Annotated[TokenData, Depends(get_current_user)]):
    """
    Эндпоинт для получения списка городов.
    :param db: Сессия БД.
    :param current_user: Текущий пользователь.
    :return: Результат работы соответствующего метода.
    """
    try:
        return get_cities(db)
    except HTTPException as e:
        raise e


@forms.post('/interests', response_model=Interests)
def api_create_interest(db: Annotated[Session, Depends(get_db)],
                        interest_title: Annotated[str, Form()],
                        current_user: Annotated[TokenData, Depends(get_current_user)]):
    """
    Эндпоинт для создания интереса.
    :param db: Сессия БД.
    :param interest_title: Наименование интереса.
    :param current_user: Текущий пользователь.
    :return: Результат работы соответствующего метода.
    """
    try:
        return create_interest(db, interest_title)
    except HTTPException as e:
        raise e


@forms.get('/interests', response_model=list[Interests])
def api_get_interests(db: Annotated[Session, Depends(get_db)],
                      current_user: Annotated[TokenData, Depends(get_current_user)]):
    """
    Эндпоинт получения интересов.
    :param db: Сессия БД.
    :param current_user: Текущий пользователь.
    :return: Результат работы соответствующего метода.
    """
    return get_interests(db)


@forms.post('/user/interests', response_model=list[UsersInterests])
def api_add_user_interest(db: Annotated[Session, Depends(get_db)],
                          current_user: Annotated[TokenData, Depends(get_current_user)],
                          interests_id: Annotated[list[int], Form()]):
    """
    Эндпоинт для добавления интересов пользоватлю.
    :param db: Сессия БД.
    :param current_user: Текущий пользователь.
    :param interests_id: Массив с id интересов.
    :return: Результат работы соответствующего метода.
    """
    try:
        return add_user_interests(db, current_user.user_id, interests_id)
    except HTTPException as e:
        raise e


@forms.get('/user/{user_id}/interests', response_model=list[UsersInterests])
def api_get_user_interests(db: Annotated[Session, Depends(get_db)],
                           user_id: int,
                           current_user: Annotated[TokenData, Depends(get_current_user)]):
    """
    Эндпоинт для получения интересов пользователя.
    :param db: Сессия БД.
    :param user_id: Id пользователя.
    :param current_user: Текущий пользователь.
    :return: Результат работы соответствующего метода.
    """
    return get_user_interests(db, user_id)


@forms.post('/user/form', response_model=UsersForm)
def api_create_form(db: Annotated[Session, Depends(get_db)],
                    name: Annotated[str, Form()],
                    surname: Annotated[str, Form()],
                    birth_date: Annotated[str, Form()],
                    sex: Annotated[bool, Form()],
                    city_id: Annotated[int, Form()],
                    current_user: Annotated[TokenData, Depends(get_current_user)]):
    """
    Эндпоинт для добавления анкеты пользователя.
    :param db: Сессия БД.
    :param name: Имя пользователя.
    :param surname: Фамилия пользователя.
    :param birth_date: Дата рождения пользователя.
    :param sex: Пол пользователя.
    :param city_id: Id города пользователя.
    :param current_user: Текущий пользователь.
    :return: Результат работы соответствующего метода.
    """
    try:
        return create_form(db, current_user.user_id, name, surname, birth_date, sex, city_id)
    except HTTPException as e:
        raise e


@forms.get('/user/form', response_model=UsersForm)
def api_get_form(db: Annotated[Session, Depends(get_db)],
                 current_user: Annotated[TokenData, Depends(get_current_user)]):
    """
    Эндпоинт для получения анкеты пользователя.
    :param db: Сессия БД.
    :param current_user: Текущий пользователь.
    :return: Результат работы соответствующего метода.
    """
    return get_user_form(db, current_user.user_id)


@forms.post('/user/photo', response_model=list[UsersPhotos])
def api_add_photos(db: Annotated[Session, Depends(get_db)],
                   photos: Annotated[list[bytes], File()],
                   current_user: Annotated[TokenData, Depends(get_current_user)]):
    """
    Эндпоинт для добавления фотографий пользователя.
    :param db: Сессия БД.
    :param photos: Массив с фотографиями пользователя.
    :param current_user: Текущий пользователь.
    :return: Результат работы соответствующего метода.
    """
    try:
        return add_user_photos(db, current_user.user_id, photos)
    except HTTPException as e:
        raise e


@forms.get('/user/{user_id}/photo', response_model=list[UsersPhotos])
def api_get_photos(db: Annotated[Session, Depends(get_db)],
                   user_id: int,
                   current_user: Annotated[TokenData, Depends(get_current_user)]):
    """
    Эндпоинт для получения ссылок на фотографии пользователя.
    :param db: Сессия БД.
    :param user_id: Id пользователя.
    :param current_user: Текущий пользователя.
    :return: Результат работы соответствующего метода.
    """
    return get_user_photos(db, user_id)


@forms.get('/user/photo/{photo_id}')
def api_photo_url(db: Annotated[Session, Depends(get_db)],
                  photo_id: int,
                  current_user: Annotated[TokenData, Depends(get_current_user)]):
    """
    Эндопоинт для получения фото по ссылке.
    :param db: Сессия БД.
    :param photo_id: Id фотографии.
    :param current_user: Текущий пользователь.
    :return: Результат работы соответствующего метода.
    """
    try:
        photo = get_photo_url(db, photo_id)
        photo_stream = BytesIO(photo.photo)
        return StreamingResponse(content=photo_stream, media_type="image/jpeg")
    except HTTPException as e:
        raise e
