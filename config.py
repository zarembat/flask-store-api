import os 


# Find the absolute file path to the top level project directory
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Base configuration class. Contains default configuration settings + configuration settings applicable to all environments.
    """

    # Default settings
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False
    PROPAGATE_EXCEPTIONS = False
    FLASK_RUN_PORT = 5000

    # Settings applicable to all environments
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', default='tomek')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://') if os.environ.get('DATABASE_URL') else "sqlite:///" + os.path.join(basedir, 'dev.db')
    PROPAGATE_EXCEPTIONS = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
