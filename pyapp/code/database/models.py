# Defines Tables Defination 

from enum import unique
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

from .database import Base

class Users(Base):
    __tablename__ = "users"

    # 'users' table store the information about Users

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column(String, nullable=False, index=True, unique=True)
    password = Column(String, nullable=False)
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Data(Base):
    __tablename__ = "data"

    # 'data' table store the key-value pair

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    key = Column(String, primary_key=True, index=True, nullable=False, unique=True)
    value = Column(String, nullable=False)
    ownerId = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="NO ACTION"), nullable=False)
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # defines relationship b/w 'data' and 'users' table
    owner = relationship("Users")
