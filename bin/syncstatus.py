from __future__ import absolute_import, print_function

import argparse

from synchronizer import syncstatus, logger


def build_parser():
    """Build command line interface

    Returns:
        [argparse.ArgumentParser] -- ArgumentParser object
    """
    description = "Compare two files or directory paths and return sync status. "
    "Sync status refers to name and os.stat() comparisons."

    parser = argparse.ArgumentParser(
        prog="Get sync status",
        description=description
    )

    parser.add_argument(
        "src_path",
        help="Path to a file or directory."
    )
    parser.add_argument(
        "trg_path",
        help="Path to a file or directory."
    )
    parser.add_argument(
        "--get_sync_status",
        action="store_true",
        help="Compare two files or directory paths and return sync status. "
        "Sync status refers to name and os.stat() comparisons."
    )
    parser.add_argument(
        "--ignore_name",
        action="store_true",
        help="Ignores name comparison."
    )
    parser.add_argument(
        "--get_most_recent",
        choices=["st_mtime", "st_atime", "st_ctime"],
        default=None,
        const="st_mtime",
        nargs="?",
        type=str,
        help="Compares two paths and returns whichever has the most recent stat time. "
        "Default stat used for comparison is st_mtime which is: Time of most recent "
        "content modification."
    )
    parser.add_argument(
        "--log",
        action="store_true",
        help="Activate logging. Useful for debugging."
    )

    return parser


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()

    if args:
        src_path = args.src_path
        trg_path = args.trg_path
        sync_stat = args.get_sync_status
        ignore_name = args.ignore_name
        get_most_recent = args.get_most_recent
        log_bool = args.log

        if log_bool:
            logger.init_logger()

        if sync_stat:
            print(syncstatus.get_sync_status(
                src_path, trg_path, ignore_name)[1]
            )

        if get_most_recent is not None:
            print("Most recent by {}: {}".format(
                get_most_recent,
                syncstatus.get_most_recent(src_path, trg_path, get_most_recent))
            )
