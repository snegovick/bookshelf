from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, LargeBinary
from sqlalchemy.orm import sessionmaker, relationship, backref

import uuid
import hashlib
import os

import config

from model_base import Base
from datetime import *

class MSession(Base):
    __tablename__ = config.db_prefix+'_msession'

    id = Column(Integer, primary_key=True)
    uuid = Column(String)
    user_id =  Column(Integer, ForeignKey(config.db_prefix+"_user.id"))
    creation_time = Column(DateTime)
    keepalive_till = Column(DateTime)
    

    def __init__(self, user_id, ttl_days):
        self.uuid = uuid.uuid4().bytes.encode('base64').rstrip('=\n').replace('/', '_')
        self.creation_time = datetime.now()
        self.user_id = user_id
        dt = timedelta(ttl_days)
        self.keepalive_till = self.creation_time+dt

    def check_if_valid(self):
        if self.keepalive_till>datetime.now():
            print "session is ok:", self.keepalive_till, "<=", datetime.now()
            return True
        print "session is bad:", self.keepalive_till, ">", datetime.now()       
        return False

    def __repr__(self):
        return "<Session('%i')>" % (self.id)
