import logging
import os
import sys


def initialize_logging():
    loggers = {}

    # Check for environmental variables
    logger_env_vars = {
        'FEATURETOOLS_LOG_LEVEL': 'featuretools',
        'FEATURETOOLS_ES_LOG_LEVEL': 'featuretools.entityset',
        'FEATURETOOLS_BACKEND_LOG_LEVEL': 'featuretools.computation_backend'
    }
    for logger_env, logger in logger_env_vars.items():
        log_level = os.environ.get(logger_env, None)
        if log_level is not None:
            loggers[logger] = log_level

    # Set log level to info if not otherwise specified.
    loggers.setdefault('featuretools', 'info')
    loggers.setdefault('featuretools.computation_backend', 'info')
    loggers.setdefault('featuretools.entityset', 'info')

    fmt = '%(asctime)-15s %(name)s - %(levelname)s    %(message)s'
    out_handler = logging.StreamHandler(sys.stdout)
    err_handler = logging.StreamHandler(sys.stdout)
    out_handler.setFormatter(logging.Formatter(fmt))
    err_handler.setFormatter(logging.Formatter(fmt))
    err_levels = ['WARNING', 'ERROR', 'CRITICAL']

    for name, level in list(loggers.items()):
        LEVEL = getattr(logging, level.upper())
        logger = logging.getLogger(name)
        logger.setLevel(LEVEL)
        for _handler in logger.handlers:
            logger.removeHandler(_handler)

        if level in err_levels:
            logger.addHandler(err_handler)
        else:
            logger.addHandler(out_handler)
        logger.propagate = False

initialize_logging()
