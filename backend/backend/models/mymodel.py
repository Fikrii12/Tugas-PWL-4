from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    DateTime,
    DECIMAL,
    ForeignKey,
    Float
)

from .meta import Base
Base = declarative_base()
DBSession = scoped_session(sessionmaker())
class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)


Index('my_index', MyModel.name, unique=True, mysql_length=255)

class User(Base):
    __tablename__ = 'user'
    id_user = Column(Integer, primary_key=True)
    nama = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    status = Column(String(255), nullable=False)

Index('user', User.nama, unique=True, mysql_length=255)


class Movie(Base):
    __tablename__ = 'movie'
    movieName = Column(String(255), primary_key=True)
    image = Column(String(255), nullable=False)
    
Index('movie', Movie.movieName, unique=True, mysql_length=255)
