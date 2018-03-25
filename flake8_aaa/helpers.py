import ast

import py

from flake8_aaa.exceptions import NotAMarker
from flake8_aaa.marker import Marker


def is_test_file(filename):
    """
    Args:
        filename (str): Path to file being checked passed by flake8

    Returns:
        bool: This looks like a pytest test file.

    Examples:
        1.  Non-test files give False.
        >>> is_test_file('./test.py')
        False
        >>> is_test_file('./helper.py')
        False
        >>> is_test_file('tests/conftest.py')
        False

        2.  Finds files that start with 'test_' to be test files.
        >>> is_test_file('./test_helpers.py')
        True
    """
    return py.path.local(filename).basename.startswith('test_')


def find_test_functions(tree):
    """
    Args:
        tree (ast.Module)

    Returns:
        list (ast.FunctionDef): Fuctions that look like tests.
    """
    test_nodes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name.startswith('test'):
            test_nodes.append(node)
    return test_nodes


def load_markers(file_tokens):
    """
    Args:
        file_tokens (list (tokenize.TokenInfo))

    Returns:
        dict: Key the dictionary using the starting line of the comment.
    """
    out = {}
    for token in file_tokens:
        try:
            marker = Marker.build(token)
        except NotAMarker:
            continue
        out[marker.token.start[0]] = marker
    return out


def check_function(function_def):
    """
    Check test function for errors. Test functions that are just 'pass' are
    skipped.

    Args:
        (ast.FunctionDef)

    Returns:
        list (tuple): Errors in flake8 (line_number, offset, text)
    """
    if len(function_def.body) == 1:
        if isinstance(function_def.body[0], ast.Pass):
            return []

    for node in function_def.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name) and target.id == 'result':
                return []

    return [
        (node.lineno, node.col_offset, 'AAA01 no result variable set in test'),
    ]
