import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    COVALENT_API = 'ckey_75ec2368885f44c6abb4f325006'


class TestingConfig(Config):
    TESTING = True
    COVALENT_API = ""


class ProductionConfig(Config):
    COVALENT_API = ""


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}