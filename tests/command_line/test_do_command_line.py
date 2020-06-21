import ast

import pytest

from flake8_aaa.command_line import do_command_line
from flake8_aaa.helpers import find_test_functions, is_test_file


@pytest.fixture
def example_file(tmpdir):
    """
    Returns:
        file: Test file like argparse returns which has a 'name' property. This
        is deliberately named to not look like a test file - which means that
        the command line functionality of running files regardless of if
        they're a test file or not can be tested.
    """
    f = tmpdir.join('example_file.py')
    f.write("""
def test():
    do_stuff()

def test_other():
    do_other_stuff()
""")
    f.name = 'example_file.py'
    return f


def test_example_file_is_test(example_file):
    result = is_test_file(example_file.name)

    assert result is False


def test_example_file_has_functions(example_file):
    lines = example_file.readlines()
    tree = ast.parse(''.join(lines))

    result = find_test_functions(tree)

    assert len(result) == 2


# --- TESTS ---


def test(example_file, capsys):
    with example_file.open() as f:

        result = do_command_line(f)

    assert result == 2
    assert capsys.readouterr().out == '''
------+------------------------------------------------------------------------
 2 DEF|def test():
       ^ AAA01 no Act block found in test
 3 ???|    do_stuff()
------+------------------------------------------------------------------------
    1 | ERROR
------+------------------------------------------------------------------------
 5 DEF|def test_other():
       ^ AAA01 no Act block found in test
 6 ???|    do_other_stuff()
------+------------------------------------------------------------------------
    1 | ERROR
======+========================================================================
        FAILED with 2 ERRORS
'''.lstrip()
