from __future__ import absolute_import, print_function

import argparse

from synchronizer import copier, logger


def build_parser():
    """Build command line interface

    Returns:
        [argparse.ArgumentParser] -- ArgumentParser object
    """
    description = "Copies src_path to trg_path. Takes both files and directories "
    "as source. If given source is a file and it's part of a sequence it'll find "
    "and copy the entire sequence of files."

    parser = argparse.ArgumentParser(
        prog="Copies src_path to trg_path",
        description=description
    )
    parser.add_argument(
        "src_path",
        help="Path to a file or directory."
    )
    parser.add_argument(
        "trg_path",
        help="Path to a directory."
    )
    parser.add_argument(
        "--force_overwrite",
        type=str_to_bool,
        default=True,
        const=True,
        nargs='?',
        help="If True empties trg_path before copying src_path contents. If "
             "src_path it's a file it'll only remove that file. Default: True"
    )
    parser.add_argument(
        "--include_tx",
        type=str_to_bool,
        default=False,
        const=False,
        nargs='?',
        help="If tx files are found that match given src_path, they're also copied."
    )
    parser.add_argument(
        "--only_tx",
        type=str_to_bool,
        default=False,
        const=False,
        nargs='?',
        help="Finds tx files that match given src_path, but copies tx only, "
        "not src_path. For this flag to work, include_tx must be passed and "
        "set to True."
    )
    parser.add_argument(
        "--find_sequence",
        type=str_to_bool,
        default=True,
        const=True,
        nargs='?',
        help="If set to False, it'll skip trying to find sequence files for "
        "given src_path. default: True"
    )
    parser.add_argument(
        "--log",
        action='store_true',
        help="Activate logging. Useful for debugging."
    )

    return parser


def str_to_bool(value):
    """Takes value and returns its boolean equivalent

    Arguments:
        value {string or bool} -- String or bool representing a boolean value
            True = 'yes', 'true', 't', 'y', '1'
            False = 'no', 'false', 'f', 'n', '0'

    Raises:
        argparse.ArgumentTypeError: 'Boolean value expected'

    Returns:
        [bool] -- Boolean equivalent of value
    """
    if isinstance(value, bool):
        return value
    if value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()

    if args:
        src_path = args.src_path
        trg_path = args.trg_path
        force_overwrite = args.force_overwrite
        include_tx = args.include_tx
        only_tx = args.only_tx
        find_sequence = args.find_sequence
        log_bool = args.log

        if log_bool:
            logger.init_logger()

        result = copier.process_paths(
            src_path, trg_path, force_overwrite,
            include_tx=include_tx,
            only_tx=only_tx,
            find_sequence=find_sequence
        )
        if result and force_overwrite:
            print("Copied {} to {}".format(src_path, trg_path))
        elif result and not force_overwrite:
            print("force_overwrite was set to False. Nothing was copied.")
            if not log_bool:
                print("Try again with --log option to debug.")
        else:
            print("There was a problem processing your request.")
            if not log_bool:
                print("Try again with --log option to debug.")
