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
