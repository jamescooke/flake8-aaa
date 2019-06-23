import pytest

from flake8_aaa.helpers import build_footprint


@pytest.mark.parametrize(
    'code_str, first_line_no, expected_lines', [
        (
            '''
def test():  # 0
    with pytest.raises(Exception):  # 1
        do_thing()  # 2

    other_thing()  # 4
''', 2, set([1, 2])
        ),
        (
            '''
@pytest.mark.xfail()  # 0
def test_other():  # 1
    result = do_thing(  # 2
        'yes',  # 3
        None,  # 4
    )  # 5

    assert result is None  # 7
''', 2, set([2, 3, 4, 5])
        ),
    ]
)
def test(first_node_with_tokens, first_line_no, expected_lines):
    first_test_node = first_node_with_tokens.body[0]

    result = build_footprint(first_test_node, first_line_no)

    assert result == expected_lines


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
