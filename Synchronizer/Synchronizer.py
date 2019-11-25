# coding=utf-8
from __future__ import absolute_import, print_function

import os
import shutil

from synchronizer.logger import logger

# TODO: argparse?
# TODO: Configurar CI en GitLab


def get_sync_status(
        src_path, trg_path,
        ignore_name=False,
        ignore_stats=['st_uid', 'st_gid', 'st_atime', 'st_ctime']):
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
            (default: {['st_uid', 'st_gid', 'st_atime', 'st_ctime']})
            'st_mode': 'Protection bits'
            'st_ino': 'inode number'
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
            1 = "In sync",
            2 = "Out of sync",
            3 = "Both paths missing",
            4 = "Source file missing",
            5 = "Target file missing",
            6 = "Different kind of paths (file-dir, dir-file)"
        None -- Not implemented status comparison
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
        same_kind = (os.path.isfile(src_path) and os.path.isfile(trg_path)) or\
                    (os.path.isdir(src_path) and os.path.isdir(trg_path))
        if same_kind:
            what_kind = "Files"
            if os.path.isdir(src_path) and os.path.isdir(trg_path):
                what_kind = "Directories"
            compare_items = compare_stats(
                    src_path, trg_path, ignore_name, ignore_stats
                )
            result = True
            logger_string += "\tMatch comparison results:\n"
            for key, value in compare_items.iteritems():
                logger_string += "\t\t{}: {}\n".format(key, str(value))
                if not value:
                    # If any of the stats is different, status is Not in sync
                    result = False
            if result:
                logger.debug("{} in sync.\n{}".format(
                    what_kind, logger_string)
                    )
                return (1, status_dict[1])
            else:
                logger.debug("{} out of sync.\n{}".format(
                    what_kind, logger_string)
                    )
                return (2, status_dict[2])
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
        status = "Source path exists but target path doesn't.\n"
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
        logger.error("Not implemented status comparison.\n{}".format(
            logger_string)
            )
        return None


def compare_stats(
        src_path, trg_path,
        ignore_name=False,
        ignore_stats=['st_uid', 'st_gid', 'st_atime', 'st_ctime']):
    """Compares stats and file names for two given paths. Returns a
    dict with all comparison results.

    Arguments:
        src_path {string} -- Source path, file or dir
        trg_path {string} -- Source path, file or dir

    Keyword Arguments:
        ignore_name {bool} -- Ignores name comparison
            (default: {False})
        ignore_stats {list} -- Ignores this list of stats. Names correspond to
            what os.stats() returns, see Python docs.
            (default: {['st_uid', 'st_gid', 'st_atime', 'st_ctime']})

    Returns:
        dict -- {Stat description: Comparison result bool}
    """
    src_stat = os.stat(src_path)  # noqa: F841
    trg_stat = os.stat(trg_path)  # noqa: F841
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
    if src_file_name != trg_file_name and not ignore_name:
        result["Name"] = False
    elif src_file_name == trg_file_name and not ignore_name:
        result["Name"] = True

    for key, value in stats_dict.iteritems():
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


def process_paths(src_path, trg_path, force_overwrite=True, **kwargs):
    src_path = os.path.normcase(os.path.abspath(src_path))
    trg_path = os.path.normcase(os.path.abspath(trg_path))
    logger_string = "\tSource: {}\n\tTarget: {}\n".format(
                src_path, trg_path
                )
    src_is_dir = False
    if os.path.isdir(src_path):
        src_is_dir = True

    success = False
    # Sanity checks
    if src_path == trg_path:
        logger.debug(
            "Skipped: Source and target are the same.\n{}".format(
                logger_string)
            )
        success = False
    elif not os.path.exists(src_path):
        logger.debug(
            "Skipped: Source path doesn't exist.\n{}".format(
                logger_string)
            )
        success = False
    elif src_is_dir:
        success = _process_dirs(src_path, trg_path, force_overwrite)
    else:
        success = _process_files(src_path, trg_path, force_overwrite, **kwargs)
    return success


