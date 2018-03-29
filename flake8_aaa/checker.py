from .function import Function
from .helpers import find_test_functions, is_test_file


class Checker:
    """
    Attributes:
        markers (dict (int: list(Marker))): List of markers per line, keyed by
            the line number of where they appear in the file.
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
        self.markers = {}

    def run(self):
        """
        (line_number, offset, text, check)
        """
        if is_test_file(self.filename):
            for function_def in find_test_functions(self.tree):
                function = Function(function_def)
                for error in function.check():
                    yield error + (type(self), )
