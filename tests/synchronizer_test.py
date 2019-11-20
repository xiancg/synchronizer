# coding=utf-8
from __future__ import absolute_import, print_function

from synchronizer import synchronizer

import pytest
import os


@pytest.fixture
def sync():
    return synchronizer.Synchronizer()

class TestClass:
    def test_get_sync_status(self, sync):
        src_path = "C:/Users/RTX 2070 - 3TB - NXA/Desktop/MediaLibrary.png"
        trg_path = "C:/Users/RTX 2070 - 3TB - NXA/Desktop/MediaLibrary.png"
        result = sync.get_sync_status(src_path, trg_path)
        assert 1 == result, "Sync status is not 1"

    def test_get_dir_size(self, sync):
        pass
