from sqlalchemy import create_engine, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, LargeBinary
from sqlalchemy.orm import sessionmaker, relationship, backref

import uuid

import config

from model_base import Base

class Book(Base):
    __tablename__ = config.db_prefix+'_book'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey(config.db_prefix+"_user.id"))
    uuid = Column(String)
    time = Column(DateTime)
    content = Column(Text)
    storeid = Column(Text)
    images = relationship("Image", back_populates='books')

    def __init__(self, time, owner, attributes, storeid):
        self.uuid = uuid.uuid4().bytes.encode('base64').rstrip('=\n').replace('/', '_')
        self.time = time
        self.owner_id = owner
        self.content = attributes
        self.storeid = storeid

    def __repr__(self):
        return "<Book('%s')>" % (self.content, )
