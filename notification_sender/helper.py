import logging
from logging import config
from dynaconf import settings


class LogHelper:
    @staticmethod
    def create_logger(name):
        logging_dict_config = dict((k.lower(), v) for k, v in settings.as_dict('logging').items())
        config.dictConfig(logging_dict_config)
        return logging.getLogger(name)

    @staticmethod
    def set_log_level_module(module: str, level: str):
        logging.getLogger(module).setLevel(level.upper())

