import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev-products.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False