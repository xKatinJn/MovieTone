from app import app, db
from flask import render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.htm', title='Главная')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    return render_template('registr-exit.htm')
