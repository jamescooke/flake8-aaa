from .helpers import check_function, find_test_functions, is_test_file


class Checker:

    name = 'aaa'
    version = '0.1'

    def __init__(self, tree, filename):
        self.filename = filename
        self.tree = tree

    def run(self):
        """
        (line_number, offset, text, check)
        """
        if is_test_file(self.filename):
            for function_def in find_test_functions(self.tree):
                for error in check_function(function_def):
                    yield error + (type(self), )
