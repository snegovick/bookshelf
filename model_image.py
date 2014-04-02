from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, LargeBinary
from sqlalchemy.orm import sessionmaker, relationship, backref

import uuid

import config

from model_base import Base

class Image(Base):
    __tablename__ = config.db_prefix+'_image'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey(config.db_prefix+"_user.id"))
    book_id = Column(Integer, ForeignKey(config.db_prefix+"_book.id"))
    uuid = Column(String)
    time = Column(DateTime)
    books = relationship("Book", order_by="Book.id", back_populates="images")

    def __init__(self, time, ownerid):
        self.uuid = uuid.uuid4().bytes.encode('base64').strip('+=\n').replace('/', '_')
        self.time = time
        self.owner_id = ownerid

    def get_image_uri(self):
        return config.upload_dir+self.uuid

    def __repr__(self):
        return "<Image('%s')>" % (self.uuid, )
