import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'development-key'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgres://ctrqofwsvyrxvn:q7MlX9AfLHSCqCrODmXX9OpraO@ec2-54-243-201-3.compute-1.amazonaws.com:5432/d2v507p6853v9t'


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL','postgresql://localhost/codernr_dev')
