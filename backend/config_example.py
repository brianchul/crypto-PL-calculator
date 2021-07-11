import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    MAX_RETRY = 2
    COVALENT_API = os.environ.get("COVALENT_API")
    BITQUERY_API = os.environ.get("BITQUERY_API")
    REDIS_URL = os.environ.get("REDIS_URL")
    REDIS_PORT = os.environ.get("REDIS_PORT")

class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}