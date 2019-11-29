# coding=utf-8
from __future__ import absolute_import, print_function

from synchronizer import syncstatus, logger

import pytest
import os

# Empty directory to use for testing
try:
    trg_empty_dir = os.path.join(
            os.path.split(__file__)[0], "data", "trg_path"
        )
    if not os.path.exists(trg_empty_dir):
        os.mkdir(trg_empty_dir)
except (IOError, OSError) as why:
    raise why

# Debug logging
logger.init_logger()
# logger.init_file_logger()


# --------------------------------------------------------
#  TESTING DATA
# --------------------------------------------------------
path_root = os.path.join(
                os.path.normcase(
                    os.path.abspath(os.path.split(__file__)[0])
                ),
                "data"
            )
path_dir = os.path.join(path_root, "directory", "src_path")
path_single_file = os.path.join(
                    path_root, "singlefile",
                    "src_path", "C_cresta_02__MSH-BUMP.1001.png"
                )
# Fixtures
data_dir = pytest.mark.datafiles(path_dir)
data_single_file = pytest.mark.datafiles(path_single_file)


class Test_SyncStatus:
    @data_single_file
    def test_get_sync_status_files(self, datafiles):
        # Same file, ignoring last modification
        src_path = os.path.join(
            str(datafiles), "C_cresta_02__MSH-BUMP.1001.png"
            )
        trg_path = path_single_file
        result = syncstatus.get_sync_status(
            src_path, trg_path,
            ignore_stats=[
                'st_uid', 'st_gid', 'st_atime',
                'st_ctime', 'st_mtime', 'st_ino', 'st_dev'
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
        result_dif = syncstatus.get_sync_status(src_path, dif_trg_path)
        assert result_dif is not None
        if result_dif:
            assert result_dif[0] == 2, "Sync status is not 2"

    @data_dir
    def test_get_sync_status_dirs(self, datafiles):
        # Same dir, ignoring last modification
        src_path = str(datafiles)
        trg_path = path_dir
        result = syncstatus.get_sync_status(
            src_path, trg_path,
            ignore_name=True,
            ignore_stats=[
                'st_uid', 'st_gid', 'st_atime',
                'st_ctime', 'st_mtime', 'st_ino', 'st_dev'
                ]
            )
        assert result is not None
        if result:
            assert result[0] == 1, "Sync status is not 1"
        # Same dir, one file is different
        src_path = path_dir
        dif_trg_path = os.path.join(
                path_root, "directory", "dif_trg_path"
                )
        result_dif = syncstatus.get_sync_status(
            src_path, dif_trg_path,
            ignore_name=True,
            ignore_stats=[
                'st_uid', 'st_gid', 'st_atime',
                'st_ctime', 'st_mtime', 'st_ino', 'st_dev'
                ]
            )
        assert result_dif is not None
        if result_dif:
            assert result_dif[0] == 2, "Sync status is not 2"

    def test_both_paths_missing(self):
        src_path = os.path.join(path_root, "doesnotexist")
        trg_path = os.path.join(path_root, "doesnotexist2")
        result = syncstatus.get_sync_status(
            src_path, trg_path, ignore_name=True
            )
        assert result[0] == 3

    def test_src_path_missing(self):
        src_path = os.path.join(path_root, "doesnotexist")
        trg_path = path_root
        result = syncstatus.get_sync_status(
            src_path, trg_path, ignore_name=True
            )
        assert result[0] == 4

    def test_trg_path_missing(self):
        src_path = path_root
        trg_path = os.path.join(path_root, "doesnotexist")
        result = syncstatus.get_sync_status(
            src_path, trg_path, ignore_name=True
            )
        assert result[0] == 5

    def test_diff_path_kinds_src_is_file(self):
        src_path = path_single_file
        trg_path = path_root
        result = syncstatus.get_sync_status(
            src_path, trg_path, ignore_name=True
            )
        assert result[0] == 6

    def test_diff_path_kinds_trg_is_file(self):
        src_path = path_root
        trg_path = path_single_file
        result = syncstatus.get_sync_status(
            src_path, trg_path, ignore_name=True
            )
        assert result[0] == 6

    def test_src_trg_equal(self):
        src_path = path_single_file
        trg_path = path_single_file
        result = syncstatus.get_sync_status(
            src_path, trg_path, ignore_name=True
            )
        assert result[0] == 7

    def test_different_name(self):
        src_path = path_single_file
        trg_path = os.path.join(
                path_root, "sequence", "src_path",
                "C_cresta_01__MSH-BUMP.1001.png"
            )
        result = syncstatus.compare_stats(
            src_path, trg_path, ignore_name=False
            )
        assert result["Name"] is False

    def test_get_dir_size_not_dir(self):
        dir_path = path_single_file
        result = syncstatus.get_dir_size(dir_path)
        assert result is None

    @data_single_file
    def test_get_most_recent(self, datafiles):
        src_path = path_single_file
        trg_path = str(datafiles)
        result = syncstatus.get_most_recent(src_path, trg_path)
        assert result == trg_path

    def test_get_most_recent_equal(self):
        src_path = path_single_file
        trg_path = path_single_file
        result = syncstatus.get_most_recent(src_path, trg_path)
        assert result is None

    def test_invalid_stat(self):
        src_path = path_single_file
        result = syncstatus.get_most_recent(src_path, src_path, 'st_size')
        assert result is None
