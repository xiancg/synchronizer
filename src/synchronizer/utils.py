# coding=utf-8

# Copyright (C) 2019 - Chris Granados
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License, or any
# later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from __future__ import absolute_import, print_function

import os

from synchronizer.logger import logger


def get_sequence_files(file_path):
    """Find and return all files that are part of a sequence matching ``file_path``.
    If no sequence found, returns None. Two files are enough to make
    a sequence, even if they're not sequential. This assumes the sequence
    digits are right beside the file extension.

        e.g.:
            - C_myfile_v568.jpg
            - MJ_thisisafileseq_4568.dpx
            - MB_udimsforthewin.1008.tx

    Arguments:
        ``file_path`` {string} -- Path to a file

    Returns:
        [list] -- List of sequence files including given file_path.
        None if sequence is not found.
    """
    path_parts = os.path.split(file_path)
    parent_folder = path_parts[0]
    file_with_ext = path_parts[1]
    file_name, file_ext = file_with_ext.rsplit(".", 1)

    if is_sequence(file_path):
        name_pattern = get_sequence_name_pattern(file_path)
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
        if not is_sequence_complete(sequence_files, name_pattern):
            logger.warning(
                "Missing frames on sequence for "
                "file_path: {}".format(file_path)
            )
        return sequence_files
    return None


def is_sequence(file_path):
    """Looks for sibling files in the same directory. Since two sibling
    files is enough to make a sequence, even if they are not sequential, if it
    finds one, it'll stop looking and return True. This assumes the sequence
    digits are right beside the file extension.

        e.g.:
            - C_myfile_v568.jpg
            - MJ_thisisafileseq_4568.dpx
            - MB_udimsforthewin.1008.tx

    If you want to get a complete list of files, use get_sequence_files()

    Arguments:
        ``file_path`` {str} -- Full path to a file

    Returns:
        [bool] -- If another a file is found with the same name pattern,
        True is returned. Missing files are taken into account.
    """
    file_path_norm = os.path.realpath(os.path.normcase(file_path))
    parent_folder, file_with_ext = os.path.split(file_path)
    file_name, file_ext = file_with_ext.rsplit(".", 1)

    name_pattern = get_sequence_name_pattern(file_path)
    if not name_pattern:
        return False

    files_and_dirs = os.listdir(parent_folder)
    result = False
    for each in files_and_dirs:
        each_path = os.path.join(parent_folder, each)
        each_path_norm = os.path.realpath(
                os.path.normcase(each_path)
            )
        if os.path.isfile(each_path):
            each_file_name, each_file_ext = each.rsplit(".", 1)
            if file_path_norm == each_path_norm:
                continue
            elif each[:len(name_pattern)].lower() == name_pattern.lower()\
                    and each_file_ext.lower() == file_ext.lower():
                result = True
                logger.debug(
                    "File belongs to a sequence: {}".format(file_path)
                )
                break

    return result


def is_sequence_complete(files, name_pattern):
    """Evaluates a list of sequence files, if the sequence is missing one
    or more files, returns False. If sequence is complete, returns True.
    This assumes the sequence digits are right beside the file extension.

        e.g.:
            - C_myfile_v568.jpg
            - MJ_thisisafileseq_4568.dpx
            - MB_udimsforthewin.1008.tx

    Arguments:
        ``files`` {list} -- List of complete file paths to a file sequence.
        You could use get_sequence_files() to get a list.

        ``name_pattern`` {str} -- As returned by get_sequence_name_pattern(),
        It's a string consisting of the base name for the file without
        trailing digits.

        e.g.:
            - File: 'C_cresta_02__MSH-BUMP.1001.png'\n
            - Name Pattern: 'C_cresta_02__MSH-BUMP.'

    Returns:
        [bool] -- True if sequence is complete. False otherwise.
    """
    files = sorted(files)
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
    """Finds the name pattern and number of digits that make the name
    of the file. Both elements are used by other functions to identify
    file sequences. This assumes the sequence digits are right beside
    the file extension.

    e.g.:
        - C_myfile_v568.jpg

        - MJ_thisisafileseq_4568.dpx

        - MB_udimsforthewin.1008.tx

    Arguments:
        ``file_path`` {string} -- Full path to a file

    Returns:
        [str] -- A string consisting of the base name for the file
        without trailing digits.

        e.g.:
            - File: 'C_cresta_02__MSH-BUMP.1001.png'

            - Name Pattern: 'C_cresta_02__MSH-BUMP.'

        [None] -- If no digits can be found in the name, returns None
    """
    path_parts = os.path.split(file_path)
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
        logger.debug(
            "Sequence name pattern not found for {}".format(file_path)
        )
        return None

    name_pattern = file_name[:-digits_number]

    return name_pattern


def create_dir(dirpath):
    """Creates given directory.

    Arguments:
        ``dirpath`` {str} -- Full path to a directory that needs to be created.

    Returns:
        [bool] -- True if directory creation was successful, False otherwise.
    """
    if not os.path.exists(dirpath):
        try:
            os.makedirs(dirpath)
            logger.debug(
                "Directory structure created: {}".format(
                    dirpath)
            )
            return True
        except (IOError, OSError) as why:
            logger.critical(
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
