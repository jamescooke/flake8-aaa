import astroid
import asttokens

from .__about__ import __short_name__, __version__
from .function import Function
from .helpers import find_test_functions, is_test_file


class Checker:
    """
    Attributes:
        ast_tokens (asttokens.ASTTokens): Tokens for the file.
        filename (str): Name of file under check.
        tree (astroid.Module): Astroid tree loaded from file.
    """

    name = __short_name__
    version = __version__

    def __init__(self, tree, filename):
        """
        Args:
            tree: Ignored, but is required for flake8 to recognise this as a
                plugin.
            filename (str)
        """
        self.filename = filename
        self.tree = None
        self.ast_tokens = None

    def load(self):
        with open(self.filename) as f:
            file_contents = f.read()
        self.tree = astroid.parse(file_contents)
        self.ast_tokens = asttokens.ASTTokens(file_contents, tree=self.tree)

    def run(self):
        """
        (line_number, offset, text, check)
        """
        if is_test_file(self.filename):
            self.load()
            for function_def in find_test_functions(self.tree):
                function = Function(function_def, self.ast_tokens)
                function.parse()
                for error in function.check():
                    yield error + (type(self), )
