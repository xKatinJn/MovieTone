import re
import email_validator
from app.models import User

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, ValidationError


class EqualTo(object):
    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % self.fieldname)
        if field.data != other.data:
            if self.message is None:
                message = field.gettext('Данные в полях должны быть одинаковы.')

            raise ValidationError(message)


class Email(object):
    user_regex = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*\Z"  # dot-atom
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"\Z)',  # quoted-string
        re.IGNORECASE)

    def __init__(
        self,
        message=None,
        granular_message=False,
        check_deliverability=False,
        allow_smtputf8=True,
        allow_empty_local=False,
    ):
        if email_validator is None:
            raise Exception("Install 'email_validator' for email validation support.")
        self.message = message
        self.granular_message = granular_message
        self.check_deliverability = check_deliverability
        self.allow_smtputf8 = allow_smtputf8
        self.allow_empty_local = allow_empty_local

    def __call__(self, form, field):
        try:
            if field.data is None:
                raise email_validator.EmailNotValidError()
            email_validator.validate_email(
                field.data,
                check_deliverability=self.check_deliverability,
                allow_smtputf8=self.allow_smtputf8,
                allow_empty_local=self.allow_empty_local,
            )
        except email_validator.EmailNotValidError as e:
            message = self.message
            if message is None:
                if self.granular_message:
                    message = field.gettext(e)
                else:
                    message = field.gettext("Неправильный почтовый формат.")
            raise ValidationError(message)


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


class EditProfileForm(FlaskForm):
    email = StringField('Email', validators=[Email()], render_kw={'placeholder': 'Email'})
    password = PasswordField('Пароль1', render_kw={'placeholder': 'Новый пароль'})
    password_rep = PasswordField('Пароль2', validators=[EqualTo('password')],
                                 render_kw={'placeholder': 'Повторите пароль'})
    nickname = StringField('Никнейм', render_kw={'placeholder': 'Никнейм'})
    name = StringField('Имя', render_kw={'placeholder': 'Имя и фамилия'})
    birthday = DateField('Дата рождения', render_kw={"placeholder": "YYYY-MM-DD"})
    sex = SelectField('Пол', choices=[('Мужской', 'Мужской'), ('Мужской', 'Женский')])
    country = StringField('Страна', render_kw={'placeholder': 'Страна'})
    language = StringField('Язык', render_kw={'placeholder': 'Язык'})
    submit = SubmitField('Сохранить')
    back = SubmitField('Назад')


class CreatePostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()], render_kw={'placeholder': 'До 64 символов'})
    preview_text = TextAreaField('Превью-текст', validators=[DataRequired()],
                                 render_kw={'placeholder': 'До 128 символов'})
    text = TextAreaField('Основной текст', validators=[DataRequired()], render_kw={'placeholder': 'Основной текст'})
    type = SelectField('Выберите категорию', choices=[(1, 'Сериал'), (2, 'Кино'), (3, 'Игра')])
    submit_create = SubmitField('Создать')
