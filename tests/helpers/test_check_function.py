import ast

from flake8_aaa.helpers import check_function, find_test_functions


def test_pass():
    tree = ast.parse("""
def test():
    pass
""")
    function_node = find_test_functions(tree)[0]

    result = check_function(function_node)

    assert result == []


def test_result_assigned():
    tree = ast.parse("""
def test():
    result = 1

    assert result == 1
""")
    function_node = find_test_functions(tree)[0]

    result = check_function(function_node)

    assert result == []


def test_no_result():
    tree = ast.parse("""
def test():
    assert 1 + 1 == 2
""")
    function_node = find_test_functions(tree)[0]

    result = check_function(function_node)

    assert result == [
        # (line_number, offset, text)
        (3, 4, 'AAA01 no result variable set in test'),
    ]
