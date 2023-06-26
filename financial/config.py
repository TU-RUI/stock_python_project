import logging
import logging.config
import os

from flask import Flask
from model import db


class BaseConfig:
    host_port = os.environ["DB_HOST_PORT"]
    db_name = os.environ["DB_NAME"]
    db_user = os.environ["DB_USER"]
    db_password = os.environ["DB_PASSWORD"]
    API_KEY = os.environ["API_KEY"]
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{db_user}:{db_password}@{host_port}/{db_name}'


class DevConfig(BaseConfig):
    DEBUG = True


class ProdConfig(BaseConfig):
    DEBUG = False


# use in different env
config = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'default': DevConfig,
}

log_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        }
    },
    'root': {
        'handlers': ['console'],
        'level': "INFO"
    },
}


def createe_app():
    app = Flask(__name__)
    env_name = os.getenv('ENV')
    config_object = config.get(env_name, DevConfig)
    app.config.from_object(config_object)
    logging.config.dictConfig(log_config)
    db.init_app(app)
    logging.info(f'app start! now env is {env_name}')
    return app


app = createe_app()
