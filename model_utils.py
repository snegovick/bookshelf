import model
import config

import datetime
import json
import os
import Image


def msession_find_valid(model_session, user):
    print "querying sessions"
    sessions = model_session.query(model.MSession).filter(model.MSession.user_id == user.id).all()
    valid_session = None
    if (len(sessions)>0):
        for s in sessions:
            if not s.check_if_valid():
                print "deleting session"
                model_session.delete(s)
                model_session.commit()
            else:
                print "valid session"
                valid_session = s
    return valid_session

def msession_create_new(model_session, user, ttl):
    print "new session"
    valid_session = model.MSession(user.id, ttl)
    model.session.add(valid_session)
    model.session.commit()
    return valid_session


def user_get_by_name(model_session, name):
    users = model.session.query(model.User).filter(model.User.name == name).all()
    if (len(users)>0):
        return users[0]
    return None

def user_get_by_uuid(model_session, uuid):
    users = model.session.query(model.User).filter(model.User.uuid == uuid).all()
    if (len(users)>0):
        return users[0]
    return None


def book_get_by_uuid(uuid):
    books = model.session.query(model.Book).filter(model.Book.uuid == uuid).all()
    if (len(books)>0):
        return books[0]
    return None

def find_image_by_uuid(uuid):
    images = model.session.query(model.Image).filter(model.Image.uuid == uuid).all()
    if len(images)<1:
        return None
    return images[0]

def book_new(user, attributes, storeid, images, book):
    if (book == None):
        print "creating new book"
        p = model.Book(datetime.datetime.now(), user.id, attributes, storeid)
    else:
        print "using old book"
        p = book
        p.content = attributes
        p.storeid = storeid
    for i in images:
        image = find_image_by_uuid(i)
        if image != None:
            p.images.append(image)
    model.session.add(p)
    model.session.commit()
    return True

def blog_follow(model_session, node, user):
    print node.followers
    node.followers.append(user)
    model.session.add(node)
    model.session.commit()
    return True

def check_user_session(username, sid):
    error = None
    print "username:", username
    if (username==None) or (len(username)<3):
        user = None
        error = "Not logged in"
    else:
        user = user_get_by_name(model.session, username)
        print "user:", user
        if user == None:
            error = "No such user"
        else:
            valid_session = msession_find_valid(model.session, user)
            if valid_session == None:
                error = "Not logged in"
            elif valid_session.uuid != sid:
                error = "Bad session"
    return error, user

import imghdr
from pgmagick import Image, FilterTypes

def save_image(file, owner):
    error = None
    ext = os.path.splitext(file.filename)[1]

    image = model.Image(datetime.datetime.now(), owner.id)
    
    filename = image.uuid+ext

    if (ext==''):
        error = "No extension is set"
        return error, filename, ""
    
    image = model.Image(datetime.datetime.now(), owner.id)
    
    filename = image.uuid+ext
    image.uuid = filename

    fpath = os.path.join(config.upload_dir, filename)
    file.save(fpath)
    print fpath
    
    im = Image(fpath.encode("utf8"))
    im.quality(100)
    im.filterType(FilterTypes.SincFilter)
    im.scale('50x50')
    im.sharpen(1.0)
    thumb_path = os.path.join(config.upload_dir, "thumb_"+filename)
    # im.write(thumb_path.encode("utf8"))
    im.write(str(thumb_path.decode("utf8")))
    
    print file.filename

    model.session.add(image)
    model.session.commit()
    return error, filename, config.upload_dir


def check_keys_in_json(keys, json):
    for k in keys:
        if k not in json:
            return False
    return True

def get_books_list():
    books = model.session.query(model.Book).order_by("time desc").all()
    return books
