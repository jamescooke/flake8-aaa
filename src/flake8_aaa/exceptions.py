import typing


class Flake8AAAException(Exception):
    pass


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

    def to_flake8(self, checker_cls: typing.Type) -> typing.Tuple[int, int, str, typing.Type]:
        """
        Args:
            checker_cls (type): Class performing the check to be passed back to
                flake8.

        Returns:
            tuple: Error to pass back to Flake8.
        """
        return (
            self.line_number,
            self.offset,
            self.text,
            checker_cls,
        )
