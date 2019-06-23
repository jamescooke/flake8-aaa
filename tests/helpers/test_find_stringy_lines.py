import pytest

from flake8_aaa.helpers import find_stringy_lines


@pytest.mark.parametrize(
    'code_str, offset, expected_lines', [
        (
            '''
# Comments with numbers are the *relative* line numbers to the start of the
# test function.

def test():  # 0
    with pytest.raises(Exception):  # 1
        do_thing()  # 2
''', 5, set()
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
''', 2, set([3])
        ),
        (
            '''
@pytest.mark.parametrize('m', ["""  # 0

hello"""])  # 2
def test_other(m):  # 3
    """  # 4
    Make sure that message is a greeting  # 5

    Hard coded  # 7
    """  # 8
    with pytest.raises(AttributeError) as excinfo:  # 9

        result = m.add()  # 11

    assert str(excinfo.value) == """  # 13

message  # 15
    """  # 16
''', 2, set([0, 1, 2, 4, 5, 6, 7, 8, 13, 14, 15, 16])
        ),
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
