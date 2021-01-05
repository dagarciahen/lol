import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False

    # database config
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    SECRET_KEY = 'V=7T&w8d&@q9|k9'  # Overwrite this with ENV vars in Production
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
