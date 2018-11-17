import pytest
from asttokens.util import Token

from flake8_aaa.helpers import get_last_token


@pytest.mark.parametrize('code_str', [
    '''
def f():
    do_thing()
''',
])
def test(first_node_with_tokens):
    result = get_last_token(first_node_with_tokens)

    assert isinstance(result, Token)
    assert result.string == ')'
