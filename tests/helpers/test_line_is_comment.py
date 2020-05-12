import pytest

from flake8_aaa.helpers import line_is_comment


@pytest.mark.parametrize(
    'line, expected_result', [
        ('# do thing', True),
        ('    # do thing', True),
        ('got = compile()  # act', False),
        ('x = 1', False),
        ('assert result is True', False),
        ('', False),
        ('  """', False),
        ('    assert result == \'\'\'', False),
        ('\'\'\'.lstrip()', False),
    ]
)
def test(line, expected_result):
    result = line_is_comment(line)

    assert result is expected_result
