import os


class Config(object):
    SECRET_KEY = 'ASdddsaAS###!@#3123kb9aasDdn09123s109'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or 'mysql+pymysql://sammy:password@localhost/movietone_db'

    SQLACLHEMY_TRACK_MODIFICATIONS = False
