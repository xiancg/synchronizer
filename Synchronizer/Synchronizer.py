# coding=utf-8
from __future__ import absolute_import, print_function

import os
import sys
import shutil

from synchronizer.logger import logger

class Synchronizer(object):
    def __init__(self):
        print("Synchronizer created.")
    
    def get_sync_status(self, src_path, trg_path):
        return 1

# --------------------------------------------------------
#  Main
# --------------------------------------------------------
def main():
    pass

if __name__ == "__main__" or 'eclipsePython' in __name__:
    main()