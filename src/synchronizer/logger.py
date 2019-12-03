# coding=utf-8
from __future__ import absolute_import, print_function

import logging
import sys
import os
import json
from datetime import date

logger = logging.getLogger(name='synclog')


def init_logger():
    logger.setLevel(logging.DEBUG)
    # Formatter
    formatter = logging.Formatter(
                '[%(asctime)s:%(module)s:%(funcName)s:%(lineno)s:%(levelname)s] %(message)s')
    # STDOUT stream
    streamHandler = logging.StreamHandler(sys.stdout)
    streamHandler.setLevel(logging.DEBUG)
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)


def init_file_logger():
    # Formatter
    formatter = logging.Formatter(
                '[%(asctime)s:%(module)s:%(funcName)s:%(lineno)s:%(levelname)s] %(message)s')
    # Log file stream
    userPath = os.path.expanduser("~")
    module_dir = os.path.split(__file__)[0]
    config_location = os.path.join(module_dir, "cfg", "config.json")
    config = dict()
    with open(config_location) as fp:
        config = json.load(fp)
    finalDir = os.path.join(userPath, "." + config["logger_dir_name"])

    try:
        if not os.path.exists(finalDir):
            os.mkdir(finalDir)
    except OSError:
        pass

    today = date.today()
    date_string = today.strftime("%d-%m-%Y")
    log_file_path = os.path.join(finalDir, 'sync_{}.log'.format(date_string))
    fileHandler = logging.FileHandler(log_file_path, mode='a')
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
