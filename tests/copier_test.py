# coding=utf-8
from __future__ import absolute_import, print_function

from synchronizer import copier, syncstatus, logger

import os
import shutil
import pytest

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
# Fixtures
data_dir = pytest.mark.datafiles(path_dir)
trg_dir = pytest.mark.datafiles(trg_path_dir)
data_single_file = pytest.mark.datafiles(path_single_file)


class Test_ProcessPaths:
    def test_process_dir(self, datafiles):
        src_path = path_dir
        trg_path = str(datafiles)
        success = copier.process_paths(src_path, trg_path, True)
        assert success is True, "Failed to process paths"
        for each in os.listdir(src_path):
            src_file_path = os.path.join(src_path, each)
            trg_file_path = os.path.join(trg_path, each)
            assert os.path.exists(trg_file_path) is True
            status = syncstatus.get_sync_status(
                    src_file_path, trg_file_path,
                    ignore_stats=['st_uid', 'st_gid', 'st_atime',
                                  'st_ctime', 'st_mtime',
                                  'st_ino', 'st_dev']
                )
            assert status[0] == 1, "Files are not in sync"

    @trg_dir
    def test_process_file(self, datafiles):
        src_path = path_single_file
        trg_path = str(datafiles)
        trg_file_path = os.path.join(
            trg_path, "C_cresta_02__MSH-BUMP.1001.png"
        )
        success = copier.process_paths(src_path, trg_path)
        assert success is True, "Failed to process paths"
        status = syncstatus.get_sync_status(
                    src_path, trg_file_path,
                    ignore_stats=['st_uid', 'st_gid', 'st_atime',
                                  'st_ctime', 'st_mtime',
                                  'st_ino', 'st_dev']
                )
        assert status[0] == 1, "File is not in sync"

    @trg_dir
    def test_process_texture_only(self, datafiles):
        src_path = os.path.join(path_texture)
        trg_path = str(datafiles)
        trg_file_path = os.path.join(
            trg_path, "C_cresta_02__MSH-BUMP.1001.png"
        )
        tx_file_path = os.path.join(trg_path, "C_cresta_02__MSH-BUMP.1001.tx")
        success = copier.process_paths(src_path, trg_path, include_tx=False)
        assert success is True, "Failed to process paths"
        status = syncstatus.get_sync_status(
                    src_path, trg_file_path,
                    ignore_stats=['st_uid', 'st_gid', 'st_atime',
                                  'st_ctime', 'st_mtime',
                                  'st_ino', 'st_dev']
                )
        assert status[0] == 1, "File is not in sync"
        tx_file_exists = os.path.exists(tx_file_path)
        assert tx_file_exists is False, "tx shouldn't have been copied."

    @trg_dir
    def test_process_texture_with_tx(self, datafiles):
        src_path = os.path.join(path_texture)
        src_tx_path = src_path.rsplit(".", 1)[0] + ".tx"
        trg_path = str(datafiles)
        trg_file_path = os.path.join(
            trg_path, "C_cresta_02__MSH-BUMP.1001.png"
        )
        tx_file_path = os.path.join(trg_path, "C_cresta_02__MSH-BUMP.1001.tx")
        success = copier.process_paths(src_path, trg_path, include_tx=True)
        assert success is True, "Failed to process paths"
        status = syncstatus.get_sync_status(
                    src_path, trg_file_path,
                    ignore_stats=['st_uid', 'st_gid', 'st_atime',
                                  'st_ctime', 'st_mtime',
                                  'st_ino', 'st_dev']
                )
        assert status[0] == 1, "File is not in sync"
        status = syncstatus.get_sync_status(
                    src_tx_path, tx_file_path,
                    ignore_stats=['st_uid', 'st_gid', 'st_atime',
                                  'st_ctime', 'st_mtime',
                                  'st_ino', 'st_dev']
                )
        assert status[0] == 1, "File is not in sync"

    @trg_dir
    def test_process_tx_only(self, datafiles):
        src_path = os.path.join(path_texture)
        src_tx_path = src_path.rsplit(".", 1)[0] + ".tx"
        trg_path = str(datafiles)
        tx_file_path = os.path.join(trg_path, "C_cresta_02__MSH-BUMP.1001.tx")
        success = copier.process_paths(
                src_path, trg_path,
                include_tx=True, only_tx=True
            )
        assert success is True, "Failed to process paths"
        status = syncstatus.get_sync_status(
                    src_tx_path, tx_file_path,
                    ignore_stats=['st_uid', 'st_gid', 'st_atime',
                                  'st_ctime', 'st_mtime',
                                  'st_ino', 'st_dev']
                )
        assert status[0] == 1, "File is not in sync"

    @trg_dir
    def test_sequence(self, datafiles):
        src_path = path_sequence
        trg_path = str(datafiles)
        success = copier.process_paths(src_path, trg_path)
        assert success is True, "Failed to process paths"
        files_copied = os.listdir(trg_path)
        assert len(files_copied) == 5, "Sequence didn't copy correctly"

    @trg_dir
    def test_sequence_with_missing_frames(self, datafiles):
        src_path = path_missing
        trg_path = str(datafiles)
        success = copier.process_paths(src_path, trg_path)
        assert success is True, "Failed to process paths"
        files_copied = os.listdir(trg_path)
        assert len(files_copied) == 8, "Sequence didn't copy correctly"

    @trg_dir
    def test_sequence_with_tx(self, datafiles):
        src_path = path_sequence_tx
        trg_path = str(datafiles)
        success = copier.process_paths(src_path, trg_path, include_tx=True)
        assert success is True, "Failed to process paths"
        files_copied = os.listdir(trg_path)
        assert len(files_copied) == 10, "Sequence didn't copy correctly"

    def test_src_trg_equal(self):
        src_path = path_dir
        trg_path = path_dir
        result = copier.process_paths(src_path, trg_path)
        assert result is False

    def test_src_missing(self):
        src_path = os.path.join(path_dir, "doesnotexist.jpg")
        trg_path = path_dir
        result = copier.process_paths(src_path, trg_path)
        assert result is False

    def test_trg_is_not_dir(self):
        src_path = path_dir
        trg_path = path_single_file
        result = copier.process_paths(src_path, trg_path)
        assert result is False


