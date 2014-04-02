 #!/usr/bin/env python

import re
import os
import json
import model
import config
import model_utils

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, send_from_directory, jsonify
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder="./templates/")
config.set_config(app)

logger = app.logger#, getLogger('sqlalchemy'),
#           getLogger('otherlibrary')]
import logging
fh = logging.FileHandler("./app.log")
fh.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))

logger.addHandler(fh)

fh.setLevel(logging.INFO)

@app.route('/api/login', methods=['GET', 'POST'])
def login_handler():
    error = None
    if (request.method == 'POST'):
        print "checking pasword"

        user = model_utils.user_get_by_name(model.session, request.json['username'])
        print "check_pass:", user.check_password(request.json['password'])
        if (user == None):
            error = 'Invalid username'
            print "bad login"
            logger.info("bad login")
        elif not user.check_password(request.json['password']):
            error = 'Invalid password'
            print "bad pass"
            logger.info("bad pass")
        else:
            valid_session = model_utils.msession_find_valid(model.session, user)
            if (valid_session == None):
                valid_session = model_utils.msession_create_new(model.session, user, 2)
            session['sid'] = valid_session.uuid

            print "login ok"
            logger.info("login OK")
            status = True
            session['username'] = request.json['username']
            session['uuid'] = user.uuid
            data={"uuid": user.uuid}
    return jsonify(error=error, status=status, data=data)

@app.route('/api/getauthstatus', methods=['GET', 'POST'])
def get_auth_status():
    status = False
    error=None
    ret_err, user = model_utils.check_user_session(session.get("username"), session.get("sid"))
    print "auth status:", ret_err
    if ret_err != None:
        uuid = None
        error = ret_err
    else:
        uuid = user.uuid

    return jsonify(error=error, uuid=uuid)

@app.route('/api/logout', methods=['GET', 'POST'])
def logout():
    error = None
    session.pop('username', None)
    return jsonify(error=error)

@app.route('/api/getlist', methods=['GET'])
def getlist():
    entries = []
    error = None
    print "getlist request"
    books = model_utils.get_books_list()
    entries = [{"images": [i.uuid for i in b.images], "storeid": b.storeid, "uuid": b.uuid, "content": json.loads(b.content)} for b in books]
    print entries
    return jsonify(error=error, entries=entries)

@app.route('/api/upload', methods=['GET', 'POST'])
def upload_file():
    error = None
    data = None
    print "upload"
    if request.method == 'POST':
        ret_err, user = model_utils.check_user_session(session.get("username"), session.get("sid"))
        if (ret_err!=None):
            error = ret_err
        else:
            print "uploading file"
            data = {}
            data["files"] = {}
            for i, file in enumerate(request.files.getlist('file')):
                print "i:", i
                ferror, filename, path = model_utils.save_image(file, user)
                print "error:", ferror, "name:", filename
                if ferror == None:
                    data["files"][i] = {"orig_name": file.name, "name": filename, "path": path, "status":True}
                else:
                    data["files"][i] = {"orig_name": file.name, "name": filename, "path": path, "status":False}
    return jsonify(error=error, data=data)

def __mk_book_content(header, year, authors):
    return json.dumps({"header": header, "year": year, "authors": authors})

@app.route('/api/post_book', methods=['GET', 'POST'])
def post_book():
    print "post book"
    error = None
    ret_err, user = model_utils.check_user_session(session.get("username"), session.get("sid"))
    if (ret_err!=None):
        error = ret_err
    else:
        uuid = request.json['uuid']
        print "uuid:", uuid
        book = None
        if uuid!=None:
            book = model_utils.book_get_by_uuid(uuid)
        header = request.json['header']
        year = request.json['year']
        storeid = str(request.json['storeid']).lower()

        authors = request.json['authors']
        images = []
        if "images" in request.json:
            images = request.json["images"]
            print images
        model_utils.book_new(user, __mk_book_content(header, year, authors), storeid, images, book)
        
    return jsonify(error=error)

@app.route('/api/getbook/<book_uuid>', methods=['GET'])
def getbook(book_uuid):
    data = None
    error = None
    print "getbook request"
    book = model_utils.book_get_by_uuid(book_uuid)
    if book != None:
        
        data = {"images": [i.uuid for i in book.images], "storeid": book.storeid, "uuid": book.uuid, "content": json.loads(book.content)}
    print data
    return jsonify(error=error, data=data)


if __name__ == '__main__':
    @app.route('/', defaults={'some_path': ''})
    @app.route('/<path:some_path>')
    def debug_serve_root(some_path):
        return send_from_directory('./static', 'layout.html')

    app.debug = False
    app.run(port=40020)

app.wsgi_app = ProxyFix(app.wsgi_app)
