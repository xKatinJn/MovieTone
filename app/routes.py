from app import app, db
from app.forms import RegistrationForm, LoginForm
from app.models import User
from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.htm', title='Главная')


@app.route('/sign', methods=['GET', 'POST'])
def sign():
    if current_user.is_authenticated:
        return redirect('index')

    reg_form = RegistrationForm()
    log_form = LoginForm()

    if reg_form.reg_submit.data and reg_form.validate():
        email = reg_form.email.data
        password = reg_form.password.data

        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    if log_form.log_submit.data and log_form.validate():
        email = log_form.email.data
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(log_form.password.data):
            return render_template('registr-exit.htm', title='Авторизация', log_form=log_form, reg_form=reg_form,
                                   log_error=True)
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('registr-exit.htm', title='Авторизация', log_form=log_form, reg_form=reg_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('sign')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.htm', title='О проекте')


@app.route('/vacancy', methods=['GET'])
def vacancy():
    return render_template('vacancy.htm', title='Вакансии')


@app.route('/review', methods=['GET'])
def review():
    return render_template('review.htm', title='Рецензии')