def get_sequence_files(file_path):
    file_path = os.path.realpath(os.path.normcase(file_path))
    path_parts = os.path.split(file_path)
    parent_folder = path_parts[0]
    file_with_ext = path_parts[1]
    file_name, file_ext = file_with_ext.rsplit(".", 1)

    if is_sequence(file_path):
        name_pattern, hash_str = get_sequence_name_pattern(file_path)
        files_and_dirs = os.listdir(parent_folder)
        sequence_files = list()
        for each in files_and_dirs:
            each_path = os.path.realpath(
                os.path.normcase(os.path.join(parent_folder, each))
            )
            if os.path.isfile(each_path):
                each_file_name, each_file_ext = each.rsplit(".", 1)
                if each[:len(name_pattern)].lower() == name_pattern.lower()\
                        and each_file_ext.lower() == file_ext.lower():
                    sequence_files.append(each_path)
        sequence_files = sorted(sequence_files)
        return sequence_files
    return None


def is_sequence(file_path):
    """Looks for sibling files in the same directory. Since two sibling
    files is enough to make a sequence, if it finds one, it'll stop
    looking and return True.

    If you want to get a complete list of files, use get_sequence_files()

    Arguments:
        file_path {string} -- Full path to a file

    Returns:
        bool -- If another a file is found with the same name pattern,
        True is returned. No missing files are taken into account.
    """
    file_path = os.path.realpath(os.path.normcase(file_path))
    parent_folder, file_with_ext = os.path.split(file_path)
    file_name, file_ext = file_with_ext.rsplit(".", 1)

    name_pattern, hash_str = get_sequence_name_pattern(file_path)
    if not (name_pattern or hash_str):
        return False

    files_and_dirs = os.listdir(parent_folder)
    result = False
    for each in files_and_dirs:
        each_path = os.path.realpath(
                os.path.normcase(os.path.join(parent_folder, each))
            )
        if os.path.isfile(each_path):
            each_file_name, each_file_ext = each.rsplit(".", 1)
            if file_path == each_path:
                continue
            elif each[:len(name_pattern)].lower() == name_pattern.lower()\
                    and each_file_ext.lower() == file_ext.lower():
                result = True
                logger.debug("File belongs to a sequence: {}".format(file_path))
                break

    return result


def is_sequence_complete(files, name_pattern):
    first_file = files[0]
    last_file = files[-1]
    split_first_file = os.path.split(first_file)[1]
    first_file_name = split_first_file.rsplit(".", 1)[0]
    first_file_number = int(first_file_name[len(name_pattern):])

    split_last_file = os.path.split(last_file)[1]
    last_file_name = split_last_file.rsplit(".", 1)[0]
    last_file_number = int(last_file_name[len(name_pattern):])

    difference = last_file_number - first_file_number + 1

    if len(files) != difference:
        return False

    return True


def get_sequence_name_pattern(file_path):
    path_parts = os.path.split(os.path.realpath(os.path.normcase(file_path)))
    file_with_ext = path_parts[1]
    file_name, file_ext = file_with_ext.rsplit(".", 1)
    # Get number of digits in file_name
    digits_number = 0
    for each in file_name[::-1]:
        if each.isdigit() or each == '#':
            digits_number += 1
        else:
            break

    if digits_number == 0:
        logger.debug("Sequence name pattern not found for {}".format(file_path))
        return None, None

    name_pattern = file_name[:-digits_number]
    hash_str = "#" * digits_number

    return name_pattern, hash_str


def _process_dirs(src_path, trg_path, force_overwrite):
    src_path = os.path.normcase(os.path.abspath(src_path))
    trg_path = os.path.normcase(os.path.abspath(trg_path))
    logger_string = "\tSource: {}\n\tTarget: {}\n".format(
                src_path, trg_path
                )
    trg_exists = os.path.exists(trg_path)
    success = False
    try:
        if not trg_exists:
            shutil.copytree(src_path, trg_path)
            logger.debug(
                "Finished copying source to target.\n{}".format(
                    logger_string)
            )
            success = True
        elif trg_exists and force_overwrite:
            shutil.rmtree(trg_path)
            shutil.copytree(src_path, trg_path)
            logger.debug(
                "Finished overwriting target with source.\n{}".format(
                    logger_string)
            )
            success = True
        else:
            logger.warning(
                "Target already existed and force_overwrite was set to False."
                "\n{}".format(logger_string)
            )
            success = True
    except (IOError, OSError) as why:
        logger.error(
            "System Error while processing directories.\n{}\n{}".format(
                logger_string, why)
            )
        success = False
    return success


