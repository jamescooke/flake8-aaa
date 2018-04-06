import astroid
import asttokens

from .function import Function
from .helpers import find_test_functions, is_test_file


class Checker:
    """
    Attributes:
        filename (str): Name of file under check.
        ast_tokens (asttokens.ASTTokens): Tokens for the file.
        tree (astroid.Module): Astroid tree loaded from file.

    Get text for a node:

        self.ast_tokens.get_text(first_node)

    Get tokens for a node, including comments:

        list(self.ast_tokens.get_tokens(first_node, include_extra=True))
    """

    name = 'aaa'
    version = '0.1'

    def __init__(self, filename):
        """
        Args:
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
            for function_def in find_test_functions(self.tree):
                function = Function(function_def)
                function.pull_markers(self.markers)
                for error in function.check():
                    yield error + (type(self), )
