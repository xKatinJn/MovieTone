import datetime
from app import db, login

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    nickname = db.Column(db.String(32), unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    birthday = db.Column(db.String(32))
    sex = db.Column(db.String(16))
    language = db.Column(db.String(64))
    country = db.Column(db.String(64))
    has_photo = db.Column(db.Boolean)
    photo_path = db.Column(db.String(128))

    def __repr__(self):
        return '<User: {}>'.format(self.nickname)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Statuses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return f'<Statuses id: {self.id}, name: {self.name}>'


class UserStatuses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

    def __repr__(self):
        return f'<UserStatuses id: {self.id}, status_id: {self.status_id}, status_id: {self.user_id}>'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer)
    title = db.Column(db.String(64))
    title_preview_text = db.Column(db.String(128))
    text = db.Column(db.Text)
    type = db.Column(db.Integer)
    photo_preview_path = db.Column(db.String(256))
    photo_header_path = db.Column(db.String(256))
    has_photo_preview = db.Column(db.Boolean)
    has_photo_header = db.Column(db.Boolean)
    date = db.Column(db.Date, default=datetime.datetime.now())

    def __repr__(self):
        return f'<Post id: {self.id}, title: {self.title}>'


class PostType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))

    def __repr__(self):
        return f'<PostType id: {self.id}, name: {self.name}>'
