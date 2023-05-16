from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from datetime import datetime

from models import Cities, Interests, UsersInterests, UsersForm, UsersPhotos

from controllers.errors_controller import city_not_create_exception, interest_not_create_exception, \
    form_not_create_exception, city_exists_exception, interest_exists_exception, form_exists_exception, \
    interest_not_add_exception, no_interest_exception, photo_not_add_exception, no_photo_exception


def create_city(db: Session, city_title: str):
    """
    Метод для добавления города в БД.
    :param db: Сессия БД.
    :param city_title: Наименования города.
    :return: Ошибку создания или результат типа Cities.
    """
    try:
        if db.query(Cities).filter_by(title=city_title).first():
            raise city_exists_exception
        city = Cities(title=city_title)
        db.add(city)
        db.commit()
        return city
    except SQLAlchemyError as e:
        db.rollback()
        raise city_not_create_exception


def get_cities(db: Session):
    """
    Метод получения городов из БД.
    :param db: Сессия БД.
    :return: Массив с записями типа Cities.
    """
    cities = db.query(Cities).all()
    return cities


def create_interest(db: Session, interest_title: str):
    """
    Метод добавления интереса в БД.
    :param db: Сессия БД.
    :param interest_title: Наименования интереса.
    :return: Ошибку создания или результат типа Interests.
    """
    try:
        if db.query(Interests).filter_by(title=interest_title).first():
            raise interest_exists_exception
        interest = Interests(title=interest_title)
        db.add(interest)
        db.commit()
        return interest
    except SQLAlchemyError as e:
        db.rollback()
        raise interest_not_create_exception


def get_interests(db: Session):
    """
    Метод получения интересов из БД.
    :param db: Сессия БД.
    :return: Массив с записями типа Interests.
    """
    interests = db.query(Interests).all()
    return interests


def add_user_interests(db: Session, user_id: int, interests_id: list[int]):
    """
    Метод для добавления интересов пользователя в БД.
    :param db: Сессия БД.
    :param user_id: Id текущего пользователя.
    :param interests_id: Массив с id интересов.
    :return: Ошибку создания или массив с записями типа Interests.
    """
    try:
        if not all(db.query(Interests).filter_by(id=interest_id).first() is not None for interest_id in interests_id):
            raise no_interest_exception
        user_interests = []
        for interest_id in interests_id:
            if not db.query(UsersInterests).filter_by(user_id=user_id, interest_id=interest_id).first():
                user_interest = UsersInterests(
                    user_id=user_id,
                    interest_id=interest_id
                )
                db.add(user_interest)
                db.commit()
                user_interests.append(
                    {**user_interest.user.__dict__, **user_interest.interest.__dict__, **user_interest.__dict__})
        return user_interests
    except SQLAlchemyError as e:
        db.rollback()
        raise interest_not_add_exception


def get_user_interests(db: Session, user_id: int):
    """
    Метод для получения интересов пользователя из БД.
    :param db: Сессия БД.
    :param user_id: Id текущего пользователя.
    :return: Массив с записями типа Interests.
    """
    user_interests = db.query(UsersInterests).filter_by(user_id=user_id).all()
    resp = []
    for user_interest in user_interests:
        resp.append({**user_interest.user.__dict__, **user_interest.interest.__dict__, **user_interest.__dict__})
    return resp


def create_form(db: Session, user_id: int, name: str, surname: str,
                birth_date: str, sex: int, city_id: int):
    """
    Метод для создания анкеты пользователя в БД.
    :param db: Сессия БД.
    :param user_id: Id текущего пользователя.
    :param name: Имя пользователя.
    :param surname: Фамилия пользователя.
    :param birth_date: Дата рождения пользователя.
    :param sex: Пол пользователя.
    :param city_id: Id города, в котором живет пользователь.
    :return: Ошибку создания или результат типа IsersForm.
    """
    try:
        if db.query(UsersForm).filter_by(user_id=user_id).first():
            raise form_exists_exception
        user_form = UsersForm(
            user_id=user_id,
            name=name,
            surname=surname,
            birth_date=datetime.strptime(birth_date, '%d.%m.%Y'),
            sex=sex,
            city_id=city_id
        )
        db.add(user_form)
        db.commit()
        return {**user_form.user.__dict__, **user_form.city.__dict__, **user_form.__dict__}
    except SQLAlchemyError as e:
        db.rollback()
        raise form_not_create_exception


def get_user_form(db: Session, user_id: int):
    """
    Метод для получения анкеты пользователя.
    :param db: Сессия БД.
    :param user_id: Id текущего пользователя.
    :return: Результат типа UsersForm.
    """
    user_form = db.query(UsersForm).filter_by(user_id=user_id).first()
    return {**user_form.user.__dict__, **user_form.city.__dict__, **user_form.__dict__}


def add_user_photos(db: Session, user_id: int, photos: list[bytes]):
    """
    Метод для добавления фотографий пользователя в БД.
    :param db: Сессия БД.
    :param user_id: Id текущего пользователя.
    :param photos: Массив с фотографиями.
    :return: Ошибку создания или массив с записями типа UsersPhotos.
    """
    try:
        resp = []
        for photo in photos:
            user_photo = UsersPhotos(
                user_id=user_id,
                photo=photo
            )
            db.add(user_photo)
            db.commit()
            resp.append({'photo_url': f'http://localhost:8000/forms/user/photo/{user_photo.id}',
                        **user_photo.__dict__})
        return resp
    except SQLAlchemyError as e:
        db.rollback()
        raise photo_not_add_exception


def get_user_photos(db: Session, user_id: int):
    """
    Метод для получения ссылок на фотографии пользователя.
    :param db: Сессия БД.
    :param user_id: Id текущего пользователя.
    :return: Массив с записями типа UsersPhotos.
    """
    user_photos = db.query(UsersPhotos).filter_by(user_id=user_id).all()
    resp = []
    for user_photo in user_photos:
        resp.append({'photo_url': f'/api/forms/user/photo/{user_photo.id}',
                     **user_photo.__dict__})
    return resp


def get_photo_url(db: Session, photo_id: int):
    """
    Метод для получения фотографии по ссылке.
    :param db: Сессия БД.
    :param user_id: Id текущего пользователя.
    :param photo_id: Id фотографии.
    :return: Ошибку получения фотографии или фото.
    """
    photo = db.query(UsersPhotos).filter_by(id=photo_id).first()
    if not photo:
        raise no_photo_exception
    return photo
