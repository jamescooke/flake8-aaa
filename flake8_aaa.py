class Thing(object):

    name = 'aaa'
    version = '0.1'

    def __init__(self, tree):
        self.tree = tree

    def run(self):
        """
        (line_number, offset, text, check)
        """
        yield (3, 0, 'AAA01 no result variable set in test', type(self))
