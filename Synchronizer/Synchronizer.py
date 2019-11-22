# coding=utf-8
from __future__ import absolute_import, print_function

import os
# import sys
# import shutil
# import time
# import filecmp

from synchronizer.logger import logger

# TODO: Configurar CI en GitLab


def get_sync_status(
        src_path, trg_path,
        ignore_file_name=False,
        ignore_stats=['st_uid', 'st_gid', 'st_atime', 'st_ctime']):
    """Compare two files or directory paths and return sync status.
    Sync status refers to name and os.stat() comparisons.

    Arguments:
        src_path {string} -- Source path, file or directory
        trg_path {string} -- Target path, file or directory

    Keyword Arguments:
        ignore_file_name {bool} -- Ignores file name comparison
            (default: {False})
        ignore_stats {list} -- Ignores this list of stats. Names correspond to
            what os.stats() returns, see Python docs.
            (default: {['st_uid', 'st_gid', 'st_atime', 'st_ctime']})

    Returns:
        tuple -- (Status code, Status description)
            1 = "In sync",
            2 = "Out of sync",
            3 = "Both paths missing",
            4 = "Source file missing",
            5 = "Target file missing",
            6 = "Different kind of paths (file-dir, dir-file)"
    """
    status_dict = {
            1: "In sync",
            2: "Out of sync",
            3: "Both paths missing",
            4: "Source file missing",
            5: "Target file missing",
            6: "Different kind of paths (file-dir, dir-file)"
            }
    src_path = os.path.normcase(os.path.abspath(src_path))
    trg_path = os.path.normcase(os.path.abspath(trg_path))
    logger_string = "\tSource: {}\n\tTarget: {}\n".format(
                src_path, trg_path
                )
    if os.path.exists(src_path) and os.path.exists(trg_path):
        if os.path.isfile(src_path) and os.path.isfile(trg_path):
            compare_files = compare_files_stat(
                src_path, trg_path, ignore_file_name, ignore_stats
                )
            result = True
            logger_string += "\tMatch comparison results:\n"
            for key, value in compare_files.iteritems():
                logger_string += "\t\t{}: {}\n".format(key, str(value))
                if not value:
                    # If any of the stats is different, status is Not in sync
                    result = False
            if result:
                logger.debug("Files in sync.\n{}".format(logger_string))
                return (1, status_dict[1])
            else:
                logger.debug("Files out of sync.\n{}".format(logger_string))
                return (2, status_dict[2])
        elif os.path.isdir(src_path) and os.path.isdir(trg_path):
            # ! Implement dir comparison functions
            pass
    elif not os.path.exists(src_path) and not os.path.exists(trg_path):
        logger.debug("Both given paths do not exist.\n{}".format(
            logger_string)
            )
        return (3, status_dict[3])
    elif not os.path.exists(src_path) and os.path.exists(trg_path):
        status = "Source path does not exist but target path does.\n"
        logger.debug(status + logger_string)
        return (4, status_dict[4])
    elif not os.path.exists(trg_path) and not os.path.exists(trg_path):
        status = "Source path does exist but target path doesn't.\n"
        logger.debug(status + logger_string)
        return (5, status_dict[5])
    elif os.path.isfile(src_path) and os.path.isdir(trg_path):
        logger.debug("Different kind of paths (file-dir)\n{}".format(
            logger_string)
            )
        return (6, status_dict[6])
    elif os.path.isdir(trg_path) and os.path.isfile(src_path):
        logger.debug("Different kind of paths (dir-file)\n{}".format(
            logger_string)
            )
        return (6, status_dict[6])
    else:
        logger.error("Sync status function failed.\n{}".format(
            logger_string)
            )
        return None


def compare_files_stat(
        src_path, trg_path,
        ignore_file_name=False,
        ignore_stats=['st_uid', 'st_gid', 'st_atime', 'st_ctime']):
    """Compares stats and file names for two given paths. Returns a
    dict with all comparison results.

    Arguments:
        src_path {string} -- Source path, file
        trg_path {string} -- Source path, file

    Keyword Arguments:
        ignore_file_name {bool} -- Ignores file name comparison
            (default: {False})
        ignore_stats {list} -- Ignores this list of stats. Names correspond to
            what os.stats() returns, see Python docs.
            (default: {['st_uid', 'st_gid', 'st_atime', 'st_ctime']})

    Returns:
        dict -- {Stat description: Comparison result bool}
    """
    src_stat = os.stat(src_path)
    trg_stat = os.stat(trg_path)
    stats_dict = {
        'st_mode': 'Protection bits',
        'st_ino': 'inode number',
        'st_dev': 'Device',
        'st_nlink': 'Number of hard links',
        'st_uid': 'User id of owner',
        'st_gid': 'Group id of owner',
        'st_size': 'File size',
        'st_atime': 'Most recent access',
        'st_mtime': 'Last modification',
        'st_ctime': 'Most recent metadata change'
    }
    result = dict()
    src_file_name = os.path.split(src_path)[1]
    trg_file_name = os.path.split(trg_path)[1]
    if src_file_name != trg_file_name and not ignore_file_name:
        result["File Name"] = False
    elif src_file_name == trg_file_name and not ignore_file_name:
        result["File Name"] = True

    for key, value in stats_dict.iteritems():
        if key not in ignore_stats:
            if eval("src_stat.{}".format(key)) != \
               eval("trg_stat.{}".format(key)):
                result[value] = False
            else:
                result[value] = True

    return result


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
