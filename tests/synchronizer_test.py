# coding=utf-8
from __future__ import absolute_import, print_function

from synchronizer import synchronizer as sync

import pytest
import os

# --------------------------------------------------------
#  TESTING DATA
# --------------------------------------------------------
path_root = os.path.join(
            os.path.normcase(
            os.path.abspath(os.path.split(__file__)[0])),
            "data")
path_dir = os.path.join(path_root, "directory", "src_path")
path_single_file = os.path.join(path_dir, "C_cresta_02__MSH-BUMP.1001.png")
path_missing = os.path.join(path_root, "missingframes", "src_path")
path_sequence = os.path.join(path_root, "sequence", "src_path")
path_texture = os.path.join(path_root, "texture", "src_path")

data_root = pytest.mark.datafiles(path_root)
data_dir = pytest.mark.datafiles(path_dir)
data_single_file = pytest.mark.datafiles(path_single_file)
data_missing = pytest.mark.datafiles(path_missing)
data_sequence = pytest.mark.datafiles(path_sequence)
data_texture = pytest.mark.datafiles(path_texture)

# --------------------------------------------------------
#  TESTS
# --------------------------------------------------------

class TestClass:
    @data_single_file
    def test_get_sync_status(self, datafiles):
        src_path = str(datafiles)
        trg_path = str(datafiles)
        result = sync.get_sync_status(src_path, trg_path)
        assert 1 == result[0], "Sync status is not 1"

    def test_get_dir_size(self):
        pass