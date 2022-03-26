import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    # `export DATABASE_URL="postgresql://admin:@localhost/users"`


class ProductionConfig(Config):
    DEBUG = False


class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
