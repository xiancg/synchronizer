# coding=utf-8
'''
Library to copy and compare files and directories.
Created on Mar 25, 2015
@author: Chris Granados - Xian chris.granados@xiancg.com http://www.chrisgranados.com/
'''
from __future__ import absolute_import, print_function

import os
import sys
import shutil
import time
from datetime import date
import logging

logger = logging.getLogger(name='synclog')

def init_logger():
    logger.setLevel(logging.DEBUG)
    #Formatter
    formatter = logging.Formatter(
                '[%(asctime)s:%(module)s:%(funcName)s:%(lineno)s:%(levelname)s] %(message)s')
    #STDOUT stream
    streamHandler = logging.StreamHandler(sys.stdout)
    streamHandler.setLevel(logging.DEBUG)
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)

def init_file_logger():
    #Formatter
    formatter = logging.Formatter(
                '[%(asctime)s:%(module)s:%(funcName)s:%(lineno)s:%(levelname)s] %(message)s')
    #Log file stream
    userPath = os.path.expanduser("~")
    finalDir = os.path.join(userPath, ".Synchronizer")
    try:
        if not os.path.exists(finalDir):
            os.mkdir(finalDir)
    except:
        pass
    today = date.today()
    date_string = today.strftime("%d-%m-%Y")
    log_file_path = os.path.join(finalDir, 'Synchronizer_{}.log'.format(date_string))
    fileHandler = logging.FileHandler(log_file_path, mode='a')
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

class Synchronizer(object):
    pass

# * Sync session events
init_logger()

# -------------------------
# Main
# -------------------------
def main():
    pass

if __name__ == "__main__":
    main()