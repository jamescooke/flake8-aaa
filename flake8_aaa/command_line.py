import ast
from typing import IO

from .checker import Checker


def do_command_line(infile: IO[str]) -> int:
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
    for func in checker.all_funcs():
        errors = func.get_errors()
        print(func, end='')
    return len(errors)
