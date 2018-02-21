class Thing(object):

    name = 'My flake8 plugin'
    version = '0.0'

    def __init__(self, tree, filename):
        print(tree)
