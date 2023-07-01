from abc import abstractmethod
import os

class Config:

    PG_DATABASE = os.environ.get('PG_DATABASE')
    PG_USER = os.environ.get('PG_USER')
    PG_PASSWORD = os.environ.get('PG_PASSWORD')
    PG_PORT = os.environ.get('PG_PORT')
    PG_HOST = os.environ.get('PG_HOST')
    REDIS_HOST = os.environ.get('REDIST_HOST')
    REDIS_PORT = os.environ.get('REDIS_PORT')
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')

    @abstractmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):

    DEBUG = True

class TestingConfig(Config):
    TESTING = True


config = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'default': DevelopmentConfig
        }
