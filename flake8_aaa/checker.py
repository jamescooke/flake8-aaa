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
        tree (ast.Module): Tree passed from flake8.
    """

    name = __short_name__
    version = __version__

    def __init__(self, tree, lines, filename):
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

    def load(self):
        self.ast_tokens = asttokens.ASTTokens(''.join(self.lines), tree=self.tree)

    def run(self):
        """
        (line_number, offset, text, check)
        """
        if is_test_file(self.filename):
            self.load()
            for function_def in find_test_functions(self.tree):
                function = Function(function_def)
                function.parse()
                for error in function.check():
                    yield error + (type(self), )
