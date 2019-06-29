import pytest
from asttokens.util import Token

from flake8_aaa.helpers import build_footprint, find_stringy_lines, get_first_token


# *** NOTE ***
# This is a temporary test hidden away from py35, please do not edit - change
# the main files in `/tests` dir instead.

@pytest.mark.parametrize('code_str, expected', [
    ('''
f"hello world"
''', 'f"hello world"'),
])
def test_strings(first_node_with_tokens, expected):
    result = get_first_token(first_node_with_tokens)

    assert isinstance(result, Token)
    assert result.string == expected


@pytest.mark.parametrize(
    'code_str, first_line_no, expected_lines', [
        (
            '''
def test_f_string_check(version):  # 0
    result = do(
        f"""/path/to/folder/

        {version}/thing.py""",  # 4
    )
''', 2, set([2, 3, 4])
        ),
    ]
)
def test_f_string(first_node_with_tokens, first_line_no, expected_lines):
    f_string_node = first_node_with_tokens.body[0].value.args[0]

    result = build_footprint(f_string_node, first_line_no)

    assert result == expected_lines


@pytest.mark.parametrize(
    'code_str, offset, expected_lines', [
        (
            '''
def test_f_string_check(version):  # 0
    result = do(
        f"""/path/to/folder/

        {version}/thing.py""",  # 4
    )

    assert result is True
''', 2, set([2, 3, 4])
        ),
    ]
)
def test(first_node_with_tokens, offset, expected_lines):
    result = find_stringy_lines(first_node_with_tokens, offset)

    assert result == expected_lines
