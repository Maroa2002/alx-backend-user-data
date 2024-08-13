#!/usr/bin/env python3
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class User(Base):
    """
    SQLAlchemy User model that represents the 'users' table in the database.

    Attributes:
        id (int): The primary key of the user, represented as an integer.
        email (str): The user's email, a non-nullable string with a maximum
            length of 250 characters.
        hashed_password (str): The hashed password of the user, a non-nullable
            string with a maximum length of 250 characters.
        session_id (str): The session ID associated with the user, an optional
            string with a maximum length of 250 characters.
        reset_token (str): The reset token for password recovery, an optional
            string with a maximum length of 250 characters.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
