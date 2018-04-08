class Flake8AAAException(Exception):
    pass


class FunctionNotParsed(Flake8AAAException):
    """
    ``Function.check()`` was called without ``Function.parse()`` being called
    first.
    """


class NotActionBlock(Flake8AAAException):
    """
    Used when parsing if lines of a function should be considered Action
    blocks.
    """
