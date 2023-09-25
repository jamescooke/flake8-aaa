import sys

import pytest
from asttokens.util import Token

from flake8_aaa.helpers import get_first_token


@pytest.mark.parametrize('code_str', [
    '''
def f():
    do_thing()
''',
])
def test(first_node_with_tokens) -> None:
    result = get_first_token(first_node_with_tokens)

    assert isinstance(result, Token)
    assert result.string == 'def'


@pytest.mark.parametrize(
    'code_str, expected', [
        ('''
"hello world"
''', '"hello world"'),
        ('''
r'hello world'
''', 'r\'hello world\''),
    ]
)
def test_strings(first_node_with_tokens, expected: str) -> None:
    result = get_first_token(first_node_with_tokens)

    assert isinstance(result, Token)
    assert result.string == expected


@pytest.mark.skipif(sys.version_info >= (3, 12), reason='Requires Python 3.11 or lower')
@pytest.mark.parametrize('code_str', ['''
f"hello world"
'''])
def test_f_string(first_node_with_tokens) -> None:
    result = get_first_token(first_node_with_tokens)

    assert isinstance(result, Token)
    assert result.string == 'f"hello world"'


@pytest.mark.skipif(sys.version_info < (3, 12), reason="Requires Python 3.12 or higher")
@pytest.mark.parametrize('code_str', ['''
f"hello world"
'''])
def test_f_string_tokens(first_node_with_tokens) -> None:
    """
    Python 3.12 has tokens for f-strings, where previous versions didn't.

    This test added while upgrading to py312, but there were no integration
    tests that this affected, just internal checks. More info on the f-string
    change: https://github.com/gristlabs/asttokens/issues/109
    """
    result = get_first_token(first_node_with_tokens)

    assert isinstance(result, Token)
    assert result.string == 'f"'  # FSTRING_START token
