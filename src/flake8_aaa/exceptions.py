import typing

Flake8Error = typing.NamedTuple(
    'Flake8Error', [
        ('line_number', int),
        ('offset', int),
        ('text', str),
        ('checker_cls', type),
    ]
)


class Flake8AAAException(Exception):
    pass


class EmptyBlock(Flake8AAAException):
    """
    Block has no nodes.
    """


class ValidationError(Flake8AAAException):
    """
    Attributes:
        line_number (int)
        offset (int)
        text (str)
    """

    def __init__(self, line_number, offset, text):
        self.line_number = line_number
        self.offset = offset
        self.text = text

    def to_flake8(self, checker_cls: type) -> Flake8Error:
        """
        Args:
            checker_cls: Class performing the check to be passed back to
                flake8.
        """
        return Flake8Error(
            line_number=self.line_number,
            offset=self.offset,
            text=self.text,
            checker_cls=checker_cls,
        )