def _process_files(src_path, trg_path, force_overwrite, **kwargs):
    src_path = os.path.normcase(os.path.abspath(src_path))
    trg_path = os.path.normcase(os.path.abspath(trg_path))

    skip_non_tx = False
    if kwargs.get("only_tx"):
        skip_non_tx = kwargs.get("only_tx")

    include_tx = False
    if kwargs.get("include_tx"):
        include_tx = kwargs.get("include_tx")

    dir_success = _create_dir(trg_path)
    if not dir_success:
        # If directory creation failed, stop execution
        return False

    if is_sequence(src_path):
        sequence_files = get_sequence_files(src_path)
        for each in sequence_files:
            if not skip_non_tx:
                _process_original_files(each, trg_path, force_overwrite)
            if include_tx:
                _process_tx(each, trg_path, force_overwrite)
            if skip_non_tx and not include_tx:
                logger.warning(
                    "only_tx argument set to True, but include_tx not passed "
                    "or set to False. Nothing will be processed."
                )
    else:
        if not skip_non_tx:
            _process_original_files(src_path, trg_path, force_overwrite)
        if include_tx:
            _process_tx(src_path, trg_path, force_overwrite)
        if skip_non_tx and not include_tx:
            logger.warning(
                "only_tx argument set to True, but include_tx not passed or "
                "set to False. Nothing will be processed."
            )
    return True


def _create_dir(dirpath):
    if not os.path.exists(dirpath):
        try:
            os.makedirs(dirpath)
            logger.debug(
                "Directory structure created: {}".format(
                    dirpath)
            )
            return True
        except (IOError, OSError) as why:
            logger.error(
                "Directory structure couldn't be created: {}\n{}".format(
                    dirpath, why)
            )
            return False
    else:
        logger.debug(
            "Directory structure already existed: {}".format(
                dirpath)
        )
        return True


def _process_original_files(src_path, trg_path_dir, force_overwrite):
    try:
        src_file_name = os.path.split(src_path)[1]
        trg_file_exists = os.path.exists(
                os.path.join(trg_path_dir, src_file_name)
            )
        if not trg_file_exists \
                or (trg_file_exists and force_overwrite):
            shutil.copy2(src_path, trg_path_dir)
            logger.debug(
                "Copied {} to {}".format(src_path, trg_path_dir)
            )
        else:
            logger.debug(
                "File already existed and force_overwrite was set to False: {}"
                "\n\t{}".format(os.path.join(trg_path_dir, src_file_name))
            )
    except (IOError, OSError) as why:
        logger.warning(
            "System Error while processing source file: {}\n{}".format(
                src_path, why)
        )


def _process_tx(original_file_path, trg_path_dir, force_overwrite):
    src_tx_path = original_file_path.rsplit(".", 1)[0] + ".tx"
    if os.path.exists(src_tx_path):
        try:
            src_tx_name = os.path.split(src_tx_path)[1]
            trg_file_exists = os.path.exists(
                    os.path.join(trg_path_dir, src_tx_name)
                )
            if not trg_file_exists \
                    or (trg_file_exists and force_overwrite):
                shutil.copy2(src_tx_path, trg_path_dir)
                logger.debug(
                    "Copied {} to {}".format(
                        src_tx_path, trg_path_dir)
                )
            else:
                logger.debug(
                    "File already existed and force_overwrite was set to "
                    "False: {}\n\t{}".format(
                        os.path.join(trg_path_dir, src_tx_name))
                )
        except (IOError, OSError) as why:
            logger.warning(
                "System Error while processing source tx file: {}\n{}".format(
                    src_tx_path, why)
            )
    else:
        logger.warning(
            "The specified source TX file doesn't exist: {}".format(
                src_tx_path)
        )
