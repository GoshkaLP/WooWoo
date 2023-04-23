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
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def get_user(db: Session, email: str):
    if user := db.query(Users).filter_by(email=email).first():
        return UsersSchema(**user.__dict__)


def authenticate_user(db: Session, email: str, password: str):
    user = get_user(db, email)
    if not user:
        # return False
        raise user_not_found_exception
    if not verify_password(password, user.password):
        # return False
        raise wrong_password_exception
    return user


def register_user(db: Session, email: str, password: str, repeat_password: str):
    user = get_user(db, email)
    if not user:
        if password != repeat_password:
            # return False
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
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=365)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    # credentials_exception = HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Could not validate credentials",
    #     headers={"WWW-Authenticate": "Bearer"},
    # )
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
