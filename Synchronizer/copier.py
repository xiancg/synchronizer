# coding=utf-8
from __future__ import absolute_import, print_function

import os
import shutil

from synchronizer.logger import logger
from synchronizer import utils


def process_paths(src_path, trg_path, force_overwrite=True, **kwargs):
    """Copies src_path to trg_path. Takes both files and directories
    as source. If given source is a file and it's part of a sequence
    it'll find and copy the entire sequence of files.

    Arguments:
        src_path {string} -- Path to a file or directory
        trg_path {string} -- Path to a directory

    Keyword Arguments:
        force_overwrite {bool} -- Empties trg_path before copying src_path
            contents. If src_path it's a file it'll only remove that file.
            (default: {True})

    Optional Keyword Arguments:
        include_tx {bool} -- If tx files are found that match given
            src_path, they're also copied.
        only_tx {bool} -- Finds tx files that match given src_path,
            but copies tx only, not src_path. For this flag to work,
            include_tx must be passed and set to True.
        find_sequence {bool} -- If set to False, it'll skip trying to find
            sequence files for given src_path (default: {True})

    Returns:
        [bool] -- If files were processed correctly, True is returned.
            False otherwise.
    """
    src_path_norm = os.path.normcase(os.path.abspath(src_path))
    trg_path_norm = os.path.normcase(os.path.abspath(trg_path))
    logger_string = "\tSource: {}\n\tTarget: {}\n".format(
                src_path, trg_path
                )
    src_is_dir = False
    if os.path.isdir(src_path):
        src_is_dir = True

    success = False
    # Sanity checks
    if not os.path.isdir(trg_path):
        logger.warning(
            "Skipped: Target path must be a directory.\n{}".format(
                logger_string)
            )
        success = False
    elif not os.path.exists(src_path):
        logger.warning(
            "Skipped: Source path doesn't exist.\n{}".format(
                logger_string)
            )
        success = False
    elif src_path_norm == trg_path_norm:
        logger.warning(
            "Skipped: Source and target are the same.\n{}".format(
                logger_string)
            )
        success = False
    elif src_is_dir:
        success = _process_dirs(src_path, trg_path, force_overwrite)
    else:
        success = _process_files(src_path, trg_path, force_overwrite, **kwargs)
    return success


def _process_dirs(src_path, trg_path, force_overwrite):
    """Copies src_path to trg_path. Takes directories as source.

    Not meant to be used directly, use process_paths() instead.

    Arguments:
        src_path {string} -- Path to a directory
        trg_path {string} -- Path to a directory

    Keyword Arguments:
        force_overwrite {bool} -- Empties trg_path before copying src_path
            contents (default: {True})

    Returns:
        [bool] -- If directories were processed correctly, True is returned.
            False otherwise.
    """
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
    """Copies src_path to trg_path. Takes a file as source.
    If given file is part of a sequence it'll find and copy the
    entire sequence of files.

    Not meant to be used directly, use process_paths() instead.

    Arguments:
        src_path {string} -- Path to a file
        trg_path {string} -- Path to a directory

    Keyword Arguments:
        force_overwrite {bool} -- Empties trg_path before copying src_path
            contents (default: {True})

    Optional Keyword Arguments:
        include_tx {bool} -- If tx files are found that match given
            src_path, they're also copied. (default: {False})
        only_tx {bool} -- Finds tx files that match given src_path,
            but copies tx only, not src_path. For this flag to work,
            include_tx must be passed and set to True. (default: {False})
        find_sequence {bool} -- If set to False, it'll skip trying to find
            sequence files for given src_path (default: {True})

    Returns:
        [bool] -- If file was processed correctly, True is returned.
            False otherwise.
    """
    skip_non_tx = False
    if kwargs.get("only_tx"):
        skip_non_tx = kwargs.get("only_tx")

    include_tx = False
    if kwargs.get("include_tx"):
        include_tx = kwargs.get("include_tx")

    find_sequence = True
    if kwargs.get("find_sequence"):
        find_sequence = kwargs.get("find_sequence")

    dir_success = utils.create_dir(trg_path)
    if not dir_success:
        # If directory creation failed, stop execution
        return False

    if utils.is_sequence(src_path) and find_sequence:
        sequence_files = utils.get_sequence_files(src_path)
        for each in sequence_files:
            if not skip_non_tx:
                _process_original_files(each, trg_path, force_overwrite)
            if include_tx:
                _process_tx(each, trg_path, force_overwrite)
            if skip_non_tx and not include_tx:
                logger.warning(
                    "only_tx argument set to True, but include_tx not "
                    "passed or set to False. Nothing will be processed."
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


def _process_original_files(src_path, trg_path, force_overwrite):
    """Sometimes no tx are desired, so this only deals with src_path,
    ignoring tx files if they exist.

    Not meant to be used directly, use process_paths() instead.

    Arguments:
        src_path {string} -- Path to a file
        trg_path {string} -- Path to a directory
        force_overwrite {bool} -- Empties trg_path before copying src_path
    """
    success = False
    try:
        src_file_name = os.path.split(src_path)[1]
        trg_file_exists = os.path.exists(
                os.path.join(trg_path, src_file_name)
            )
        if not trg_file_exists \
                or (trg_file_exists and force_overwrite):
            shutil.copy2(src_path, trg_path)
            logger.debug(
                "Copied {} to {}".format(src_path, trg_path)
            )
            success = True
        else:
            logger.debug(
                "File already existed and force_overwrite was set to False: "
                "\n\t{}".format(os.path.join(trg_path, src_file_name))
            )
            success = True
    except (IOError, OSError) as why:
        logger.warning(
            "System Error while processing source file: {}\n{}".format(
                src_path, why)
        )
        success = False
    return success


def _process_tx(original_file_path, trg_path, force_overwrite):
    """Takes original texture as parameter and finds adjacent tx file to
    copy it to trg_path.

    Not meant to be used directly, use process_paths() instead.

    Arguments:
        src_path {string} -- Path to a file
        trg_path {string} -- Path to a directory
        force_overwrite {bool} -- Empties trg_path before copying src_path
    """
    src_tx_path = original_file_path.rsplit(".", 1)[0] + ".tx"
    success = False
    if os.path.exists(src_tx_path):
        try:
            src_tx_name = os.path.split(src_tx_path)[1]
            trg_file_exists = os.path.exists(
                    os.path.join(trg_path, src_tx_name)
                )
            if not trg_file_exists \
                    or (trg_file_exists and force_overwrite):
                shutil.copy2(src_tx_path, trg_path)
                logger.debug(
                    "Copied {} to {}".format(
                        src_tx_path, trg_path)
                )
                success = True
            else:
                logger.debug(
                    "File already existed and force_overwrite was set to "
                    "False: \n\t{}".format(
                        os.path.join(trg_path, src_tx_name))
                )
                success = True
        except (IOError, OSError) as why:
            logger.warning(
                "System Error while processing source tx file: {}\n{}".format(
                    src_tx_path, why)
            )
            success = False
    else:
        logger.warning(
            "The specified source TX file doesn't exist: {}".format(
                src_tx_path)
        )
        success = False
    return success
