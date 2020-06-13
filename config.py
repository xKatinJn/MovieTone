import os


class Config(object):
    SECRET_KEY = 'secret_key'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or 'mysql+pymysql://sammy:password@localhost/movietone_db'

    SQLACLHEMY_TRACK_MODIFICATIONS = False

# insert into post_type values (1, 'Series'), (2, 'Movies'), (3, 'Games');
# insert into statuses values (1, 'User'), (2, 'GlavRed');
