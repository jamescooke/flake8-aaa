from .function import Function
from .helpers import find_test_functions, is_test_file, load_markers


class Checker:
    """
    Attributes:
        markers (dict (int: list(Marker))): List of markers per line, keyed by
            the line number of where they appear in the file.

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

    def __init__(self, tree, filename, file_tokens):
        """
        Args:
            tree (ast.Module): AST tree of the file under check.
            filename (str)
            file_tokens (list (tokenize.TokenInfo))
        """
        self.tree = tree
        self.file_tokens = file_tokens
        self.filename = filename
        self.markers = load_markers(file_tokens)

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
