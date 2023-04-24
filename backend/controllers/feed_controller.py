from sqlalchemy.orm import Session

from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy import and_, or_

from models import UsersLikes, Matches, UsersInterests, UsersForm, Users

from controllers.errors_controller import like_not_create_exception, match_not_create_exception


def like_user(db: Session, from_user_id: int, to_user_id: int):
    if db.query(UsersLikes).filter_by(from_user_id=from_user_id, to_user_id=to_user_id).first():
        raise like_not_create_exception
    try:
        user_match = None
        user_like = UsersLikes(
            from_user_id=from_user_id,
            to_user_id=to_user_id
        )
        db.add(user_like)
        db.commit()
        if db.query(UsersLikes).filter_by(from_user_id=to_user_id, to_user_id=from_user_id).first():
            try:
                user_match = Matches(
                    first_user_id=from_user_id,
                    second_user_id=to_user_id
                )
                db.add(user_match)
                db.commit()
            except SQLAlchemyError as e:
                db.rollback()
                raise match_not_create_exception
        resp = {
            'like': user_like,
            'match': user_match
        }
        return resp
    except SQLAlchemyError:
        db.rollback()
        raise like_not_create_exception


def get_user_matches(db: Session, user_id: int):
    user_match_first = db.query(Matches).filter_by(first_user_id=user_id).all()
    user_match_second = db.query(Matches).filter_by(second_user_id=user_id).all()
    return user_match_first + user_match_second


def get_user_feed(db: Session, user_id: int):
    # Получение текущего пользователя и его города
    current_user = db.query(Users).filter_by(id=user_id).one()
    current_city_id = current_user.user_form[0].city_id
    current_sex = current_user.user_form[0].sex

    # Базовый запрос для проверки наличия записи в UsersForms и отсутствия записи в Matches
    base_query = db.query(Users).filter(
        and_(
            Users.user_form.any(),
            ~Users.matches_received.any(Matches.second_user_id == user_id),
            ~Users.matches_initiated.any(Matches.first_user_id == user_id),
            Users.user_form.any(UsersForm.sex != current_sex),
            Users.id != user_id,
            Users.deleted == False
        )
    )

    # Запрос №1: пользователи с общими интересами и из одного города
    users_with_common_interests_and_city = base_query.join(UsersInterests, UsersInterests.user_id == Users.id).join(
        UsersForm, UsersForm.user_id == Users.id).filter(
        and_(
            UsersInterests.interest_id.in_(
                db.query(UsersInterests.interest_id).filter_by(user_id=user_id)),
            UsersForm.city_id == current_city_id
        )
    ).distinct().all()

    # Запрос №2: пользователи из одного города, но без общих интересов
    users_from_same_city = base_query.join(UsersForm, UsersForm.user_id == Users.id).filter(
        and_(
            ~Users.id.in_([u.id for u in users_with_common_interests_and_city]),
            UsersForm.city_id == current_city_id
        )
    ).distinct().all()

    # Запрос №3: пользователи без общих интересов и из других городов
    remaining_users = base_query.join(UsersForm, UsersForm.user_id == Users.id).filter(
        and_(
            ~Users.id.in_([u.id for u in users_with_common_interests_and_city]),
            ~Users.id.in_([u.id for u in users_from_same_city]),
            UsersForm.city_id != current_city_id
        )
    ).distinct().all()

    # Объединение результатов и возврат списка пользователей
    matched_profiles = users_with_common_interests_and_city + users_from_same_city + remaining_users
    matched_profiles = [{**user.user_form[0].city.__dict__, **user.user_form[0].__dict__}
                        for user in matched_profiles]
    return matched_profiles
