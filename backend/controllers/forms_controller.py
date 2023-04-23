from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from datetime import datetime

from fastapi import UploadFile

from models import Cities, Interests, UsersInterests, UsersForm, UsersPhotos

from controllers.errors_controller import city_not_create_exception, interest_not_create_exception, \
    form_not_create_exception, city_exists_exception, interest_exists_exception, form_exists_exception, \
    interest_not_add_exception, no_interest_exception, photo_not_add_exception, no_photo_exception


def create_city(db: Session, city_title: str):
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
    cities = db.query(Cities).all()
    return cities


def create_interest(db: Session, interest_title: str):
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
    interests = db.query(Interests).all()
    return interests


def add_user_interests(db: Session, user_id: int, interests_id: list[int]):
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
    user_interests = db.query(UsersInterests).filter_by(user_id=user_id).all()
    resp = []
    for user_interest in user_interests:
        resp.append({**user_interest.user.__dict__, **user_interest.interest.__dict__, **user_interest.__dict__})
    return resp


def create_form(db: Session, user_id: int, name: str, surname: str,
                birth_date: str, sex: int, city_id: int):
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
    user_form = db.query(UsersForm).filter_by(user_id=user_id).first()
    return {**user_form.user.__dict__, **user_form.city.__dict__, **user_form.__dict__}


def add_user_photos(db: Session, user_id: int, photos: list[bytes]):
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
    user_photos = db.query(UsersPhotos).filter_by(user_id=user_id).all()
    resp = []
    for user_photo in user_photos:
        resp.append({'photo_url': f'http://localhost:8000/forms/user/photo/{user_photo.id}',
                     **user_photo.__dict__})
    return resp


def get_photo_url(db: Session, user_id: int, photo_id: int):
    photo = db.query(UsersPhotos).filter_by(user_id=user_id, id=photo_id).first()
    if not photo:
        raise no_photo_exception
    return photo
