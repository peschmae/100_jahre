# Builtin config values: http://flask.pocoo.org/docs/0.10/config/
import os
import logging


class BaseConfig(object):
    DEBUG = os.environ.get('DEBUG', False)
    HOST = os.environ.get('HOST', 'localhost')
    PORT = int(os.environ.get('PORT', 5000))

    DATABASE_SERVER = os.environ.get('DATABASE_SERVER', 'localhost')
    DATABASE_USER = os.environ.get('DATABASE_USER', 'regform')
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD', 'regform')
    DATABASE_NAME = os.environ.get('DATABASE_NAME', 'registration_form')

    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LOCATION = 'jira-batch-issue.log'
    LOGGING_LEVEL = logging.DEBUG


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False


    LOGGING_LEVEL = logging.FATAL


config = {
    "development": "registration_page.config.DevelopmentConfig",
    "testing": "registration_page.config.TestingConfig",
    "production": "registration_page.config.ProductionConfig",
    "default": "registration_page.config.DevelopmentConfig"
}


def configure_app(app):
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.cfg', silent=True)
    # Configure logging
    handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
    handler.setLevel(app.config['LOGGING_LEVEL'])
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