class Test_ProcessDirs:
    def test_trg_not_existing(self):
        src_path = path_dir
        trg_path = os.path.join(path_root, "TEMP_DIR_DELETE")
        result = copier._process_dirs(
                src_path, trg_path, force_overwrite=True
            )
        assert result is True
        assert os.path.exists(trg_path) is True
        shutil.rmtree(trg_path)
        assert os.path.exists(trg_path) is False

    def test_trg_exists_overwrite_false(self):
        src_path = path_dir
        trg_path = os.path.join(path_root, "TEMP_DIR_DELETE")
        os.mkdir(trg_path)
        result = copier._process_dirs(
                src_path, trg_path, force_overwrite=False
            )
        assert result is True
        shutil.rmtree(trg_path)
        assert os.path.exists(trg_path) is False

    def test_exception(self):
        src_path = os.path.join(path_root, "doesnotexist")
        trg_path = os.path.join(path_root, "TEMP_DIR_DELETE")
        result = copier._process_dirs(
                src_path, trg_path, force_overwrite=True
            )
        assert result is False


class Test_ProcessFiles:
    def test_origfile_exists_overwrite_false(self):
        src_path = path_single_file
        trg_path = os.path.join(
                path_root, "singlefile", "src_path"
            )
        result = copier._process_original_files(
                src_path, trg_path, force_overwrite=False
            )
        assert result is True

    @trg_dir
    def test_missing_include_tx_sequence(self, datafiles):
        src_path = path_sequence
        trg_path = str(datafiles)
        result = copier._process_files(
            src_path, trg_path, force_overwrite=False,
            only_tx=True, include_tx=False
            )
        assert result is True

    @trg_dir
    def test_missing_include_tx_file(self, datafiles):
        src_path = path_single_file
        trg_path = str(datafiles)
        result = copier._process_files(
            src_path, trg_path, force_overwrite=False,
            only_tx=True, include_tx=False
            )
        assert result is True

    def test_txfile_exists_overwrite_false(self):
        src_path = path_texture
        trg_path = os.path.join(
                path_root, "texture", "src_path"
            )
        result = copier._process_tx(
                src_path, trg_path, force_overwrite=False
            )
        assert result is True

    def test_txfile_not_existing(self):
        src_path = path_single_file
        trg_path = os.path.join(
                path_root, "texture", "src_path"
            )
        result = copier._process_tx(
                src_path, trg_path, force_overwrite=False
            )
        assert result is False
