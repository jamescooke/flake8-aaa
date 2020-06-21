import tokenize

import pytest


@pytest.mark.parametrize('code_str', ['# stuff'])
def test_first_token(first_token):
    result = first_token

    assert isinstance(result, tokenize.TokenInfo)
    assert result.type == tokenize.COMMENT
    assert result.string == '# stuff'
