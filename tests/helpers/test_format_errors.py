import pytest

from flake8_aaa.helpers import format_errors


@pytest.mark.parametrize(
    'num_errors, output', [
        (0, '    0 | ERRORS\n'),
        (1, '    1 | ERROR\n'),
        (2, '    2 | ERRORS\n'),
        (913, '  913 | ERRORS\n'),
    ]
)
def test(num_errors, output):
    result = format_errors(num_errors)

    assert result == output
