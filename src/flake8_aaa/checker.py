from ast import AST
from typing import Generator, List, Tuple

import asttokens

from .__about__ import __short_name__, __version__
from .function import Function
from .helpers import find_test_functions, is_test_file


class Checker:
    """
    Attributes:
        ast_tokens (asttokens.ASTTokens): Tokens for the file.
        filename (str): Name of file under check.
        lines (list (str))
        tree (ast.AST): Tree passed from flake8.
    """

    name = __short_name__
    version = __version__

    def __init__(self, tree: AST, lines: List[str], filename: str):
        """
        Args:
            tree
            lines (list (str))
            filename (str)
        """
        self.tree = tree
        self.lines = lines
        self.filename = filename
        self.ast_tokens = None

    def load(self) -> None:
        self.ast_tokens = asttokens.ASTTokens(''.join(self.lines), tree=self.tree)

    def all_funcs(self, skip_noqa: bool = False) -> Generator[Function, None, None]:
        return (Function(f, self.lines) for f in find_test_functions(self.tree, skip_noqa=skip_noqa))

    def run(self) -> Generator[Tuple[int, int, str, type], None, None]:
        """
        Yields:
            tuple (line_number: int, offset: int, text: str, check: type)
        """
        if is_test_file(self.filename):
            self.load()
            for func in self.all_funcs():
                yield from func.check_all(type(self))
