__version__ = '0.1.0'

import connexion
from flask import request
from .helper import LogHelper

LOGGER = LogHelper.create_logger(__name__)
LogHelper.set_log_level_module('pika', 'CRITICAL')

connexion = connexion.FlaskApp(__name__, specification_dir='api/')


@connexion.app.before_request
def before_request():
    LOGGER.info(f'{request.scheme.upper()}/{request.method} - {request.path} - {request.json}')


@connexion.app.after_request
def after_request(response):
    LOGGER.info(f'{request.scheme.upper()}/{response.status_code} - {request.path} - {response.json}')
    return response


