# coding=utf-8
from __future__ import absolute_import, print_function

import os
import datetime

import six

from synchronizer.logger import logger


status_dict = {
            1: "In sync",
            2: "Out of sync",
            3: "Both paths do not exist",
            4: "Source path does not exist",
            5: "Target path does not exist",
            6: "Different kind of paths (file-dir, dir-file)",
            7: "Source and Target are exactly the same path"
            }


def get_sync_status(
        src_path, trg_path,
        ignore_name=False,
        ignore_stats=['st_uid', 'st_gid', 'st_atime',
                      'st_ctime', 'st_ino', 'st_dev']):
    """Compare two files or directory paths and return sync status.
    Sync status refers to name and os.stat() comparisons.

    Arguments:
        src_path {string} -- Source path, file or directory
        trg_path {string} -- Target path, file or directory

    Keyword Arguments:
        ignore_name {bool} -- Ignores name comparison
            (default: {False})
        ignore_stats {list} -- Ignores this list of stats. Names correspond to
            what os.stat() returns.
            (default: {['st_uid', 'st_gid', 'st_atime', 'st_ctime'
                'st_ino', 'st_dev']})
            'st_mode': 'File type and file mode bits'
            'st_ino': 'inode or file index'
            'st_dev': 'Device'
            'st_nlink': 'Number of hard links'
            'st_uid': 'User id of owner'
            'st_gid': 'Group id of owner'
            'st_size': 'File size'
            'st_atime': 'Most recent access'
            'st_mtime': 'Last modification'
            'st_ctime': 'Most recent metadata change'

    Returns:
        tuple -- (Status code, Status description)
            1 = "In sync"
            2 = "Out of sync"
            3 = "Both paths do not exist"
            4 = "Source path does not exist"
            5 = "Target path does not exist"
            6 = "Different kind of paths (file-dir, dir-file)"
            7 = "Source and Target are the same"
        None -- Not implemented status comparison
    """
    src_path_norm = os.path.normcase(os.path.abspath(src_path))
    trg_path_norm = os.path.normcase(os.path.abspath(trg_path))
    logger_string = "\tSource: {}\n\tTarget: {}\n".format(
                src_path, trg_path
                )
    if os.path.exists(src_path) and os.path.exists(trg_path):
        same_kind = (os.path.isfile(src_path) and os.path.isfile(trg_path)) or\
                    (os.path.isdir(src_path) and os.path.isdir(trg_path))
        if same_kind:
            if src_path_norm == trg_path_norm:
                logger.debug("{}.\n{}".format(
                    status_dict[7], logger_string)
                    )
                return (7, status_dict[7])
            compare_items = compare_stats(
                    src_path, trg_path, ignore_name, ignore_stats
                )
            result = True
            logger_string += "\tMatch comparison results:\n"
            for key, value in six.iteritems(compare_items):
                logger_string += "\t\t{}: {}\n".format(key, str(value))
                if not value:
                    # If any of the stats is different, status is Not in sync
                    result = False
            if result:
                logger.debug("{}.\n{}".format(
                    status_dict[1], logger_string)
                    )
                return (1, status_dict[1])
            else:
                logger.debug("{}.\n{}".format(
                    status_dict[2], logger_string)
                    )
                return (2, status_dict[2])
        elif os.path.isfile(src_path) and os.path.isdir(trg_path):
            logger.debug("{}.\n{}".format(
                status_dict[6], logger_string)
                )
            return (6, status_dict[6])
        elif os.path.isdir(src_path) and os.path.isfile(trg_path):
            logger.debug("{}.\n{}".format(
                status_dict[6], logger_string)
                )
            return (6, status_dict[6])
        else:
            logger.error("Not implemented status comparison.\n{}".format(
                logger_string)
                )
            return None
    elif not os.path.exists(src_path) and not os.path.exists(trg_path):
        logger.debug("{}.\n{}".format(
            status_dict[3], logger_string)
            )
        return (3, status_dict[3])
    elif not os.path.exists(src_path) and os.path.exists(trg_path):
        logger.debug("{}.\n{}".format(
            status_dict[4], logger_string)
            )
        return (4, status_dict[4])
    elif not os.path.exists(trg_path) and not os.path.exists(trg_path):
        logger.debug("{}.\n{}".format(
            status_dict[5], logger_string)
            )
        return (5, status_dict[5])
    else:
        logger.error("Not implemented status comparison.\n{}".format(
            logger_string)
            )
        return None


