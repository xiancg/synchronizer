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
                    os.path.abspath(os.path.split(__file__)[0])
                ),
                "data"
            )
trg_path_dir = os.path.join(path_root, "trg_path")
path_dir = os.path.join(path_root, "directory", "src_path")
path_single_file = os.path.join(
                    path_root, "singlefile",
                    "src_path", "C_cresta_02__MSH-BUMP.1001.png"
                )
path_missing = os.path.join(
        path_root, "missingframes", "src_path",
        "C_cresta_02__MSH-BUMP.1001.png"
    )
path_sequence = os.path.join(
        path_root, "sequence", "src_path",
        "C_cresta_02__MSH-BUMP.1001.png"
    )
path_sequence_tx = os.path.join(
        path_root, "sequence_with_tx", "src_path",
        "C_cresta_02__MSH-BUMP.1001.png"
    )
path_texture = os.path.join(
                path_root,
                "texture", "src_path",
                "C_cresta_02__MSH-BUMP.1001.png")

data_dir = pytest.mark.datafiles(path_dir)
trg_dir = pytest.mark.datafiles(trg_path_dir)
data_single_file = pytest.mark.datafiles(path_single_file)


class Test_SyncStatus:
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

    @data_dir
    def test_get_sync_status_dirs(self, datafiles):
        # Same dir, ignoring last modification
        src_path = str(datafiles)
        trg_path = path_dir
        result = sync.get_sync_status(
            src_path, trg_path,
            ignore_name=True,
            ignore_stats=[
                'st_uid', 'st_gid', 'st_atime',
                'st_ctime', 'st_mtime'
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
        result_dif = sync.get_sync_status(
            src_path, dif_trg_path,
            ignore_name=True,
            ignore_stats=[
                'st_uid', 'st_gid', 'st_atime',
                'st_ctime', 'st_mtime'
                ]
            )
        assert result_dif is not None
        if result_dif:
            assert result_dif[0] == 2, "Sync status is not 2"


class Test_ProcessPaths:
    def test_process_dir(self, datafiles):
        src_path = path_dir
        trg_path = str(datafiles)
        success = sync.process_paths(src_path, trg_path, True)
        assert success == 1, "Failed to process paths"
        for each in os.listdir(src_path):
            src_file_path = os.path.join(src_path, each)
            trg_file_path = os.path.join(trg_path, each)
            assert os.path.exists(trg_file_path) == 1
            status = sync.get_sync_status(
                    src_file_path, trg_file_path,
                    ignore_stats=['st_uid', 'st_gid', 'st_atime',
                                  'st_ctime', 'st_mtime']
                )
            assert status[0] == 1, "Files are not in sync"

    @trg_dir
    def test_process_file(self, datafiles):
        src_path = path_single_file
        trg_path = str(datafiles)
        trg_file_path = os.path.join(trg_path, "C_cresta_02__MSH-BUMP.1001.png")
        success = sync.process_paths(src_path, trg_path)
        assert success == 1, "Failed to process paths"
        status = sync.get_sync_status(
                    src_path, trg_file_path,
                    ignore_stats=['st_uid', 'st_gid', 'st_atime',
                                  'st_ctime', 'st_mtime']
                )
        assert status[0] == 1, "File is not in sync"

    @trg_dir
    def test_process_texture_only(self, datafiles):
        src_path = os.path.join(path_texture)
        trg_path = str(datafiles)
        trg_file_path = os.path.join(trg_path, "C_cresta_02__MSH-BUMP.1001.png")
        tx_file_path = os.path.join(trg_path, "C_cresta_02__MSH-BUMP.1001.tx")
        success = sync.process_paths(src_path, trg_path, include_tx=False)
        assert success == 1, "Failed to process paths"
        status = sync.get_sync_status(
                    src_path, trg_file_path,
                    ignore_stats=['st_uid', 'st_gid', 'st_atime',
                                  'st_ctime', 'st_mtime']
                )
        assert status[0] == 1, "File is not in sync"
        assert os.path.exists(tx_file_path) == 0, "tx copied, but it shouldn't have been."

    @trg_dir
    def test_process_texture_with_tx(self, datafiles):
        src_path = os.path.join(path_texture)
        src_tx_path = src_path.rsplit(".", 1)[0] + ".tx"
        trg_path = str(datafiles)
        trg_file_path = os.path.join(trg_path, "C_cresta_02__MSH-BUMP.1001.png")
        tx_file_path = os.path.join(trg_path, "C_cresta_02__MSH-BUMP.1001.tx")
        success = sync.process_paths(src_path, trg_path, include_tx=True)
        assert success == 1, "Failed to process paths"
        status = sync.get_sync_status(
                    src_path, trg_file_path,
                    ignore_stats=['st_uid', 'st_gid', 'st_atime',
                                  'st_ctime', 'st_mtime']
                )
        assert status[0] == 1, "File is not in sync"
        status = sync.get_sync_status(
                    src_tx_path, tx_file_path,
                    ignore_stats=['st_uid', 'st_gid', 'st_atime',
                                  'st_ctime', 'st_mtime']
                )
        assert status[0] == 1, "File is not in sync"

    @trg_dir
    def test_process_tx_only(self, datafiles):
        src_path = os.path.join(path_texture)
        src_tx_path = src_path.rsplit(".", 1)[0] + ".tx"
        trg_path = str(datafiles)
        tx_file_path = os.path.join(trg_path, "C_cresta_02__MSH-BUMP.1001.tx")
        success = sync.process_paths(
                src_path, trg_path,
                include_tx=True, only_tx=True
            )
        assert success == 1, "Failed to process paths"
        status = sync.get_sync_status(
                    src_tx_path, tx_file_path,
                    ignore_stats=['st_uid', 'st_gid', 'st_atime',
                                  'st_ctime', 'st_mtime']
                )
        assert status[0] == 1, "File is not in sync"

    @trg_dir
    def test_sequence(self, datafiles):
        src_path = path_sequence
        trg_path = str(datafiles)
        success = sync.process_paths(src_path, trg_path)
        assert success == 1, "Failed to process paths"
        files_copied = os.listdir(trg_path)
        assert len(files_copied) == 5, "Sequence didn't copy correctly"

    @trg_dir
    def test_sequence_with_missing_frames(self, datafiles):
        src_path = path_missing
        trg_path = str(datafiles)
        success = sync.process_paths(src_path, trg_path)
        assert success == 1, "Failed to process paths"
        files_copied = os.listdir(trg_path)
        assert len(files_copied) == 8, "Sequence didn't copy correctly"

    @trg_dir
    def test_sequence_with_tx(self, datafiles):
        src_path = path_sequence_tx
        trg_path = str(datafiles)
        success = sync.process_paths(src_path, trg_path, include_tx=True)
        assert success == 1, "Failed to process paths"
        files_copied = os.listdir(trg_path)
        assert len(files_copied) == 10, "Sequence didn't copy correctly"
