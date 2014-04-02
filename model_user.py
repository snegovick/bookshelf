from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, LargeBinary
from sqlalchemy.orm import sessionmaker, relationship, backref

import uuid
import hashlib
import os

import config

from model_base import Base

class User(Base):
    __tablename__ = config.db_prefix+'_user'

    id = Column(Integer, primary_key=True)
    uuid = Column(String)
    name = Column(String)
    pwd_hash = Column(String)
    mode = Column(Integer)
    time = Column(DateTime)
    salt = Column(String)
    content = Column(Text)
    books = relationship("Book")

    def __init__(self, time, name, pwd, content):
        self.uuid = uuid.uuid4().bytes.encode('base64').rstrip('=\n').replace('/', '_')
        self.time = time
        self.content = content
        self.name = name
        number = os.urandom(16)
        self.salt = number.encode('base64').rstrip('=\n').replace('/', '_')
        pwd = self.salt+pwd
        self.pwd_hash = hashlib.sha256(pwd).hexdigest()

    def check_password(self, password):
        pwd = self.salt+password
        pwd_hash = hashlib.sha256(pwd).hexdigest()
        return (pwd_hash==self.pwd_hash)

    def __repr__(self):
        return "<User('%i %s')>" % (self.id, self.content)
