# coding=utf-8
from __future__ import absolute_import, print_function

from Synchronizer import Synchronizer

import unittest
import os


class SynchronizerTest(unittest.TestCase):
    def setUp(self):
        self.sync = Synchronizer()

    def test_get_sync_status(self):
        src_path = ""
        trg_path = ""
        result = self.sync.get_sync_status(src_path, trg_path)
        self.assertEqual(1, result)

    def test_get_dir_size(self):
        pass

# --------------------------------------------------------
#  Main
# --------------------------------------------------------
if __name__ == "__main__" or 'eclipsePython' in __name__:
    unittest.main()
