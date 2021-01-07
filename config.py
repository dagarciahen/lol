import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False

    # app
    SITE_URL = 'http://localhost:5000'

    # database config
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # mail configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'cicerotravelers@gmail.com'
    MAIL_PASSWORD = 'cicero234'
    MAIL_DEBUG = True


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    SECRET_KEY = 'V=7T&w8d&@q9|k9'  # Overwrite this with ENV vars in Production
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