def compare_stats(
        src_path, trg_path,
        ignore_name=False,
        ignore_stats=['st_uid', 'st_gid', 'st_atime',
                      'st_ctime', 'st_ino', 'st_dev']):
    """Compares stats and file names for two given paths. Returns a
    dict with all comparison results.

    Arguments:
        src_path {string} -- Source path, file or directory
        trg_path {string} -- Target path, file or directory

    Keyword Arguments:
        ignore_name {bool} -- Ignores name comparison
            (default: {False})
        ignore_stats {list} -- Ignores this list of stats. Names correspond to
            what os.stat() returns.
            (default: {['st_uid', 'st_gid', 'st_atime', 'st_ctime'
                'st_ino', 'st_dev']})
            'st_mode': 'File type and file mode bits'
            'st_ino': 'inode or file index'
            'st_dev': 'Device'
            'st_nlink': 'Number of hard links'
            'st_uid': 'User id of owner'
            'st_gid': 'Group id of owner'
            'st_size': 'File size'
            'st_atime': 'Most recent access'
            'st_mtime': 'Last modification'
            'st_ctime': 'Most recent metadata change'

    Returns:
        dict -- {Stat description: Comparison result bool}
    """
    src_stat = os.stat(src_path)  # noqa: F841
    trg_stat = os.stat(trg_path)  # noqa: F841
    stats_dict = {
        'st_mode': 'File type and file mode bits',
        'st_ino': 'inode or file index',
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
    if src_file_name != trg_file_name and not ignore_name:
        result["Name"] = False
    elif src_file_name == trg_file_name and not ignore_name:
        result["Name"] = True
    for key, value in six.iteritems(stats_dict):
        if key not in ignore_stats:
            if eval("src_stat.{}".format(key)) != \
               eval("trg_stat.{}".format(key)):
                result[value] = False
            else:
                result[value] = True

    if os.path.isdir(src_path) and os.path.isdir(trg_path):
        src_dir_size = get_dir_size(src_path)
        trg_dir_size = get_dir_size(trg_path)
        result['Dir size'] = False
        if src_dir_size == trg_dir_size:
            result['Dir size'] = True

    return result


def get_most_recent(src_path, trg_path, use_stat='st_mtime'):
    """Compares two paths and returns whichever has the most recent stat time.
    Default stat used for comparison is st_mtime which is: Time of most recent
    content modification.

    Arguments:
        src_path {string} -- Source path, file or directory
        trg_path {string} -- Target path, file or directory

    Keyword Arguments:
        use_stat {string} -- Stat used for comparison (default: {'st_mtime'})
            Valid options:
                'st_mtime': Time of most recent content modification
                'st_atime': Time of most recent access
                'st_ctime': Time of creation on Windows, time of most recent
                    metadata change on Unix

    Returns:
        [string] -- Path of whichever has the most recent stat time.
        None if both path stats are equal or an invalid stat options is passed.
    """
    valid_stats = ['st_mtime', 'st_atime', 'st_ctime']

    logger_string = "\tSource: {}\n\tTarget: {}\n".format(
        src_path, trg_path
        )
    if use_stat in valid_stats:
        src_stat = os.stat(src_path)  # noqa: F841
        trg_stat = os.stat(trg_path)  # noqa: F841

        src_most = eval("src_stat.{}".format(use_stat))
        trg_most = eval("trg_stat.{}".format(use_stat))
        if trg_most > src_most:
            return trg_path
        elif trg_most < src_most:
            return src_path
        else:
            readable_time = datetime.datetime.fromtimestamp(src_most)
            logger.debug(
                "Both src_path and trg_path have equal {}: {}\n".format(
                    use_stat, readable_time, logger_string)
                )
            return None

    valid_stats_str = ", ".join(valid_stats)
    logger.debug(
        "use_stat= {} is invalid. Valid options: {}\n".format(
            use_stat, valid_stats_str)
        )
    return None


def get_dir_size(dir_path):
    """Walks thru given directory to calculate total size.

    Arguments:
        dir_path {string} -- Directory to measure size.

    Returns:
        int -- Size of directory in bytes, as reported by the sum
        of all its files os.stat()
        None -- If dir_path is not a directory, returns None
    """
    if os.path.isdir(dir_path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(dir_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size
    return None
