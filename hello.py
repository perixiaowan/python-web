#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from flask import Flask, url_for,request , render_template,redirect,send_from_directory,session,make_response,g, abort,flash

from werkzeug.utils import secure_filename
import sqlite3
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


UPLOAD_FOLDER = 'uploads'
#UPLOAD_FOLDER = 'D:\\uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# 把上传文件限制为最大 16 MB. 如果请求传输一个更大的文件， Flask 会抛出一个 RequestEntityTooLarge 异常。
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# set session's secret_key
app.config['SECRET_KEY'] = '123456'

@app.route('/')
def index():
    username = request.form['username']
    print("request cookies username = %s" %(request.cookies.get('username')))
    #username = request.cookies.get('username')
    resp = make_response(render_template('login.html'))
    resp.set_cookie('username', username)
    return resp
    # if 'username' in session:
    #     return 'Logged in as %s' % (session['username'])
    # return 'You are not logged in'

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['username'] = username
        session['password'] = password

        print("password is %s" %(session['password']))
        print("SECRET_KEY is %s" % (app.config['SECRET_KEY']))
        resp = make_response(render_template('login.html'))
        resp.set_cookie('username', username)
        return render_template('index.html', name=username)
    return render_template('login.html', error=error)

    # error = None
    # if request.method == 'POST':
    #     if valid_login(request.form['username'],
    #                    request.form['password']):
    #         return log_the_user_in(request.form['username'])
    #     else:
    #         error = 'Invalid username/password'
    # # the code below is executed if the request method
    # # was GET or the credentials were invalid
    # return render_template('login.html', error=error)



@app.route('/loginpage')
def loginpage():
    return render_template('login.html',error="")


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login'))


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


@app.route('/user/<username>')
def profile(username): pass

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'


# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('loginpage'))
#     print(url_for('loginpage', next='/'))
#     print(url_for('profile', username='John Doe'))


# with app.test_request_context('/hello', method='POST'):
#     # now you can do something with the request until the
#     # end of the with block, such as basic assertions:
#
#     assert request.path == '/hello'
#     assert request.method == 'POST'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print("os.path:%s" %(os.path))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #file.save(app.config['UPLOAD_FOLDER'], filename)
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

# 类似 function uploaded_file
# app.add_url_rule('/uploads/<filename>', 'uploaded_file',
#                  build_only=True)
# app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
#     '/uploads':  app.config['UPLOAD_FOLDER']
# })




def valid_login(username,passwd):
    if username == 'xiaowan' and passwd == '123456':
        return True

def log_the_user_in(username):
    return render_template('index.html', name=username)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8888, debug=True)