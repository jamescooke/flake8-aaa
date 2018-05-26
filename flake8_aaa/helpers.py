import ast
import os


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
    return os.path.basename(filename).startswith('test_')


class TestFuncLister(ast.NodeVisitor):
    """
    Helper to walk the ast Tree and find functions that looks like tests.
    Matching function nodes are kept in ``_found_func`` attr.

    Attributes:
        _found_func (list (ast.node))
    """

    def __init__(self, *args, **kwargs):
        super(TestFuncLister, self).__init__(*args, **kwargs)
        self._found_funcs = []

    def visit_FunctionDef(self, node):
        if node.name.startswith('test'):
            self._found_funcs.append(node)


def find_test_functions(tree):
    """
    Args:
        tree (ast.Module)

    Returns:
        list (ast.FunctionDef): Functions that look like tests.
    """
    function_finder = TestFuncLister()
    function_finder.visit(tree)
    return function_finder._found_funcs


def node_is_result_assignment(node):
    """
    Args:
        node: An ``ast`` node.

    Returns:
        bool: ``node`` corresponds to the code ``result =``, assignment to the
        ``result `` variable.

    Note:
        Performs a very weak test that the line starts with 'result =' rather
        than testing the tokens.
    """
    return node.first_token.line.strip().startswith('result =')


def node_is_pytest_raises(node):
    """
    Args:
        node: An ``ast`` node, augmented with ASTTokens

    Returns:
        bool: ``node`` corresponds to a With node where the context manager is
        ``pytest.raises``.
    """
    return isinstance(node, ast.With) and node.first_token.line.strip().startswith('with pytest.raises')


def node_is_noop(node):
    """
    Args:
        node (ast.node)

    Returns:
        bool: Node does nothing.
    """
    return (type(node) is ast.Expr and type(node.value) is ast.Str) or (type(node) is ast.Pass)


def function_is_noop(function_node):
    """
    Args:
        function_node (ast.FunctionDef): A function.

    Returns:
        bool: Function does nothing - is just ``pass`` or docstring.
    """
    return all(node_is_noop(n) for n in function_node.body)
