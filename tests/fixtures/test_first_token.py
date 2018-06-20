import tokenize

import pytest
import six


@pytest.mark.skipif(six.PY2, reason='py2')
@pytest.mark.parametrize('code_str', ['# stuff'])
def test_first_token_py3(first_token):
    result = first_token

    assert isinstance(result, tokenize.TokenInfo)
    assert result.type == tokenize.COMMENT
    assert result.string == '# stuff'


@pytest.mark.skipif(six.PY3, reason='py3')
@pytest.mark.parametrize('code_str', ['# stuff'])
def test_first_token_py2(first_token):
    result = first_token

    assert isinstance(result, tuple)
    assert result[0] == tokenize.COMMENT
    assert result[1] == '# stuff'
