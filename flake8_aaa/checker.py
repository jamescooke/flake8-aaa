from .function import Function
from .helpers import find_test_functions, is_test_file


class Checker:

    name = 'aaa'
    version = '0.1'

    def __init__(self, tree, filename, tokens, file_tokens):
        self.filename = filename
        self.tree = tree
        self.file_tokens = file_tokens

    def run(self):
        """
        (line_number, offset, text, check)
        """
        if is_test_file(self.filename):
            for function_def in find_test_functions(self.tree):
                function = Function(function_def)
                for error in function.check():
                    yield error + (type(self), )
