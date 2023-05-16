from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import relationship, column_property
from .db import Base
from datetime import datetime


# CREATE TABLE "Users" (
#   "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
#   "email" varchar(50) NOT NULL,
#   "password" varchar(50) NOT NULL,
#   "created_at" timestamp DEFAULT (now()),
#   "deleted" boolean DEFAULT false
# );
#
class Users(Base):
    """
    Модель Users.
    """
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    deleted = Column(Boolean, default=False)

# CREATE TABLE "UsersVerification" (
#   "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
#   "user_id" int NOT NULL,
#   "verification_photo" bytea NOT NULL,
#   "created_at" timestamp DEFAULT (now()),
#   "deleted" boolean DEFAULT false
# );
#
class UsersVerification(Base):
    """
    Модель UsersVerification.
    """
    __tablename__ = "UsersVerification"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    verification_photo = Column(BYTEA, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    deleted = Column(Boolean, default=False)

    user = relationship('Users', backref='user_verification')


# CREATE TABLE "UsersTokensSalt" (
#   "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
#   "user_id" int NOT NULL,
#   "salt" varchar(7) NOT NULL,
#   "created_at" timestamp DEFAULT (now()),
#   "deleted" boolean DEFAULT false
# );
#

# class UsersTokensSalt(Base):
#     __tablename__ = "UsersTokensSalt"
#
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
#     salt = Column(String(7), nullable=False)
#     created_at = Column(DateTime, default=datetime.now())
#     deleted = Column(Boolean, default=False)

# CREATE TABLE "UsersPhotos" (
#   "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
#   "user_id" int NOT NULL,
#   "photo" bytea NOT NULL,
#   "created_at" timestamp DEFAULT (now()),
#   "deleted" boolean DEFAULT false
# );
class UsersPhotos(Base):
    """
    Модель UsersPhotos.
    """
    __tablename__ = "UsersPhotos"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    photo = Column(BYTEA, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    deleted = Column(Boolean, default=False)

    user = relationship('Users', backref='user_photos')
# CREATE TABLE "Roles" (
#   "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
#   "name" varchar(50) NOT NULL,
#   "created_at" timestamp DEFAULT (now()),
#   "deleted" boolean DEFAULT false
# );
#
class Roles(Base):
    """
    Модель Roles.
    """
    __tablename__ = "Roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    deleted = Column(Boolean, default=False)
# CREATE TABLE "UsersRoles" (
#   "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
#   "user_id" int NOT NULL,
#   "role_id" int NOT NULL,
#   "created_at" timestamp DEFAULT (now()),
#   "deleted" boolean DEFAULT false
# );
#
class UsersRoles(Base):
    """
    Модель UsersRoles.
    """
    __tablename__ = "UsersRoles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    role_id = Column(Integer, ForeignKey('Roles.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    deleted = Column(Boolean, default=False)

    user = relationship('Users', backref='user_role')
    role = relationship('Roles', backref='user_role')


# CREATE TABLE "Cities" (
#   "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
#   "title" varchar(100) NOT NULL,
#   "created_at" timestamp DEFAULT (now()),
#   "deleted" boolean DEFAULT false
# );
#
class Cities(Base):
    """
    Модель Cities.
    """
    __tablename__ = "Cities"

    id = Column(Integer, primary_key=True)
    city_title = Column('title', String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    deleted = Column(Boolean, default=False)

# CREATE TABLE "UsersForm" (
#   "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
#   "user_id" int NOT NULL,
#   "name" varchar(50) NOT NULL,
#   "surname" varchar(50) NOT NULL,
#   "birth_date" timestamp NOT NULL,
#   "sex" boolean NOT NULL,
#   "city_id" int NOT NULL,
#   "created_at" timestamp DEFAULT (now()),
#   "deleted" boolean DEFAULT false
# );
#
class UsersForm(Base):
    """
    Модель UsersForm.
    """
    __tablename__ = "UsersForm"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    birth_date = Column(DateTime, nullable=False)
    sex = Column(Boolean, nullable=False)
    city_id = Column(Integer, ForeignKey('Cities.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    deleted = Column(Boolean, default=False)

    user = relationship('Users', backref='user_form')
    city = relationship('Cities', backref='user_form')


# CREATE TABLE "Interests" (
#   "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
#   "title" varchar(50) NOT NULL,
#   "created_at" timestamp DEFAULT (now()),
#   "deleted" boolean DEFAULT false
# );
#
class Interests(Base):
    """
    Модель Interests.
    """
    __tablename__ = "Interests"

    id = Column(Integer, primary_key=True)
    interest_title = Column('title', String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    deleted = Column(Boolean, default=False)

# CREATE TABLE "UsersInterests" (
#   "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
#   "user_id" int NOT NULL,
#   "interest_id" int NOT NULL,
#   "created_at" timestamp DEFAULT (now()),
#   "deleted" boolean DEFAULT false
# );
#
class UsersInterests(Base):
    """
    Модель UsersInterests.
    """
    __tablename__ = "UsersInterests"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    interest_id = Column(Integer, ForeignKey('Interests.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    deleted = Column(Boolean, default=False)

    user = relationship('Users', backref='user_interests')
    interest = relationship('Interests', backref='user_interests')

# CREATE TABLE "UsersLikes" (
#   "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
#   "from_user_id" int NOT NULL,
#   "to_user_id" int NOT NULL,
#   "created_at" timestamp DEFAULT (now()),
#   "deleted" boolean DEFAULT false
# );
#
class UsersLikes(Base):
    """
    Модель UsersLikes.
    """
    __tablename__ = "UsersLikes"

    id = Column(Integer, primary_key=True)
    from_user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    to_user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    deleted = Column(Boolean, default=False)

    from_user = relationship('Users', foreign_keys='UsersLikes.from_user_id')
    to_user = relationship('Users', foreign_keys='UsersLikes.to_user_id', backref='likes_received')

    # user = relationship('Users', backref='user_likes')

# CREATE TABLE "Matches" (
#   "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
#   "first_user_id" int NOT NULL,
#   "second_user_id" int NOT NULL,
#   "created_at" timestamp DEFAULT (now()),
#   "deleted" boolean DEFAULT false
# );
#
class Matches(Base):
    """
    Модель Matches.
    """
    __tablename__ = "Matches"

    id = Column(Integer, primary_key=True)
    first_user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    second_user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    deleted = Column(Boolean, default=False)

    first_user = relationship('Users', foreign_keys='Matches.first_user_id', backref='matches_received')
    second_user = relationship('Users', foreign_keys='Matches.second_user_id', backref='matches_initiated')
    # user = relationship('Users', backref='match')


# CREATE TABLE "Dialogs" (
#   "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
#   "title" varchar(50) NOT NULL,
#   "created_at" timestamp DEFAULT (now()),
#   "deleted" boolean DEFAULT false
# );
#
class Dialogs(Base):
    """
    Модель Dialogs.
    """
    __tablename__ = "Dialogs"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    deleted = Column(Boolean, default=False)
# CREATE TABLE "UsersDialogs" (
#   "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
#   "user_id" int NOT NULL,
#   "dialog_id" int NOT NULL,
#   "created_at" timestamp DEFAULT (now()),
#   "deleted" boolean DEFAULT false
# );
#
class UsersDialogs(Base):
    """
    Модель UsersDialogs.
    """
    __tablename__ = "UsersDialogs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    dialog_id = Column(Integer, ForeignKey('Dialogs.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    deleted = Column(Boolean, default=False)

    user = relationship('Users', backref='user_dialogs')
    dialogs = relationship('Dialogs', backref='user_dialogs')


# CREATE TABLE "Messages" (
#   "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
#   "from_id" int NOT NULL,
#   "dialog_id" int NOT NULL,
#   "content" varchar(100) NOT NULL,
#   "created_at" timestamp DEFAULT (now()),
#   "deleted" boolean DEFAULT false
# );
#
class Messages(Base):
    """
    Модель Messages.
    """
    __tablename__ = "Messages"

    id = Column(Integer, primary_key=True)
    from_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    dialog_id = Column(Integer, ForeignKey('Dialogs.id'), nullable=False)
    content = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    deleted = Column(Boolean, default=False)

    user = relationship('Users', backref='messages')
    dialogs = relationship('Dialogs', backref='messages')


# CREATE TABLE "Personalities" (
#   "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
#   "title" varchar(10) NOT NULL,
#   "created_at" timestamp DEFAULT (now()),
#   "deleted" boolean DEFAULT false
# );
#
class Personalities(Base):
    """
    Модель Personalities.
    """
    __tablename__ = "Personalities"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    deleted = Column(Boolean, default=False)
# CREATE TABLE "UsersPersonalities" (
#   "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
#   "user_id" int NOT NULL,
#   "personality_id" int NOT NULL,
#   "created_at" timestamp DEFAULT (now()),
#   "deleted" boolean DEFAULT false
# );
#
class UsersPersonalities(Base):
    """
    Модель UsersPersonalities.
    """
    __tablename__ = "UsersPersonalities"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    personality_id = Column(Integer, ForeignKey('Personalities.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    deleted = Column(Boolean, default=False)

    user = relationship('Users', backref='user_personalities')
    personality = relationship('Personalities', backref='user_personalities')


# CREATE TABLE "Warnings" (
#   "id" INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
#   "to_user_id" int NOT NULL,
#   "description" varchar(255) NOT NULL,
#   "created_at" timestamp DEFAULT (now()),
#   "deleted" boolean DEFAULT false
# );
class Warnings(Base):
    """
    Модель Warnings.
    """
    __tablename__ = "Warnings"

    id = Column(Integer, primary_key=True)
    to_user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    deleted = Column(Boolean, default=False)

    user = relationship('Users', backref='warnings')
