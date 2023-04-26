from models import SessionLocal


def get_db():
    """
    Метод получения сессии БД.
    :return: Сессию БД.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
