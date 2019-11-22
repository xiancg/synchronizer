# coding=utf-8
from __future__ import absolute_import, print_function

from synchronizer import synchronizer as sync

import pytest
import os

# --------------------------------------------------------
#  TESTING DATA
# --------------------------------------------------------
path_root = os.path.join(
            os.path.normcase(os.path.abspath(os.path.split(__file__)[0])),
            "data"
            )
path_dir = os.path.join(path_root, "directory", "src_path")
path_single_file = os.path.join(
                path_root, "singlefile",
                "src_path", "C_cresta_02__MSH-BUMP.1001.png"
                )
path_missing = os.path.join(path_root, "missingframes", "src_path")
path_sequence = os.path.join(path_root, "sequence", "src_path")
path_texture = os.path.join(path_root, "texture", "src_path")

data_root = pytest.mark.datafiles(path_root)
data_dir = pytest.mark.datafiles(path_dir)
data_single_file = pytest.mark.datafiles(path_single_file)
data_missing = pytest.mark.datafiles(path_missing)
data_sequence = pytest.mark.datafiles(path_sequence)
data_texture = pytest.mark.datafiles(path_texture)


class TestClass:
    @data_single_file
    def test_get_sync_status_files(self, datafiles):
        # Same file, ignoring last modification
        src_path = os.path.join(
            str(datafiles), "C_cresta_02__MSH-BUMP.1001.png"
            )
        trg_path = path_single_file
        result = sync.get_sync_status(
            src_path, trg_path,
            ignore_stats=[
                'st_uid', 'st_gid', 'st_atime',
                'st_ctime', 'st_mtime'
                ]
            )
        assert result is not None
        if result:
            assert result[0] == 1, "Sync status is not 1"
        # Different files, same name
        dif_trg_path = os.path.join(
                path_root, "singlefile",
                "dif_trg_path", "C_cresta_02__MSH-BUMP.1001.png"
                )
        result_dif = sync.get_sync_status(src_path, dif_trg_path)
        assert result_dif is not None
        if result_dif:
            assert result_dif[0] == 2, "Sync status is not 2"

    def get_sync_status_dirs(self):
        pass

    def test_get_dir_size(self):
        pass
