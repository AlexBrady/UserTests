
import os

db_path = os.path.join(os.path.dirname(__file__), 'user_tests.db')
db_uri = 'sqlite:///{}'.format(db_path)


class Base:
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
