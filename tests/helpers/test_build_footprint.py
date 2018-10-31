import pytest

from flake8_aaa.helpers import build_footprint


@pytest.mark.parametrize(
    'code_str, first_line_no, expected_lines', [
        ('''
def test():
    with pytest.raises(Exception):
        do_thing()

    other_thing()
''', 2, set([1, 2])),
        (
            '''
@pytest.mark.xfail()
def test_other():
    result = do_thing(
        'yes',
        None,
    )

    assert result is None
''', 2, set([2, 3, 4, 5])
        ),
    ]
)
def test(first_node_with_tokens, first_line_no, expected_lines):
    first_test_node = first_node_with_tokens.body[0]

    result = build_footprint(first_test_node, first_line_no)

    assert result == expected_lines
