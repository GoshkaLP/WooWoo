from sqlalchemy.orm import Session

from models import Users


def get_user(db: Session):
    user = db.query(Users).first()
    return user
