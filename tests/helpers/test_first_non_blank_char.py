import pytest

from flake8_aaa.helpers import first_non_blank_char


@pytest.mark.parametrize(
    'line, char_index',
    [
        # Empty string has no non-blank chars.
        ('', 0),
        # First char after whitespace or tabs works.
        ('    return', 4),
        ('        return', 8),
    ]
)
def test(line, char_index):
    result = first_non_blank_char(line)

    assert result == char_index
