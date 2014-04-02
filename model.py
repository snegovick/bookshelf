# -*- encoding: utf-8 -*-

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, relationship, backref

import json

import config

from model_book import *
from model_user import *
from model_session import *
from model_image import *
from model_base import Base

import datetime
import os.path

def model_init():
        user = User(datetime.datetime.now(), "admin", "adminpwd", "{picture: \"\"}")
        session.add(user)
        session.commit()

        for i in ["test", "jungle book", "red book"]:
                book = Book(datetime.datetime.now(), user.id, json.dumps({"header": i}))
                session.add(book)
        session.commit()




need_init = True
if os.path.isfile(config.db_file):
        need_init = False

engine = create_engine(config.db, echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

session = Session()

if (need_init):
        model_init()


if __name__=="__main__":
    import sys
    if len(sys.argv)>1:
        if sys.argv[1] == "create":
            Base.metadata.create_all(engine)
