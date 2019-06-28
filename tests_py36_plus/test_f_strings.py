import pytest
from asttokens.util import Token

from flake8_aaa.helpers import build_footprint, find_stringy_lines, get_first_token


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
    """
    f-strings do work - it appears it's the Str nodes inside the JoinedStr that
    are not tokenised.
    """
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
    """
    * First node with tokens is the function
    * Offset is the line number of the start of the function, this can be the
        first line of any part of it including the decorator.
    * Expected lines is the set of stringy lines expected.

    TODO extract the last test because it's a work around and only for py36
    """
    result = find_stringy_lines(first_node_with_tokens, offset)

    assert result == expected_lines
