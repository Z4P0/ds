import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """ some default settings """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'wh3r3!$th3D0CT0R?'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    DS_MAIL_SUBJECT_PREFIX = 'DS | '
    DS_MAIL_SENDER = 'DS Admin <ds.admin@dohertysoccer.com'
    DS_ADMIN = os.environ.get('DS_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """ development configuration """
    DEBUG =True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:////'+os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    """ testing configuration """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:////'+os.path.join(basedir, 'data-testing.sqlite')


class ProductionConfig(Config):
    """ production configuration """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:////'+os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
