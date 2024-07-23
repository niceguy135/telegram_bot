import logging
from sys import stdout


LOG_LEVEL = logging.DEBUG


class BotLogging:

    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler(stdout)
    formater = logging.Formatter("{%(asctime)s} [%(levelname)s]: %(message)s", datefmt="%H:%M:%S")
    handler.setFormatter(formater)
    logger.addHandler(handler)
    logger.setLevel(LOG_LEVEL)

    @classmethod
    def get_logger(cls):
        return cls.logger


def log_decor(logger: logging.Logger):
    def actual_log_decor(func_handler):

        def print_simple_log(*args, **kwargs):
            logger.debug(f"{func_handler.__name__} has been called! Message: {args[0].text}")
            return func_handler(*args, **kwargs)

        return print_simple_log

    return actual_log_decor

