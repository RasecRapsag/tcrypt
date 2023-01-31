import argparse
import sys


class TCrypt(argparse.ArgumentParser):
    def __init__(self) -> None:
        super().__init__(
            prog='tcrypt',
            description='Interface for handling truecrypt files.',
            epilog='Proctect your data! :-)',
            allow_abbrev=False,
            formatter_class=lambda prog: argparse.HelpFormatter(
                prog, max_help_position=40
            )
        )
        self.version = '1.0'
        self.initialize()

    def initialize(self) -> None:
        self.add_argument('--version', action='version')
        self.version = f'TCrypt version: {self.version}'

        group = self.add_mutually_exclusive_group(required=True)
        group.add_argument(
            '-i', '--init', action='store',
            help='start truecypt container', metavar='<dir>'
        )
        group.add_argument(
            '-s', '--stop', action='store_true',
            help='stop truecrypt container'
        )
        group.add_argument(
            '-l', '--list', action='store_true',
            help='list mounted truecrypt volumes'
        )
        group.add_argument(
            '-m', '--mount', action='store',
            help='mount truecrypt volume', metavar='<file>'
        )
        group.add_argument(
            '-d', '--dismount',
            action='store_true', help='dismount truecrypt volume'
        )
        self.args = self.parse_args()

    def error(self, message):
        self.print_usage()
        sys.stderr.write(f'error: {message}\n')
        sys.exit(2)
