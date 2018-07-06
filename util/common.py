import os
import logging
import yaml
from logging.handlers import TimedRotatingFileHandler


def get_logger(module_name):
    logger = logging.getLogger(module_name)

    conf_file = os.getcwd() + os.path.sep + 'conf' + os.path.sep + 'user-conf.yaml'
    with open(conf_file) as f:
        log_config = yaml.load(f).get('logs')

    level = log_config.get('log_level')
    logger.setLevel(eval('logging.' + level))
    log_dir = os.getcwd() + os.path.sep + 'output'

    logfile = log_dir + os.path.sep + log_config.get('log_file')

    formatter_str = log_config.get('formatter')
    formatter_str = formatter_str.replace('*', '%')

    # Set Logging Handler
    if not len(logger.handlers):
        # handler = logging.FileHandler(logfile)
        handler = TimedRotatingFileHandler(logfile, 'midnight', 1, backupCount=5)
        handler.setLevel(eval('logging.' + level))
        formatter = logging.Formatter(formatter_str)
        handler.setFormatter(formatter)

        # add the handlers to the logger
        logger.addHandler(handler)

    return logger
