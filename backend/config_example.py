import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    COVALENT_API = os.environ.get("COVALENT_API")
    MAX_RETRY = 2
    BITQUERY_API = os.environ.get("BITQUERY_API")


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