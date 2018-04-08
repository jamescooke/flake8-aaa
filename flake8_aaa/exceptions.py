class Flake8AAAException(Exception):
    pass


class NotActionBlock(Flake8AAAException):
    """
    Used when parsing if lines of a function should be considered Action
    blocks.
    """
