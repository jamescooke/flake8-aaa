import ast

from flake8_aaa.helpers import find_test_functions


def test_empty():
    tree = ast.parse("print('hi')")

    result = find_test_functions(tree)

    assert result == []


def test_some():
    tree = ast.parse(
        """
import pytest


@pytest.fixture
def a_number():
    return 1


def test():
    pass


def test_thing(a_number):
    result = a_number == 1

    assert result is True
"""
    )

    result = find_test_functions(tree)

    assert [fn.name for fn in result] == ['test', 'test_thing']
