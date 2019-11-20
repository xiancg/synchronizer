# coding=utf-8
from __future__ import absolute_import, print_function

from synchronizer import synchronizer as sync

import pytest
import os

# --------------------------------------------------------
#  TESTING DATA
# --------------------------------------------------------
data_root = os.path.join(os.path.split(__file__)[0], "data")
data_dir = os.path.join(data_root, "directory", "src_path")
data_single_file = os.path.join(data_dir, "C_cresta_02__MSH-BUMP.1001.png")
data_missing = os.path.join(data_root, "missingframes", "src_path")
data_sequence = os.path.join(data_root, "sequence", "src_path")
data_texture = os.path.join(data_root, "texture", "src_path")

# --------------------------------------------------------
#  TESTS
# --------------------------------------------------------

class TestClass:
    def test_get_sync_status(self):
        src_path = data_single_file
        trg_path = data_single_file
        result = sync.get_sync_status(src_path, trg_path)
        assert 1 == result, "Sync status is not 1"

    def test_get_dir_size(self):
        pass