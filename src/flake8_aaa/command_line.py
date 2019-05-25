import ast
import typing

from .checker import Checker
from .exceptions import ValidationError


def do_command_line(infile: typing.IO[str]) -> int:
    """
    Currently a small stub to create an instance of Checker for the passed
    ``infile`` and run its test functions through linting.

    Args:
        infile

    Returns:
        int: Number of flake8 errors raised.
    """
    lines = infile.readlines()
    tree = ast.parse(''.join(lines))
    checker = Checker(tree, lines, infile.name)
    checker.load()
    num_errors = 0

    for func in checker.all_funcs(skip_noqa=True):
        try:
            errors = list(func.check_all())
        except ValidationError as error:
            errors = [error.to_aaa()]
        print(func.__str__(errors), end='')
        num_errors += len(errors)

    print('======+========================================================================')
    if num_errors:
        print('        FAILED with {} ERROR{}'.format(num_errors, 'S' if num_errors > 1 else ''))
    else:
        print('        PASSED!')

    return num_errors
