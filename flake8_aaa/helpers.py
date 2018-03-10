import py


def is_test_file(filename):
    """
    Args:
        filename (str): Path to file being checked passed by flake8

    Returns:
        bool: This looks like a pytest test file.

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
