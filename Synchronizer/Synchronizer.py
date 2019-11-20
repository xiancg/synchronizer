# coding=utf-8
from __future__ import absolute_import, print_function

import os
import sys
import shutil
import time

from synchronizer.logger import logger

# TODO: Revisar flake
# TODO: Terminar de implementar el primer test
# TODO: Configurar CI en GitLab

status_dict = {
            1: "In sync",
            2: "Out of sync",
            3: "Same date, different size",
            4: "Different date, same size",
            5: "Both paths missing",
            6: "Source file missing",
            7: "Target file missing",
            8: "Different kind of paths (file-dir, dir-file)"
            }


def get_sync_status(src_path, trg_path):
    if os.path.exists(src_path) and os.path.exists(trg_path):
        srcTime = time.ctime(os.path.getmtime(src_path))
        trgTime = time.ctime(os.path.getmtime(trg_path))
        srcSize = os.path.getsize(src_path)
        trgSize = os.path.getsize(trg_path)
        if os.path.isdir(src_path) and os.path.isdir(trg_path):
            srcSize = get_dir_size(src_path)
            trgSize = get_dir_size(trg_path)
        # In sync
        if srcTime == trgTime and srcSize == trgSize:
            return (1, status_dict[1])
        # Out of sync
        elif srcTime != trgTime and srcSize != trgSize:
            return (2, status_dict[2])
        # Same date, different size
        elif srcTime == trgTime and srcSize != trgSize:
            return (3, status_dict[3])
        # Different date, same size
        elif srcTime != trgTime and srcSize == trgSize:
            return (4, status_dict[4])
    # Both paths missing
    elif not os.path.exists(src_path) and not os.path.exists(trg_path):
        return (5, status_dict[5])
    # Source path missing
    elif not os.path.exists(src_path):
        return (6, status_dict[6])
    # Target path missing
    elif not os.path.exists(trg_path):
        return (7, status_dict[7])
    # Different kind of paths (file-dir)
    elif os.path.isfile(src_path) and os.path.isdir(trg_path):
        return (8, status_dict[8])
    # Different kind of paths (dir-file)
    elif os.path.isdir(trg_path) and os.path.isfile(src_path):
        return (8, status_dict[8])
    # Fail
    else:
        return None


def get_dir_size(path):
    if os.path.isdir(path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size
    else:
        return None