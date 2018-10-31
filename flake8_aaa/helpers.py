import ast
import os
from typing import List, Optional, Set, Tuple

from asttokens.util import Token


def is_test_file(filename: str) -> bool:
    """
    Check that path to file being checked passed by flake8 looks like a pytest
    test file.

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
    """

    def __init__(self, *args, **kwargs):
        super(TestFuncLister, self).__init__(*args, **kwargs)
        self._found_funcs = []  # type: List[ast.FunctionDef]

    def visit_FunctionDef(self, node):  # pylint: disable=invalid-name
        if node.name.startswith('test'):
            self._found_funcs.append(node)

    def get_found_funcs(self) -> List[ast.FunctionDef]:
        return self._found_funcs


def find_test_functions(tree: ast.AST) -> List[ast.FunctionDef]:
    """
    Collect functions that look like tests.
    """
    function_finder = TestFuncLister()
    function_finder.visit(tree)
    return function_finder.get_found_funcs()


def node_is_result_assignment(node: ast.AST) -> bool:
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
    # `.first_token` is added by asttokens
    token = node.first_token  # type: ignore
    return token.line.strip().startswith('result =')


def node_is_pytest_raises(node: ast.AST) -> bool:
    """
    Args:
        node: An ``ast`` node, augmented with ASTTokens

    Returns:
        bool: ``node`` corresponds to a With node where the context manager is
        ``pytest.raises``.
    """
    # `.first_token` is added by asttokens
    token = node.first_token  # type: ignore
    return isinstance(node, ast.With) and token.line.strip().startswith('with pytest.raises')


def node_is_unittest_raises(node: ast.AST) -> bool:
    """
    ``node`` corresponds to a With node where the context manager is unittest's
    ``self.assertRaises``.
    """
    # `.first_token` is added by asttokens
    token = node.first_token  # type: ignore
    return isinstance(node, ast.With) and token.line.strip().startswith('with self.assertRaises')


def node_is_noop(node: ast.AST) -> bool:
    """
    Node does nothing.
    """
    return isinstance(node.value, ast.Str) if isinstance(node, ast.Expr) else isinstance(node, ast.Pass)


def function_is_noop(function_node: ast.FunctionDef) -> bool:
    """
    Function does nothing - is just ``pass`` or docstring.
    """
    return all(node_is_noop(n) for n in function_node.body)


def format_errors(errors: Optional[List[Tuple[int, int, str, type]]]) -> str:
    """
    Formats a Function's errors for command line use.

    Note:
        Only works with a single error per Function.
    """
    if errors is None:
        return '    0 | ERRORS (yet)\n'
    if errors:
        assert len(errors) == 1
        return '    1 | ERROR\n'
    return '    0 | ERRORS\n'


def get_first_token(node: ast.AST) -> Token:
    """
    Wrapper to solve typing errors. mypy complains that ``ast.AST`` has no
    property ``first_token`` or ``last_token``. That's because these are added
    by the asttokens library. For now, this ignoring of type, which I think is
    required to get mypy to pass at this time, is encapsulated in this helper
    function.
    """
    return node.first_token  # type: ignore


def get_last_token(node: ast.AST) -> Token:
    """
    Performs same purpose as get_first_token.
    """
    return node.last_token  # type: ignore


def build_footprint(node: ast.AST, first_line_no: int) -> Set[int]:
    """
    Generates a list of lines that the passed node covers, relative to the
    marked lines list - i.e. start of function is line 0.
    """
    return set(
        range(
            get_first_token(node).start[0] - first_line_no,
            get_last_token(node).end[0] - first_line_no + 1,
        )
    )


def build_multinode_footprint(nodes: List[ast.AST], first_line_no: int) -> Set[int]:
    out = set()  # type: Set[int]
    for node in nodes:
        out = out.union(build_footprint(node, first_line_no))
    return out
