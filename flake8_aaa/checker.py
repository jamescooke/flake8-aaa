from .helpers import is_test_file


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
            yield (3, 0, 'AAA01 no result variable set in test', type(self))
