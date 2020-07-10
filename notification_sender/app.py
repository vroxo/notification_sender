from . import connexion
from .ext import configuration, database, commands


def create_app():
    connexion.add_api('swagger.yaml', strict_validation=True, validate_responses=True)
    configuration.init_app(connexion.app)
    database.init_app(connexion.app)
    commands.init_app(connexion.app)

    return connexion.app

