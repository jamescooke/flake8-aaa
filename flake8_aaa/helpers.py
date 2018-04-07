import astroid
import py


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
        tree (astroid.Module)

    Returns:
        list (astroid.FunctionDef): Fuctions that look like tests.
    """
    test_nodes = []
    for node in tree.get_children():
        if node.is_function and node.name.startswith('test'):
            test_nodes.append(node)
    return test_nodes


def node_is_result_equals(node):
    """
    Args:
        node: An ``astroid`` node.

    Returns:
        bool: ``node`` corresponds to the code ``result =``, assignment to the
        ``result `` variable.
    """
    return (
        isinstance(node, astroid.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], astroid.AssignName)
        and node.targets[0].name == 'result'
    )


def node_is_pytest_raises(node):
    """
    Args:
        node: An ``astroid`` node.

    Returns:
        bool: ``node`` corresponds to a With node where the context manager is
        ``pytest.raises``.
    """
    if (isinstance(node, astroid.With)):
        child = next(node.get_children())
        if child.as_string().startswith('pytest.raises'):
            return True
    return False
