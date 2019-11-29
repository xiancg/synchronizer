# coding=utf-8
from __future__ import absolute_import, print_function

from synchronizer import utils, logger

import os
import shutil

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


class Test_Utils:
    def test_seq_digits_not_found(self):
        file_path = os.path.join(
                path_root, "singlefile",
                "no_pattern", "C_cresta_01__MSH-BUMP.png"
            )
        result = utils.get_sequence_files(file_path)
        assert result is None
        result = utils.is_sequence(file_path)
        assert result is False
        result = utils.get_sequence_name_pattern(file_path)
        assert result is None

    def test_create_dirs(self):
        dir_path = os.path.join(path_root, "TEMP_DIR_DELETE")
        result = utils.create_dir(dir_path)
        assert result is True
        assert os.path.exists(dir_path) is True
        shutil.rmtree(dir_path)
        assert os.path.exists(dir_path) is False

    def test_create_dir_fails(self):
        dir_path = ""
        result = utils.create_dir(dir_path)
        assert result is False
