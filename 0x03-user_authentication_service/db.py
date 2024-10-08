#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database and return the user object."""
        user = User(email=email, hashed_password=hashed_password)
        session = self._session

        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find the first user with the given id"""
        session = self.__session
        try:
            user = session.query(User).filter_by(**kwargs).one()
            return user

        except NoResultFound:
            raise NoResultFound("No user found")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query parameters")

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update the data of a specific user"""
        session = self.__session
        valid_attributes = set(User.__table__.columns.keys())
        invalid_keys = set(kwargs.keys()) - valid_attributes

        if invalid_keys:
            raise ValueError("Invalid attributes")
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            setattr(user, key, value)
        session.commit()
