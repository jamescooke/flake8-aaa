# Dirty hack to allow for direct running of flake8-aaa from the command line,
# bypassing flake8's harness. Goal of this is to allow for debugging of
# analysis, especially around how flake8-aaa has assigned lines of code to
# particular blocks.

import argparse
import sys

from .command_line import do_command_line


def main() -> int:
    parser = argparse.ArgumentParser(description='flake8-aaa command line debug')
    parser.add_argument('infile', type=argparse.FileType('r'), help='File to be linted')
    args = parser.parse_args()
    result = do_command_line(args.infile)
    args.infile.close()
    return result


if __name__ == '__main__':
    sys.exit(main())
