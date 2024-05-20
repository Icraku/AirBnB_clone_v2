#!/usr/bin/python3
"""DB storage
"""
import models
from models.base_model import BaseModel, Base
from models.city import City
from models.state import State
from os import getenv
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')


class DBStorage:
    """database storage for mysql conversion
    """
    __engine = None
    __session = None

    def __init__(self):
        """Initializer for DBStorage"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            HBNB_MYSQL_USER,
            HBNB_MYSQL_PWD,
            HBNB_MYSQL_HOST,
            HBNB_MYSQL_DB), pool_pre_ping=True)
        env = getenv("HBNB_ENV")
        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query the current session and list all instances of cls"""
        result = {}
        if cls:
            for row in self.__session.query(cls).all():
                key = "{}.{}".format(cls.__name__, row.id)
                result.update({key: row})
        else:
            for cls in [State, City]:  # You need to list all your models here
                for row in self.__session.query(cls).all():
                    key = "{}.{}".format(cls.__name__, row.id)
                    result.update({key: row})
        return result

    def rollback(self):
        """Rollback changes"""
        self.__session.rollback()

    def new(self, obj):
        """Add object to current session"""
        self.__session.add(obj)

    def save(self):
        """Commit current done work"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reload the session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the session"""
        self.__session.remove()
