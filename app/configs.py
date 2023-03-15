from datetime import timedelta

class Config(object):
    '''Flask Config'''
    SECRET_KEY = 'secret'
    # JWT_SECRET_KEY = 'secret'
    # JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    # JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    SESSION_COOKIE_NAME = 'scenario builder'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1342@localhost/sb_db?charset=utf8'
    SWAGGER_UI_DOC_EXPANSION = 'list'


# class TestingConfig(DevelopmentConfig):
#     __test__ = False
#     TESTING = True
#     # SQLALCHEMY_DATABASE_URI = ''


class DevelopmentConfig(Config):
    '''Flask Config for dev'''
    DEBUG = True


class ProductionConfig(Config):
    '''Flask Config for Production'''
    pass