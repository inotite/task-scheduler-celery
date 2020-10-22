import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'martin-mcguire-sageglass'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    BROKER_URL = os.getenv('REDIS_URL', 'redis://{host}:{port}/0'.format(host=REDIS_HOST, port=str(REDIS_PORT)))
    CELERY_RESULT_BACKEND = BROKER_URL

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

available_configs = dict(development=DevelopmentConfig, production=ProductionConfig)
selected_config = os.getenv("FLASK_ENV", "development")
config = available_configs.get(selected_config, "development")