import ast

from flake8_aaa.function import Function
from flake8_aaa.helpers import find_test_functions


def test_pass():
    tree = ast.parse("""
def test():
    pass
""")
    function_node = find_test_functions(tree)[0]
    function = Function(function_node)

    result = function.check()

    assert result == []


def test_result_assigned():
    tree = ast.parse("""
def test():
    result = 1

    assert result == 1
""")
    function_node = find_test_functions(tree)[0]
    function = Function(function_node)

    result = function.check()

    assert result == []


def test_no_result():
    tree = ast.parse("""
def test():
    assert 1 + 1 == 2
""")
    function_node = find_test_functions(tree)[0]
    function = Function(function_node)

    result = function.check()

    assert result == [
        # (line_number, offset, text)
        (3, 4, 'AAA01 no result variable set in test'),
    ]


def test_no_qa():
    tree = ast.parse("""
def test():
    x = 1 + 1  # noqa: AAA01
    assert x == 2
""")
    function_node = find_test_functions(tree)[0]
    function = Function(function_node)

    result = function.check()

    assert result == []
