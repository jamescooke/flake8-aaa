from .function import Function
from .helpers import find_test_functions, is_test_file, load_markers


class Checker:
    """
    Attributes:
        filename (str): Name of file under check.
        tokens (asttokens.ASTTokens): Tokens for the file.
        tree (astroid.Module): Astroid tree loaded from file.

    TODO: Checker should parse and tokenise the file if it's a test file:

        tree = astroid.parse(code)
        tokens = asttokens.ASTTokens(code, tree=tree)
        first_node = tree.get_children().__next__()

    Get text for a node:

        tokens.get_text(first_node)

    Get tokens for a node, including comments:

        list(tokens.get_tokens(first_node, include_extra=True))
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
        self.tokens = None

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
