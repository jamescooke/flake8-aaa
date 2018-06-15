from flake8_aaa.checker import Checker
from flake8_aaa.exceptions import ValidationError


def test():
    result = ValidationError(
        line_number=99,
        offset=777,
        text='__MESSAGE__',
    )

    assert result.to_flake8(Checker) == (99, 777, '__MESSAGE__', Checker)
