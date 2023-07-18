import typing

from .helpers import flatten_list


class Flake8Error(typing.NamedTuple):
    line_number: int
    offset: int
    text: str
    checker_cls: type


class AAAError(typing.NamedTuple):
    line_number: int
    offset: int
    text: str


class Flake8AAAException(Exception):
    pass


class UnexpectedConfigValue(Flake8AAAException):
    """
    Value of passed config is invalid.
    """

    def __init__(self, option_name: str, value: str, allowed_values: typing.List[str]) -> None:
        self.option_name = option_name
        self.value = value
        self.allowed_values = allowed_values

    def __str__(self) -> str:
        return (
            'Error loading option / configuration...\n'
            f'    Option: {self.option_name}\n'
            f'    Want:   {flatten_list(self.allowed_values)}\n'
            f'    Got:    "{self.value}"\n'
        )


class TokensNotLoaded(Flake8AAAException):
    """
    `Checker.all_funcs()` was called before `ast_tokens` was populated. Usually
    this is done by `Checker.load()`.
    """


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

    def to_aaa(self) -> AAAError:
        return AAAError(
            line_number=self.line_number,
            offset=self.offset,
            text=self.text,
        )
