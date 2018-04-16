from __future__ import print_function, absolute_import, unicode_literals

import argparse

from .api import print_submissions_to_score


def init_parser():
    """Defines command-line interface"""
    parser = argparse.ArgumentParser(
        prog=__file__,
        description='Print command to score the submissions on backend')

    parser.add_argument('config', type=str,
                        help='Backend configuration file with database '
                             'connexion and RAMP event details.')
    parser.add_argument('event_name', type=str,
                        help='Event name of the submission.')
    parser.add_argument('--force', action='store_true',
                        help='Overwrite existing values in the db')

    return parser


def main():
    parser = init_parser()
    args = parser.parse_args()

    print_submissions_to_score(args.config, args.event_name, args.force)


if __name__ == '__main__':
    main()
