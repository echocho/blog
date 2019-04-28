import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
print(basedir)

class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'hello i am secret')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DEV_DATABASE_URI', \
                                        'postgres://postgres:@localhost:5432/blog-dev')

class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_TEST_DATABASE_URI', \
                                        'postgres://postgres:@localhost:5432/blog-test')

config = {'development': DevelopmentConfig,
          'test': TestingConfig}