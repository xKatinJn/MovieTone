from app.models import User

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, ValidationError


class LoginForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired(), Email()], render_kw={"placeholder": "Введите почту"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"placeholder": "Введите пароль"})
    log_submit = SubmitField('Вход')


class RegistrationForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired(), Email()], render_kw={"placeholder": "Введите почту"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"placeholder": "Введите пароль"})
    reg_submit = SubmitField('Регистрация')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email занят')
