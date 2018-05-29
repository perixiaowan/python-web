#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, flash, redirect, render_template, \
     request, url_for

import logging

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    return render_template('index-02.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
                request.form['password'] != 'secret':
            error = 'Invalid credentials'
        else:
            flash('You were successfully logged in')
            return redirect(url_for('index'))
    return render_template('login-02.html', error=error)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000, debug=True)