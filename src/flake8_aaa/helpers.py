import ast
import io
import os
import re
import tokenize
from typing import List

from asttokens.util import Token

test_file_pattern = re.compile(r'^(test(_.*|s)?|.*_test)\.py$')


def is_test_file(filename: str) -> bool:
    """
    Returns:
        Path to file passed by Flake8 looks like a Pytest test file.
    """
    return bool(test_file_pattern.match(os.path.basename(filename)))


def first_non_blank_char(line: str) -> int:
    for pos, char in enumerate(line):
        if not char.isspace():
            return pos
    return 0


class TestFuncLister(ast.NodeVisitor):
    """
    Helper to walk the ast Tree and find functions that looks like tests.
    Matching function nodes are kept in ``_found_func`` attr.

    TODO: move to visitors.py
    """

    def __init__(self, skip_noqa: bool):
        super().__init__()
        self.skip_noqa = skip_noqa
        self._found_funcs: List[ast.FunctionDef] = []

    def visit_FunctionDef(self, node):
        if node.name.startswith('test'):
            if not self.skip_noqa or not node.first_token.line.strip().endswith('# noqa'):
                self._found_funcs.append(node)

    def get_found_funcs(self) -> List[ast.FunctionDef]:
        return self._found_funcs


def find_test_functions(tree: ast.AST, skip_noqa: bool = False) -> List[ast.FunctionDef]:
    """
    Collect functions that look like tests.

    Args:
        tree
        skip_noqa: Flag used by command line debugger to skip functions that
            are marked with "# noqa". Defaults to ``False``.
    """
    function_finder = TestFuncLister(skip_noqa)
    function_finder.visit(tree)
    return function_finder.get_found_funcs()


def node_is_result_assignment(node: ast.AST) -> bool:
    """
    Args:
        node: An ``ast`` node.

    Returns:
        bool: ``node`` corresponds to the code ``result =``, assignment to the
        ``result `` variable.
    """
    if isinstance(node, ast.Assign):
        return len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and node.targets[0].id == "result"

    if isinstance(node, ast.AnnAssign):
        return node.target.id == "result"  # type: ignore

    return False


cm_exp = re.compile(r'^\s*with\ pytest\.(raises|deprecated_call|warns)\(')


def node_is_pytest_context_manager(node: ast.AST) -> bool:
    """
    Identify node as being one of the Pytest context managers used to catch
    exceptions and warnings.

    Pytest's context managers as of 7.2 are:

    * pytest.raises()
    * pytest.deprecated_call()
    * pytest.warns()

    Args:
        node: An ``ast`` node, augmented with ASTTokens

    Returns:
        bool: ``node`` corresponds to a With node where the context manager is
            a Pytest context manager.
    """
    return isinstance(node, ast.With) and bool(cm_exp.match(get_first_token(node).line))


def node_is_unittest_raises(node: ast.AST) -> bool:
    """
    ``node`` corresponds to a With node where the context manager is unittest's
    ``self.assertRaises``.
    """
    return isinstance(node, ast.With) and get_first_token(node).line.strip().startswith('with self.assertRaises')


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


def filter_arrange_nodes(nodes: List[ast.stmt], act_block_first_line_number: int) -> List[ast.stmt]:
    """
    Args:
        nodes: List of body nodes of test function.
        act_block_first_line_number: Real line number of Act block first line.

    Returns:
        All nodes are not docstrings or ``pass`` that start before the Act
        block's first line.
    """
    return [
        node for node in nodes if node.lineno < act_block_first_line_number and not isinstance(node, ast.Pass)
        and not (isinstance(node, ast.Expr) and isinstance(node.value, ast.Str))
    ]


def line_is_comment(line: str) -> bool:
    """
    Helper for checking that a single line is a comment. Will be replaced by a
    complete `find_comment_lines()` helper in #148. Could also use `tokens`
    from Flake8.
    """
    # TODO use existing tokens
    try:
        first_token = next(tokenize.generate_tokens(io.StringIO(line).readline))
    except tokenize.TokenError:
        # Assume that a token error happens because this is *not* a comment
        return False
    return first_token.type == tokenize.COMMENT


def flatten_list(items: List[str]) -> str:
    """
    Given a list of strings, flatten them to '"X", "Y" or "Z"' format.

    Raises:
        ValueError: When an empty list is received.
    """
    if len(items) == 1:
        return f'"{items[0]}"'

    try:
        last = items[-1]
    except IndexError:
        # Empty list
        raise ValueError('Empty list of values received')

    return ', '.join(f'"{item}"' for item in items[:-1]) + f' or "{last}"'
