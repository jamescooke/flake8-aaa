import tokenize

import pytest

from flake8_aaa.marker import TokenWrapper


@pytest.mark.parametrize('code_str', [
    '# AAA Act',
    '# AAA act',
    '# aaa act',
])
def test(code_str, first_token):
    result = TokenWrapper(first_token)

    assert result.type == tokenize.COMMENT
    assert result.string == code_str
    assert result.start == (1, 0)
