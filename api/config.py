import os


class Config:
    TESTING = False
    DEBUG = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')


class Development(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    SQLALCHEMY_ECHO = True
    JSONIFY_PRETTYPRINT_REGULAR = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    JWT_SECRET_KEY = 'secret'


class Testing(Config):
    FLASK_ENV = 'testing'
    TESTING = True
    DEBUG = True
    SQLALCHEMY_ECHO = True
    JSONIFY_PRETTYPRINT_REGULAR = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    JWT_SECRET_KEY = 'irrelevant'


config = {'development': Development, 'testing': Testing}
